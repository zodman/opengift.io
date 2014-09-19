/**
 * Author: Artem Smirnov <tonakai.personal@gmail.com>
 * easyFormStepper
 * to provide easy interface to step throw form
 * v.001
 */
(function($) {
    $.easyFormStepper = function(element, options) {
        var defaults = {
            eventSpace: "easyFormStepper",
            questionContainer: "",
            buttonNextSelector: "",
            buttonPrevSelector: "",
            buttonSubmitSelector: "",
            buttonCancelSelector: "",
            onClose: function($element) {},
            onStart: function($element) {},
            onStepStart: function(step, $element) {},
            onStepSubmit: function() {},
            onStepSkip: function() {},
            onStepValidation: function() {},
            onSubmit: function(answers) {},
            onCancel: function() {},
            transition: function(step, newStep, fn) {}
        };

        var KEY_ESCAPE = 27;
        var KEY_ENTER = 13;

        var plugin = this;
        var current_question = 0;
        var step = false;
        var steps = false;
        var aStepsSkipped = new Array();

        var $element = $(element),
            element = element;
        var validateStep = function() {
            if (step === false) return true;
            plugin.settings.onStepValidation(step);
            var st = $(step).find('input');
            if (st.attr('required') && !st.val()) {
                return false;
            }
            return true;
        };
        var hasPrevStep = function() {
            return current_question > 0;
        };

        var canSubmit = function() {
            if (aStepsSkipped.length > 0) {
                return false;
            }
            for (var i = steps.length - 1; i >= 0; i--) {
                var el = $(steps[i]).find('input');
                if (el && el.attr('required') && !el.val()) {
                    return false;
                }
            };
            return true;
        };

        var updateButtons = function() {
            $(plugin.settings.buttonNextSelector).prop('disabled', !hasNextStep());
            $(plugin.settings.buttonPrevSelector).prop('disabled', !hasPrevStep());
            $(plugin.settings.buttonSubmitSelector).prop('disabled', !canSubmit());
        };
        var setCurrentStep = function(iStepKey) {
            $newStep = steps[iStepKey];
            current_question = iStepKey;
            if (!$newStep) {
                return false;
            }
            plugin.settings.transition(step, $newStep, function() {
                plugin.settings.onStepStart($newStep, $element);
            });
            step = $newStep;
            updateButtons();
        };
        var hasNextStep = function() {
            return (steps.length - 1 > current_question);
        };
        var bindEvents = function() {
            //cancels
            $(plugin.settings.buttonCancelSelector).bind("click." + plugin.settings.eventSpace, plugin.cancel);
            $(document).bind("keyup." + plugin.settings.eventSpace, function(ev) {
                if (ev.keyCode === KEY_ESCAPE || ev.which === KEY_ESCAPE) {
                    plugin.cancel();
                }
                $(document).unbind('keyup.' + plugin.settings.eventSpace);
            });
            $(plugin.settings.questionContainer).on("keyup." + plugin.settings.eventSpace, "input", function(ev) {
                updateButtons();
                if (ev.keyCode === KEY_ENTER || ev.which === KEY_ENTER) {
                    ev.preventDefault();
                    plugin.nextStep();
                }
            });
            //form submit
            $(plugin.settings.buttonSubmitSelector).bind("click." + plugin.settings.eventSpace, plugin.submit);
            $(plugin.settings.buttonNextSelector).bind("click." + plugin.settings.eventSpace, plugin.nextStep);
            $(plugin.settings.buttonPrevSelector).bind("click." + plugin.settings.eventSpace, plugin.prevStep);
        };

        plugin.settings = {};

        plugin.cancel = function() {
            plugin.settings.onCancel();
            plugin.close();
        };

        plugin.submit = function() {
            var answers = new Array();
            for (var i = steps.length - 1; i >= 0; i--) {
                answers.push($(steps[i]).find('input').val());
            };
            plugin.settings.onSubmit(answers.reverse());
            plugin.close();
        };

        plugin.close = function() {
            plugin.settings.onClose($element);
        };

        plugin.nextStep = function() {
            if (!hasNextStep()) {
                if (aStepsSkipped.length === 0) {
                    plugin.submit();
                } else {
                    setCurrentStep(aStepsSkipped.pop());
                }
                return false;
            }
            if (validateStep()) {
                plugin.settings.onStepSubmit();
            } else {
                plugin.settings.onStepSkip();
                console.log('skip');
                aStepsSkipped.push(current_question);
            }
            setCurrentStep(current_question + 1);
        };

        plugin.prevStep = function() {
            if (current_question === 0) {
                return false;
            }
            setCurrentStep(current_question - 1);
        };


        plugin.init = function() {
            plugin.settings = $.extend({}, defaults, options);
            steps = $element.find(plugin.settings.questionContainer);
            bindEvents();
            current_question = -1;
            plugin.nextStep();
        };

        plugin.init();
        plugin.settings.onStart($element);
    }
    $.fn.easyFormStepper = function(options) {
        return this.each(function() {
            if (undefined == $(this).data('easyFormStepper')) {
                var plugin = new $.easyFormStepper(this, options);
                $(this).data('easyFormStepper', plugin);
            }
        });
    };
})(jQuery);