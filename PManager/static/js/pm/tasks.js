/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 24.02.13
 * Time: 21:57
 */
var CRITICALLY_THRESHOLD = 0.7;
(function ($) {

    window.taskClass = Backbone.Model.extend({
        'url': function () {
            return '/task/' + this.id + '/';
        },
        'initialize': function () {
            if (arTimers && arTimers[this.id]) {
                this.set('timer', arTimers[this.id]);
            }
        },
        'getFromServer': function (callback) {
            var t = this;
            this.fetch({
                'success': function (model, data) {
                    try {
                        data = $.parseJSON(data);
                        if (typeof(data) == typeof({}) && data.id) {
                            for (var i in data) {
                                model.set(i, data[i]);
                            }
                        }
                    } catch (e) {
                            console.log('Parse error');
                    }
                    try {
                        if (callback)
                            callback.call(t);
                    } catch (e) {
                            console.log('Callback error');
                    }
                },
                'error': function (model, data) {
                    console.log('Read task error');
                }});
        },
        'getMenuItems': function () {
            var arItems = [];
            if (this.model.get('canEdit')) {
                arItems.push({
                    'itemClass': 'Edit',
                    'itemText': 'Изменить',
                    'itemMethod': 'editTask',
                    'icon': 'edit'
                });
            }

            if (this.get('observer')) {
                arItems.push({
                    'itemClass': 'ResetPlanning',
                    'itemText': 'Не наблюдаю',
                    'itemMethod': 'stopObserve',
                    'icon': 'eye-slash'
                });
            } else {
                arItems.push({
                    'itemClass': 'BringPlanning',
                    'itemText': 'Наблюдаю',
                    'itemMethod': 'startObserve',
                    'icon': 'eye'
                });
            }
            if (this.get('canSetOnPlanning')) {
                if (this.get('onPlanning')) {
                    arItems.push({
                        'itemClass': 'ResetPlanning',
                        'itemText': 'Завершить планирование',
                        'itemMethod': 'closePlanning',
                        'icon': 'list-alt'
                    });
                } else {
                    arItems.push({
                        'itemClass': 'BringPlanning',
                        'itemText': 'Вывести на планирование',
                        'itemMethod': 'addToPlaning',
                        'icon': 'users'
                    });
                }
            }

            if (!this.get('closed') && !this.get('subtasksQty')) {
                var status = this.get('status');

                if (status == 'ready') {
                    arItems.push({
                        'itemClass': 'SetRevision',
                        'itemText': 'На доработку',
                        'itemMethod': 'setRevision',
                        'icon': 'thumbs-down'
                    });
                } else if (status == 'not_approved') {
                    if (this.get('canApprove')) {
                        arItems.push({
                            'itemClass': 'SetRevision',
                            'itemText': 'Подтвердить выполнение',
                            'itemMethod': 'approveTask',
                            'icon': 'check-square-o'
                        });
                    }
                } else {
                    arItems.push({
                        'itemClass': 'SetReady',
                        'itemText': 'На проверку',
                        'itemMethod': 'setReady',
                        'icon': 'check-square-o'
                    });
                }
            }

            if (this.get('canBaneUser')) {
                arItems.push({
                    'itemClass': 'baneUser',
                    'itemText': 'Пользователь не справился',
                    'itemMethod': 'baneUser',
                    'icon': 'exclamation-o'
                });
            }

            if (this.get('canSetCritically')) {
                var criticallyObj = {
                    'itemClass': 'Critically',
                    'itemMethod': 'toggleCritically'
                };
                if (this.get('critically') > CRITICALLY_THRESHOLD) {
                    criticallyObj['icon'] = 'ban';
                    criticallyObj['itemText'] = 'Не критичная';
                } else {
                    criticallyObj['icon'] = 'exclamation';
                    criticallyObj['itemText'] = 'Критичная';
                }
                arItems.push(criticallyObj);
            }

            if (this.get('canRemove')) {
                arItems.push({
                    'itemClass': 'Remove',
                    'itemText': 'Удалить',
                    'itemMethod': 'removeTask',
                    'icon': 'times-circle'
                });
            }
            return arItems;
        }
    });

    window.taskList = Backbone.Collection.extend({'model': window.taskClass});

    window.taskViewClass = Backbone.View.extend({
        events: function () {
            if (this.options.events) {
                return this.options.events
            } else
                return {
                    "click a.js-task_play:not('.started'):not('.disabled')": "taskStart",
                    "click a.js-task_play.started": "showPauseDialog",
                    "click a.pause_comment_success": "taskStop",
                    "click a.pause_comment_cancel": "taskStop",
                    "click a.add-subtask": "addSubTask",
                    "click a.js-task_menu": "showMenu",
                    "click a.js-task_done:not('.closed')": "closeTask",
                    "click a.js-task_done.closed": "openTask",
                    "click a.js-select_resp": "showResponsibleMenu",
                    "click a.js-resp-approve": "responsibleApprove",
                    "click .jsPlanTimeList a": "changePlanTime"
                }
        },
        'initialize': function () {
            if (!this.el) {
                this.$el = $('.taskLine_' + this.model.id);
                this.el = this.$el.get(0);
            }
            this.arPlanTimes = [
                [0.5, '30 мин.'],
                [1, '1 ч.'],
                [2, '2 ч.'],
                [3, '3 ч.'],
                [4, '4 ч.'],
                [6, '6 ч.'],
                [8, '8 ч.'],
                [10, '10 ч.'],
                [16, '16 ч.'],
                [20, '20 ч.'],
                [32, '32 ч.']
            ];
        },
        'createEl': function () {
            this.$el = $('<div></div>')
                .attr('id', 'taskLine_' + this.model.id + '')
                .addClass('task clearfix')
                .attr('data-taskid', this.model.id);
            this.el = this.$el.get(0);

            return this;
        },
        'getUrl': function () {
            return '/task_detail/?id=' + this.model.id;
        },
        'showModalStart': function () {
            //todo: разработчик нажимает раньше, чем узнает
            $('<div class="modal fade"><div id="previewModal" class="modal fade wiki-modal in" style="display: block;" aria-hidden="false"><div class="modal-dialog"><div class="modal-content ui-resizable"></div></div></div>')
                .find('modal-content').append('<h3>Сколько примерно времени у вас займет данная задача?</h3>')
                .append('<select></select>').end().modal('show');
        },
        'template': function (taskInfo, params) {
            if (!params) params = {};
            var linkSpanReplace = function ($link) {
                var $span = $('<span></span>').addClass($link.get(0).className).text($link.text());
                $link.replaceWith($span);
                return $span;
            };
            if (!window.taskHtml) return false;
            var html = window.taskHtml;
            html = html.replace(/\#TASK\_ID\#/ig, taskInfo.id);
            html = html.replace(/\#TASK\_NUMBER\#/ig, taskInfo.number);
            html = html.replace(/\#TASK\_URL\#/ig, taskInfo.url);
            html = html.replace(/\#TASK\_NAME\#/ig, taskInfo.name);

            var sLastMessage;
            if (taskInfo.last_message && taskInfo.last_message.author)
                sLastMessage = taskInfo.last_message.author + ': ' + taskInfo.last_message.text;
            else if (taskInfo.last_message)
                sLastMessage = taskInfo.last_message.text;
            else
                sLastMessage = '';

            html = html.replace(/\#LAST\_MESSAGE\#/ig, sLastMessage);

            if (!taskInfo.subtasksQty) taskInfo.subtasksQty = '';
            html = html.replace(/\#ACTIVE\_SUBTASK\_QTY\#/ig, taskInfo.subtasksQty);

            if (!taskInfo.deadline) taskInfo.deadline = '';
            if (taskInfo.deadline) taskInfo.deadline = 'до&nbsp;' + taskInfo.deadline;
            html = html.replace(/\#DEADLINE#/ig, taskInfo.deadline);

            var sFileList = '';
            for (var file_path in taskInfo.files) {
                var file = taskInfo.files[file_path];
                sFileList += '<span>&nbsp;</span><a target="_blank" class="icon-download-alt icon-'
                    + file.type + (file.is_picture ? ' fnc' : '')
                    + '" href="' + file.url + '"></a>';
            }
            html = html.replace(/\#FILE\_LIST#/ig, sFileList);

            var $row = $(html),
                parent = taskInfo.parent;

            var oTaskContainers = {
                '$taskNameCont': $row.find('.task-line_name'),
                '$statusContainer': $row.find('.task-name_status'),
                '$addSubtaskColumn': $row.find('.task_add-subtask'),
                '$timer': $row.find('.js-time'),
                '$responsibleLink': $row.find('.js_task_responsibles .dropdown'),
                '$planTime': $row.find('.task-plantime')
            };

            if (params.timerTag) {
                var $newTimerTag = $('<' + params.timerTag + ' data-toggle="dropdown" class="js-time"></' + params.timerTag + '>');
                oTaskContainers.$timer
                    .replaceWith($newTimerTag);
                oTaskContainers.$timer = $newTimerTag;
            }

            if (taskInfo.onPlanning) {
                $('<span class="task-icon onplan" title="На планировании">')
                    .appendTo(oTaskContainers.$statusContainer);
            }
            if (taskInfo.status == 'ready') {
                $('<span class="task-icon ready" title="Готова к проверке"></span>')
                    .appendTo(oTaskContainers.$statusContainer);
            } else if (taskInfo.status == 'not_approved') {
                $('<i class="fa fa-comments" style="color:#ee4343;cursor:default;" title="Задача не подтверждена"></i>')
                    .appendTo(oTaskContainers.$statusContainer);
            } else if (taskInfo.overdue) {
                $('<span class="task-icon overdue" title="Просрочена"></span>')
                    .appendTo(oTaskContainers.$statusContainer);
            }


            if (parent) {
                oTaskContainers.$addSubtaskColumn.html('<div>&nbsp;</div>');
            }

            if (taskInfo.planTime)
                taskInfo.planTime = '' + taskInfo.planTime + ' ч.';
            else
                taskInfo.planTime = '';

            var sPlanTime = '';
            if ((!taskInfo.subtasksQty || taskInfo.planTime) && (taskInfo.onPlanning || taskInfo.canSetPlanTime)) {
                sPlanTime += '<span class="dropdown">&nbsp;[ ~ </span>' +
                    '<span class="dropdown">' +
                    (taskInfo.subtasksQty ? '':'<a data-toggle="dropdown" class="jsPlanTimeHolder">')
                    + (taskInfo.planTime || 'Оценить')
                    + (taskInfo.subtasksQty ? '':'</a>');
                sPlanTime += '<ul class="dropdown-menu jsPlanTimeList">';

                for (var i in this.arPlanTimes) {
                    var planTime = this.arPlanTimes[i];
                    sPlanTime += '<li><a rel="' + planTime[0] + '">' + planTime[1] + '</a></li>';
                }
                sPlanTime += '</ul>';
                sPlanTime += '</span>';
                sPlanTime += '<span class="dropdown">]</span>';
                if (taskInfo.planTimes && taskInfo.planTimes.length > 0) {
                    sPlanTime += '<span class="dropdown arrow">';
                    sPlanTime += '<a data-toggle="dropdown" ><b class="caret"></b></a>';
                    sPlanTime += '<div class="dropdown-menu pull-right">';
                    for (i in taskInfo.planTimes) {
                        var oPlanTime = taskInfo.planTimes[i];

                        sPlanTime += '<a href="' + oPlanTime.user_url + '" rel="' + oPlanTime.user_id + '">' + oPlanTime.user_name + '</a>&nbsp;-&nbsp;' + oPlanTime.time + '&nbsp;ч<br />';
                    }
                    sPlanTime += '</div>';
                    sPlanTime += '</span>';
                }
            } else {
                sPlanTime += '&nbsp;';
            }
            oTaskContainers.$planTime.append(sPlanTime);

            var sTimerListTpl = '<a href="#URL#" rel="#">#USER#</a> - <span>#HOURS#:#MINUTES#:#SECONDS#</span><br />';
            if (taskInfo.timers && taskInfo.timers.length > 0) {
                var $realTimeListHolder = $('<div class="dropdown-menu pull-right"></div>').insertAfter(oTaskContainers.$timer);
                for (var i in taskInfo.timers) {
                    var realTime = taskInfo.timers[i];
                    var sCTHTML = sTimerListTpl.replace('#URL#', realTime.user_url);
                    sCTHTML = sCTHTML.replace('#USER#', realTime.user);
                    sCTHTML = sCTHTML.replace('#HOURS#', ((realTime.time.hours < 10 ? '0' : '') + realTime.time.hours));
                    sCTHTML = sCTHTML.replace('#MINUTES#', ((realTime.time.minutes < 10 ? '0' : '') + realTime.time.minutes));
                    sCTHTML = sCTHTML.replace('#SECONDS#', ((realTime.time.seconds < 10 ? '0' : '') + realTime.time.seconds));

                    $realTimeListHolder.append(sCTHTML);
                }
            }

            var $buttonClose = $row.find('.js-task_done');
            if (taskInfo.subtasksQty) {
                $buttonClose.hide();
            } else {
                $buttonClose.show();
                if (taskInfo.closed)
                    $buttonClose.addClass('closed');
                else
                    $buttonClose.removeClass('closed');
            }

            var $buttonStart = $row.find('.js-task_play');
            if (!taskInfo.closed) {
                if (taskInfo.startedTimerExist)
                    $buttonStart.addClass('started').find('.fa').removeClass('fa-play').addClass('fa-pause');
                else
                    $buttonStart.removeClass('started').find('.fa').removeClass('fa-pause').addClass('fa-play');
            }
            if (!params.responsibleTag) params.responsibleTag = 'a';
            var $respLink = $('<' + params.responsibleTag + '></' + params.responsibleTag + '>').attr({
                'data-toggle': 'dropdown'
            }).addClass('js-select_resp').appendTo(oTaskContainers.$responsibleLink);

            if (taskInfo.resp && taskInfo.resp[0] && taskInfo.resp[0]['name']) {
                var respName = taskInfo.resp[0];

                $respLink.text(respName['name']);
            } else if (taskInfo.recommendedUser && taskInfo.needRespRecommendation && !taskInfo.subtasksQty) {
                var restRec = $respLink.text(taskInfo.recommendedUser.name + '?').addClass('recommended');
                $('<a href=""></a>').addClass('fa fa-thumbs-o-up fa-lg fa-border js-resp-approve')
                    .attr('rel', taskInfo.recommendedUser.id).insertAfter(restRec);
            } else {
                $respLink.text('Нет ответственного');
            }

            return $row.html();
        },
        'disableTimerButton': function () {
            this.$('.js-task_play').addClass('disabled');
        },
        'enableTimerButton': function () {
            this.$('.js-task_play').removeClass('disabled').removeClass('transparent');
        },
        'hideTimerButton': function () {
            this.$('.js-task_play').addClass('disabled transparent');
        },
        'render': function () {
            var templateParams = {

            }

            var playBtnStatus = 'enabled';
            if (this.model.get('subtasksQty') > 0) {
                templateParams.responsibleTag = 'span';
                templateParams.timerTag = 'span';
                playBtnStatus = 'transparent';
            }
            this.$el.html(this.template(this.model.toJSON(), templateParams));

            if (this.model.get('closed')) {
                this.$el.addClass('closed');
                playBtnStatus = 'disabled'
            } else {
                this.$el.removeClass('closed');
            }

            if (this.model.get('onPlanning'))
                this.$el.addClass('onplan').attr('data-onplan', 'Y');
            else this.$el.removeClass('onplan').attr('data-onplan', 'N');

            var iSTUID = this.model.get('startedTimerUserId');
            if (iSTUID) {
                this.$el.attr('data-started_timer_user_id', iSTUID);
                if (window.baseUserParams.userId != iSTUID) playBtnStatus = 'disabled';
            }

            if (this.model.get('critically') > CRITICALLY_THRESHOLD) this.$el.addClass('critically').parent('.task-wrapper').addClass('critically');
            else this.$el.removeClass('critically').parent('.task-wrapper').removeClass('critically');

            if (this.model.get('startedTimerExist')) this.$el.addClass('started');
            else this.$el.removeClass('started');

            if (!this.model.get('viewed')) this.$el.addClass('newEvent');
            else this.$el.removeClass('newEvent');

            //создание таймера и добавление его модельке
            var timer = this.model.get('timer');
            if (this.model.get('time') && !this.model.get('timer')) {
                var timer = this.createTimer(this.model.get('time'));

                this.model.set('timer', timer);
            }

            if (timer) {
                timer.container = this.$el.find('.js-time').get(0);

                $(timer.container).html(timer.toString());

                if (this.model.get('startedTimerExist')) {
                    timer.start();
                } else {
                    timer.stop();
                }
            }

            if (playBtnStatus == 'disabled') {
                this.disableTimerButton();
            } else if (playBtnStatus == 'enabled') {
                this.enableTimerButton();
            } else {
                this.hideTimerButton();
            }

//                this.$('.fnc').fancybox();
            this.delegateEvents();

            if (this.$el.parent().get(0))
                setTaskCellsHeight(this.$el);

//                this.$(':checkbox').iCheck({
//                    checkboxClass: 'icheckbox_flat-grey'
//                });
            return this;
        },
        'showPauseCommentForm': function () {
            if (this.model.get('started')) {

            }
        },
        'checkModel': function (callback, forced) {
            if (!this.model.get('full') || forced) {
                this.model.getFromServer(callback);
            } else {
                callback();
            }
        },
        'createTimer': function (time) {
            var timer = new PM_Timer(time);
            timer.container = this.$el.find('.js-time').get(0);
            return timer;
        },
        'showPauseDialog': function () {
            var t = this;
            t.$('.pause_dialog').show();
            setTimeout(function () {
                t.$('.pause_dialog').one('clickoutside', function () {
                    $(this).hide();
                });
            }, 100);
            return false;
        },
        'showNextPopup': function (e) {
            var $target = $(e.currentTarget),
                $popup = $target.next();
            $popup.toggle();
            if ($popup.is(':visible')) {
                setTimeout(function () {
                    $popup.unbind('clickoutside').bind('clickoutside', function () {
                        $(this).hide()
                    });
                }, 10);
            }

            return false;
        },
        'changePlanTime': function (e) {
            var time = $(e.currentTarget).attr('rel'),
                obj = this;

            taskManager.SetTaskProperty(this.model.id, 'planTime', time, function (data) {
                obj.checkModel(function () {
                    obj.planTime = time;
                    obj.render();
                }, true);
            });
//                this.$el.find('.jsPlanTimeHolder').text(
//                    this.$el.find('.jsPlanTimeList a[rel="'+time+'"]').text()
//                );
            this.$('.task-plantime > .dropdown > .dropdown-menu').hide();
            return false;
        },
        'showResponsibleMenu': function () {
            var taskId = this.model.id,
                obj = this,
                userList = $('.responsibles.dropdown-menu').clone().show().find('a').each(function () {
                    var uId = $(this).attr('rel'), width = 0;

                    if (taskRespSummary[taskId])
                        if (taskRespSummary[taskId][uId])
                            var width = 100 * taskRespSummary[taskId][uId];

                    $(this).find('.js-progress-success').css('width', width + '%');
                    //responsible change
                    $(this).click(function () {
                        obj.changeResponsible($(this).attr('rel'));
                        $(this).closest('ul').remove();
                        return false;
                    });
                }).end();

            $('.js_task_responsibles .dropdown-menu').remove();
            var position = getObjectCenterPos(this.$('.js_task_responsibles .dropdown'));

            userList.appendTo('body').css({
                'position': 'absolute',
                'top': (position.top + position.height + 5),
                'left': position.left
            });

            setTimeout(function () {
                userList.bind('clickoutside', function () {
                    $(this).remove();
                })
            }, 10);

            return false;
        },
        'responsibleApprove': function (e) {
            var uid = $(e.currentTarget).attr('rel');
            this.changeResponsible(uid);
            return false;
        },
        'stopAllTask': function () {
//            $('.Item.started a.taskPlayStop.stop').trigger('click');
        },
        'stopTaskViewWithoutServerSide': function (e) {
            this.taskStop(e, true);
            this.model.set({
                'started': false,
                'startedTimerExist': false
            });
            this.render();
        },
        'startTaskViewWithoutServerSide': function (e) {
            this.model.set({
                'started': true,
                'startedTimerExist': true
            });
            this.model.get('timer').start();
            this.render();
        },
        'taskStop': function (e, onlyView) {
//                if (!this.model.get('started')) return false;

            var comment = this.$('textarea[name=comment]').val();

            if (e && $(e.currentTarget).hasClass('pause_comment_cancel')) {
                this.$('textarea[name=comment]').val('');
                comment = '';
            } else if (!comment) {
                this.$('textarea[name=comment]').addClass('alert-error').one('keyup', function () {
                    $(this).removeClass('alert-error');
                    return false;
                });
                return false;
            }
            this.$('.js-task_play').removeClass('started');
            var obj = this;

            if (!onlyView)
                taskManager.TaskStop(this.model.id, {
                    'comment': comment,
                    'public': (this.$('input[name=addComment]').is(':checked') ? 1 : 0)
                }, function (data) {
                    obj.model.set({
                        'started': false,
                        'startedTimerExist': false
                    });

                    if (obj.model.get('timer'))
                        obj.model.get('timer').stop();

                    if (window.mainTimer) {
                        window.mainTimer.stop();
                        if (CURRENT_TASK_VIEW) {
                            CURRENT_TASK_VIEW.stopTaskViewWithoutServerSide(e);
                        }
                    }
                    obj.$('.pause_dialog').hide();
                    obj.render();
                    userDynamics.getOpenTask();
                });

            return false;
        },
        'taskStart': function (e, onlyView) {
            if (this.model.get('started')) return false;

            var obj = this;
            if (!onlyView) {
                obj.stopAllTask();
                taskManager.TaskStart(this.model.id, function (data) {
                    data = $.parseJSON(data);

                    if (data.error) {
                        alert(data.error);
                        return false;
                    }

                    obj.$('.js-task_play').addClass('started');
                    obj.model.set({
                        'started': true,
                        'startedTimerExist': true,
                        'deadline': data.deadline
                    });

                    if (!obj.model.get('timer')) {
                        var timer = new PM_Timer({'container': obj.$('.js-time').get(0)});
                        $(timer.container).html(timer.toString());
                        obj.model.set('timer', timer);
                    }

                    obj.render();

                    obj.model.get('timer').start();

                    if (window.mainTimer) {
                        currentTaskInit(false, obj.model);
                        window.mainTimer.start();
                        if (CURRENT_TASK_VIEW) {
                            CURRENT_TASK_VIEW.startTaskViewWithoutServerSide(e);
                        }
                    }
                });
            }
            return false;
        },
        'openTask': function () {
            if (!this.model.get('closed')) return false;
            this.taskStop();

            var obj = this;
            taskManager.TaskOpen(this.model.id, function (data) {
                obj.model.set('closed', false);
                obj.render();
            });

            return false;
        },
        'closeTask': function () {
            if (this.model.get('closed')) return false;
            this.taskStop();

            var obj = this;
            taskManager.TaskClose(this.model.id, function (data) {
                data = $.parseJSON(data);
                obj.model.set('closed', data.closed);
                obj.model.set('status', data.status);
                if (data.closed) {
                    obj.render();
                } else {
                    obj.checkModel(function () {
                        obj.render();
                    });
                }

                obj.delegateEvents();
            });

            return false;
        },
        'addToPlaning': function () {
            if (this.model.get('onPlanning')) return false;
            var obj = this;
            taskManager.AddToPlanning(this.model.id, function () {
                obj.checkModel(function () {
                    obj.model.set('onPlanning', true);
                    obj.render();
                });
            });
            return false;
        },
        'editTask': function () {
            document.location.href = '/task_edit/?id=' + this.model.id + '&backurl=' + (window.backurl ? window.backurl : "/");
        },
        'stopObserve': function () {
            var t = this;
            taskManager.simpleAction(this.model.id, 'stopObserve', function () {
                t.model.set({
                    'observer': false
                });
                t.render();
            });
        },
        'startObserve': function () {
            var t = this;
            taskManager.simpleAction(this.model.id, 'startObserve', function () {
                t.model.set({
                    'observer': true
                });
                t.render();
            });
        },
        'closePlanning': function () {
            if (!this.model.get('onPlanning')) return false;
            var obj = this;
            taskManager.RemoveFromPlanning(this.model.id, function () {
                obj.checkModel(function () {
                    obj.model.set('onPlanning', false);
                    obj.render();
                });
            });
            return false;
        },
        'approveTask': function () {
            var t = this;
            if (!t.model.get('resp')[0] || !t.model.get('resp')[0]['name']) {
                alert('Подтвердить выполнение задачи можно только если выбран исполнитель.');
                return false;
            }
            if (!t.model.get('planTime')) {
                alert('Подтвердить выполнение можно только для оцененной задачи.');
                return false;
            }
            if (ACCOUNT_TOTAL < t.model.get('planPrice')) {
                alert(
                    'У вас недостаточно средств для выполнения данной задачи (необходимо ' +
                        Math.round(t.model.get('planPrice')) +
                        ' sp).'
                );
                return false;
            }

            this.setRevision();
            return true;
        },
        'setRevision': function () {
            var t = this;
            taskManager.SetTaskProperty(this.model.id, 'status', 'revision', function (data) {
                t.checkModel(function () {
                    t.model.set('status', 'revision');
                    t.render();
                });
            });
        },
        'removeTask': function () {
            if (confirm('Вы действительно хтотите удалить эту задачу?')) {
                taskManager.deleteTask(this.model.id, function () {

                });
                this.model.destroy();
                if (!this.model.get('parent'))
                    this.$el.parent().remove();
                this.remove();
            }
        },
        'setReady': function () {
            var t = this;
            taskManager.SetTaskProperty(this.model.id, 'status', 'ready', function (data) {
                t.checkModel(function () {
                    t.model.set('status', 'ready');
                    t.render();
                });
            });
        },
        'baneUser': function () {
            var t = this;
            taskManager.BaneUser(this.model.id, function (data) {
                t.checkModel(function () {
                    t.model.set('resp', []);
                    t.render();
                });
            })
        },
        'toggleCritically': function () {
            var t = this, critically;

            if (this.model.get('critically') > CRITICALLY_THRESHOLD) {
                critically = 0.5;
            } else {
                critically = 0.95;
            }
            taskManager.SetTaskProperty(this.model.id, 'critically', critically, function (data) {
                t.checkModel(function () {
                    t.model.set('critically', critically);
                    t.render();
                });
            });
        },
        'addSubTask': function () {

        },
        'changeResponsible': function (uid) {
            var obj = this;
            taskManager.ChangeResponsible(this.model.id, uid, function (data) {
                obj.checkModel(function () {
                    obj.model.set('recommendedUser', false);
                    obj.model.set('resp', [
                        {'name': data}
                    ]);
                    obj.render();
                });
            })
        },
        'showMenu': function (e) {
            var arMenu = this.model.getMenuItems(),
                menuClass = 'task-menu',
                $taskMenu = $('<ul class="dropdown-menu pull-right text-left ' + menuClass + '"></ul>'),
                obj = this;
            $('.' + menuClass + '').remove();
            for (var i in arMenu) {
                var menuItem = arMenu[i],
                    $menuItem = $('<a></a>');
                (function (func) {
                    $menuItem
                        .append('<i class="fa fa-' + menuItem['icon'] + '"></i>&nbsp;&nbsp;')
                        .append(menuItem['itemText'])
                        .addClass(menuItem['itemClass'])
                        .attr('rel', menuItem['rel'])
                        .click(function () {
                            obj[func]();
                            $taskMenu.remove();
                            return false;
                        });
                    $('<li></li>').append($menuItem).appendTo($taskMenu);
                })(menuItem['itemMethod']);
            }

            $taskMenu.appendTo(this.$('.js-options_popup'))
                .show();
            $(document).one('click', function () {
                $taskMenu.remove();
            });

            e.stopPropagation();
            return false;
        }
    });

    var taskAjaxManagerClass = function () {

    };

    taskAjaxManagerClass.prototype = {
        'ajaxUrl': '/task_handler',
        'taskAjaxRequest': function (data, callback, type) {
            return PM_AjaxPost(this.ajaxUrl, data, callback, type);
        },
        'TaskOpen': function (task_id, call) {
            if (!task_id) return false;
            this.taskAjaxRequest({
                'action': 'taskOpen',
                'id': task_id
            }, call);
            return this;
        },
        'TaskClose': function (task_id, call) {
            if (!task_id) return false;
            this.taskAjaxRequest({
                'action': 'taskClose',
                'id': task_id
            }, call);
            return this;
        },
        'simpleAction': function (task_id, action, call) {
            if (!task_id) return false;
            this.taskAjaxRequest({
                'action': action,
                'id': task_id
            }, call);
            return this;
        },
        'deleteTask': function (task_id, call) {
            if (!task_id) return false;
            this.taskAjaxRequest({
                'action': 'deleteTask',
                'id': task_id
            }, call);
            return this;
        },
        'TaskStart': function (task_id, call) {
            if (!task_id) return false;
            this.taskAjaxRequest({
                'action': 'taskPlay',
                'id': task_id,
                'play': task_id
            }, call);
            return this;
        },
        'TaskStop': function (task_id, addParams, call) {
            if (!task_id) return false;
            this.taskAjaxRequest(
                $.extend(addParams, {
                    'action': 'taskStop',
                    'id': task_id,
                    'pause': task_id
                }), call);
            return this;
        },
        'CreateTask': function (taskParams, parentTask, call) {
            if (!taskParams.taskname) return false;
            this.taskAjaxRequest({
                'action': 'fastCreate',
                'task_name': taskParams.taskname,
                'files': taskParams.files,
                'parent': parentTask
            }, call);
        },
        'SetTaskProperty': function (task_id, prop_code, val, call) {
            if (task_id && prop_code && val) {
                this.taskAjaxRequest({
                    'id': task_id,
                    'prop': prop_code,
                    'val': val
                }, call);
            }
        },
        'AddToPlanning': function (id, call) {
            if (id) {
                this.taskAjaxRequest({
                    'id': id,
                    'prop': 'to_plan'
                }, call);
            }
        },
        'BaneUser': function (id, call) {
            if (id) {
                this.taskAjaxRequest({
                    'id': id,
                    'action': 'baneUser'
                }, call);
            }
        },
        'RemoveFromPlanning': function (id, call) {
            if (id) {
                this.taskAjaxRequest({
                    'id': id,
                    'prop': 'from_plan'
                }, call);
            }
        },
        'ChangeResponsible': function (id, uid, call) {
            if (!id) return false;
            if (!uid) return false;
            return this.taskAjaxRequest({
                'id': id,
                'resp': uid
            }, call);
        }
    };

    taskManager = new taskAjaxManagerClass();

    /**
     * создание на основе <div ..><a ... </a><a ... </a></div> моделей
     * поп-апов к input на основе введенных данных
     * @param input
     */
    var inputHintsManagerClass = function (input, tags, blocks) {
        this.$input = $(input);
        this.currentHint = false;
        this.inputText = '';
        //this.tags = tags;
        this.tags = {
            'Responsible': 'для ',
            'Date': ' до ',
            'Author': ' от ',
            'About': 'примерно '
        };
        //this.hintBlocks = blocks;
        this.hintBlocks = {
            'Responsible': $('#responsible_list'),
            'Date': $('#date_select_list'),
            'About': $('#deadline_select_list'),
            'Author': $('#author_list')
        };
        this.init();
    };

    inputHintsManagerClass.prototype = {
        'init': function () {
            var obj = this;
            obj.$input.keyup(function (e) {
                var key = getKeyPressed(e)
                    , tag = "", exist = false;
                obj.createCommand = '';
                for (var keytag in obj.tags) {
                    tag = obj.tags[keytag];

                    if ($(this).val().lastIndexOf(tag) != -1 && $(this).val().lastIndexOf(tag) == ($(this).val().length - tag.length)) {
                        obj.createCommand = tag;
                    }
                }

                if (e.ctrlKey && key == 32) { //ctrl+space
                    if (obj.createCommand)
                        obj.showHintByTag(this);
                } else if (e.ctrlKey && key == 78) { //ctrl+N
                    $('body,html').scrollTop(obj.$input.focus().offset().top);
                    return false;
                } else if (key == 40 && obj.currentHint.name) { //arrow down
                    obj.currentHint.container.find('a:visible').removeClass('selected').filter(':first').addClass('selected').focus();
                } else if (!e.ctrlKey && key != 13) {
                    obj.showHintByTag(this);
                }
            });

            for (var i in obj.hintBlocks) {
                obj.hintBlocks[i].keydown(function (e) {
                    var key = getKeyPressed(e);
                    if (obj.currentHint) {
                        if (key == 40) { //down
                            $(this).find('a.selected').removeClass('selected').next().addClass('selected').focus();
                            return false;
                        } else if (key == 38) { //up
                            $(this).find('a.selected').removeClass('selected').prev().addClass('selected').focus();
                            return false;
                        }
                    }
                });
            }
            for (var i in this.hintBlocks) {
                var block = this.hintBlocks[i];

                block.find('a').click(function () {
                    obj.pasteTag($(this).attr('rel'), i);
                    return false;
                });
            }
        },
        'showHint': function (hintName) {
            if (!hintName) return false;
            var hint_block = this.hintBlocks[hintName];
            var field = this.$input;
            var tags = this.tags;
            var obj = this;
            this.posDivToField(hint_block, field);

            this.inputText = '';

            $(field).unbind('keyup.' + hintName).bind('keyup.' + hintName, function (e) {
                var key = getKeyPressed(e);
                var lastFor = 0;
                if (lastFor = $(this).val().lastIndexOf(tags[hintName])) {
                    obj.inputText = $(this).val().substring((lastFor + tags[hintName].length), $(this).val().length);

                    var userLinks = obj.hintBlocks[hintName].find('a').show();

                    if (obj.inputText)
                        userLinks.not(":Contains('" + obj.inputText + "')").hide();

                    if (!userLinks.filter(":visible").get(0)) {
                        obj.hideHint()
                    }
                }
            });

            this.currentHint = {
                'name': hintName,
                'container': hint_block
            };
            return hint_block;
        },
        'posDivToField': function (block, field_selector) {
            if (!block) return false;
            var field = $(field_selector);
            if (typeof(block) == 'object') {
                block.show().appendTo(field.parent());
            }
        },
        'pasteTag': function (name, tag, new_val) {
            this.hideHint();
            /*var full_name = this.hintBlocks[tag].find('a[rel='+name+']').text();*/
            var inpval = this.$input.val();
            var pos = inpval.lastIndexOf(this.tags[tag]);

            pos += this.tags[tag].length;
            inpval = inpval.substring(0, pos);
            this.$input.val(
                inpval + "#" + (name == 'new' ? '' : name) + "#"
            ).focus();
            if (name == 'new') {
                var len = this.$input.val().length - 1;
                this.$input.get(0).setSelectionRange(len, len);
            }
            return false;
        },
        'hideHint': function () {
            if (this.currentHint.name) {
                this.currentHint.container.find('*').show().end().hide();
                this.$input.unbind('keyup.' + this.currentHint.name);
                this.currentHint = {}
            }
        },
        'showHintByTag': function (field) {
            if (!this.createCommand) return false;
            var currentTag = false;
            for (i in this.tags) {
                if (this.tags[i] == this.createCommand) {
                    currentTag = i;
                    break;
                }
            }
            if (currentTag) {
                this.showHint(currentTag, field);
            }
            /*else{
             this.hideHint();
             }*/
        }
    };

    $.fn.addTaskFilePasteSimple = function () {
        this.addFilePaste(function (data) {
            data = $.parseJSON(data);
            if (data && data.fid)
                $(this).val($(this).val() + ' файл #' + data.fid + '#').focus();
        });
        return this;
    }

})(jQuery);