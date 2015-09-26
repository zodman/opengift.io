$(function () {
    var kanbanView = window.taskViewClass.extend({
        'render': function () {
            var template = $('.js-task-wrapper-template').html();
            var $el = $('<div></div>').addClass('task task-wrapper-kanban')
                .attr('rel', this.model.id).append(template);

            var avatar = $el.find('.js-avatar-container');
            if (this.model.get('avatar')) {
                avatar.attr('rel', JSON.stringify(this.model.get('avatar')));
                $.updateAvatar(avatar, { size: 30 });
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
                t.draggable = $(this).css({
                    'width': $(this).width()
                });
                var view = t.taskViews[t.draggable.attr('rel')];
                view.model.set('parentBlock', $(this).parent());
                t.offsetTaskY = e.clientY - $(this).offset().top + $(window).scrollTop();
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
                                           e.clientY > offset.top && e.clientY < offset.bottom;

                        if (isOverColumn) {
                            t.overColumn = $(this);
                            var $columnObjects = false;
                            t.overColumn.children().each(function(){
                                if (
                                    !$columnObjects &&
                                    $(this).offset().top + $(this).width() / 2 > e.clientY + $(window).scrollTop()
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
                        'top': e.clientY - t.offsetTaskY,
                        'left': e.clientX - t.offsetTaskX,
                        'z-index': 99999
                    }).appendTo('body');
                }
            });
        },
        getTasksFromServer: function () {
            var t = this;

            PM_AjaxPost(
                "/task_handler",
                {
                    'action': 'all',
                    'startPage': 3,
                    'project': this.options.project
                },
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
    $(document).on('mousedown', '.js-task_menu', function(e) {
        e.stopPropagation();
        return false;
    });
});