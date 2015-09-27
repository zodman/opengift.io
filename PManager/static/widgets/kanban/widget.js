$(function () {
    var kanbanView = window.taskViewClass.extend({
        'render': function () {
            var template = $('.js-task-wrapper-template').html();
            var $el = $('<div></div>').addClass('task task-wrapper-kanban')
                .attr('rel', this.model.id).append(template);

            var avatar = $el.find('.js-avatar-container');
            if (this.model.get('avatar')) {
                avatar.attr('rel', JSON.stringify(this.model.get('avatar')));
                $.updateAvatar(
                    avatar,
                    { size: 30 }
                );
            }

            $el.find('.js-task-status').attr('rel', this.model.get(this.model.get('status_type')));
            $el.find('.js-task-name').text(this.model.get('name'));
            this.$el.replaceWith($el);
            this.$el = $el;
            this.el = this.$el.get(0);
            this.delegateEvents();
        }
    });

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
        initDND: function() {
            var t = this;
            $(document).on('mousedown touchstart', '.task-wrapper-kanban', function(e) {
                t.draggable = $(this);
                var view = t.taskViews[t.draggable.attr('rel')],
                    $oldColumn = $(this).parent(),
                    statusName = $(this).parent().data('prop');
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
                        t.$dummyBlock.replaceWith(t.draggable);

                        var view = t.taskViews[t.draggable.attr('rel')];
                        view.model.set(
                            t.overColumn.data('prop'),
                            t.overColumn.attr('rel')
                        );
                        view.render();

                        taskManager.SetTaskProperty(
                            view.model.id,
                            t.overColumn.data('prop'),
                            t.overColumn.attr('rel'),
                            function(data){
                                try {
                                    data = $.parseJSON(data);
                                    if (data.error) {
                                        alert(data.error);
                                        view.$el.appendTo(view.model.get('parentBlock'));
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
                    } else {
                        if (t.$dummyBlock.is(':visible')) {
                            t.$dummyBlock.replaceWith(t.draggable);
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
                                console.log($(this).offset().top + ','+parseInt(e.clientY + $(window).scrollTop()));
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
                    var taskView = new kanbanView({'model': task});
                    taskView.render();
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