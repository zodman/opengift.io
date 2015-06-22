(function() {
  var DropArea, Task;

  DropArea = (function() {
    DropArea.count = 2;

    DropArea.getIndex = function() {
      DropArea.count += 1;
      return DropArea.count;
    };

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
        create: (function(_this) {
          return function(event, ui) {
            return _this.el.css('z-index', 1);
          };
        })(this),
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

    DropArea.prototype.getNextOffset = function(elementWidth, elementHeight) {
      var currentOffset, heightLimit, offs, widthLimit;
      widthLimit = this.width - elementWidth - this.borders.right;
      heightLimit = this.el.height() - elementHeight;
      currentOffset = this.nextOffset;
      this.nextOffset = {
        left: (this.nextOffset.left + this.step.left) % widthLimit,
        top: this.nextOffset.top + this.step.top
      };
      offs = {
        left: this.borders.left + this.position.left + currentOffset.left,
        top: this.borders.top + currentOffset.top
      };
      if (offs.top > heightLimit) {
        this.widget.setHeight(offs.top + elementHeight + this.borders.bottom);
      }
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
          return function() {
            return _this.el.css('z-index', DropArea.getIndex());
          };
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

    Task.prototype.setStatus = function(value) {
      this.status = value;
      this.position = this.el.position();
      if (!this.widget.validBox(this.position, this)) {
        this.setPosition(null, this.widget.options.animationTime);
        return this.store();
      }
    };

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
        if (this.widget.validBox(value, this)) {
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
      var drop, newPosition;
      newPosition = this.el.position();
      drop = this.widget.getDropByPosition(newPosition);
      if (drop == null) {
        return this.failMove();
      }
      this.position = newPosition;
      if (drop.status !== this.status) {
        this.status = drop.status;
        this.widget.onStatusChange(this);
      }
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
      var drop, elH, elW, offset;
      drop = this.widget.dropAreas[this.status];
      elW = this.el.width();
      elH = this.el.height();
      offset = drop.getNextOffset(elW, elH);
      return offset;
    };

    Task.prototype.setPosition = function(position, animateDuration) {
      var currentOffset, elH;
      if (animateDuration == null) {
        animateDuration = 0;
      }
      if (position == null) {
        position = this.getPositionDefault();
      }
      currentOffset = this.widget.offset;
      position = {
        left: position.left,
        top: position.top
      };
      elH = this.el.height();
      if (elH + position.top > this.widget.getHeight()) {
        this.widget.setHeight(elH + position.top);
      }
      this.el.animate(position, animateDuration);
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
      getDropByPosition: function(position) {
        var drop, key, ref;
        ref = this.dropAreas;
        for (key in ref) {
          drop = ref[key];
          if (drop.position.left + drop.borders.left < position.left && drop.position.left + drop.width - drop.borders.right > position.left) {
            return drop;
          }
        }
        return false;
      },
      validBox: function(position, task) {
        var boundaries, drop;
        drop = this.dropAreas[task.status];
        if (drop == null) {
          return false;
        }
        boundaries = {
          left: drop.position.left + drop.borders.left,
          right: drop.position.left + drop.width + drop.borders.left
        };
        if (position.left < boundaries.left) {
          return false;
        }
        if (position.left > boundaries.right) {
          return false;
        }
        if (position.left + task.el.width() > boundaries.right) {
          return false;
        }
        return true;
      },
      onStatusChange: function(task) {
        return this._trigger(':onstatuschange', this, task);
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
      setHeight: function(height) {
        var drop;
        this.element.css('height', height + 'px');
        for (drop in this.drops) {
          drop.setHeight(height);
        }
        return this._storeHeight(height);
      },
      getHeight: function() {
        return this.element.height();
      },
      _initResizable: function() {
        return this.element.resizable({
          handles: "s",
          minHeight: 400,
          create: (function(_this) {
            return function() {
              var height;
              height = _this._restoreHeight();
              return _this.setHeight(height);
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
        var key, ref, task;
        ref = this.tasks;
        for (key in ref) {
          task = ref[key];
          task.render();
        }
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
