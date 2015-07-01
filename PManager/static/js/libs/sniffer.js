/**
 * Created by gvammer on 02.07.15.
 */

var Sniffer = {
    'getErrors': function(path, author, project) {
        PM_AjaxPost(
            '/sniffer/get_errors/',
            {
                'path': path,
                'user': author,
                'project': project
            },
            function(data){
                alert(data);
            }
        );
        return false;
    }
};