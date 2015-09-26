/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 */

$(function () {
	$('.user-prizes-slider').bxSlider({
		slideWidth: 150,
		minSlides: 3,
		maxSlides: 3,
		controls:true,
        autoControls:false,
		pager:false,
        hideControlOnEnd:true,
        infiniteLoop:false,
		mode:'horizontal',
		auto:true,
		pause:5000,
        nextText:'<i class="fa fa-angle-right"></i>',
        prevText:'<i class="fa fa-angle-left"></i>'
	});

    var widget_ud = new widgetObject({id: 'user_detail'});
    widget_ud.state = {
        taskCreate: false,
        hintOpened: {
            'Responsible': false,
            'Date': false,
            'Author': false
        }
    };

    widget_ud.templateUrl = "/static/item_templates/tasklist/task.html";
    widget_ud.container = $('#user_detail');
    widget_ud.user_id = global_user_id;
    widget_ud.userInfoSelector = '.userInfo';
    widget_ud.taskList = new window.taskList();
    widget_ud.taskListObservers = new window.taskList();
    widget_ud.taskTemplates = {};
    widget_ud.$taskContainer = $('.js-tasks');
    widget_ud.$taskContainerObservers = $('.js-tasks-observers');

    $.extend(widget_ud, {
        'init': function () {
            this.$userInfoBlock = this.container.find(this.userInfoSelector);
            var oTask;
            for (var i in aTaskList) {
                aTaskList[i]['is_responsible_list'] = true;
                oTask = new window.taskClass(aTaskList[i]);
                widget_ud.taskList.add(oTask);
            }
//            for (var i in aTaskListObservers){
//                oTask = widget_ud.taskList.get(aTaskListObservers[i]['id']);
//                if (oTask) {
//                    oTask.set('is_observer_list', true);
//                }else{
//                    aTaskListObservers[i]['is_observer_list'] = true;
//                    oTask =  new window.taskClass(aTaskListObservers[i]);
//                    widget_ud.taskList.add(oTask);
//                }
//            }
            this.addOnlineStatusListeners();
            widget_ud.taskList.each(function (task) {
                if (task.get('is_observer_list')) {
                    widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainerObservers);
                }
                if (task.get('is_responsible_list')) {
                    widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainer);
                }
            });
            widget_ud.taskListObservers.each(function (task) {
                widget_ud.addTaskLine(task.toJSON(), widget_ud.$taskContainerObservers);
            });
            $('.js-delete-user').click(function () {
                return confirm('Вы действительно хотите удалить данного пользователя?');
            });
            $('.js-role-check').click(function () {
                PM_AjaxPost(
                    '/users_ajax/',
                    {
                        'action': 'setRole',
                        'role': $(this).attr('name'),
                        'roleProject': $(this).data('project'),
                        'user': $(this).data('user-id'),
                        'set': ($(this).is(':checked') ? 1 : 0)
                    },
                    function (data) {
//                        alert(data);
                    }
                )
            });
            dashboard('#dashboard', USER_TIME_DATA);

            var $specialtyInput = $('.js-save_specialty'),
                $searchDropdown = $('.js-search_specialties'),
                $specialties = $('.js-specialties');

            var appendSkills = function (id, name) {
                var $specialty = ('<li><span class="tag-name">' + name + '</span><span class="tag-num"><i class="fa fa-times tag-num-icon js-delete_specialty"' +
                'data-specialty="' + id + '"></i></span></span></li>');
                $specialties.append($specialty);
                if ($specialties.hasClass('hidden')) {
                    $specialties.removeClass('hidden')
                }
            };

            $specialtyInput.keypress(function(e) {
                var $t = $(this);
                var key = e.keyCode;
                if (key == 13) { // Enter key
                    PM_AjaxPost(
                        '/users_ajax/',
                        {
                            'action': 'addSpecialty',
                            'specialty': $t.val(),
                            'user': $t.data('user-id')
                        },
                        function (response) {
                            if (response == 'already has this specialty') {
                                $t.val('');
                            } else {
                                var data = $.parseJSON(response);
                                appendSkills(data['id'], data['name']);
                                $t.val('');
                            }
                            $searchDropdown.hide();
                        }
                    );
                }
                if (key == 40) { // Down key
                    $searchDropdown.find('li:visible').removeClass('active').eq(0).addClass('active').find('a').focus()
                }
            }).on('click', function(e) {e.stopPropagation();});

            $searchDropdown.keypress(function (e) {
                var key = e.keyCode;

                if (key == 40) { //down
                    if ($(this).find('li.active').is(':last-child')) {
                        return false
                    } else {
                        $(this).find('li.active').removeClass('active').next(':visible').addClass('active').find('a').focus();
                    }
                    return false;
                } else if (key == 38) { //up
                    if ($(this).find('li.active').is(':first-child')) {
                        $(this).find('li.active').removeClass('active');
                        $specialtyInput.focus()
                    } else {
                        $(this).find('li.active').removeClass('active').prev(':visible').addClass('active').find('a').focus();
                    }
                    return false;
                } else if (key == 13) {
                    $specialtyInput.val($(this).find('a').text()).focus();
                    $searchDropdown.hide();
                }
            });

            $searchDropdown.on('click', '*', function(e) {
                e.stopPropagation();
                $specialtyInput.val($(this).text()).focus();
                $searchDropdown.hide();
            });

            $searchDropdown.on('mouseover', 'li', (function() {
                $(this).activateListItem().find('a').blur()
            }));

            widget_ud.container.on('click', '.js-delete_specialty', function () {
                var $t = $(this);
                PM_AjaxPost(
                    '/users_ajax/',
                    {
                        'action': 'deleteSpecialty',
                        'specialty': $t.data('specialty'),
                        'user': $('.js-save_specialty').data('user-id')
                    },
                    function () {
                        $t.parent().parent().remove();
                    }
                )
            });

            var search_val = null;
            $specialtyInput.keyup(function() {
                var $t = $(this);
                if ($t.val() != search_val) {
                    search_val = $t.val();
                    if (search_val.length > 2) {
                        $.post(
                            '/ajax/specialty/',
                            {
                                'action': 'specialty_search',
                                'search_text': $t.val(),
                                'user': $t.data('user-id')
                            },
                            function (response) {
                                var data = $.parseJSON(response);
                                if (data.length > 0) {
                                    $searchDropdown.empty();
                                    for (var i = 0; i < data.length; i++) {
                                        var $skill = $('<li><a href=#>' + data[i] + '</a></li>');
                                        $searchDropdown.append($skill)
                                    }
                                    $searchDropdown.show()
                                }
                            }
                        )
                    }
                }
            });

            $(document).on('click', function() {
                $searchDropdown.hide()
            })
        },
        'addTaskLine': function (taskData, $container) {
            var task = widget_ud.taskList.get(taskData.id);
            var view = new window.taskViewClass({'model': task});

            widget_ud.taskTemplates[task.id] = view;
            view.createEl().render();

            var $task_el = $('<div></div>').addClass('task-wrapper')
                .append(view.$el)
                .append('<div class="subtask" style="display: none;"></div>');
            $container.append($task_el);
            view.$('.js-select_resp, .add-subtask').each(function () {
                $(this).replaceWith($('<strong></strong>').append($(this).find('.fa-plus').remove().end().html()));
            });
            view.delegateEvents();
        },
        'addOnlineStatusListeners': function () {
            baseConnector.addListener('connect', function () {
                if (widget_ud.statusInterval) clearInterval(widget_ud.statusInterval);
                widget_ud.statusInterval = setInterval(function () {
                    widget_ud.setOnlineStatusFromServer();
                }, 5000)
            });

            baseConnector.addListener('userLogin', function (userData) {
                if (userData.id == widget_ud.user_id) {
                    widget_ud.setUserStatus('online');
                }
            });
        },
        "setOnlineStatusFromServer": function () {
            baseConnector.send("users:get_user_data", {
                    'id': this.user_id
                },
                function (userData) {
                    userData = $.parseJSON(userData);
                    widget_ud.setUserStatus(userData['status']);
                }
            );
        },
        'setUserStatus': function (status) {
            if (status)
                this.$userInfoBlock.attr('data-status', status);
        }
    });

    widget_ud.init();

    document.mainController.widgetsData["user_detail"] = widget_ud;

//    $('.TabsMenu li').click(
//        function () {
//            $(this).addClass('Active').siblings().removeClass('Active');
//            $('.TabsHolder .Block').removeClass('visible').filter('.' + $(this).attr('data-block')).addClass('visible');
//            return false;
//        }
//    );
    $('#myTab a').bind(function (e) {
        e.preventDefault();
        $(this).tab('show');
        return false;
    });
    $('.js-link-tasks').click(
        function() {
            $('.js-current-tasks').trigger('click');
        }
    );
    $('.js-add-project').click(
        function() {
            $('.js-tab-menu > li').removeClass('active')
        }
    );
});

function dashboard(id, fData) {
    var randomScalingFactor = function(){ return Math.round(Math.random()*100)}, i, labels = [], datasets = [[],[],[]];
    for (i in fData) {
        labels.push(fData[i]['State']);
        datasets[0].push(fData[i]['freq']['time']);
        datasets[1].push(fData[i]['freq']['tasks']);
        datasets[2].push(fData[i]['freq']['commits']);
    }
    var barChartData = {
		labels : labels,
		datasets : [
			{
				fillColor : "rgba(220,220,220,0.5)",
				strokeColor : "rgba(220,220,220,0.8)",
				highlightFill: "rgba(220,220,220,0.75)",
				highlightStroke: "rgba(220,220,220,1)",
				data : datasets[0]
			},
			{
				fillColor : "rgba(151,205,187,0.5)",
				strokeColor : "rgba(151,205,187,0.8)",
				highlightFill : "rgba(151,205,187,0.75)",
				highlightStroke : "rgba(151,205,187,1)",
				data : datasets[1]
			},
            {
				fillColor : "rgba(205,151,187,0.5)",
				strokeColor : "rgba(205,151,187,0.8)",
				highlightFill : "rgba(205,151,187,0.75)",
				highlightStroke : "rgba(205,151,187,1)",
				data : datasets[2]
			}
		]

	};

    var ctx = $(id).get(0).getContext("2d");
    window.myBar = new Chart(ctx).Bar(barChartData, {
        responsive : true
    });

}

