/**
 * Created by gvammer on 19.05.2016.
 */
(function ($) {
    $.fn.isWindowScrolledToElement = function (offset) {
        offset = parseInt(offset) || 0;
        return $(document).scrollTop() + $(window).height() > $(this).offset().top + offset;
    };

    $.fn.onScrollToElement = function (callbackOnScroll,
                                       callbackIfAlreadyScrolled,
                                       execTriggerEvenIfAlreadyScrolled,
                                       scrollOutCallback,
                                       options
    ) {
        var t = this;

        if (!t.size()) return;
        if (!options) options = {};

        $(document).bind('scroll.scrolltoelements', function () {
            if ($(t).isWindowScrolledToElement(options.offset)) {
                if (!$(t).data('scrolled-to-element')) {
                    $(t).data('scrolled-to-element', true);
                    if (typeof callbackOnScroll == 'function') callbackOnScroll.call(t);
                }
            } else {
                if ($(t).data('scrolled-to-element')) {
                    if (typeof scrollOutCallback == 'function') {
                        $(t).data('scrolled-to-element', false);
                        scrollOutCallback.call(t);
                    }
                }
            }
        });

        if (!$(t).isWindowScrolledToElement(options.offset)) {

        } else {
            if (execTriggerEvenIfAlreadyScrolled) {
                if (typeof callbackOnScroll == 'function') {
                    $(t).data('scrolled-to-element', true);
                    callbackOnScroll.call(t);
                }
            }

            if (typeof callbackIfAlreadyScrolled == 'function') callbackIfAlreadyScrolled.call(t);
        }
    };

    $.fn.scrollToThis = function() {
        if (this.offset())
            $('html, body').scrollTop(this.offset().top - ($(window).height() / 3));
        return this;
    };
})(jQuery);

function Form(formSelector) {
    this['lastError'] = false;
    this['errorsExist'] =  false;
    this['extValidator'] =  false;

    this.init = function() {
        this.$form = $(formSelector);

        this.$errorContainer = this.$form.find('.js-form-error-container');


        this.$form.on('change', '.has-error [type="checkbox"], .has-error [type="hidden"]', function () {
            var fieldGroup = $(this).closest('.js-form-group');
            fieldGroup.removeClass('has-error');
        });

        this.$form.on('keyup', '.js-required, [required]', function() {

            var input = $(this),
                fieldGroup = $(this).closest('.js-form-group'),
                currentVal = input.val();

            if(currentVal.length > 0)
                fieldGroup.removeClass('has-error');
            else
                fieldGroup.addClass('has-error');

        });

        this.$form.on('keyup', 'input[data-min-length]', function(e) {
            e.stopPropagation();

            var input = $(this),
                fieldGroup = input.closest('.js-form-group'),
                minLength = input.attr('data-min-length'),
                currentVal = input.val();

            if(currentVal.length < minLength)
                fieldGroup.addClass('has-error');
            else
                fieldGroup.removeClass('has-error');

        });

        this.$form.on('keyup', 'input[data-valmask]', function(e) {
            e.stopPropagation();

            var input = $(this),
                fieldGroup = input.closest('.js-form-group'),
                currentVal = input.val(),
                re = new RegExp($(this).data('valmask'), 'g');

            if (!re.test(currentVal))
                fieldGroup.addClass('has-error');
            else
                fieldGroup.removeClass('has-error');
        });

        this.$form.find('.has-error').eq(0).scrollToThis();
    };

    this.showError = function(text, $elem) {
        this.lastError = text;
        if (this.$errorContainer.length) {
            this.$errorContainer.html(text).show();
        } else {
            ERROR_REPORTER.showMessage(text, MESSAGE_TYPE_ERROR);
        }

        if ($elem) {
            if ($elem.closest('.js-form-group').exists()) {
                $elem.closest('.js-form-group').addClass('has-error');
            } else {
                $elem.addClass('has-error');
            }
        }
    };

    this.clearError = function() {
        this.lastError = false;
        this.$errorContainer.empty().hide();
        this.$form.find('.has-error').removeClass('has-error');
    };

    this.clear = function() {
        this.$form.find('input, textarea').not('[type=submit], [type=button]').val('');
        this.$form.find('input[type=checkbox]').removeAttr('checked');
    };

    this.validate = function() {
        var t = this;
        this.clearError();
        this.errorsExist = false;
        this.$form.find('input, textarea, select').not(':disabled, [type=checkbox], [type=radio]').filter(':visible').each(function(){
            var currentVal = $(this).val(),
                currentFieldError = false,
                fieldGroup = $(this).closest('.js-form-group');


            if ($(this).is('.js-required') || $(this).is('[required]')) {
                if (!currentVal || /^[\s]+$/.test(currentVal)) {
                    currentFieldError = $(this).data('empty-error') || true;
                } else {
                    if ($(this).data('min-length')) {
                        if (currentVal.length < parseInt($(this).data('min-length'))) {
                            currentFieldError = $(this).data('field-error') ||  MangoVars.messages['FIELD_MIN_LENGTH']
                                .replace(
                                    '#FIELD#',
                                    $(this).data('fieldname') || $(this).attr('placeholder')
                                )
                                .replace(
                                    '#VAL#',
                                    $(this).data('min-length')
                                );
                        }
                    }

                    if (!currentFieldError && $(this).data('max-length')) {
                        if (currentVal.length > parseInt($(this).data('max-length'))) {
                            currentFieldError = $(this).data('field-error') || MangoVars.messages['FIELD_MAX_LENGTH']
                                .replace(
                                    '#FIELD#',
                                    $(this).data('fieldname') || $(this).attr('placeholder')
                                )
                                .replace(
                                    '#VAL#',
                                    $(this).data('max-length')
                                );
                        }
                    }

                    if (!currentFieldError && $(this).data('valmask')) {
                        var re = new RegExp($(this).data('valmask'), 'g');
                        if (!re.test(currentVal)) {
                            currentFieldError = $(this).data('field-error') || 'Поле заполнено не верно';
                        }
                    }

                    if (!currentFieldError && $(this).data('numberTo')) {
                        if (parseFloat(currentVal) > parseFloat($(this).data('number-to'))) {
                            currentFieldError = $(this).data('field-error')  || 'Значение поля должно быть не более '+$(this).data('numberTo');
                        }
                    }

                    if (!currentFieldError && $(this).data('numberFrom')) {
                        if (isNaN(parseFloat(currentVal)) || parseFloat(currentVal) < parseFloat($(this).data('number-from'))) {
                            currentFieldError = $(this).data('field-error')  || 'Значение поля должно быть не менее '+$(this).data('numberFrom');
                        }
                    }
                }
            }

            if (currentFieldError) {
                fieldGroup.addClass('has-error');
                if (currentFieldError === true) currentFieldError = 'Заполните корректно все необходимые поля';

                t.showError(currentFieldError);
                t.errorsExist = true;
            }
        });

        // Валидация чекбоксов
        this.$form.find('input[type="checkbox"], input[type="radio"]').filter(':visible').each(function(){
            var currentFieldError = false,
                fieldGroup = $(this).closest('.js-form-group');


            if ($(this).is('.js-required') && !$('[name="'+this.name+'"]:checked').length) {
                currentFieldError = true;
            }

            if (currentFieldError) {
                fieldGroup.addClass('has-error');
                if (currentFieldError !== true) {
                    t.showError(currentFieldError);
                }
                t.errorsExist = true;
            }
        });

        if (!t.errorsExist && t.extValidator && typeof t.extValidator == 'function') {
            t.extValidator.call(t);
        }

        if(t.errorsExist){
            var firstError = t.$form.find('.error-line, .has-error').first();
            if (this.$errorContainer.length)
                firstError.scrollToThis();
        }

        return !t.errorsExist;
    };

    this.init();
}


$(function() {
    var removeErrorClass = function() {
        this.removeClass('error');
    };
    $(document).on('keyup change', 'input.error, textarea.error, select.error', removeErrorClass).on('click', '[type=checkbox].error', removeErrorClass);
});

/**
 * Error reporter
 */

var MESSAGE_TYPE_ERROR = 'danger';
var MESSAGE_TYPE_SUCCESS = 'success';
var MESSAGE_TYPE_WARNING = 'warning';
var MESSAGE_TYPE_INFO = 'info';

var ERROR_REPORTER = {
    '$block': false,
    'selectorPrefix': '.js-error-container',
    'showDelay': 10000,
    'classes': [
        'label-danger',
        'label-warning',
        'label-success'
    ],
    'hideTimeout': false,
    'errorStack': [],
    'init': function () {
        this.$block = $(this.selectorPrefix);

        $(this.selectorPrefix + '-close').click(function () {
            ERROR_REPORTER.hideMessage();
            return false;
        });
    },
    'setBlockPosition': function () {

    },
    'isModalOpened': function () {
        return $('body').hasClass('modal-open');
    },
    '$getModalErrorBlock': function (notOnlyVisible) {
        return $('.modal' + (notOnlyVisible ? '' : ':visible') + ' .js-modal-error');
    },
    'showMessage': function (text, type, woDelay) {
        if (!type) type = MESSAGE_TYPE_ERROR;

        var err = new Error();

        this.errorStack.push({
            'text': text,
            'type': type,
            'stack': err.stack
        });

        if (this.isModalOpened()) {
            this.$getModalErrorBlock().html(text).addClass('label-' + type).show();
        } else {
            this.$block.find(this.selectorPrefix + '-text').html(text).end().slideDown();

            this.$block.removeClass(this.classes.join(' ')).addClass('label-' + type);
        }

        if (this.showDelay && !woDelay) {
            if (this.hideTimeout) {
                clearTimeout(this.hideTimeout);
            }

            this.hideTimeout = setTimeout(function () {
                ERROR_REPORTER.hideMessage();
            }, this.showDelay);
        }

        if (type == MESSAGE_TYPE_ERROR) {
            this.log(text, err.stack);
        }
    },
    'hideMessage': function () {
        if (this.$block.is(':visible'))
            this.$block.slideUp();

        this.$getModalErrorBlock(true).hide();
    },
    'lastError': function () {
        return this.errorStack.length && this.errorStack[this.errorStack.length - 1];
    },
    'log': function(text, stack) {
        return true;
    }
};

(function ($) {
    $(function () {
        ERROR_REPORTER.init();
    });
})(jQuery);

var showGlobalMessages = function (errorText, type) {
    ERROR_REPORTER.showMessage(errorText, type);
};

_alert = alert;
alert = function(text) {
    ERROR_REPORTER.showMessage(text);
};

alertDefaultError = function () {
    alert('Возникла непредвиденная ошибка, попробуйте еще раз.');
};