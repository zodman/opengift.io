(function($){
    $(function(){
        $(document).on('click', '.js-pay', function(){
            $('form[name=robo] .temp-summ').val(
                $(this).closest('div').find('.temp-summ').val()
            );
            document.forms.robo.submit();
            $.fancybox.close();
            return false;
        });
    });
})(jQuery);