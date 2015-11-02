(function($){
    console.log('help me!');
    var data = window.heliardData,
        aTaskList = window.heliardData.aTaskList,
        taskRespSummary = window.heliardData.taskRespSummary,
        events = {
            "click .js-task-draft_envelopes-expand": "openDiscussion",
            "click a.js-task_menu": "showMenu",
            "click a.js-select_resp": "showResponsibleMenu",
            "click a.js-resp-approve": "responsibleApprove",
            "click .jsPlanTimeList a": "changePlanTime",
            "click a.js-task_approve": "approveTask"
        };
    var draftViewClass = window.taskViewClass.extend({
        events: events,
        'openDiscussion': function(ev){
            ev.preventDefault();
            ev.stopPropagation();
            var collapsed = true;

            if(!collapsed) {
                collapsed = true;
                return false;
            }
            if (typeof this.discussion == "undefined"){
                this.discussion = "";
            }else{
                collapsed = false;
            }
            return false;
        },
        'render': function(){
            var templateParams = {
                responsibleTag: data.responsibleTag
            }

            var playBtnStatus = 'disabled';
            if (this.model.get('subtasksQty') > 0) {
                templateParams.responsibleTag = 'span';
                templateParams.timerTag = 'span';
                playBtnStatus = 'transparent';
            }
            this.$el.html(this.template(this.model.toJSON(), templateParams));

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

            this.disableTimerButton();
            this.hideTimerButton();
            this.delegateEvents();
            if (this.$el.parent().get(0)) {
                setTaskCellsHeight(this.$el);
            }
            return this;
        }
    });
    $('document').ready(function(){
        var views = [];
        var $task_container = $('.js-tasks')
        $.extend($task_container, {
            'TL_Tasks': new window.taskList()
        });
        $('.js-invite-developers').click(function(ev){
            ev.preventDefault();
            var url = $(this).attr('href');
            $.post(url, function(response){
                if(response.error) {
                    alert(response.error);
                }
                if(response.result) {
                    if (alert(response.result)){
                        window.location.reload();
                    }else{
                        window.location.reload();
                    }
                }
            });
            return false;
        });
        for(var i= 0, len= aTaskList.length; i < len; i++) {
            var view = new draftViewClass({
                model: new taskClass(aTaskList[i]),
                responsibleMenuUrl: "/ajax/responsible_menu/?draft_id=" + data.draft.id
            });
            view.model.set('draft', data.draft);
            views[aTaskList[i].id] = view;
            view.createEl();
            $task_container.append(view.$el);
            view.render();
            view.$el.wrap("<div class='task-wrapper'></div>");
            $task_container.TL_Tasks.add(view);

        }
        baseConnector.addListener('fs.task.update',function(data){
            if (data && data.id){
                if (views[data.id]){
                    var view = views[data.id];
                    view.checkModel(function(){
                        for (var i in data){
                            if (i == 'viewedOnly') {
                                if (data[i] != document.mainController.userId) {
                                    view.model.set('viewed', false);
                                }
                            }
                            if (i != 'id'){
                                view.model.set(i, data[i]);
                            }
                        }
                        view.render();
                    });
                }
            }
        });
    });
})(jQuery);
