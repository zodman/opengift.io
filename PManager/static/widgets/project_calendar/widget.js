var ShowForm = function(el, arParams){
    $("#postform").find("input,select").each(
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
        //$('#title_inp').val('');
        $('#header_form').text(group_nm);
    }else{
        $('#header_form').text(group_nm);
    }
    var mytop = $(el).offset().top - 300;
    var myleft = $(el).offset().left - 50;
    $("#taskform")/*.css({"left":myleft+"px","top":mytop+"px"})*/.show();
    $('#title_inp').focus();
    flagcool = true;

    return false;
}

var ajaxSaveMileStone = function(data){
    PM_AjaxPost('/milestone_ajax/',data,function(data){
        $("#taskform").hide();
        document.location.reload();
    })
}

var deleteTask = function(id){
    PM_AjaxPost('/milestone_ajax/',{
        'action':'remove',
        'id':id
    },function(data){
        $(".js-milestone-"+id).remove();
    });
    return false;
}
$(function(){
    $("#postform .submit").click(function(){
        var $form = $(this).closest('form');
        var data = {
            'name':$form.find('[name=TITLE]').val(),
            'responsible':$form.find('[name=RESPONSIBLE_ID]').val(),
            'date':$form.find('[name=DEADLINE]').val(),
            'id':$form.find('[name=ID]').val(),
            'project':$form.find('[name=GROUP_ID]').val()
        }
        ajaxSaveMileStone(data);
    });
    $("#taskform").click(function(e){
        e.stopPropagation();
    });
//    $(document).click(function(){$("#taskform").hide()});
    $("input[name='DEADLINE']").datetimepicker({
        'format': 'd.m.Y',
        'timepicker': false,
        'closeOnDateSelect': true,
        'onDateSelect': function(ct){
            $(this).val = moment(ct).format('DD.MM.YYYY')
        }
    });
});