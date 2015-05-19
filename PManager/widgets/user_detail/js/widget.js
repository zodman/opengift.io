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
    $('#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        return false;
    });
});

function dashboard(id, fData) {
    var barColor = '#eee';

    function segColor(c) {
        return {time: "#428bca", tasks: "#4cae4c"}[c];
    }

    // compute total for each state.
    fData.forEach(function (d) {
        var time = d.freq.time || 1;
        d.total = (d.freq.tasks/time).toFixed(2);
    });

    // function to handle histogram.
    function histoGram(fD) {
        var hG = {}, hGDim = {t: 60, r: 0, b: 30, l: 0};
        hGDim.w = 400 - hGDim.l - hGDim.r,
            hGDim.h = 300 - hGDim.t - hGDim.b;

        //create svg for histogram.
        var hGsvg = d3.select(id).append("svg")
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b).append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

        // create function for x-axis mapping.
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
            .domain(fD.map(function (d) {
                return d[0];
            }));

        // Add x-axis to the histogram svg.
        hGsvg.append("g").attr("class", "x axis")
            .attr("transform", "translate(0," + hGDim.h + ")")
            .call(d3.svg.axis().scale(x).orient("bottom"));

        // Create function for y-axis map.
        var y = d3.scale.linear().range([hGDim.h, 0])
            .domain([0, d3.max(fD, function (d) {
                return d[1];
            })]);

        // Create bars for histogram to contain rectangles and freq labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
            .append("g").attr("class", "bar");

        //create the rectangles.
        bars.append("rect")
            .attr("x", function (d) {
                return x(d[0]);
            })
            .attr("y", function (d) {
                return y(d[1]);
            })
            .attr("width", x.rangeBand())
            .attr("height", function (d) {
                return hGDim.h - y(d[1]);
            })
            .attr('fill', barColor)
            .on("mouseover", mouseover)// mouseover is defined below.
            .on("mouseout", mouseout);// mouseout is defined below.

        //Create the frequency labels above the rectangles.
        bars.append("text").text(function (d) {
            return d3.format(",")(d[1])
        })
            .attr("x", function (d) {
                return x(d[0]) + x.rangeBand() / 2;
            })
            .attr("y", function (d) {
                return y(d[1]) - 5;
            })
            .attr("text-anchor", "middle");

        function mouseover(d) {  // utility function to be called on mouseover.
            // filter for selected state.
            var st = fData.filter(function (s) {
                    return s.State == d[0];
                })[0],
                nD = d3.keys(st.freq).map(function (s) {
                    return {type: s, freq: st.freq[s]};
                });

            // call update functions of pie-chart and legend.
            pC.update(nD);
            leg.update(nD);
        }

        function mouseout(d) {    // utility function to be called on mouseout.
            // reset the pie-chart and legend.
            pC.update(tF);
            leg.update(tF);
        }

        // create function to update the bars. This will be used by pie-chart.
        hG.update = function (nD, color) {
            // update the domain of the y-axis map to reflect change in frequencies.
            y.domain([0, d3.max(nD, function (d) {
                return d[1];
            })]);

            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);

            // transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function (d) {
                    return y(d[1]);
                })
                .attr("height", function (d) {
                    return hGDim.h - y(d[1]);
                })
                .attr("fill", color);

            // transition the frequency labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function (d) {
                    return d3.format(",")(d[1])
                })
                .attr("y", function (d) {
                    return y(d[1]) - 5;
                });
        };

        return hG;
    }

    // function to handle pieChart.
    function pieChart(pD) {
        var pC = {}, pieDim = {w: 250, h: 250};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

        // create svg for pie chart.
        var piesvg = d3.select(id).append("svg")
            .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
            .attr("transform", "translate(" + pieDim.w / 2 + "," + pieDim.h / 2 + ")");

        // create function to draw the arcs of the pie slices.
        var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

        // create a function to compute the pie slice angles.
        var pie = d3.layout.pie().sort(null).value(function (d) {
            return d.freq;
        });

        // Draw the pie slices.
        piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
            .each(function (d) {
                this._current = d;
            })
            .style("fill", function (d) {
                return segColor(d.data.type);
            })
            .on("mouseover", mouseover).on("mouseout", mouseout);

        // create function to update pie-chart. This will be used by histogram.
        pC.update = function (nD) {
            piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                .attrTween("d", arcTween);
        };
        // Utility function to be called on mouseover a pie slice.
        function mouseover(d) {
            // call the update function of histogram with new data.
            hG.update(fData.map(function (v) {
                return [v.State, v.freq[d.data.type]];
            }), segColor(d.data.type));
        }

        //Utility function to be called on mouseout a pie slice.
        function mouseout(d) {
            // call the update function of histogram with all data.
            hG.update(fData.map(function (v) {
                return [v.State, v.total];
            }), barColor);
        }

        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function (t) {
                return arc(i(t));
            };
        }

        return pC;
    }

    // function to handle legend.
    function legend(lD) {
        var leg = {};

        // create table for legend.
        var legend = d3.select('.js-user-legend').append("table").attr('class', 'legend');

        // create one row per segment.
        var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16').append("rect")
            .attr("width", '16').attr("height", '16')
            .attr("fill", function (d) {
                return segColor(d.type);
            });

        // create the second column for each segment.
        tr.append("td").text(function (d) {
            return msg(d.type);
        });

        // create the third column for each segment.
        tr.append("td").attr("class", 'legendFreq')
            .text(function (d) {
                return d3.format(",")(d.freq.toFixed(2));
            });

        // create the fourth column for each segment.
        tr.append("td").attr("class", 'legendPerc')
            .text(function (d) {
                return getLegend(d, lD);
            });

        // Utility function to be used to update the legend.
        leg.update = function (nD) {
            // update the data attached to the row elements.
            var l = legend.select("tbody").selectAll("tr").data(nD);

            // update the frequencies.
            l.select(".legendFreq").text(function (d) {
                return d3.format(",")(d.freq.toFixed(2));
            });

            // update the percentage column.
            l.select(".legendPerc").text(function (d) {
                return getLegend(d, nD);
            });
        };

        function msg(d){
            var a = {
                'time': 'Затраченное время, ч.',
                'tasks': 'Закрытые задачи'
            };

            return a[d];
        }

        function getLegend(d, aD) { // Utility function to compute percentage.
            var f = d3.sum(aD.map(function (v) {
                return v.freq;
            }));
            if (!f) return 0;
            return d3.format("%")((d.freq / f).toFixed(2));
        }

        return leg;
    }

    // calculate total frequency by segment for all state.
    var tF = ['time', 'tasks'].map(function (d) {
        return {
            type: d,
            freq: d3.sum(fData.map(function (t) {
                return t.freq[d];
            }))
        };
    });

    // calculate total frequency by state for all segment.
    var sF = fData.map(function (d) {
        return [d.State, d.total];
    });

    var hG = histoGram(sF), // create the histogram.
        pC = pieChart(tF), // create the pie-chart.
        leg = legend(tF);  // create the legend.
}

