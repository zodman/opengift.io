/**
 * Created by gvammer on 02.07.15.
 */

var Sniffer = {
    'getErrors': function(path, author) {
        PM_AjaxPost(
            '/sniffer/get_errors/',
            {
                'path': path,
                'user': author
            },
            function(data){
                alert(data);
            }
        );
    }
};