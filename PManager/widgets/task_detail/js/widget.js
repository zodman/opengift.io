/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 */
var widget_td;
$(function(){
    widget_td = new widgetObject({id:'task_detail'});

    widget_td.state = {
        taskCreate:false,
        hintOpened:{
            'Responsible':false,
            'Date':false,
            'Author':false
        }
    }

    widget_td.task_id = arJSParams['taskId'];
    widget_td.TaskTimers = arTimers;
    widget_td.message_selector = '.js-taskMessage';
    widget_td.message_remove_selector = '.js-removeTaskMessage';
    widget_td.$container = $('#task_detail');
    widget_td.$task_holder = widget_td.$container.find('.subtask');
    widget_td.$messageList = widget_td.$container.find('.js-commentsContainer');
    widget_td.$userToSelect = false;
    widget_td.$createTaskInput = widget_td.$container.find('.js-addTaskInput input:text');
    widget_td.$blockAfterNewTask = widget_td.$task_holder.find('.js-addTaskInput');
    widget_td.$messageForm = widget_td.$container.find('form.newMessage');
    widget_td.subtasks = new window.taskList();
    widget_td.subtaskTemplates = {};

    widget_td.messageListHelper = new messageListManager(widget_td.$messageList, widget_td.task_id, task_detail_message_tpl);

    widget_td.subtaskTemplate = '<hr /><div id="taskLine_#TASK_ID#" data-taskid="#TASK_ID#" class="task clearfix">' +
                                    '<div class="span7 task-title">' +
                                        '<span class="task-name-wrapper"> #TASK_NAME# </span>' +
                                    '</div>' +
                                    '<div class="span2 task-responsibles">' +
                                        '<span class="dropdown">' +
                                            '<a href="" data-toggle="dropdown"></a>' +
                                        '</span>' +
                                    '</div>' +
                                    '<div class="span2 task-time">' +
                                        '<div class="inline task-timer">' +
                                            '<span class="dropdown">' +
                                                '<a class="Time" href="#" data-toggle="dropdown">#TIMER#</a>' +
                                            '</span>' +
                                        '</div>' +
                                        '<div class="inline task-plantime"> #PLAN_TIME# </div>' +
                                    '</div>' +
                                    '<div class="task-manage">' +

                                    '</div>' +
                                '</div>';

    $.extend(widget_td,{
        'init':function(){
            var t = this;
            t.model = new window.taskClass(taskDetail);

            t.view = new window.taskViewClass({
                el:widget_td.$container.find('.widget-title').get(0),
                $el:widget_td.$container.find('.widget-title').eq(0),
                model:t.model
            });
            t.view.render = function(){
                if (this.model.get('closed')){
                    this.$el.addClass('closed').find('.js-task_done').addClass('closed');
                }else{
                    this.$el.removeClass('closed').find('.js-task_done').removeClass('closed');
                }
                if (this.model.get('startedTimerExist')){
                    this.$('.js-task_play').addClass('started').find('.fa').removeClass('fa-play-circle').addClass('fa-pause');
                }else{
                    this.$('.js-task_play').removeClass('started').find('.fa').addClass('fa-play-circle').removeClass('fa-pause');
                }

                //from tasks.js
                var $buttonClose = this.$('.js-task_done');
                var $approveBtn = this.$('.js-task_approve');
                if (this.model.get('subtasksQty')) {
                    $buttonClose.hide();
                    $approveBtn.hide();
                } else {
                    if (this.model.get('closed')) {
                        $buttonClose.hide();
                        $approveBtn.hide();
                    } else {
                        if (this.model.get('status') == 'not_approved') {
                            if (this.model.get('canApprove'))
                                $approveBtn.show();

                            $buttonClose.hide();
                        } else {
                            $approveBtn.hide();
                            $buttonClose.show();
                            var $closeIcon = $buttonClose.find('.fa');
                            if (this.model.get('canClose')) {
                                $closeIcon.removeClass('fa-check').addClass('fa-close');
                            } else {
                                $closeIcon.removeClass('fa-close').addClass('fa-check');
                            }
                        }
                    }
                }
                this.undelegateEvents();
                this.delegateEvents();
            }

            baseConnector.addListener('connect', function(){
                    t.view.checkModel(function(){
                    t.view.render();
                }, true)
            });

            $('.sendTaskMessage').on("click", function(){
                var closeTask = $(this).hasClass('btn-close'),
                    btn = this,
                    actions = false,
                    parForm = $(this).closest("form.newMessage"),
                    getTextarea = parForm.find("textarea"),
                    getCheckboxs = parForm.find("input[type=checkbox]"),
                    searchLoadBufPhotos = parForm.find("input[name=uploaded_files]"),
                    searchInputPhotos = parForm.find("input[type=file]");


                if(getTextarea.val() != '') actions = true; //Проверка Textarea
                /*getCheckboxs.each(function(){ //Проверка Checkbox'ы
                    if($(this).prop("checked")) actions = true;
                });*/
                if(searchLoadBufPhotos.length) actions = true; //Проверка закрепленных из буфера фотографии
                searchInputPhotos.each(function(){ //Проветка выбор фотографии
                    if($(this).val() != '') actions = true;
                });

                if(actions){
                    if (!$(btn).pushed()){
                        if (closeTask) {
                            $(btn).parent().find('[name=close]').val('Y');
                        }

                        $(btn).pushTheButton();
                        widget_td.newMessage(function(data){
                            $(btn).pullTheButton();
                        });
                    }
                    getTextarea.closest(".form-group.has-error").removeClass("has-error");
                } else getTextarea.focus().closest(".form-group").addClass("has-error");

                return false;
            });

            //Отслеживать ctrl+enter
            $(document).keydown(function(event) {
                if (event.which == 13 && (event.ctrlKey || event.metaKey)){
                    $('.sendTaskMessage:not(.btn-close, .js-change_resp)').click();
                };
            });

            $(document).on("keypress", "form.newMessage .combobox-container .combobox", function(e){
                if(e.which == 13){
                    $('.sendTaskMessage:not(.btn-close)').click();
                    $("form.newMessage").submit(function(){
                        return false;
                    });
                }
            });

            widget_td.$task_holder.on('click','.js-ShowClosedSubtasks', function(){
                var proc,h='hidden';
                if ($(this).data('open')){
                    proc = function(view){
                        return view.$el.addClass(h).prev('hr').addClass(h);
                    }
                    $(this).data('open',false).text('Показать закрытые задачи');
                }else{
                    proc = function(view){
                        return view.$el.removeClass(h).prev('hr').removeClass(h);
                    }
                    $(this).data('open',true).text('Скрыть закрытые подзадачи');
                }
                for (var i in widget_td.subtaskTemplates){
                    var view = widget_td.subtaskTemplates[i];
                    if (view.model.get('closed')){
                        proc(view);
                    }
                }
                return false;
            });

            var task;
            for (var i in aSubTasks){
                task = new window.taskClass(aSubTasks[i]);
                widget_td.subtasks.add(task);
            }

            widget_td.subtasks.each(function(task){
                var view = new window.taskViewClass({'model':task});
                view.createEl().render();

                widget_td.addTaskElementAndHr(view.$el);

                if (view.model.get('closed')){
                    view.$el.addClass('hidden').prev('hr').addClass('hidden');
                }
                widget_td.subtaskTemplates[task.id] = view;
            });

            this.subtasks.on('add',function(task){

            });

            widget_td.messageListHelper.addMessages(arJSParams.messages);

            baseConnector.addListener('fs.comment.add', function(data){
                if (data && data.task){
                    if (data.task.id == widget_td.task_id){
                        widget_td.messageListHelper.addMessages([data]);
                    }
                }
            });

            if (arTimers)
                for (var i in arTimers){
                    if (widget_td.subtaskTemplates[i])
                        arTimers[i].container = $('#taskLine_'+i+' .js-time');
                    $(arTimers[i].container).html(arTimers[i].toString());
                }

            widget_td.$createTaskInput.enterPressed(function(e){
                    widget_td.CreateSubTask();
                    return false;
            });

            widget_td.$messageForm.find('textarea[name=task_message]').addFilePaste(function(data){
                data = $.parseJSON(data);

                if (data && data.fid)
                    widget_td.$messageForm.find('.uploaded_file')
                        .append('<p>Загружен файл: ' + data.fid + '</p>')
                        .append('<input name="uploaded_files" value="' + data.fid + '" type="hidden" />');
            });
            widget_td.removeTempScripts();
            baseConnector.addListener('fs.task.update', function(data){
                if (data.id == widget_td.model.id){
                    widget_td.model.set(data);
                    widget_td.view.render();
                }
            });

            widget_td.$messageList.on('click', '.js-quote', function(){
                widget_td.quote($(this).closest('.js-taskMessage')
                    .find('div.js-messageDetailText').eq(0).clone()
                    .find('blockquote').remove().end()
                    .text().replace(new RegExp('&lt;','mig'), '<'));
                return false;
            });
            widget_td.$messageList.on('click', '.js-reply', function(){
                var selData = widget_td.$userToSelect.data('combobox').map;
                for (var i in selData){
                    if (selData[i] == $(this).attr('rel')){
                        widget_td.$messageForm.find('input:text.combobox').val(i);
                    }
                }
                widget_td.$messageForm.find('[name=to]').val($(this).attr('rel'));

                widget_td.quote($(this).closest('.js-taskMessage')
                    .find('div.js-messageDetailText').eq(0)
                    .find('blockquote').remove().end()
                    .html().replace(new RegExp('&lt;','mig'), '<'));
                return false;
            });
            widget_td.$userToSelect = $('.combobox').combobox();
        },
        'quote': function(text) {
            if (text){
                text = '>> ' + text.replace(new RegExp('<br />(.+)','mig'), "\r\n>> $1")
                    .replace(new RegExp('<br>(.+)','mig'), "\r\n>> $1")
                    .replace(new RegExp('&gt;', 'mig'), '>')
                    .replace(new RegExp('<br>','mig'), '');
                var $txtarea = widget_td.$messageForm.find('textarea[name=task_message]');
                $txtarea.val($txtarea.val() + text + "\r\n").focus();
            }
        },
        'removeTempScripts': function(){
            $('.temp_scripts').remove();
        },
        'removeMessage': function(id){
            return this.removeMessageRequest(id, function(data){
                if (data.success == "Y")
                    $(widget_td.message_selector).filter('[data-id='+id+']').remnove();
            });
        },
        'removeMessageRequest': function(id, callback){
            return PM_AjaxPost('/task_handler',{
                'action':'removeMessage',
                'id':id
            },callback,'json');
        },
        'newMessage': function(callback){
            if (widget_td.task_id){
//                var text = widget_td.$messageForm.find('textarea[name=task_message]').val();
                widget_td.$messageForm.ajaxSubmit({
                    'success': function(data){
                        data = $.parseJSON(data);
                        widget_td.messageListHelper.addMessages([data]);
                        widget_td.$messageForm.find('textarea[name=task_message], input:file').val('');
                        widget_td.$messageForm.find('.uploaded_file').empty();
                        if (callback) callback(data);
                    }
                });
            }
        },
        'CreateTaskRow':function(oTaskData){
            if (!oTaskData.id) return false;
            var model = new window.taskClass(oTaskData);
            var view = new window.taskViewClass({model:model});
            view.createEl().render();
            this.addTaskElementAndHr(view.$el);
            return view.$el;
        },
        'addTaskElementAndHr':function($el){
            $($el).insertBefore(this.$blockAfterNewTask);
//            if ($el.prev().get(0))
//                $('<hr />').insertBefore($el);TODO: проставлять класс first
        },
        'CreateSubTask': function(taskname){
            if (!taskname) taskname = widget_td.$createTaskInput.val();
            if (!taskname) return false;

            taskManager.CreateTask({'taskname':taskname}, widget_td.task_id, function(data){
                var data = $.parseJSON(data);
                if (data.parent != widget_td.task_id) {
                    document.location.href = '/task_detail/?id='+data.parent;
                    return;
                }

                if (data.name){
                    widget_td.$createTaskInput.val('');
                    var $taskRow = widget_td.CreateTaskRow(data, widget_td.task_id);

                    if ($taskRow){
                        arTimers[data.id] = new PM_Timer();
                        arTimers[data.id].container = $taskRow.find('.Time').eq(0);

                        arTimers[data.id].container.html(arTimers[data.id].toString());
                    }

                }
            });

            return this;
        }
    });

    widget_td.init();

    document.mainController.widgetsData["task_detail"] = widget_td;
});