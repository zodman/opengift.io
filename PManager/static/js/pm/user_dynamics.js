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
                    toastr.info(
                        "<a href='" + task['url'] + "'>" + task['project__name'] + '/ '
                        + task['name'] + "</a>",
                        'Вы можете вернуться к задаче',
                        {
                            "closeButton": true,
                            "newestOnTop": false,
                            "positionClass": "toast-top-full-width",
                            "preventDuplicates": true,
                            "onclick": null,
                            "timeOut": 0,
                            "extendedTimeOut": 0,
                            "tapToDismiss": false
                        }
                    );
                }
            }, 'json');
        }
    }
}