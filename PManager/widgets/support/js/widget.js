/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 * To change this template use File | Settings | File Templates.
 */

$(function(){
    var widget_sp = new widgetObject({id:'support'});
    widget_sp.state = {
        taskCreate:false,
        hintOpened:{
            'Responsible':false,
            'Date':false,
            'Author':false
        }
    }
    
    widget_sp.container = $('.WrapperBlock.Support');

    $.extend(widget_sp,{
        'create_command':'',
        'User_List':{},
        'Tasks': new window.taskList(),
        'TaskTemplates':{

        },
        'Tags':{
            'Responsible':'для ',
            'Date':' до ',
            'Author': ' от ',
            'About':'примерно '
        },
        'TaskTimers':arTimers,
        'init': function(){
            this.container.find('.Item').each(function(){
                var started = $(this).hasClass('started'),
                    onplan = $(this).attr('data-onplan') == 'Y',
                    closed = $(this).hasClass('closed');

                var task = new window.taskClass({'id':$(this).attr('data-taskid'),'started':started,'closed':closed,'onPlanning':onplan,'name':$(this).find('.taskName').text(),'responsible':[$(this).find('.TaskAuthorName a').eq(0).text()]}),
                    view = new window.taskViewClass({'model':task,'el':$(this)});

                widget_sp.Tasks.add(task);
                widget_sp.TaskTemplates[task.id] = view;
            });
            this.Tasks.on('add',function(task){

            });
            var obj = this;
            baseConnector.addListener('fs.task.update',function(data){
                if (data && data.id){
                    if (obj.TaskTemplates[data.id]){
                        var view = obj.TaskTemplates[data.id];
                        view.checkModel(function(){
                            for (var i in data){
                                if (i != 'id'){
                                    view.model.set(i, data[i]);
                                }
                            }
                            view.render();
                        });
                    }
                }
            });
        },
        'PosDivToField': function(block,field_selector){
            if (!block) return false;
            var field = $(field_selector), left = field.offset().left + (field.val().length*5)
            if (typeof(block)=='object'){
                block.show();
            }
            return false;
        },
        'CreateTask': function(taskname,parentTask){
            if (!taskname) taskname = widget_sp.CreateTaskInput.val();
            if (!taskname) return false;
            taskManager.CreateTask(taskname, parentTask, function(data){
                var data = $.parseJSON(data);
                if (data.name){
                    widget_sp.CreateTaskInput.val('');
                    var taskRow = widget_sp.AddTaskLine(data,parentTask);
                    if (taskRow){
                        arTimers[data.id] = new PM_Timer();
                        arTimers[data.id].container = taskRow.find('.Time').eq(0);

                        arTimers[data.id].container.html(arTimers[data.id].toString());
                    }
                }
            });

            return this;
        },
        'AddTaskLine':function(taskObj,parentTask){
            if (!taskObj || !taskObj.name) return false;
            //this.CreateTaskRow(taskObj,parentTask);
            return this.CreateTaskRow(taskObj,parentTask);
        },
        'Search':function(params){
            var loader = startLoader('medium',this.Container,{'top':'-150'});

            if (!params){
                if ($('#addTaskMenu li.Active').attr('rel')) var action = $('#addTaskMenu li.Active').attr('rel');
                else var action = 'all';

                params = {
                    'task_search':this.GetSearchText(),
                    'action':action
                }
            }
            //собираем все элементы формы поиска (созданные через поисковое муню)
            var searchForm = this.SearchTask.closest('.SearcheBlock');
            searchForm.find('input[type=hidden]').each(function(){
                params[$(this).attr('name')] = $(this).val();
            });

            var obj = this;
            PM_AjaxPost("/task_handler",
                params,
                function(data){
                    var data = $.parseJSON(data);
                    stopLoader(loader);

                    if (!params.parent && !params.page){
                        arTimers = {};
                        obj.Container.empty();
                    }

                    for (i in data){
                        var taskInfo = data[i];
                        obj.CreateTaskRow(taskInfo,params.parent);
                    }
                    if ((!data || data.length<=0) && !params.parent){
                        obj.Container.html("<div><span class='empty_result'>Ничего не найдено</span></div>");
                    }
                //obj.Container = obj.Container.replaceWith(data);
            });
            return this;
        },
        'GetSearchText':function(){
            var text = this.SearchTask.val();
            if (text == this.SearchTask.attr('data-blur')) text = '';
            return text;
        },
        'CreateTaskRow':function(taskInfo,parent){
            if (!taskInfo.id) return false;
            var task = widget_sp.Tasks.get(taskInfo.id);
            if (task){
                for (var i in taskInfo){
                    task.set(i,taskInfo[i]);
                }
            }else{
                task = new window.taskClass(taskInfo);
                widget_sp.Tasks.add(task);
            }

            var view = new window.taskViewClass({'model':task});
            widget_sp.TaskTemplates[task.id] = view;

            view.createEl().render();
            if (!parent){
                this.Container.append(view.$el);
            }else{
                view.$el.appendTo($('#taskLine_'+parent).next('.SubtaskBlock'));
            }

            if (!parent)
                $('<div class="SubtaskBlock"></div>').insertAfter(view.$el);

            return view.$el;
        },
        'GetTaskUrl':function(id){
            return "task_edit/?id="+id+"";
        },
        'addSubtaskRow':function(taskId){
            var taskRow = $('#taskLine_'+taskId+'');
            if (!taskRow.next('.SubtaskBlock').html()){
                var subtaskRow = $('.AddTaskBlock.Left').clone().removeClass('Left');
                taskRow.next('.SubtaskBlock').append(subtaskRow);
                var subtaskInput = taskRow.next('.SubtaskBlock').find('input[type=text]').eq(0);
                //var subtaskRow = $('<tr class="subtask"></tr>').append('<td></td>').find('td').addClass('taskTitle').attr('colspan','4').append(subtaskInput)
                //                .end().insertAfter(taskRow);
                return subtaskInput.val('');
            }else{
                //taskRow.find('.SubtaskBlock').hide()
                //taskRow.next().remove();
                return false;
            }
        },
        'addEventsToSubtaskInput':function(input){

        }
    });

    widget_sp.init();

    var search_timeout = false;
    $('#search').keyup(function(){
        if (search_timeout) clearTimeout(search_timeout);
        var obj = this;
        search_timeout = setTimeout(function(){
            widget_sp.Search();
        },500);
    });
    $('.show-more').click(function(){
        widget_sp.Search({'page':2,'action':'all'});
    });

    $('#addTaskMenu li').click(function(){
        $('#addTaskMenu li').removeClass('Active');
        $('#get_all').removeClass('active');
        $(this).addClass('Active');

        widget_sp.Search();
        return false;
    });

    $('#get_all').click(function(){
        $('#addTaskMenu li').removeClass('Active');
        $(this).addClass('active');

        widget_sp.Search();
        return false;
    });

    document.mainController.widgetsData["taskList"] = widget_sp;
    //таймеры
    if (arTimers)
        for (var i in arTimers){
            arTimers[i].container = $('#taskLine_'+i+' .Time');
            arTimers[i].container.html(arTimers[i].toString());
        }

    $('#task_create').addFilePaste(function(data){
        data = $.parseJSON(data);
        if (data && data.fid)
            $(this).val($(this).val()+' файл #'+data.fid+'#').focus();
    });
    $('.search_menu > ul > li > ul > li > a').click(function(){
        var category = $(this).parent().parent().parent(),
            field_name = category.attr('data-code'),
            field_title = category.children('a').text(),
            value = $(this).attr('rel'),
            value_title = $(this).text(),
            search_form = $('.SearcheBlock'),
            category_container = $('.search_items_holder');

        var categoryBlock = category_container.find('span[data-code='+field_name+']');
        if (!categoryBlock.get(0)){
            category_container.append(categoryBlock = $('<span></span>').attr('data-code',field_name).text(field_title))
                              .append('<ul></ul>');
        }
        categoryBlock.next('ul').find('li[data-code='+value+']').remove()
                          .end().append('<li data-code='+value+'><a href="#" class="added-user">'+value_title+'</a><a href="#" class="delete-added-user"><img src="/static/images/red-cross.png" /></a></li>');

        if (!search_form.find('input[name='+field_name+'][value='+value+']').get(0)){
            search_form.append($('<input type="hidden" />').attr({'name':field_name,'value':value}));
        }

        $('.search_menu').hide();
        widget_sp.Search();
        return false;
    });
    $('.SearcheBlock').on('click','.delete-added-user',function(){
        var field_name = $(this).closest('ul').prev().attr('data-code'),
            value = $(this).parent().attr('data-code'),
            least = $(this).parent().parent().find('li').length == 1,
            search_form = $('.SearcheBlock');
        search_form.find('input[name='+field_name+'][value='+value+']').remove();
        if (least){
            $(this).closest('ul').prev().remove()
                           .end().remove();
        }else{
            $(this).closest('li').remove();
        }
        widget_sp.Search();
        return false;
    });
    $('.AddTaskBlock > div').bind('clickoutside', function(){
        $(this).hide();
    });
});