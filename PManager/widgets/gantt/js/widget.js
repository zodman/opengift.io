$(function () {
    var gantt = new GANTT(
        {
            'container': $('.gantt-overflow')
        },
        GANTT_TASKS,
        MILESTONES
    );
    bindDragNDrop(function(id, respId){ return gantt.assignEventTo(id, respId); });
});