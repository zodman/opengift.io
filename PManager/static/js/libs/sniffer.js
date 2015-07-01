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
                $('<div class="modal fade"><div id="previewModal" class="modal fade wiki-modal in" style="display: block;" aria-hidden="false"><div class="modal-dialog"><div class="modal-content ui-resizable"></div></div></div>')
				.find('.modal-content').append('<h3>'+path+'</h3>')
				.append(data).end().modal('show');
            }
        );
        return false;
    }
};