$(function () {
    var COOKIES_NAME = 'today_tasks',
        PROJECT_DATA_NAME = 'project',
        TODAY_COLUMN_CODE = 'today',
        getTodayTasks = function getTodayTasks(projectId) {
            var todayTasksString = $.cookie(COOKIES_NAME), todayTasks;
            projectId = projectId || 0;
            try {
                todayTasks = $.parseJSON(todayTasksString);
                if (typeof todayTasks != typeof {}) {
                    todayTasks = {}
                }
                if (todayTasks[projectId])
                    return todayTasks[projectId];
                else return []
            } catch (e) {
                return [];
            }
        },
        setTodayTasks = function setTodayTasks(projectId, arTasksId) {
            projectId = projectId || 0;
            var todayTasksString = $.cookie(COOKIES_NAME), todayTasks;

            try {
                if (todayTasksString)
                    todayTasks = $.parseJSON(todayTasksString);
                else
                    todayTasks = {};

                todayTasks[projectId] = arTasksId;
                $.cookie(COOKIES_NAME, JSON.stringify(todayTasks));
                return true;
            } catch (e) {
                return false;
            }
        },
        addTaskToColumn = function addTaskToColumn(view, $column) {
            var project = $column.data(PROJECT_DATA_NAME);
            var todayTasks = getTodayTasks(project);
            if ($column.attr('rel') == TODAY_COLUMN_CODE) {
                if ($.inArray(view.model.id, todayTasks) == -1) {
                    todayTasks.push(view.model.id);
                }
                setTodayTasks(project, todayTasks);
                //todo: investigate further
            } else if (view.model.get('parentBlock').attr('rel') == TODAY_COLUMN_CODE) {
                for (var i = todayTasks.length; --i >= 0;) {
                    if (todayTasks[i] === view.model.id) todayTasks.splice(i, 1);
                }
                setTodayTasks(project, todayTasks)
            }
        },
        insertTask = function insertTask(index, column, what){
            if(index > 1){
                return what.insertAfter(column.find('.task:eq(' + (index - 1) + ')'));
            }else{
                return what.prependTo(column);
            }
        },
        animateAppendTo = function animateAppendTo(item, sel, speed, fn) {
            item = $(item);
            var frame = { top: 0, left: 0},
                origin = item.offset(),
                previndex = parseInt(item.attr('data-previndex')) || 0,
                whiteSpace = $('<div>').addClass('kanban-empty-task'),
                whiteSpaceOrigin = whiteSpace.clone(),
                currentIndex = item.index(),
                column = item.parent(),
                destination;
            item.removeAttr('data-previndex');
            insertTask(previndex, sel, whiteSpace);
            destination = whiteSpace.offset();
            item.css({
                position: 'absolute',
                width: item.width(),
                height: item.height(),
                left: origin.left - frame.left,
                top: origin.top - frame.top,
                margin: 0,
                'z-index': 99999
            }).addClass('ui-sortable-helper');
            insertTask(currentIndex, column, whiteSpaceOrigin);
            whiteSpaceOrigin.hide({
                duration: speed,
                complete: function(){
                    whiteSpaceOrigin.remove();
                },
                easing: "easeOutCubic"
            });
            item.animate({
                top: destination.top - frame.top,
                left: destination.left - frame.left
            }, speed, "easeOutCubic", function(){
                insertTask(previndex, sel, item);
                whiteSpace.remove();
                item.attr('style','').removeClass('ui-sortable-helper');
                if(typeof(fn) === 'function'){
                    fn.call(item);
                }
            });

            return false;
        };

    $.widget("custom.kanban", {
        taskViews: {},
        _columns: {},
        columnProperty: 'status',
        ajax: {},
        options: {
            value: 0,
            project: 0,
            useColors: false,
        },
        _create: function () {
            this.initOptions();
            this.initColumns();
            this.initRequest();
            this.getTasksFromServer();
        },
        initColumns: function initColumns(){
            var column;
            this.$columns = this.element.find('.js-tasks-column');
            for (var i = this.$columns.length - 1; i >= 0; i--) {
                column = this.$columns[i];
                this._columns[$(column).attr('rel')] = $(column);
            };
        },
        initOptions: function initOptions(){
            this.options.project = this.element.data('project');
            this.options.useColors = this.element.data('use_colors');
            if(this.options.useColors){
                this.columnProperty = 'color';
            }
        },
        initRequest: function initRequest(){
            var t = this,
                propName = this.options.useColors == false ? 'status__code' : this.columnProperty,
                props = [propName],
                propVals = {};
            for (var i = this._columns.length - 1; i >= 0; i--) {
                propVals['gantt_prop_' + propName] = [i];
            };
            this.ajax.props = props;
            this.ajax.propVals = propVals;
        },
        getTasksFromServer: function getTasksFromServer() {
            var t = this;
            PM_AjaxPost(
                "/task_handler",
                $.extend({
                    'action': 'all',
                    'startPage': 3,
                    'project': this.options.project,
                    'gantt_props': this.ajax.props
                }, this.ajax.propVals),
                function (data) {
                    var i, taskData;
                    for (i in data.tasks) {
                        taskData = data.tasks[i];
                        t.addTaskRow(taskData);
                    }
                    t.filterTodayTasks();
                    t.onModelChange();
                    t.makeItSortable();
                },
                'json'
            )
        },
        filterTodayTasks: function filterTodayTasks() {
            var i, view;

            if(this._columns['today']){
                var todayTasks = getTodayTasks(this.options.project);
                for (i in this.taskViews) {
                    view = this.taskViews[i];
                    if ($.inArray(view.model.id, todayTasks) > -1) {
                        animateAppendTo(view.$el, this._columns['today'], 0);
                    }
                }
            }
        },
        onModelChange: function onModelChange() {
            var t = this;
            baseConnector.addListener('fs.task.update', function (data) {
                if (!data || !data.id || !t.taskViews[data.id]) {
                    return;
                }
                var view = t.taskViews[data.id],
                    oldColumn = view.$el.parent().attr('rel'),
                    returnToFix = function returnToFix(){
                        return (data['status'] == 'revision' &&
                            ($.inArray(view.model.get('status'), ['ready', 'today']) > -1) &&
                            view.model.get('resp') && view.model.get('resp')[0] &&
                            document.mainController.userId == view.model.get('resp')[0]['id']
                        );
                    }

                if (returnToFix()) {
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
                var col = data[t.columnProperty];
                if (col && oldColumn != col) {
                    addTaskToColumn(view, t._columns[col]);
                };
                t._columns[col].sortable("refresh");
            });
        },
        makeItSortable: function makeItSortable() {
            var t = this;
            this.$columns.sortable({
                connectWith: '.js-project-row#project_' + t.options.project + ' .js-tasks-column',
                items: "> div.task",
                placeholder: "task-kanban-dummy",
                dropOnEmpty: true,
                revert: 50,
                appendTo: $('body'),
                start: function(event, ui) {
                    ui.item.attr('data-previndex', ui.item.index());
                },
                receive: function(event, ui){
                    var toColumn = $(event.target).attr('rel');
                    var fromColumn = ui.sender.attr('rel');
                    var taskid = ui.item.data('taskid');
                    taskManager.SetTaskProperty(
                        taskid,
                        t.columnProperty,
                        toColumn,
                        function(data){
                            try{
                                data = $.parseJSON(data);
                            } catch(e){
                                console.log(e);
                                return;
                            }
                            if(data.error){
                                alert(data.error);
                                animateAppendTo(t.taskViews[taskid].$el, t._columns[fromColumn], 300, function(){
                                    t.$columns.sortable('refreshPositions')
                                });
                            };
                        }
                    );
                    t.taskViews[taskid].model.set(t.columnProperty, toColumn);
                    t.taskViews[taskid].render();
                }
            }).disableSelection();
        },
        addTaskRow: function addTaskRow(taskData) {
            var t = this;
            var key = taskData[this.columnProperty];
            var task = new window.taskClass(taskData);
            var taskView = new window.taskViewClass({'model': task});
            if(this._columns[key]){
                // todo: find out why we need status_type
                task.set('status_type', this.columnProperty);
                task.set(this.columnProperty, key);
                taskView.createEl().render();
                this._columns[key].append(taskView.$el);
                t.taskViews[task.id] = taskView;
            }else {
                console.log('error encountered, task could not resolve column');
                return;
            }
        }
    });
    $('.js-project-row').each(function () {
        $(this).kanban();
    });
});
