/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 */
var widget_tl, currentGroup;
(function($){
    $(function(){
        $("input.js-date").datepicker({
           'weekStart':1,
           'format': 'dd.mm.yyyy',
           'autoclose':true
        });
        $('.js-select-milestone').change(function(){
            var $newMilestoneFields = $('[name=milestone_name], [name=milestone_date]');
            if ($(this).val()) {
                $newMilestoneFields.hide();
            } else {
                $newMilestoneFields.show();
            }
        });
        $(document).keydown(function(e){
            var key;
            key = getKeyPressed(e);

            if (e.ctrlKey && key == 75){ //ctrl+k
                $('.task_create:first').focus();
                $('body,html').scrollTop($('.task_create:first').offset().top);
                e.stopPropagation();
                return false;
            }
        });

        var menuTaskBlock = function(name, target, onclick) {
            var $block = $('<a data-toggle="modal" data-target="'+target+'" href="#">'+name+'</a>');
            $block.click(onclick);
            return $block;
        };

        widget_tl = new widgetObject({id:'tasklist'});
        widget_tl.state = {
            taskCreate:false,
            hintOpened:{
                'Responsible':false,
                'Date':false,
                'Author':false
            }
        }
        widget_tl.container = $('.widget.tasklist');

        $.extend(widget_tl,{
            'templateUrl': "/static/item_templates/tasklist/task.html",
            'TL_create_command': '',
            'TL_User_List': {},
            'TL_Container': false,
            'TL_SearchTask': $('.search-input'),
            '$searchRulesHolder': $('.search_items_holder'),
            '$saveFilterButton': $('.js-save-search-tab'),
            '$btnSuccess': $('.btn.btn-success'),
            '$btnFilter': $('.btn.js-filter-btn'),
            '$tabContainer': $('.task-tab-filter'),
            '$taskCreateBtn': $('.btn.task-create'),
            'TL_Tasks': new window.taskList(),
            'tabsSelector': '.task-tab-filter li > a',
            'taskMoving': false,
            'taskOver': false,
            '$movedTask': false,
            'TL_TaskTemplates':{

            },
            'TL_Tags':{
                'Responsible':'для ',
                'Date':' до ',
                'Author': ' от ',
                'About':'примерно '
            },
            'TL_HintBlocks':{
                'Responsible':$('#TL_responsible_list'),
                'Date':$('#TL_date_select_list'),
                'About':$('#TL_deadline_select_list'),
                'Author':$('#TL_author_list')
            },
            'TL_HintOpened':{},
            'TL_TagLen':4,
            'TL_TaskTimers':arTimers,
            'nextPage':2,
            'init': function(){
                this.TL_Container = this.container.find('.js-tasks');
                this.TL_CreateTaskInput = this.container.find('.input-block-level');

                this.additionalTabs = (function(){
                    var cookieName = 'taskListTabs';
                    this.tabsParams = [];

                    this._save = function(){
                        var strCookie = JSON.stringify(this.tabsParams);
                        $.cookie(cookieName,strCookie);
                    }

                    this._getSavedParams = function(){
                        var strCookie = $.cookie(cookieName);
                        if (strCookie)
                            this.tabsParams = $.parseJSON(strCookie);
                        else
                            this.tabsParams = []
                    }

                    this.addCurrentState = function(name){
                        this._getSavedParams();
                        var hash = document.location.hash;
                        hash = hash.replace('#','');
                        var id = randomString(10);

                        var newTab = {
                            'id':id,
                            'name':name,
                            'location':encodeURIComponent(hash)
                        }
                        if (!this.tabsParams.push) this.tabsParams = [];
                        this.tabsParams.push(newTab);
                        this._save();
                        return newTab;
                    }

                    this.getUserTabs = function(){
                        this._getSavedParams();

                        if (this.tabsParams){
                            for (var k in this.tabsParams){
                                if (this.tabsParams[k] && this.tabsParams[k]['location'])
                                    this.tabsParams[k]['params'] = $.parseJSON(decodeURIComponent(this.tabsParams[k]['location']));
                            }
                            return this.tabsParams;
                        }
                        return [];
                    }

                    this.clearTabs = function(){
                        this.tabsParams = [];
                        this._save();
                    }
                    this.renameTab = function(id,name){
                        for (var k in this.tabsParams){
                            if (this.tabsParams[k] && this.tabsParams[k]['id'] == id)
                                this.tabsParams[k].name=name;
                        }
                        this._save();
                    }
                    this.deleteTab = function(id){
                        for (var k in this.tabsParams){
                            if (this.tabsParams[k] && this.tabsParams[k]['id'] == id)
                                delete this.tabsParams[k];
                        }
                        this._save();
                    }

                    return this;
                })();

                var oTask;
                for (var i in aTaskList){
                    oTask =  new window.taskClass(aTaskList[i]);
                    widget_tl.TL_Tasks.add(oTask);
                }

                this.TL_Tasks.on('add',function(task){
                    if ($('.js-new-first-task').get(0)){ 
                        $('.js-new-first-task').remove();
                        showTutorial();
                    }
                });

                var obj = this;
                baseConnector.addListener('fs.task.update',function(data){
                    if (data && data.id){
                        if (obj.TL_TaskTemplates[data.id]){
                            var view = obj.TL_TaskTemplates[data.id];
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

                baseConnector.addListener('fs.comment.add', function(data){
                    if (data && data.task){
                        var view = obj.TL_TaskTemplates[data.task.id];
                        if (view) {
                            view.checkModel(function(){
                                if (data.author.id != document.mainController.userId && view.model.get('viewed')){
                                    view.model.set('viewed', false);
                                }
                                view.render();
                            });
                        }
                    }
                });

                historyManager.addCallback('taskListSearch',function(data){
                    widget_tl.applyWorkFlowState(data);
                });

                widget_tl.ready(function(){
                    widget_tl.TL_Tasks.each(function(task){
                        widget_tl.TL_CreateTaskRow(task.toJSON());
                    });

                    historyManager.trigger('taskListSearch');
                    setTaskCellsHeight();
                });

                widget_tl.ready();

                this.createUserAdditionalTabs();
                var t = this;
                this.$saveFilterButton.click(function(){
                    var newTab = widget_tl.additionalTabs.addCurrentState('Мой фильтр');

                    if (newTab){
                        var $tabElem = widget_tl.addNewTabToPanel(newTab);
                        $tabElem.singleActivate();
                        $tabElem.find('a.userTab').setEditable(function(){
                            t.additionalTabs.renameTab(newTab.id, this.text());
                        });
                    }

                    return false;
                });

                this.$tabContainer.on('click', 'a.js-removeTab', function(){
                    var $tab = $(this).closest('li');
                    var tab_id = $tab.data('id');
                    widget_tl.additionalTabs.deleteTab(tab_id);
                    $tab.remove();
                    return false;
                });
                this.TL_Container.on('mousedown.taskdnd','.task .js-drag-task',function(e){
                    widget_tl.$movedTask = $(this).closest('.task').parent('.task-wrapper');
                    if (!widget_tl.$movedTask.get(0)) { //is subtask
                        widget_tl.$movedTask = $(this).closest('.task');
                    }

                    widget_tl.taskMoving = $(this).closest('.task').data('taskid');

                    widget_tl.$movedTask.css('width', widget_tl.$movedTask.width());
                    var offset = widget_tl.$movedTask.closest('.widget').offset();
                    if (offset){
                        widget_tl.offsetTaskX = -20 - offset.left;
                        widget_tl.offsetTaskY = -20 - offset.top;
                    }

                    widget_tl.$movedTask.css('position', 'absolute');
                    widget_tl.$movedTask.css('z-index', '9999');
                    widget_tl.$movedTask.css('top', e.clientY + widget_tl.offsetTaskY + $(window).scrollTop());
                    widget_tl.$movedTask.css('left', e.clientX + widget_tl.offsetTaskX);
                    $('<div></div>')
                        .addClass('temp_task')
                        .insertBefore(widget_tl.$movedTask);
//                    widget_tl.TL_Container.trigger('ousemove.taskdnd');

                    $(document.body).css('cursor','move');
                    e.preventDefault();
                });
                widget_tl.cursorOnTask = false;

                $(document).bind('mouseup.taskdnd',function(){
                    var $temTask = $('.temp_task');
                    $(document.body).css('cursor','default');

                    if (widget_tl.taskMoving){
                        if($temTask.get(0)){
                            $temTask.replaceWith(widget_tl.$movedTask);
                        }
                        widget_tl.$movedTask.css('width','100%');
                        widget_tl.$movedTask.css('position','relative');
                        widget_tl.$movedTask.css('top', '0');
                        widget_tl.$movedTask.css('left', '0');

                        if (widget_tl.taskOver) {
                            widget_tl.taskMove(widget_tl.taskMoving, widget_tl.taskOver);
                        } else {
                            widget_tl.taskMove(widget_tl.taskMoving);
                        }

                        $('.task-wrapper').removeClass('task_over');
                        if ($temTask.get(0))
                            $temTask.remove();

                        widget_tl.taskMoving = false;
                        widget_tl.$movedTask = false;
                    }
                }).on('mousemove.taskdnd', this.TL_Container, function (e){
                    if (widget_tl.$movedTask){
                        widget_tl.$movedTask.css('top', e.clientY + widget_tl.offsetTaskY + $(window).scrollTop());
                        widget_tl.$movedTask.css('left', e.clientX + widget_tl.offsetTaskX);
                        widget_tl.taskOver = false;
                        $('.task-wrapper > .task').each(function(){
                            if ($(this).data('taskid') != widget_tl.taskMoving) {
                                var pos = getObjectCenterPos(this);

                                var top = e.clientY + $(window).scrollTop();
                                var left = e.clientX + $(window).scrollLeft();
                                $(this).parent('.task-wrapper').removeClass('task_over');
                                if ((pos.top < top) && ((pos.top + pos.height) > top)) {
                                    if ((pos.left < left) && ((pos.left + pos.width) > left)) {
                                        $(this).parent('.task-wrapper').addClass('task_over');
                                        $('.temp_task').remove();
                                        widget_tl.taskOver = $(this).data('taskid');
                                    }
                                }
                            }
                        });
                        if (!widget_tl.taskOver) {
                            $('.task-wrapper').each(function(){
                                var pos = getObjectCenterPos(this);
                                var top = e.clientY + $(window).scrollTop();
                                var left = e.clientX + $(window).scrollLeft();
                                if (pos.top > top && pos.left < left) {
                                    $('.temp_task').remove();
                                    $('<div></div>')
                                        .addClass('temp_task')
                                        .insertBefore(this);
                                    return false;
                                }
                            });
                        }
                    }
                });

                $(document).on('click', '.js-task-checkbox', function(){
                    var $chTasks = $('.js-task-checkbox:checked');
                    if ($chTasks.get(0)){
                        $block = menuTaskBlock('Добавить цель', '#add-to-milestone', function(){
                            var $taskInputContainer = $('.js-tasks-for-milestone').empty();
                            $('.js-task-checkbox:checked').each(function(){
                                $taskInputContainer.append('<input type="hidden" name="task" value="' + $(this).attr('name') + '" />');
                            });
                        });
                        bottomPanel.addBlock('addToMilestone', $block);
                        //TODO: вынести в отдельный класс
                        $block = menuTaskBlock('Назначить наблюдателей', '#add-observers', function(){
                            var $taskInputContainer = $('.js-tasks-for-observers').empty();
                            $('.js-task-checkbox:checked').each(function(){
                                $taskInputContainer.append('<input type="hidden" name="task" value="' + $(this).attr('name') + '" />');
                            });
                        });
                        bottomPanel.addBlock('addObservers', $block);
                        $block = menuTaskBlock('Пригласить разработчиков HELIARD', '#invite-developers', function(){
                            var tasks = [];
//                            if (ACCOUNT_TOTAL <= 0) {
//                                alert('Данная услуга доступна только при положительном балансе. Пожалуйста, пополните ваш счет.');
//                                return false;
//                            }else{
                                $('.js-task-checkbox:checked').each(function(){
                                    tasks.push($(this).attr('name'));
                                    $(this).attr('checked', false);

    //                                $taskInputContainer.append('<input type="hidden" name="task" value="' + $(this).attr('name') + '" />');
                                });
                                PM_AjaxPost("/task_handler",
                                    {
                                        'action': 'inviteUsers',
                                        'tasks': tasks
                                    },
                                    function(data){
                                        bottomPanel.hide();
                                    }
                                );
//                            }
                        });
                         bottomPanel.addBlock('inviteDevelopers', $block);
                    }else{
                        bottomPanel.removeBlock('addToMilestone');
                        bottomPanel.removeBlock('addObservers');
                        bottomPanel.removeBlock('inviteDevelopers');
                    }
                });
//                    .on('.iCheck-helper','click',function(){
//                        $(this).sibling(':checkbox').eq(0).trigger('click');
//                    });
            },
            'taskMove':function(id, parentId){
                var parentTask = this.TL_Tasks.get(parentId);
                var task = this.TL_Tasks.get(id);
                if(parentId && !parentTask){ //drop task to subtask
                    alert('Вы не можете перенести в эту задачу.');
                    return false;
                }else if(task && !task.get('parent') && !parentTask){ //drop parent task to free space
                    widget_tl.taskInsertBefore(id, $('[data-taskid='+id+']').parent().next().find('.task:first').data('taskid'));
                    return true;
                }else if (id){
                    if (confirm('Вы действительно хотите перенести эту задачу в ' + (parentTask?'задачу #"' + parentTask.id + '"':'общий список') + '?')) {
                        taskManager.taskAjaxRequest({
                            'action':'appendTask',
                            'id':id,
                            'parent_id':parentTask?parentTask.id:0
                        },function(){
                            if (parentTask) {
                                widget_tl.TL_TaskTemplates[id].$el.parent('.task-wrapper').remove();
                                widget_tl.TL_TaskTemplates[id].remove();
                                widget_tl.TL_Tasks.remove(id);
                            }
                        },'json');
                        if (!parentTask){
                            var $tsk = $('[data-taskid='+id+']');
                            $('<div></div>').addClass('task-wrapper').insertAfter($tsk).append($tsk);
                            widget_tl.taskInsertBefore(id, $tsk.parent().next().find('.task:first').data('taskid'));
                        }
                        return true;
                    } else {
                        return false;
                    }
                }
            },
            'taskInsertBefore': function(id, before_id) {
                taskManager.taskAjaxRequest({
                        'action':'insertBefore',
                        'id':id,
                        'before_id':before_id
                    },function(){

                    },'json');
            },
            'createUserAdditionalTabs': function(){
                var aUserTabs = this.additionalTabs.getUserTabs();
                for (var k in aUserTabs){
                    if (aUserTabs[k])
                        this.addNewTabToPanel(aUserTabs[k]);
                }
            },
            'addNewTabToPanel': function(oTab){
                var t = this;
                var $newTab = $('<li style="position:relative;"></li>').attr('data-id',oTab.id),
                    $tabLink = $('<a></a>').attr({
                        'href':'#'+oTab.location
                    })
                        .text(oTab.name)
                        .addClass('userTab'),
                    $removeLink = $('<div class="widget-control" style="right:-5px;top:-5px;"><a class="w-close js-removeTab">Закрыть</a></div>');

                this.$tabContainer.prepend($newTab.append($tabLink).append($removeLink));
                return $newTab;
            },
            'applyWorkFlowState': function(params){
                if (params.taskListFilter){
                    this.$searchRulesHolder.empty();
                    this.TL_SearchTask.val('');
                    var filter = params.taskListFilter;
                    if (filter.task_search){
                        this.TL_SearchTask.val(filter.task_search);
                    }
                    var aFilterFields  = [
                        'responsible',
                        'author',
                        'closed',
                        'viewed',
                        'date_modify',
                        'date_create'
                    ];
                    var field;
                    for (var i in aFilterFields){
                        field = aFilterFields[i];
                        if (field.indexOf('date_') === 0 && filter[field]){
                            this.addVisualSearchElement(field,filter[field].join(','));
                        }else
                            for (var k in filter[field])
                                this.addVisualSearchElement(field,filter[field][k]);
                    }

                    if (filter.action){
                        var $userTabEqualsQuery = $(this.tabsSelector).filter('[href="#'+encodeURIComponent(JSON.stringify(params))+'"]');
                        if ($userTabEqualsQuery.get(0)){
                            $userTabEqualsQuery.closest('li').singleActivate();
                        }else{
                            $(this.tabsSelector).filter('[rel='+filter.action+']').closest('li').singleActivate();
                        }
                    }

                    if (filter.page){
                        filter.startPage = filter.page;
                        delete filter.page;
                    }

                    this.TL_SilentSearch(filter);
                }
            },
            'checkSearchInput': function(){
                var h = 'hidden';
                var br = 'border-r4';
                var $userTabEqualsQuery = $(this.tabsSelector).filter('[href="#'+encodeURIComponent(document.location.hash.replace('#',''))+'"]');
                with (this.TL_SearchTask){
                    if (val() || this.$searchRulesHolder.children().size()){
                        if (val()){
                            siblings('.icon-remove').show();
                        }
                        //try to find existing user tabs
                        if (!$userTabEqualsQuery.get(0))
                            this.$saveFilterButton.removeClass(h);
                            this.$btnFilter.removeClass(br);
                    }else{
                        this.$btnFilter.addClass(br);
                        this.$saveFilterButton.addClass(h);
                        siblings('.icon-remove').hide();
                    }
                }
            },
            'TL_ShowHint': function(hintName,field){
                if (!hintName) return false;
                var hint_block = this.TL_HintBlocks[hintName];

                this.TL_PosDivToField(hint_block,field);

                this.inputedText='';

                $(field).unbind('keyup.'+hintName).bind('keyup.'+hintName,function(e){
                    var key = getKeyPressed(e);
                    var lastFor = 0;
                    if (lastFor = $(this).val().lastIndexOf(widget_tl.TL_Tags[hintName])){
                        widget_tl.inputedText = $(this).val().substring((lastFor + widget_tl.TL_Tags[hintName].length),$(this).val().length);

                        var userLinks = widget_tl.TL_HintBlocks[hintName].find('li').show();

                        if (widget_tl.inputedText)
                            userLinks.not(":Contains('"+widget_tl.inputedText+"')").hide();

                        if (!userLinks.filter(":visible").get(0)){
                            widget_tl.TL_HideHint()
                        }
                    }
                });

                this.TL_HintOpened = {
                    'name':hintName,
                    'container':hint_block
                }
                return hint_block;
            },
            'TL_HideHint': function(){
                if (this.TL_HintOpened.name) {
                    this.TL_HintOpened.container.find('*').show().end().hide();
                    this.TL_CreateTaskInput.unbind('keyup.'+this.TL_HintOpened.name);
                    this.TL_HintOpened = {}
                }
            },
            'TL_ShowTaskCreateHint': function(field) {
                if (!widget_tl.TL_create_command) return false;
                var currentTag = false;
                for (i in this.TL_Tags){
                    if (this.TL_Tags[i] == this.TL_create_command) {
                        currentTag = i;
                        break;
                    }
                }
                if (currentTag){
                    this.TL_ShowHint(currentTag,field);
                }

                return false;
            },
            'TL_PosDivToField': function (block,field_selector) {
                if (!block) return false;
                var field = $(field_selector), left = field.offset().left + (field.val().length*5);
                block.insertAfter(field_selector);
                if (typeof(block)=='object'){
                    block.show();
                }
                return false;
            },
            'TL_CreateSelectTag': function(name,tag,new_val,input){
                this.TL_HideHint();

                var inpval = input.val();
                var pos = inpval.lastIndexOf(this.TL_Tags[tag]);

                pos += this.TL_Tags[tag].length;
                inpval = inpval.substring(0,pos);

                input.val(
                    inpval + "#" + (name=='new'?'':name) + "#"
                ).focus();

                if (name == 'new') {
                    var len = input.val().length-1;
                    input.get(0).setSelectionRange(len, len);
                }

                return false;
            },
            'TL_CreateTask': function(taskParams, parentTask){
                if (!taskParams.taskname) taskParams.taskname = widget_tl.TL_CreateTaskInput.val();
                if (!taskParams.taskname) return false;

                var t = this;
                var btn = t.$taskCreateBtn;
                if (!$(btn).pushed()){
                    $(btn).pushTheButton();
                    taskManager.CreateTask(taskParams, parentTask, function(data){
                        data = $.parseJSON(data);
                        if (data.name){
                            widget_tl.TL_CreateTaskInput.filter('[value="' + taskParams.taskname + '"]').val('');
                            var taskRow = widget_tl.TL_CreateTaskRow(data, parentTask, true);
                        }

                        if (data.parent != parentTask) { //replace parent to container
                            var newParent = t.TL_Tasks.get(parentTask);
                            if (!newParent) return false;
                            newParent.id = data.parent;
                            newParent.set('id', data.parent);
                            var newParentView = new window.taskViewClass({'model': newParent});
                            newParentView.$el = t.TL_TaskTemplates[parentTask].$el;

                            newParentView.el = newParentView.$el.get(0);

                            delete t.TL_TaskTemplates[parentTask];
                            var forced = true;
                            newParentView.checkModel(function(){
                                newParent.undelegateEvents();
                                newParentView.render();
                            }, forced);
                            t.TL_TaskTemplates[data.parent] = newParentView;

                            var oldParent = new window.taskClass({id: parentTask});
                            var oldParentView = new window.taskViewClass({'model': oldParent});
                            oldParentView.createEl().checkModel(function(){
                                oldParentView.render();
                            }, forced);

                            newParentView.$el.attr({
                                'id': 'taskLine_'+data.parent,
                                'data-taskid': data.parent
                            }).find('.js-time').empty().end()
                            .closest('.task-wrapper')
                                .find('.input-block-level').data('parent', data.parent)
                                .attr('data-parent', data.parent);
                            t.SubtaskBlock(newParent.id).append(oldParentView.$el);
                        }
                        $(btn).pullTheButton();
                    });
                }
                
                $('.task-file-upload input[type=hidden]').remove();

                return this;
            },
            'TL_SilentSearch': function(params){
                return this.TL_Search(params, true);
            },
            'TL_Search': function(params, silent) {
//                var loader = startLoader(
//                    'medium',
//                    this.TL_SearchTask.closest('.js-searchFilterBlock').find('.input-group-btn'),
//                    {'left':120,'top':-20}
//                );
                if (!$('.show-more').pushed()) //if not show more btn clicked
                    $('.js-search-btn').pushTheButton();

                if (!params) params = {};
                if (!params.parent){
                    if (!params.task_search && this.TL_GetSearchText()){
                        params.task_search = this.TL_GetSearchText();
                    }
                    if (!params.action){
                        var $activeTab = this.$tabContainer.find('li.active > a');
                        if ($activeTab.attr('rel'))
                            params.action = $activeTab.attr('rel');
                        else params.action = 'all';
                    }
                    if (!params.group){
                        var $group = this.container.find('input[name=group]:checked');
                        params.group = $group.val();
                    }

                    //собираем все элементы формы поиска (созданные через поисковое меню)
                    this.$searchRulesHolder.find('input[type=hidden]').each(function(){
                        if (!params[$(this).attr('name')])
                            params[$(this).attr('name')] = [];

                        params[$(this).attr('name')].push($(this).val());
                    });

                    if (!silent){
                        var paramsForHistory = params;
                        if (paramsForHistory.startPage){
                            widget_tl.nextPage = paramsForHistory.startPage + 1;
                            paramsForHistory.page = paramsForHistory.startPage;
                            delete paramsForHistory.startPage;
                            //startPage генерируется при первом вызове фильтра по хэшу и не должна в нем сохраняться
                            //так как она нужна только для инициации стартового кол-ва задач при загрузке страницы
                        }

                        historyManager.addParams({'taskListFilter':paramsForHistory});
                    }
                }


                window.backurl = document.location.href;
                this.checkSearchInput();
                var obj = this;
                PM_AjaxPost("/task_handler",
                    params,
                    function(data){
                        var data = $.parseJSON(data),
                            paginator = data.paginator,
                            tasks = data.tasks;
//                        stopLoader(loader);
                        $('.js-search-btn').pullTheButton();

                        if (!params.parent && !params.page){
                            arTimers = {};
                            obj.TL_Container.empty();
                        }

                        for (i in tasks){
                            var taskInfo = tasks[i];
                            if (obj.TL_SearchTask.val()){
                                var val = taskInfo.name;
                                    val = val.replace(new RegExp(obj.TL_SearchTask.val(),'mig'),"<mark>"+obj.TL_SearchTask.val()+"</mark>");
                                    taskInfo.name = val;
                            }

                            obj.TL_CreateTaskRow(taskInfo, params.parent);
                        }
                        if ((!tasks || tasks.length <= 0) && !params.parent && !params.page){
                            obj.TL_Container.html("<div><span class='empty_result'>Ничего не найдено</span></div>");
                        }
                        if (!params.parent){
                            if (paginator.lastPage) {
                                obj.container.find('.show-more').hide().pullTheButton();
                            } else {
                                obj.container.find('.show-more').show().pullTheButton();
                            }
                        }
                });
                return this;
            },
            'addGroupRow': function(group){
                if (!group.name) {
                    group = {
                        'name': 'Свободные задачи'
                    }
                }
                var row = '<div class="task-wrapper milestone task-group-' + group.code + '">' +
                                '<div class="task clearfix" ' + (group.closed ? 'style="color: green;" ' : '') +
                    'data-milestoneId="' + group.id + '">' +
                                        '' + group.name + (group.date ? ' до ' + group.date : '') + '' +
                    (group.date ? '<div class="pull-right milestone-icons">' +
                							'<a href="#" class="fa fa-edit"></a>' +
											'<a href="#" class="fa fa-check-square-o"></a>' +
										'</div>' : '') +
                
                                '</div>' +
                            '</div>';
                var $row = $(row);

                $row.appendTo(this.TL_Container);
            },
            'TL_GetSearchText':function(){
                var text = this.TL_SearchTask.val();
                if (text == this.TL_SearchTask.attr('data-blur')) text = '';
                return text;
            },
            'SubtaskBlock':function(taskId){
                return $('#taskLine_'+taskId).parent().find('.subtask');
            },
            'TL_CreateTaskRow':function(taskInfo, parent, is_new){
                if (!taskInfo || !taskInfo.name) return false;
                if (!taskInfo.id) return false;

                var task = widget_tl.TL_Tasks.get(taskInfo.id);
                if (task) {
                    for (var i in taskInfo){
                        task.set(i, taskInfo[i]);
                    }
                } else {
                    task = new window.taskClass(taskInfo);
                    widget_tl.TL_Tasks.add(task);
                }

                if (!currentGroup && task.get('group').id
                    || currentGroup && currentGroup.id != task.get('group').id) {
                    currentGroup = task.get('group');

                    this.addGroupRow(task.get('group'));
                }
                var view = new window.taskViewClass({'model': task});
                widget_tl.TL_TaskTemplates[task.id] = view;

                view.createEl().render();
                if (!parent) {
                    var $task_el = $('<div></div>').addClass('task-wrapper')
                                    .append(view.$el)
                                    .append('<div class="add-task-input" style="display: none;"><input maxlength="1000" class="input-block-level form-control" data-parent="' + view.model.id + '" type="text" placeholder="Добавить подзадачу..."></div>')
                                    .append('<div class="subtask" style="display: none;"></div>');

                    if (is_new) {
                        var taskExist = this.TL_Container.find('.task-wrapper:first').get(0);
                        if (taskExist)
                            $task_el.insertBefore(taskExist);
                        else
                            $task_el.appendTo(this.TL_Container);
                    } else {
                        $task_el.appendTo(this.TL_Container);
                    }

                    if (view.model.get('critically') > CRITICALLY_THRESHOLD){
                        $task_el.addClass('critically')
                    }
                } else {
                    if (is_new){
                        this.SubtaskBlock(parent).prepend(view.$el);
                    } else {
                        this.SubtaskBlock(parent).append(view.$el);
                    }
                }

                taskRespSummary[task.id] = taskInfo.responsibleList;

                arTimers[task.id] = new PM_Timer(taskInfo.time);
                arTimers[task.id].container = view.$el.find('.js-time').eq(0);
                $(arTimers[task.id].container).html(arTimers[task.id].toString());
                setTaskCellsHeight(view.$el);
                return view.$el;
            },
            'TL_GetTaskUrl':function(id){
                return "task_edit/?id="+id+"";
            },
            'addEventsToSubtaskInput':function(input){

            },
            'addVisualSearchElement': function(field_name, value){
                value = value.split(',');
                var $category = $('.js-search-menu > li[data-code='+field_name+']'),
                    $rulesContainer = this.$searchRulesHolder,
                    $categoryBlock = $rulesContainer.find('span[data-code='+field_name+']'),
                    field_title = $category.children('a').text(),
                    sValueHtml = '',
                    bIsDate = field_name.indexOf('date_') === 0,
                    bIsRange = value == 'range',
                    sAddDatePickerClass = bIsDate?'datepick':'',
                    val,
                    aDatesPrefixes = ['c&nbsp;','по&nbsp;'];
                if (bIsRange && bIsDate) {
                    value = ['01.08.2014', '10.09.2014']
                }
                for (var i in value){
                    val = value[i];
                    var $valueItem = $category.find('a[rel="'+val+'"]').eq(0),
                        value_title = $valueItem.text(),
                        $newInputHidden = function(name, value){
                            return $('<input type="hidden" />').attr({'name':name,'value':value});
                        };

                    if (bIsDate){
                        value_title = val;
                        if (bIsRange){
                            var sPrefix = aDatesPrefixes[i];
                            sValueHtml = sPrefix+'<a data-field="'+field_name+'" class="'+sAddDatePickerClass+' added-user">'+val+'</a>';
                        }
                    }
                    if (!sValueHtml){
                        sValueHtml = '<a data-field="' + field_name + '" class="' + sAddDatePickerClass + ' added-user">' + value_title + '</a>';
                    }

                    var $input;

                    if (!($input = $rulesContainer.find('input[name='+field_name+'][value="'+val+'"]').get(0))){
                        $input = $newInputHidden(field_name,val);
                        $rulesContainer.append($input);
                    }
                    if (!$categoryBlock.get(0)){
                        $rulesContainer.append($categoryBlock = $('<span></span>').addClass('search-group')
                            .attr('data-code',field_name)
                            .append('<h6 data-code="responsible" class="clearfix">' + field_title + ':</h6>'));
                    }

                    var $tmpContainer = $categoryBlock.find('span[data-code="'+val+'"]').remove()
                        .end().append('<span data-code="'+val+'">'+sValueHtml+' <a class="close">&times;</a></span>');

                    if (sAddDatePickerClass)
                        $tmpContainer.find('.'+sAddDatePickerClass).each(function(){
                            $(this).datepicker({
                                'weekStart':1,
                                'format': 'dd.mm.yyyy',
                                'autoclose':true,
                                'callback': function($elem){
                                    var d = $elem.data('date');
                                    $elem.text(d);
                                    $input.val(d);
                                    widget_tl.TL_Search();
                                }
                            });
                        });
                }
            },

            'getSimilar':function(text,callback){
                if (this.ajaxSimilarHandler) this.ajaxSimilarHandler.abort();
                this.ajaxSimilarHandler = PM_AjaxPost("/task_handler",{
                    'text':text,
                    'action':'getSimilar'
                },callback,'json')
            }
        });

        widget_tl.init();
        widget_tl.similarSearchTimeout = false;
        widget_tl.TL_CreateTaskInput.keyup(function(e){
            var key = getKeyPressed(e),t=this;
            widget_tl.TL_create_command = '';
            for (var keytag in widget_tl.TL_Tags){
                tag = widget_tl.TL_Tags[keytag];

                if ($(this).val().lastIndexOf(tag)!=-1 && $(this).val().lastIndexOf(tag) == ($(this).val().length-tag.length)){
                    widget_tl.TL_create_command = tag;
                }
            }

            if (e.ctrlKey && key == 32){ //ctrl+space
                if (widget_tl.TL_create_command)
                    widget_tl.TL_ShowTaskCreateHint(this);
            }else if (e.ctrlKey && key == 78){ //ctrl+N
                $('body,html').scrollTop(t.focus().offset().top);
                return false;
            }else if(key == 40 && widget_tl.TL_HintOpened.name){ //arrow down
                widget_tl.TL_HintOpened.container.find('li:visible').removeClass('active').eq(0).addClass('active').find('a').focus();
            }else if(!e.ctrlKey && key!=13){
                widget_tl.TL_ShowTaskCreateHint(this);
            }

            if (widget_tl.similarSearchTimeout) clearTimeout(widget_tl.similarSearchTimeout);
            widget_tl.similarSearchTimeout = setTimeout(function(){
                widget_tl.getSimilar(widget_tl.TL_CreateTaskInput.val(), function(data){
                    var cl = 'js-similar_result';
                    var $similarResult = widget_tl.TL_CreateTaskInput.parent().find('.'+cl);
                    if (!$similarResult.get(0)){
                        $similarResult = $('<div></div>').addClass(cl).insertAfter(widget_tl.TL_CreateTaskInput);
                    }
                    if (data.length){
                        var $link = $('<a></a>').addClass('dropdown').attr('data-toggle','dropdown').text(data.length + ' похожих');
                        var sAddMessage = '';
                        if (data.length > 20){
                            sAddMessage = '<span style="color:red">&nbsp;Постарайтесь конкретизировать задачу.</span>'
                        }

                        var $menu = $('<ul></ul>').addClass('dropdown-menu').attr('role','dropdown');
                        for (var i in data){
                            var task = data[i];
                            $menu.append(
                                $('<li></li>').append(
                                    $('<a></a>').attr('href',task.url).text(task.name)
                                )
                            )
                        }
                        $similarResult.empty().append($link).append(sAddMessage).append($menu);
                    }else{
                        $similarResult.remove();
                    }
                });
            },400);
        });

        widget_tl.TL_CreateTaskInput.keydown(function(e){
            var key = getKeyPressed(e);
            if (e.ctrlKey && key == 32) return false; //ctrl+space
            else if (key==13 && !widget_tl.TL_HintOpened.name){
                var parent = $(this).data('parent'),
                    taskParams = {'taskname':$(this).val()};
                $('.task-file-upload input[type=hidden]').each(function(){
                    if (!taskParams[this.name]) taskParams[this.name] = [];
                    taskParams[this.name].push($(this).val());
                });
                widget_tl.TL_CreateTask(taskParams, parent);
                $(this).val('');
                $('.qq-upload-list').empty();
                return false;
            }
        });

        widget_tl.$taskCreateBtn.click(function(){
            var input = $('input.task-create'),
                taskParams = {'taskname':input.val()};
            $('.task-file-upload input[type=hidden]').each(function(){
                if (!taskParams[this.name]) taskParams[this.name] = [];
                taskParams[this.name].push($(this).val());
            });
            input.val('');
            widget_tl.TL_CreateTask(taskParams);

            $('.qq-upload-list').empty();//TODO:устранить дублирование кода
            return false;
        });

        for (var i in widget_tl.TL_HintBlocks){
            widget_tl.TL_HintBlocks[i].keydown(function(e){
                var key = getKeyPressed(e);
                if (widget_tl.TL_HintOpened){
                    if(key == 40){ //down
                        $(this).find('li.active').removeClass('active').next(':visible').addClass('active').find('a').focus();
                        return false;
                    }else if(key == 38){ //up
                        $(this).find('li.active').removeClass('active').prev(':visible').addClass('active').find('a').focus();
                        return false;
                    }
                }
            });
        }

        $('.widget.tasklist')
        .on('click','a.add-subtask',function(){
            //show subtasks
            var $task = $(this).closest('.task');
            var $taskWrapper = $task.closest('.task-wrapper');
            var taskId = $task.attr('data-taskid');

            var $subtaskContainer = $task.parent().find('.subtask');
            var is_open = $subtaskContainer.is(':visible');

            if (!is_open){
                $taskWrapper.addClass('active');
                $task.parent().find('.add-task-input').show();
                if (!$subtaskContainer.html()){
                    widget_tl.TL_SilentSearch({'parent':taskId});
                }

                $subtaskContainer.show().prev().find('input').focus().enterPressed(function(obj){
                    if ($(obj).val())
                        widget_tl.TL_CreateTask({
                            'taskname':$(obj).val()
                        },$(obj).data('parent'));

                    $(obj).val('');
                });//.addTaskFilePasteSimple();
            }else{
                $taskWrapper.removeClass('active');
                $task.parent().find('.add-task-input').hide();
                $subtaskContainer.hide();
            }

            return false;
        });

        var search_timeout = false;

        $('.search-input').keyup(function(){
            if (search_timeout) clearTimeout(search_timeout);
            search_timeout = setTimeout(function(){
                widget_tl.TL_Search();
            },500);
        });

        $('.show-more').click(function(){
            $(this).pushTheButton();
            widget_tl.TL_Search({'page':widget_tl.nextPage});
            widget_tl.nextPage++;
            return false;
        });
        $('input[name=group]').click(function(){
            widget_tl.TL_Search();
        });
        $(widget_tl.tabsSelector).click(function(){
            $(this).parent().singleActivate();
            if ($(this).hasClass('userTab')){
                return true; //search will be executed by hash
            }else{
                widget_tl.TL_Search();
            }

            return false;
        });

        document.mainController.widgetsData["taskList"] = widget_tl;

        if (arTimers)
            for (var i in arTimers){
                arTimers[i].container = $('#taskLine_'+i+' .js-time').get(0);
                $(arTimers[i].container).html(arTimers[i].toString());
            }

        $('.input-block-level').addTaskFilePasteSimple();

        $('.js-search-menu > li > ul > li > a').click(function(){
            var category = $(this).closest('.js-search-menu > li'),
                field_name = category.attr('data-code'),
                value = $(this).attr('rel');

            widget_tl.addVisualSearchElement(field_name,value);

            widget_tl.TL_Search();
            return false;
        });

        widget_tl.$searchRulesHolder.on('click','.close',function(){
            var sFieldName = $(this).closest('span.search-group').attr('data-code'),
                value = $(this).parent().attr('data-code'),
                bLeastBlock = $(this).closest('span.search-group').children('span').length == 1,
                $search_form = widget_tl.$searchRulesHolder;

            $search_form.find('input[name='+sFieldName+'][value="'+value+'"]').remove();

            if (bLeastBlock){
                $(this).closest('span.search-group').remove();
            }else{
                $(this).closest('span').remove();
            }

            widget_tl.TL_Search();
            return false;
        });

        $('.AddTaskBlock > div').bind('clickoutside', function(){
            $(this).hide();
        });

        $('.js-searchFilterBlock .icon-remove').click(function(){
            $(".search-input").val('');
            $(this).hide();
            widget_tl.TL_Search();
        });
        ///FINE UPLOADER
        var errorHandler = function(event, id, fileName, reason, xhr) {
            qq.log("id: " + id + ", fileName: " + fileName + ", reason: " + reason);
        };

        var fileNum = 0;
        $('.task-file-upload').fineUploader({
            debug: false,
            request: {
                endpoint: "/upload/receiver",
                paramsInBody: true
            },
            text: {
                cancelButton:'Отмена',
                retryButton:'Повторить',
                deleteButton:'Удалить'
            },
            chunking: {
                enabled: true
            },
            resume: {
                enabled: true
            },
            retry: {
                enableAuto: true,
                showButton: true
            },
            deleteFile: {
                enabled: true,
                endpoint: '/upload/receiver',
                forceConfirm: false
                //params: {foo: "bar"}
            },
            display: {
                fileSizeOnSubmit: true
            }
    //        ,
    //        paste: {
    //            targetElement: $(document)
    //        }
        })
        .on('error', errorHandler)
        .on('uploadChunk resume', function(event, id, fileName, chunkData) {
            qq.log('on' + event.type + ' -  ID: ' + id + ", FILENAME: " + fileName + ", PARTINDEX: " + chunkData.partIndex + ", STARTBYTE: " + chunkData.startByte + ", ENDBYTE: " + chunkData.endByte + ", PARTCOUNT: " + chunkData.totalParts);
        })
        .on("upload", function(event, id, filename) {
            $(this).fineUploader('setParams', {"hey": "ho"}, id);
        })
        .on("complete",function(event,id,filename,data){
            if (data.id){
                $('<input type="hidden" name="files" />').val(data.id).appendTo($('.task-file-upload'));
                $(this).fineUploader('setDeleteFileParams', {"file_id": data.id}, id);
            }
        });
    });
})(jQuery);

$.fn.singleActivate = function(){
    return this.addClass('active').siblings().removeClass('active').end();
};

var isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i);
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i);
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
    }
};

(function($){
    $(document).ready(function(){
        if(isMobile.any()){
            $('.input-group-btn').addClass('mobile-menu');
            $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
                event.preventDefault(); 
                event.stopPropagation(); 
                $(this).parent().siblings().removeClass('open');
                $(this).parent().toggleClass('open');
            });
        }
        $('ul.dropdown-menu [data-toggle=dropdown-item]').on('click', function(event) {
            $(this).parents('.input-group-btn').removeClass('open');
        });
    });
})(jQuery);
