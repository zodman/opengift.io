/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:34
 */
(function ($) {
    window.historyManager = (function () {
        var history = $.history;
        var self = this;
        this.params = {};
        this.callbacks = [];
        this.url = '';

        this.trigger = function (event) {
            for (var k in self.callbacks) {
                if (self.callbacks[k]['name'] == event) {
                    self.parseUrl(self.url);
                    self.callbacks[k]['func'].call(self, self.params);
                }
            }
        }
        this.addParams = function (params) {
            this.params = $.extend(this.params, params);
            this.pushUrl();
        }
        this.addCallback = function (name, callback) {
            if (typeof name == 'function') {
                callback = name;
                name = false;
            }
            self.callbacks.push({'name': name, 'func': callback});
        }
        this.pushUrl = function () {
            history.push(encodeURIComponent(JSON.stringify(this.params)));
        }
        this.parseUrl = function (url) {
            if (url) {
                this.params = $.parseJSON(decodeURIComponent(url));
            }
        }

        history.on('load change', function (event, url, type) {
            if (url) {
                this.url = url;
                self.parseUrl(url);
                for (var k in self.callbacks) {
                    self.callbacks[k]['func'].call(self, self.params);
                }
            }
        });
        history.listen('hash');
        return this;
    })();
})(jQuery);

function closePopups() {
    $('.pup').hide();
}

function getKeyPressed(e) {
    var key;
    if (window.event) {
        key = window.event.keyCode;
    } else {
        key = e.keyCode;
    }
    return key;
}

try {
    jQuery.expr[":"].Contains = jQuery.expr.createPseudo(function (arg) {
        return function (elem) {
            return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
        };
    });
} catch (e) {

}

$.fn.enterPressed = function (func) {
    this.unbind('keydown.enter').bind('keydown.enter', function (e) {
        var key = getKeyPressed(e);
        if (key == 13) func(this);
    });
    return this;
}

var widgetObject = function (widgetData) {
    this.id = widgetData.id;
    this.aReadyFunc = [];
    this.state = {

    }
    this.container = widgetData.container;
    if (widgetData.init && typeof widgetData.init == 'function')
        this.init = widgetData.init;
}

widgetObject.prototype = {
    init: function () {

    },
    'ready': function (callback) {
        if (callback) {
            this.aReadyFunc.push(callback);
        } else {
            for (var i in this.aReadyFunc) {
                this.aReadyFunc[i].call(this);
            }
        }
    }
}

var mainControllerClass = function (data) {
    this.userId = data.userId;
    this.isClient = data.isClient ? true : false;
    this.isEmployee = data.isEmployee ? true : false;
    this.isAdmin = data.isAdmin ? true : false;

    this.widgetsData = data.widgetsData;
    this.init();
}

mainControllerClass.prototype = {
    init: function () {

    },
    inviteUser: function($btn, $email) {
        var arVal = [];
        $email.each(function(){
            if ($(this).val()) {
                var roles = [], $roleChecks = $(this).closest('.js-invite-cont').find(':checkbox');
                $roleChecks.filter(':checked').each(function(){
                    roles.push($(this).val());
                    $(this).attr('checked', false);
                });
                if (roles.length <= 0) {
                    alert('Выберите хоть одну роль в проекте.');
                    return false;
                }
                arVal.push({
                    'email': $(this).val(),
                    'roles': roles
                });
            }
        });

        if (arVal.length <= 0) {
                alert('Введите корректный email');
                return false;
        } else {
            PM_AjaxPost(
                '/users_ajax/',
                {
                    'action': 'inviteUser',
                    'email': arVal
                },
                function(data){
                    $email.val('');
                    if (data == 'ok') {
                        alert('Пользователи успешно приглашены!');
                    } else {
                        alert(data);
                    }
                }
            )
        }
    }
}

function formatDate(date) {
    var dd = date.getDate();
    var mm = date.getMonth() + 1;
    var yyyy = date.getFullYear();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }
    var formatted = dd + '.' + mm + '.' + yyyy;
    if (typeof hours === 'number' && typeof minutes === 'number') {
        // hours and minutes can be 0
        if (hours < 10) {
            hours = '0' + hours;
        }
        if (minutes < 10) {
            minutes = '0' + minutes;
        }
        formatted += ' ' + hours + ':' + minutes;
    }
    return formatted;
}
function PM_AjaxPost(url, data, func, type) {
    if (!data.project) {
        if (window.currentProject)
            data.project = parseInt(window.currentProject);
        else
            data.project = 0;
    }

    return $.post(url, data, func, type);
}

var PM_Timer = function (data) {
    if (typeof(data) == 'object' || typeof(data) == 'array') {
        if (data.seconds) this.seconds = data.seconds * 1; else this.seconds = 0;
        if (data.minutes) this.minutes = data.minutes * 1; else this.minutes = 0;
        if (data.hours) this.hours = data.hours * 1; else this.hours = 0;
        if (data.container) this.container = data.container;
        if (data.started) this.started = data.started;
    } else if (parseInt(data)) {
        this.seconds = parseInt(data);
        this.minutes = 0;
        this.hours = 0;
    } else {
        this.seconds = 0;
        this.minutes = 0;
        this.hours = 0;
    }

    this.init();
    if (this.started) {
        this.start();
    }
}
PM_Timer.prototype = {
    'init': function () {
        if (this.seconds > 60) {
            this.minutes += Math.floor(this.seconds / 60);
            this.seconds = this.seconds % 60;
        }
        if (this.minutes > 60) {
            this.hours += Math.floor(this.minutes / 60);
            this.minutes = this.minutes % 60;
        }
    },
    'start': function () {
        var obj = this;
        if (this.interval) clearInterval(this.interval);
        this.interval = setInterval(function () {
            obj.seconds++;
            obj.init();
            obj.fill();
        }, 1000);
        this.started = true;
    },
    'stop': function () {
        if (this.interval) clearInterval(this.interval);
        this.started = false;
    },
    'toString': function () {
        var hours = this.hours * 1,
            minutes = this.minutes * 1,
            seconds = this.seconds * 1;

        if (hours < 10 && (hours.length < 2 || hours.length == undefined)) hours = '0' + hours + '';
        if (minutes < 10 && (minutes.length < 2 || minutes.length == undefined)) minutes = '0' + minutes + '';
        if (seconds < 10 && (seconds.length < 2 || seconds.length == undefined)) seconds = '0' + seconds + '';

        return hours + ":" + minutes + ":" + seconds;
    },
    'fill': function(){
        if (this.container) {
            $(this.container).html(this.toString())
        }
    }
}

/***
 *
 * @param name - may be "small
 * @param container
 * @param add_params
 */
function startLoader(name, container, add_params) {
    container = $(container);
    if (typeof(container) == 'object') {
        if (!container.is(":visible")) {
            return false;
        }
    }
    $loader = $('.loader.' + name + '');
    var objPos = getObjectCenterPos(container);

    if (!add_params) add_params = {"left": 0, "top": 0}
    if (!add_params.left) add_params.left = 0;
    if (!add_params.top) add_params.top = 0;

    if (add_params.modal) {
        return $loader.css({
            position: 'fixed',
            left: '50%',
            top: '50%'
        }).show();
    }
    if (add_params.exception) {
        $loader.addClass('dont_hide');
    } else {
        $loader.removeClass("dont_hide");
    }
    var w_h = parseInt($loader.width());
    return $loader.css({
        'position': 'absolute',
        'left': (objPos.left + (objPos.width / 2) + add_params.left - w_h / 2),
        'top': (objPos.top + (objPos.height / 2) + add_params.top - w_h / 2)
    }).show();
}

function stopLoader(objloader) {
    if (objloader && typeof(objloader.hide) == 'function')
        objloader.hide();
}

function stopLoaders() {
    $('.loader').hide();
}
function getObjectCenterPos(container) {
    if (typeof(container) == 'object') {
        container = $(container);
        if (!container.is(":visible")) {
            return false;
        }
    }
    var heightObj = 0;
    var widthObj = 0;
    var offset = {}
    if (container && container != "") {
        $container = $(container);
        offset = $container.offset();
        var cont = $container.get(0);
        if (cont) {
            heightObj = cont.offsetHeight;
            widthObj = cont.offsetWidth;
        }
    }
    var ret = {left: offset.left, top: offset.top, width: widthObj, height: heightObj}
    return ret;
}

$(function () {
    $('.optionRowPopUp, .widgets-list').bind("clickoutside", function () {
        $(this).hide();
    });

    $('input[data-blur],textarea[data-blur]').focus(function () {
        if ($(this).val() == $(this).attr('data-blur')) {
            $(this).val('');
        }
    }).blur(function () {
            if ($(this).val() == '') {
                $(this).val($(this).attr('data-blur'));
            }
        });

    $(document).on('click', 'a', function () {
        closePopups();
    });
});

function showOverlay() {
    $('.overlay').show();
}
function hideOverlay() {
    $('.overlay').hide();
}
$.fn.pushed = function () {
    return this.hasClass('activated');
}
$.fn.pushTheButton = function () {
    this.data(
        'loader',
        startLoader('small', this.get(0))
    );
    this.addClass('activated');
    return this;
}
$.fn.pullTheButton = function () {
    stopLoader(this.data('loader'));
    this.removeClass('activated');
    return this;
}
$.fn.hasAttr = function (name) {
    return this.attr(name) !== undefined;
};

$.fn.selectText = function () {
    var range, selection;
    return this.each(function () {
        if (document.body.createTextRange) {
            range = document.body.createTextRange();
            range.moveToElementText(this);
            range.select();
        } else if (window.getSelection) {
            selection = window.getSelection();
            range = document.createRange();
            range.selectNodeContents(this);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    });
    return this;
};

$.fn.setEditable = function (callback) {
    var t = this;
    setTimeout(function () {
        t.attr('contenteditable', true).focus().selectText();
        $(document).unbind('mouseup.editableContent').one('mouseup.editableContent', function () {
            $(t).attr('contenteditable', false).trigger('blur');
            callback.call(t);
        });
        t.enterPressed(function () {
            $(t).attr('contenteditable', false).trigger('blur');
            callback.call(t);
        });
    }, 100);
}

var bLinkEscape;
$(function () {
    $(document).on('mousedown', 'a[href]', function () {
        bLinkEscape = true;
    });
    $('.js-main-fnc').fancybox({
        'type': 'ajax'
    });
});

window.onbeforeunload = function (evt) {
    if (!bLinkEscape) {
        if (oMyCurrentTimer.started) {
            var message = "Вы продолжаете работать над задачей. Все равно закрыть окно?";
            if (typeof evt == "undefined") {
                evt = window.event;
            }
            if (evt) {
                evt.returnValue = message;
            }
            return message;
        }
    }
};

$(document).on('click', '.js-send_feedback', function() {
    startLoader('small', '.js-send_feedback');
    $.post('/ajax/feedback/',
           $('.js-feedback_form').serialize(),
           function(html) {
               $('.js-modal_content').html(html);
               stopLoaders();
           }
    )
});

$(document).on('click', '.js-feedback', function () {
    $.get('/ajax/feedback/', function (data) {
        $('.js-modal_content').html(data);
        stopLoaders();
    });
});

$(document).on('shown.bs.modal', function () {
    startLoader('medium', '.js-feedback_loader');
});
