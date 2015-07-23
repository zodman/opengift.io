/**
 * Created by rayleigh on 23.07.15.
 */
;$(document).ready(function(){
    $(".article-text").markdown({
        language:'ru',
        onPreview: function(e) {
            var markdown = $(e.parseContent());
            markdown.find('code').wrap('<pre>');
            // this is a hack - to html method to return actual string,
            // if not this - will be returned first element html only.
            return $('<div>').append(markdown).html();
        }
    });
});