(function() {
  var DropArea, Task;

  DropArea = (function() {
    function DropArea(el, widget) {
      this.el = $(el);
      this.status = this.el.attr(widget.options.attributeName);
      this.step = widget.options.defaultStep;
      this.position = this.el.position();
      this.borders = this.getBorders();
      this.nextOffset = {
        left: 0,
        top: 0
      };
      this.width = this.el.width();
      this.el.droppable({
        tolerance: "fit",
        hoverClass: "highlighted",
        scope: widget.scope,
        drop: (function(_this) {
          return function(event, ui) {
            var task;
            task = _this.widget.getTask(ui.draggable);
            return _this.widget.onDrop(task, _this);
          };
        })(this),
        accept: (function(_this) {
          return function(draggable) {
            return true;
          };
        })(this)
      });
      this.widget = widget;
    }

    DropArea.prototype.getBorders = function() {
      return {
        left: parseInt(this.el.css('border-left-width')) + parseInt(this.el.css('padding-left')) + parseInt(this.el.css('margin-left')),
        right: parseInt(this.el.css('border-right-width')) + parseInt(this.el.css('padding-right')) + parseInt(this.el.css('margin-right')),
        top: parseInt(this.el.css('border-top-width')) + parseInt(this.el.css('padding-top')) + parseInt(this.el.css('margin-top')),
        bottom: parseInt(this.el.css('border-bottom-width')) + parseInt(this.el.css('padding-bottom')) + parseInt(this.el.css('margin-bottom'))
      };
    };

    DropArea.prototype.getNextOffset = function(elementWidth) {
      var currentOffset, offs, widthLimit;
      widthLimit = this.width - elementWidth - this.borders.right;
      currentOffset = this.nextOffset;
      this.nextOffset = {
        left: (this.nextOffset.left + this.step.left) % widthLimit,
        top: this.nextOffset.top + this.step.top
      };
      offs = {
        left: this.borders.left + this.position.left + currentOffset.left,
        top: this.borders.top + currentOffset.top
      };
      return offs;
    };

    DropArea.prototype.setHeight = function(height) {
      if (height == null) {
        height = this.widget.options.resizable.minHeight || 0;
      }
      return this.el.css('height', height + 'px');
    };

    return DropArea;

  })();

  Task = (function() {
    function Task(el1, widget1) {
      this.el = el1;
      this.widget = widget1;
      this.position = this.el.position();
      this.status = false;
      this.storage = function() {};
      this.id = this.el.attr('rel');
      this.el.draggable({
        stack: "div",
        distance: 0,
        scope: this.widget.scope,
        containment: "parent",
        create: (function(_this) {
          return function() {};
        })(this),
        start: (function(_this) {
          return function() {
            _this.startMove();
            return _this.widget.onDragStart(_this);
          };
        })(this),
        revert: (function(_this) {
          return function(droppable) {
            _this.widget.onDragRevert(_this);
            if (_this.widget.isDroppable(droppable)) {
              return false;
            }
            return true;
          };
        })(this),
        stop: (function(_this) {
          return function(event, ui) {
            return _this.widget.onDragEnd(_this);
          };
        })(this)
      });
    }

    Task.prototype.render = function() {
      return this.el.show();
    };

    Task.prototype.update = function() {};

    Task.prototype.getStorageKey = function() {
      return "project_" + this.widget.kbnId + "task_" + this.id;
    };

    Task.prototype.store = function() {
      var value;
      value = this.position;
      value.status = this.status;
      return this.storage(this.getStorageKey(), value);
    };

    Task.prototype.restore = function() {
      var value;
      value = this.storage(this.getStorageKey());
      if ((value != null) && (value.status != null)) {
        if (this.widget.validBox(this)) {
          this.setPosition(value);
          return;
        }
      }
      this.setPosition();
      return this.store();
    };

    Task.prototype.startMove = function() {
      return this.position = this.el.position();
    };

    Task.prototype.completeMove = function() {
      this.position = this.el.position();
      return this.store();
    };

    Task.prototype.failMove = function() {
      return this.el.animate(this.position, this.widget.options.animationTime, (function(_this) {
        return function() {
          return _this.store();
        };
      })(this));
    };

    Task.prototype.getPositionDefault = function() {
      var drop, elW, offset;
      drop = this.widget.dropAreas[this.status];
      elW = this.el.width();
      offset = drop.getNextOffset(elW);
      return offset;
    };

    Task.prototype.setPosition = function(position) {
      var currentOffset;
      if (position == null) {
        position = this.getPositionDefault();
      }
      currentOffset = this.widget.offset;
      position = {
        left: position.left,
        top: position.top
      };
      this.el.animate(position, 0);
      return this.position = this.el.position();
    };

    Task.prototype.initialize = function() {
      this.restore();
      this.update();
      return this.render();
    };

    return Task;

  })();

  (function($) {
    return $.widget('tonakai.kanban', {
      options: {
        animationTime: 200,
        storagePrefix: 'hl_kb_',
        defaultStep: {
          left: 40,
          top: 40
        },
        drops: '.js-tasks-column',
        tasks: '.js-task-wrapper',
        attributeName: 'rel',
        resizable: {
          minHeight: 400
        }
      },
      validBox: function(task) {
        var boundaries, drop;
        drop = this.dropAreas[task.status];
        if (drop == null) {
          return false;
        }
        boundaries = {
          left: drop.position.left,
          right: drop.position.left + drop.width
        };
        if (task.position.left < boundaries.left) {
          return false;
        }
        if (task.position.left + task.width > boundaries.right) {
          return false;
        }
        return true;
      },
      onDrop: function(task, drop) {
        return this._trigger(':ondrop', this, {
          drop: drop,
          task: task
        });
      },
      onDragRevert: function(task) {
        return this._trigger(':dragrevert', this, task);
      },
      onDragStart: function(task) {
        return this._trigger(':dragstart', this, task);
      },
      onDragEnd: function(task) {
        return this._trigger(':dragend', this, task);
      },
      _storeHeight: function(height) {
        return window.localStorage.setItem(this._storeResizeKey(), height);
      },
      _restoreHeight: function() {
        var e, val;
        val = window.localStorage.getItem(this._storeResizeKey());
        if (val == null) {
          return this.options.resizable.minHeight;
        }
        try {
          val = JSON.parse(val);
          return val;
        } catch (_error) {
          e = _error;
          return this.options.resizable.minHeight;
        }
      },
      getTask: function(element) {
        var id;
        id = element.attr(this.options.attributeName);
        if (this.tasks[id]) {
          return this.tasks[id];
        }
        return false;
      },
      _create: function() {
        if (!this._browser_is_supported()) {
          return false;
        }
        if (!this._dependencies_resolved()) {
          return false;
        }
        this.kbnId = this.element.attr(this.options.attributeName);
        this.dropAreas = {};
        this.tasks = {};
        this.scope = "project_kanban_" + this.kbnId;
        this.offset = this.element.offset();
        return this._setup();
      },
      _setOption: function(key, value) {
        this.options[key] = value;
        this._super(key, value);
        return this.update();
      },
      _setup: function() {
        this._initDrops();
        this._initTasks();
        this._initResizable();
        return this._trigger(':ready', this);
      },
      _initResizable: function() {
        return this.element.resizable({
          handles: "s",
          minHeight: 400,
          create: (function(_this) {
            return function() {
              var drop, height, results;
              height = _this._restoreHeight();
              _this.element.css('height', height + 'px');
              results = [];
              for (drop in _this.drops) {
                results.push(drop.setHeight(height));
              }
              return results;
            };
          })(this),
          stop: (function(_this) {
            return function() {
              var drop, height;
              height = _this.element.height();
              for (drop in _this.drops) {
                drop.setHeight(height);
              }
              return _this._storeHeight(height);
            };
          })(this)
        });
      },
      isDroppable: function(droppable) {
        if (typeof droppable.hasClass === "function" ? droppable.hasClass(this.options.drops.slice(1)) : void 0) {
          return true;
        }
        return false;
      },
      _storeResizeKey: function() {
        return this.storagePrefix + "project_" + this.knbId;
      },
      _initDrops: function() {
        return this.element.find(this.options.drops).each((function(_this) {
          return function(index, el) {
            var $el;
            $el = $(el);
            return _this.addDrop($el);
          };
        })(this));
      },
      _initTasks: function() {
        return this.element.find(this.options.tasks).each((function(_this) {
          return function(index, el) {
            var $el;
            $el = $(el);
            return _this.addTask($el);
          };
        })(this));
      },
      update: function() {
        return this.render();
      },
      addDrop: function($el) {
        this.dropAreas[$el.attr(this.options.attributeName)] = new DropArea($el, this);
        return this._trigger(':dropadd', this, this.dropAreas[$el.attr(this.options.attributeName)]);
      },
      addTask: function($el) {
        var task;
        task = new Task($el, this);
        this.tasks[$el.attr(this.options.attributeName)] = task;
        this._trigger(':taskadd', this, this.tasks[$el.attr(this.options.attributeName)]);
        return task.initialize();
      },
      render: function() {
        var results, task;
        results = [];
        for (task in this.tasks) {
          results.push(task.render());
        }
        return results;
      },
      _browser_is_supported: function() {
        if (window.navigator.appName === "Microsoft Internet Explorer") {
          return document.documentMode >= 8;
        }
        if (/iP(od|hone)/i.test(window.navigator.userAgent)) {
          return false;
        }
        if (/Android/i.test(window.navigator.userAgent)) {
          if (/Mobile/i.test(window.navigator.userAgent)) {
            return false;
          }
        }
        return true;
      },
      _dependencies_resolved: function() {
        if ($().draggable == null) {
          return false;
        }
        if ($().droppable == null) {
          return false;
        }
        return true;
      }
    });
  })(jQuery);

}).call(this);
