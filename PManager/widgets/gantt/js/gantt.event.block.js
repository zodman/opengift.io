/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 27.07.14
 * Time: 17:23
 */
var EventBlock = function (event) {
    var $eventBlock = $('.gantt-event[data-id='+event.id+']');
    if ($eventBlock.get(0)) {
        this.$elem = $eventBlock;
    } else {
        this.$elem = $('<div></div>', {
                'class': 'gantt-event'
            }
        )
        .append('<i class="fa fa-ellipsis-v js-drag-task" style="height: 22px;"></i>')
        .append('<a href="' + event.url + '">' + event.title + '</a>');
    }

    this.$elem.attr('data-id', event.id);
    if (event.planTime)
        this.$elem.append(
            '<div class="gantt-event-plantime">Примерное время: <span>' + event.planTime + ' ч.</span></div>'
        );
    if (event.closed) {
        this.$elem.addClass('closed');
    }
    if (event.status == 'ready') {
        this.$elem.addClass('ready');
    }
}
EventBlock.prototype = {

}