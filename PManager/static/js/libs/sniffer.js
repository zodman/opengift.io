/**
 * Created by gvammer on 02.07.15.
 */

var Sniffer = {
    'getErrors': function(path) {
        PM_AjaxPost(
            '/sniffer/get_errors/',
            {
                'path': path
            },
            function(data){
                alert(data);
            }
        )
    }
}