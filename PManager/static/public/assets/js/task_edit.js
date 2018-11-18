$(function () {
    function translit(text, engToRus, replace) {
        if (!text) {
            return text;
        }

        var rus = "щшчцюяёжъыэабвгдезийклмнопрстуфхь".split("");
        var eng = "shh sh ch cz yu ya yo zh __ y e a b v g d e z i j k l m n o p r s t u f x _".split(" ");

        for (var x = 0; x < rus.length; x++) {
            text = text.split(engToRus ? eng[x] : rus[x]).join(engToRus ? rus[x] : eng[x]);
            text = text.split(engToRus ? eng[x].toUpperCase() : rus[x].toUpperCase()).join(engToRus ? rus[x].toUpperCase() : eng[x].toUpperCase());
        }

        if (replace) {
            var r = replace.split(",");
            try {
                var pr = new RegExp("([^\\" + r[0] + "]+)(?=\\" + r[1] + ")", "g");
                text.match(pr).forEach(function (i) {
                    text = text.split(r[0] + i + r[1]).join(translit(i, engToRus ? "" : true))
                })
            } catch (e) {
            }
        }

        return text.toLowerCase();
    }

    var form = new Form('.js-project-form');

    if (!$('#task_edit_form').length) {
        return;
    }


    function enableSubmit() {
        $('.js-submit').filter(':visible').removeAttr('disabled');
    }

    function disableSubmit() {
        $('.js-submit').attr('disabled', 'disabled').addClass('disabled');
    }

    // update project code
    $(document).on('input', '[name="project_name"]', function (e) {
        var value = e.target.value;
        value = value.replace(/[^A-z0-9_А-я]+/g, '_');
        var _translit = translit(value);
        $('[name="project_code"]').val(_translit.toLowerCase());
    });

    $('.js-submit').unbind('click').click(function () {
        if (form.validate()) {
            disableSubmit();
            form.$form.ajaxSubmit(function (data) {
                data = $.parseJSON(data);
                setTimeout(function () {
                    $('#task_edit_form').hide();
                    $('.js-donate-for-task').attr('href', '/task_detail/?number='+data.number+'&project=' + data.project.id);
                    $('.js-manage-project').attr('href', '/project/' + data.project.id + '/');
                    $('.js-task-created').show();
                }, 500);
            });
        }
        return false;
    });

    $('input, textarea, select').change(enableSubmit).keyup(enableSubmit);
    $('input:radio, input:checkbox').change(enableSubmit);
});