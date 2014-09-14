/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 18.10.12
 * Time: 14:44
 * To change this template use File | Settings | File Templates.
 */

$(function(){
    $( ".slider_row").each(function(){
        var id = $(this).attr('data-id'),
            val = $( "#"+id+"" ).val()?$( "#"+id+"" ).val()*100:50;

        $(this).slider({
            range: "max",
            min: 1,
            max: 100,
            value: val,
            slide: function( event, ui ) {
                var val = ui.value;
                if (ui.value)
                    $( "#"+id+"" ).val( val/100 );
            }
        });
        $( "#"+id+"" ).val( "0."+val );
    });


    var widget_te = new widgetObject({id:'task_edit'});
    widget_te.state = {
        taskCreate:false,
        hintOpened:{
            'Responsible':false,
            'Date':false,
            'Author':false
        }
    }
    widget_te.container = $('#task_edit');

    $.extend(widget_te,{
    });

    widget_te.init();

    document.mainController.widgetsData["task_edit"] = widget_te;

    $(".showPopup").click(function(e){
        var box =  $(this).closest('span');
        if(box.hasClass('open')){
        box.removeClass('open');
        }else{
        box.addClass('open');
        }
        e.stopPropagation();
        var obj = box.find('.dropdown-menu');
        $(document).bind("click.ShowPopup",function (pos) {
            var leftObj = obj.offset().left;
            var topObj = obj.offset().top;
            var height = obj.outerHeight();
            var width = obj.outerWidth();
            if(pos.pageX>(leftObj+width) || pos.pageX< leftObj || pos.pageY>(height+topObj) ||  pos.pageY<topObj){
                box.removeClass('open');
                $(document).unbind("click.ShowPopup");
            }
        });
        return false;
    });
     $(".js-observers").on('click', '.js-icon-remove', function(){
            var li = $(this).closest("li");
            var flag = true;
            if(isNaN(parseInt(li.find('input').val()))){
                flag = false;
            }
            if(flag){
                var newOption = $('<option value="'+li.find('input').val()+'">'+li.find('span').text()+'</option>');
                if(li.hasAttr('data-indexoption')){
                    $(".profile-edit-responsible select  option:nth-child("+(li.attr("data-indexoption"))+")").after(newOption);
                }else{
//                     $(".profile-edit-responsible select").append(newOption);
                }
            }
            li.remove();
        });

        $('.js-select-observer').click(function(){
           if($(this).data('id')){
               addObserverTag($(this).text(), $(this).data('id'));
           }
           return false;
        });

		$(".hideFilter").click(function(eventObject){
			$(".profile-edit-filter").slideToggle(1000,function(){
				if($(this).is(":hidden")){
					$(".hideFilter").html("Разверуть&nbsp;&nbsp;<i class=\"icon-chevron-down\"></i>");
				}
				else{
					$(".hideFilter").html("Свернуть&nbsp;&nbsp;<i class=\"icon-chevron-up\"></i>");
				}
			});
			eventObject.preventDefault();
		});

   $("input[name=deadline]").datepicker({
       'weekStart':1,
       'format': 'dd.mm.yyyy',
       'autoclose':true
   });

    $('.js-changeDate').click(function(){
        var dDate;
        var dFinelDate;
        var dThisDate = new Date();
        switch ($(this).attr('data-time')){
            case 'today':
                   dDate = formatDate(dThisDate);
                   dFinelDate = dThisDate;
                break;
            case 'tomorrow':
                   var dDateTomorrow = new Date(dThisDate.getTime()+1000*60*60*24);
                   dDate = formatDate(dDateTomorrow);
                   dFinelDate = dDateTomorrow;
                break;
            case 'week':
                    var dDateWeek = new Date(dThisDate.getTime()+1000*60*60*168);
                    dDate = formatDate(dDateWeek);
                    dFinelDate = dDateWeek;
                break;
        }
        $("input[name=deadline]").val(dDate);
        $("input[name=deadline]").datepicker("setDate",dFinelDate);
        return false;
    });
});

function addObserverTag(name, id){
    $(".js-observers").append("<li><span>"+name+"&nbsp;<a class='js-icon-remove fa fa-times'></a></span><input name='observers' type='hidden' value='"+id+"'></li>");
}
function addResponsible(email) {
    var $inviteRow = $('.js-invite');
    var email = $inviteRow.val();
    email = email.replace('"','\'');
    $('.js-select-resp').find(':selected').attr('selected',false).end()
        .append('<option selected value="'+email+'">'+email+'</option>');
    $inviteRow.val('').closest('.dropdown-menu').toggle();
    return false;
}