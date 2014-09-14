/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 */

$(function(){
    var widget_ud = new widgetObject({id:'user_detail'});
    widget_ud.state = {
        taskCreate:false,
        hintOpened:{
            'Responsible':false,
            'Date':false,
            'Author':false
        }
    }
    widget_ud.templateUrl = "/static/item_templates/tasklist/task.html";
    widget_ud.container = $('#user_detail');
    widget_ud.user_id = global_user_id;
    widget_ud.userInfoSelector = '.userInfo';
    widget_ud.taskList = new window.taskList();
    widget_ud.taskListObservers = new window.taskList();
    widget_ud.taskTemplates = {};
    widget_ud.$taskContainer = $('.js-tasks');
    widget_ud.$taskContainerObservers = $('.js-tasks-observers');

    $.extend(widget_ud,{
        'init': function(){
            this.$userInfoBlock = this.container.find(this.userInfoSelector);
            var oTask;
            for (var i in aTaskList){
                aTaskList[i]['is_responsible_list'] = true;
                oTask =  new window.taskClass(aTaskList[i]);
                widget_ud.taskList.add(oTask);
            }
            for (var i in aTaskListObservers){
                oTask = widget_ud.taskList.get(aTaskListObservers[i]['id']);
                if (oTask) {
                    oTask.set('is_observer_list', true);
                }else{
                    aTaskListObservers[i]['is_observer_list'] = true;
                    oTask =  new window.taskClass(aTaskListObservers[i]);
                    widget_ud.taskList.add(oTask);
                }
            }
            this.addOnlineStatusListeners();
            widget_ud.taskList.each(function(task){
                if (task.get('is_observer_list')){
                    widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainerObservers);
                }
                if(task.get('is_responsible_list')){
                    widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainer);
                }
            });
            widget_ud.taskListObservers.each(function(task){
                widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainerObservers);
            });
            $('.js-delete-user').click(function(){
                return confirm('Вы действительно хотите удалить данного пользователя?');
            });
            $('.js-role-check').click(function(){
                PM_AjaxPost(
                    '/users_ajax/',
                    {
                        'action': 'setRole',
                        'role': $(this).attr('name'),
                        'project': $(this).data('project'),
                        'user': $(this).data('user-id'),
                        'set': $(this).is(':checked')
                    },
                    function(data){
                        alert(data);
                    }
                )
            });
        },
        'addTaskLine':function(taskData, $container){
            var task = widget_ud.taskList.get(taskData.id);
            var view = new window.taskViewClass({'model':task});

            widget_ud.taskTemplates[task.id] = view;
            view.createEl().render();

            var $task_el = $('<div></div>').addClass('task-wrapper')
                                .append(view.$el)
                                    .append('<div class="subtask" style="display: none;"></div>');
            $container.append($task_el);
            view.$('.js-select_resp, .add-subtask').each(function(){
                $(this).replaceWith($('<strong></strong>').append($(this).find('.fa-plus').remove().end().html()));
            });
            view.delegateEvents();
        },
        'addOnlineStatusListeners': function(){
            baseConnector.addListener('connect', function(){
                if (widget_ud.statusInterval) clearInterval(widget_ud.statusInterval);
                widget_ud.statusInterval = setInterval(function(){
                    widget_ud.setOnlineStatusFromServer();
                }, 5000)
            });

            baseConnector.addListener('userLogin', function(userData){
                if (userData.id == widget_ud.user_id){
                    widget_ud.setUserStatus('online');
                }
            });
        },
        "setOnlineStatusFromServer": function(){
            baseConnector.send("users:get_user_data", {
                    'id': this.user_id
                },
                function(userData){
                    userData = $.parseJSON(userData);
                    widget_ud.setUserStatus(userData['status']);
                }
            );
        },
        'setUserStatus': function(status){
            if (status)
                this.$userInfoBlock.attr('data-status', status);
        }
    });

    widget_ud.init();

    document.mainController.widgetsData["user_detail"] = widget_ud;

    $('.TabsMenu li').click(
        function(){
            $(this).addClass('Active').siblings().removeClass('Active');
            $('.TabsHolder .Block').removeClass('visible').filter('.'+$(this).attr('data-block')).addClass('visible');
            return false;
        }
    );
});