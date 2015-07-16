var ShowForm = function(el, arParams) {
    $(".js-milestone-form").find("input,select").each(
        function(){
            obj = $(this);
            if (obj.attr("name") == 'ID'){
                obj.val(arParams['id']);
            }else if(obj.attr("name") == 'TITLE'){
                obj.val($(el).parent().find('a').eq(0).text());
            }else if(obj.attr("name") == 'DEADLINE'){
                obj.val(arParams['deadline']);
            }else if(obj.attr("name") == 'RESPONSIBLE_ID' && arParams['resp_id']){
                $(this).val(arParams['resp_id']);
            }else if(obj.attr("name") == 'PRIORITY'){
                $(this).val(arParams['prior']);
            }else if(obj.attr("name") == 'GROUP_ID' && arParams['project_id']){
                $(this).val(arParams['project_id']);
            }
        }
    );

    var group_nm = $(el).parents('tr').eq(0).find('.grp_name').eq(0).text();
    if (arParams['project_id']){
        $('#title_inp').val('');
        $('#header_form').text(group_nm);
    }else{
        $('#header_form').text(group_nm);
    }

    $(".js-form-modal").show();
    $('.js-title-input').focus();

    return false;
};

var ajaxSaveMileStone = function(data){
    PM_AjaxPost('/milestone_ajax/',data,function(data){
        $("#taskform").hide();
        document.location.reload();
    })
};

var deleteTask = function(id){
    PM_AjaxPost('/milestone_ajax/',{
        'action':'remove',
        'id':id
    },function(data){
        $(".js-milestone-"+id).remove();
    });
    return false;
};

$(function(){
    $('.js-milestone-submit').click(function(){
        var $form = $(this).closest('form');
        var data = {
            'name':$form.find('[name=TITLE]').val(),
            'responsible':$form.find('[name=RESPONSIBLE_ID]').val(),
            'date':$form.find('[name=DEADLINE]').val(),
            'id':$form.find('[name=ID]').val(),
            'project':$form.find('[name=GROUP_ID]').val()
        };

        ajaxSaveMileStone(data);
    });

    $("#taskform").click(function(e){
        e.stopPropagation();
    });
    $("input[name='DEADLINE']").datetimepicker({
        'format': 'd.m.Y',
        'timepicker': false,
        'closeOnDateSelect': true,
        'onDateSelect': function(ct){
            $(this).val = moment(ct).format('DD.MM.YYYY')
        }
    });
    var slideTopProceed = false;
    var $sliderTop = $('.js-calendar-slider').bxSlider({
        infiniteLoop: false,
        slideWidth: 200,
        minSlides: 2,
        maxSlides: 7,
        pager: false,
        nextText:'<i class="fa fa-angle-right"></i>',
        prevText:'<i class="fa fa-angle-left"></i>',
        hideControlOnEnd: true,
        onSlideBefore: function($slideElement, oldIndex, newIndex){
            slideTopProceed = true;
            $sliderBot.goToSlide(newIndex);
        },
        onSlideAfter: function(){
            slideTopProceed = false;
        }
    });
    var $sliderBot = $('.js-calendar-slider-2').bxSlider({
        infiniteLoop: false,
        slideWidth: 200,
        minSlides: 2,
        maxSlides: 7,
        pager: false,
        controls: false,
        hideControlOnEnd: true,
        onSlideBefore: function($slideElement, oldIndex, newIndex){
            if (!slideTopProceed) {
                $sliderTop.goToSlide(newIndex);
                return false;
            }
        }
    });

    var navHeight = $('.calendar-project-list-title-wrapper').offset().top - 59;
    $(window).bind('scroll', function() {
        if ($(window).scrollTop() > navHeight) {
            $('.calendar-project-list-title-wrapper').addClass('fixed');
            $('.calendar-project-list-dates').addClass('top-30');
        }
        else {
            $('.calendar-project-list-title-wrapper').removeClass('fixed');
            $('.calendar-project-list-dates').removeClass('top-30');
        }
    });

});