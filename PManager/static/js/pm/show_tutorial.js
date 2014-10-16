function showTutorial () {
    $('body').addClass('first-task-slider');
    $.fancybox.open(
        [
            {href: "/static/images/first.jpg"}
        ],
        {
            helpers : {
                overlay : {
                    css : {
                        'background' : 'rgba(255, 255, 255, 0.6)'
                    }
                }
            },
            openEffect  : 'none',
            closeEffect : 'none',
            nextEffect  : 'none',
            prevEffect  : 'none',
            padding     : 0,
            margin      : [20, 60, 20, 60],
            width:700,
            height:470
        }
    )   
}  