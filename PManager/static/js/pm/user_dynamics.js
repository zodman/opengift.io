/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 07.05.14
 * Time: 18:24
 */
var userDynamics = {
    'getOpenTask': function () {
        if (taskManager) {
            taskManager.taskAjaxRequest({
                'action': 'getUserLastOpenTask'
            }, function (task) {
                if (task && task['name']) {
                    //$.bootstrapGrowl(
                    //    "Вы можете вернуться к задаче <a href='" + task['url'] + "'>"
                    //        + task['project__name'] + '/ ' + task['name'] + "</a>",
                    //    {
                    //        'delay': 0,
                    //        'width': 'auto'
                    //    }
                    //);
                    toastr.success(
                        "<a href='" + task['url'] + "'>" + task['project__name'] + '/ '
                        + task['name'] + "</a>" + "<br /><br /><button type='button' class='btn clear'>OK</button>",
                        'Вы можете вернуться к задаче',
                        {
                            "closeButton": true,
                            "debug": false,
                            "newestOnTop": false,
                            "progressBar": false,
                            "positionClass": "toast-top-full-width",
                            "preventDuplicates": false,
                            "onclick": null,
                            "showDuration": "300",
                            "hideDuration": "1000",
                            "timeOut": 0,
                            "extendedTimeOut": 0,
                            "showEasing": "swing",
                            "hideEasing": "linear",
                            "showMethod": "fadeIn",
                            "hideMethod": "fadeOut",
                            "tapToDismiss": false
                        }
                    );
                }
            }, 'json');
        }
    }
}