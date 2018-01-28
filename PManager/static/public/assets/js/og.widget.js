/**
 * Created by gvammer on 28.01.2018.
 */
var ogWidget = function (data) {
    this.partnerWallet = data.partnerWallet;
    this.project = data.project;
    this.$object = $(data.object);
    this.init();
};

var widgetFunc = function() {
    (function($) {
        $.fn.milestoneElement = function (selector) {
            return this.find('.js-og-widget-milestone-' + selector);
        };

        ogWidget.prototype = {
            'init': function () {
                var w = this;
                $('<link>')
                  .appendTo('head')
                  .attr({
                      type: 'text/css',
                      rel: 'stylesheet',
                      href: '/static/public/assets/css/og.widget.css'
                  });

                $.get('/static/public/assets/img/widget_template.html', function (data) {
                    var $widget = $(data),
                            $tplContainer = $widget.find('.js-og-widget-milestone-tpl-container');
                    var $milestoneTpl = $($tplContainer.get(0).innerHTML);
                    var oMilestone, $milestone;

                    $tplContainer.empty();
                    $(w.$object).replaceWith($widget);
                    $.post(
                        '/project/' + w.project + '/ajax/',
                        {
                            'action': 'milestones'
                        },
                        function (data) {
                            var i;
                            for (i in data) {
                                oMilestone = data[i];
                                $milestone = $milestoneTpl.clone();
                                $milestone.milestoneElement('name').html(
                                        oMilestone.name + '<br />' + oMilestone.description
                                );
                                $milestone.milestoneElement('date').text(oMilestone.date);
                                $milestone.milestoneElement('likes-qty').text(oMilestone.likesQty);
                                $milestone.milestoneElement('donations-qty').text(oMilestone.donationsQty);
                                $milestone.milestoneElement('progress-bar').css('width', oMilestone.percent + '%');
                                $milestone.milestoneElement('progress').text(oMilestone.percent + '%');
                                $milestone.milestoneElement('doit-link').attr(
                                    'href',
                                    '/project/' + w.project + '/donate/?m=' + oMilestone.id
                                );

                                $milestone.appendTo($tplContainer);
                            }
                        },
                        'json'
                    );
                });
            }
        };

        $('.js-og-widget').each(function() {
            new ogWidget({'object':this, 'project': $(this).data('project')});
        });
    })(jQuery);
};
setTimeout(function() {
    if(typeof jQuery=='undefined') {
        var headTag = document.getElementsByTagName("head")[0];
        var jqTag = document.createElement('script');
        jqTag.type = 'text/javascript';
        jqTag.src = 'https://code.jquery.com/jquery-1.10.2.js';
        jqTag.onload = widgetFunc;
        headTag.appendChild(jqTag);
    } else {
         widgetFunc();
    }
}, 1000);