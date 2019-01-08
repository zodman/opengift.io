
jQuery.noConflict();
(function( $ ) {
  $(function() {
    

    $(document).ready(function() {
        // create MultiSelect from select HTML element
        var required = $("#required").kendoMultiSelect().data("kendoMultiSelect");
    
    
        var search = function() {
            var val = $('.js-search').val(), $projects = $('.js-project-item');
            if (val == '') {
                $projects.show();
            } else {
                val = val.toLowerCase();
                $projects.each(function() {
                    var text = $(this).find('.js-project-name').text() + ' ' + $(this).find('.js-project-desc').text();
                    text = text.toLowerCase();
                    if (text.indexOf(val) > -1) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                });
            }
        };
        var searchTimeout = false;
        $('.js-search').keyup(function() {
            if (searchTimeout) clearTimeout(searchTimeout);
            searchTimeout = setTimeout(search, 300);
        });
    
    });

  });
})(jQuery);

