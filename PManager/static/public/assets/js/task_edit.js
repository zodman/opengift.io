$(function () {
  function translit(text, engToRus, replace) {
    if (!text) {
      return text;
    }

    var rus = "щшчцюяёжъыэабвгдезийклмнопрстуфхь".split("");
    var eng = "shh sh ch cz yu ya yo zh `` y' e` a b v g d e z i j k l m n o p r s t u f x `".split(" ");

    for (var x = 0; x < rus.length; x++) {
      text = text.split(engToRus ? eng[x] : rus[x]).join(engToRus ? rus[x] : eng[x]);
      text = text.split(engToRus ? eng[x].toUpperCase() : rus[x].toUpperCase()).join(engToRus ? rus[x].toUpperCase() : eng[x].toUpperCase());
    }

    if (replace) {
      var r = replace.split(",")
      try {
        var pr = new RegExp("([^\\" + r[0] + "]+)(?=\\" + r[1] + ")", "g")
        text.match(pr).forEach(function (i) {
          text = text.split(r[0] + i + r[1]).join(translit(i, engToRus ? "" : true))
        })
      } catch (e) { }
    }

    return text;
  }

  var form = new Form('.js-project-form');

  if (!$('#task_edit_form').length) {
    return;
  }

  var $project = $('.js-project-step');
  var $task = $('.js-task-step').hide();

  var ajaxUrl = '/task_handler';

  function enableSubmit() {
    $('.js-submit, .js-butto-prev, .js-button-next').filter(':visible').removeAttr('disabled');
  }

  function disableSubmit() {
    $('.js-submit').attr('disabled', 'disabled');
  }

  // update project code
  $('[name="project_name"]').on('input',function (e) {
    var value = e.target.value;
    value = value.replace(/ /g,'_');
    var _translit = translit(value);
    $('[name="project_code"]').val(_translit);
  });

  $('.js-next-btn').click(function () {
    $(this).closest('.js-form-step').find('.js-form-step-content').show();
    $(this).hide();
    if (!$('.js-form-step-content:hidden').get(0)) {
      $('.js-submit').show();
    }
    return false;
  });

  $('.js-button-next').click(function () {   
    if (form.validate()) {
      form.clearError();
      $project.hide();
      $task.show();
    }
  });

  $('.js-butto-prev').click(function () {
    $project.show();
    $task.hide();
  });

  $('.js-submit').click(function () {
    if (form.validate()) {
      disableSubmit();
      form.$form.ajaxSubmit(function (data) {
        $('.js-file-new-block').val('').not(':eq(0)').remove().end();
        data = $.parseJSON(data);
        document.location.href = '/task_detail/?number=' + data.number + '&project=' + data.project.id;
      });
    }
    return false;
  });

  $('input, textarea, select').change(enableSubmit).keyup(enableSubmit);
  $('input:radio, input:checkbox').change(enableSubmit);

  $('.js-file-remove, .js-remove').click(function () {
    $(this).closest('.js-file-block').remove();
    enableSubmit();
    return false;
  });

  $('.js-add-file').click(function () {
    $('.js-file-new-block').clone().appendTo('.js-file-new-inputs').val('');
    return false;
  });

  $('.js-toggle-section').click(function () {
    var $subList = $(this).closest('.js-section-item').find('.js-subitems-list').eq(0);
    if ($subList.is(':visible')) {
      $subList.slideUp();
    }
    else {
      $subList.slideDown();
    }
  });
});