$(function () {
    var getTodayTasks = function(projectId) {
        if (!projectId) {
            projectId = 0
        }
        var todayTasksString = $.cookie('today_tasks'), todayTasks;
        try {
            todayTasks = $.parseJSON(todayTasksString);
            if (typeof todayTasks != typeof {}) {
                todayTasks = {}
            }
            return todayTasks[projectId]
        } catch (e) {
            return [];
        }
    };

    var setTodayTasks = function(projectId, arTasksId) {
        if (!projectId) {
            projectId = 0
        }
        var todayTasksString = $.cookie('today_tasks'), todayTasks;

        try {
            if (todayTasksString)
                todayTasks = $.parseJSON(todayTasksString);
            else
                todayTasks = {};

            todayTasks[projectId] = arTasksId;
            $.cookie('today_tasks', JSON.stringify(todayTasks));
            return true;
        } catch (e) {
            return false;
        }
    };

    var addTaskToColumn = function(view, $column, $dummyBlock) {
        var project = $column.data('project');
        if ($dummyBlock) {
            view.$el.insertBefore($dummyBlock);
            $dummyBlock.remove();
        } else {
            view.$el.appendTo($column);
        }

        view.model.set(
            $column.data('prop'),
            $column.attr('rel')
        );
        view.render();
        var todayTasks = getTodayTasks(project);
        if ($column.attr('rel') == 'today') {
            if ($.inArray(view.model.id, todayTasks) == -1) {
                todayTasks.push(view.model.id);
            }
            setTodayTasks(project, todayTasks)
        } else if (view.model.get('parentBlock').attr('rel') == 'today') {
            for (var i = todayTasks.length; --i >= 0;) {
                if (todayTasks[i] === view.model.id) todayTasks.splice(i, 1);
            }
            setTodayTasks(project, todayTasks)
        }
        taskManager.SetTaskProperty(
            view.model.id,
            $column.data('prop'),
            $column.attr('rel'),
            function(data){
                try {
                    data = $.parseJSON(data);
                    if (data.error) {
                        alert(data.error);
                        view.$el.animateAppendTo(view.model.get('parentBlock'), 1000);
                        view.model.set(
                            view.model.get('oldStatusName'),
                            view.model.get('oldStatus')
                        );
                        view.render();
                    }
                } catch (e) {
                    console.log(data);
                }
            }
        );
    };

    $.fn.animateAppendTo = function(sel, speed) {
        var $this = this,
            newEle = $this.clone(true).appendTo($this.parent());
        $this.appendTo(sel);
        var newPos = $this.position();
        $this.hide();
        newEle.css({
            'position':'absolute',
            'width': newEle.width()
        }).animate(newPos, speed, function() {
            newEle.remove();
            $this.show();
        });

        return newEle;
    };

    $.widget("custom.kanban", {
        taskViews: {

        },
        options: {
            value: 0,
            project: 0
        },
        _create: function () {
            this.options.project = this.element.data('project');
            this.$columns = this.element.find('.js-tasks-column');
            this.$dummyBlock = $('<div></div>').addClass('task-kanban-dummy');
            this.getTasksFromServer();
            this.initDND();
        },
        'initAsync': function() {
            var t = this;
            baseConnector.addListener('fs.task.update', function (data) {
                if (data && data.id) {
                    if (t.taskViews[data.id]) {
                        var view = t.taskViews[data.id];
                        if (data['status'] == 'revision' && view.model.get('status') == 'ready') {
                            data['status'] = 'today';
                        }
                        for (var i in data) {
                            if (i == 'viewedOnly') {
                                if (data[i] != document.mainController.userId) {
                                    view.model.set('viewed', false);
                                }
                            }
                            if (i != 'id') {
                                view.model.set(i, data[i]);
                            }
                        }
                        view.render();
                        var $column = view.$el.parent();

                        if (data[$column.data('prop')] && $column.attr('rel') != data[$column.data('prop')]) {
                            t.$columns.each(function() {
                                if ($(this).attr('rel') == data[$column.data('prop')]) {
                                    addTaskToColumn(view, $(this));
                                }
                            });
                        }
                    }
                }
            });
        },
        initToday: function() {
            var t = this, i, view;
            this.$columns.each(function(){
                if ($(this).attr('rel') == 'today') {
                    var todayTasks = getTodayTasks($(this).data('project'));
                    for (i in t.taskViews) {
                        view = t.taskViews[i];
                        if ($.inArray(view.model.id, todayTasks) > -1) {
                            view.$el.animateAppendTo($(this));
                        }
                    }
                }
            })
        },
        initDND: function() {
            var t = this;
            $(document).on('mousedown touchstart', '.task', function(e) {
                t.draggable = $(this);
                var view = t.taskViews[t.draggable.data('taskid')],
                    $oldColumn = $(this).parent(),
                    statusName = $(this).parent().data('prop');
                t.draggable = view.$el;

                view.model.set('parentBlock', $oldColumn);
                view.model.set('oldStatusName', statusName);
                view.model.set('oldStatus', view.model.get(statusName));
                t.offsetTaskY = e.clientY - ($(this).offset().top - $(window).scrollTop());
                t.offsetTaskX = e.clientX - $(this).offset().left;
                t.overColumn = false;
                return false;
            }).on('mouseup touchend', document, function() {
                if (t.draggable) {
                    t.draggable.css({
                        'position': 'relative',
                        'top': 'auto',
                        'left': 'auto',
                        'width': '100%'
                    });
                    if (t.overColumn) {
                        var view = t.taskViews[t.draggable.data('taskid')];
                        addTaskToColumn(view, t.overColumn, t.$dummyBlock);
                    } else {
                        if (t.$dummyBlock.is(':visible')) {
                            t.draggable.insertBefore(t.$dummyBlock);
                            t.$dummyBlock.remove();
                        }
                    }
                }
                t.draggable = false;
            }).on('mousemove touchmove', this.element, function(e) {
                if (t.draggable) {
                    t.$columns.each(function () {
                        var offset = {
                            'top': $(this).offset().top,
                            'left': $(this).offset().left,
                            'right': $(this).offset().left + $(this).width(),
                            'bottom': $(this).offset().top + $(this).height()
                        };

                        var isOverColumn = e.clientX > offset.left && e.clientX < offset.right &&
                                           e.clientY + $(window).scrollTop() > offset.top &&
                                            e.clientY + $(window).scrollTop() < offset.bottom;

                        if (isOverColumn) {
                            t.overColumn = $(this);
                            var $columnObjects = false;
                            t.overColumn.children().each(function(){
                                if (
                                    !$columnObjects &&
                                    ($(this).offset().top + ($(this).height() / 2)) > (e.clientY + $(window).scrollTop())
                                    ) {
                                    $columnObjects = $(this);
                                }
                            });

                            if ($columnObjects) {
                                t.$dummyBlock.insertBefore($columnObjects).show();
                            } else {
                                t.$dummyBlock.appendTo(t.overColumn).show();
                            }
                        }
                    });

                    t.draggable.css({
                        'position': 'absolute',
                        'top': e.clientY + $(window).scrollTop() - t.offsetTaskY,
                        'left': e.clientX - t.offsetTaskX,
                        'z-index': 99999,
                        'width': t.draggable.width()
                    }).appendTo('body');
                }
            });
        },
        getTasksFromServer: function () {
            var t = this,
                props = [],
                propVals = {};

            t.$columns.each(function() {
                var propName = $(this).data('prop') == 'status' ? 'status__code' : $(this).data('prop');
                if ($.inArray(propName, props) == -1)
                    props.push(propName);

                if (!propVals['gantt_prop_' + propName]) {
                    propVals['gantt_prop_' + propName] = [];
                }
                propVals['gantt_prop_' + propName].push($(this).attr('rel'));
            });

            PM_AjaxPost(
                "/task_handler",
                $.extend({
                    'action': 'all',
                    'startPage': 3,
                    'project': this.options.project,
                    'gantt_props': props
                }, propVals),
                function (data) {
                    var i, taskData;
                    for (i in data.tasks) {
                        taskData = data.tasks[i];
                        t.addTaskRow(taskData);
                    }
                    t.initToday();
                    t.initAsync();
                },
                'json'
            )
        },
        addTaskRow: function (taskData) {
            var t = this;
            this.$columns.each(function () {
                if (taskData[$(this).data('prop')] == $(this).attr('rel')) {
                    var task = new window.taskClass(taskData);
                    task.set('status_type', $(this).data('prop'));
                    task.set('status', task.get($(this).data('prop')));
                    var taskView = new window.taskViewClass({'model': task});
                    taskView.createEl().render();
                    $(this).append(taskView.$el);

                    t.taskViews[task.id] = taskView;
                }
            })
        }
    });

    $('.js-project-row').each(function () {
        $(this).kanban();
    });
    $(document).on('mousedown', '.js-task_menu, .js-select_resp, .js-task-name', function(e) {
        e.stopPropagation();
        return false;
    });
});