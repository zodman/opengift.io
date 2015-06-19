# -*- coding:utf-8 -*-
__author__ = 'Rayleigh'
import pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_ENABLED = True
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/libs/jquery.min.js',
            'js/libs/fancybox.js',
            'js/libs/jquery.history.min.js',
            'js/libs/jquery.form.js',
            'js/libs/html5shiv.js',
            'js/libs/howler.min.js',
            'js/libs/timepicker/jquery.datetimepicker.js',
            'js/libs/socket.io.js',
            'js/libs/backbone.js',
            'js/libs/backbone.iobind.js',
            'js/libs/backbone.iosync.js',
            'js/libs/boostrap.growl.js',
            'js/libs/jquery.createAvatar.js',
            'js/libs/jquery.event.outside.min.js',
            'js/libs/apng-canvas.js',
            'js/libs/jquery.imgareaselect.min.js',
            'js/libs/jquery.cookie.js',
            'js/bootstrap/bootstrap.min.js',
            'js/bootstrap/typehead.js',
            'js/bootstrap/bootstrap-combobox.js',
            'js/pm/script.js',
            'js/pm/main.js',
            'js/pm/panel.js',
            'js/pm/tasks.js',
            'js/pm/files.js',
            'js/pm/beep.js',
            'js/pm/hint.js',
            'js/pm/user_dynamics.js',
            'js/pm/sock_connector.js',
            'js/pm/user-notice.js',
            'js/pm/current_timer.js',
            'js/pm/drowCanvas.js',
        ),
        'output_filename': 'js_compressed/base.js',
    },
    'fileup': {
        'source_filenames': (
            'js/fileup/header.js',
            'js/fileup/util.js',
            'js/fileup/promise.js',
            'js/fileup/button.js',
            'js/fileup/ajax.requester.js',
            'js/fileup/deletefile.ajax.requester.js',
            'js/fileup/handler.base.js',
            'js/fileup/window.receive.message.js',
            'js/fileup/handler.form.js',
            'js/fileup/handler.xhr.js',
            'js/fileup/paste.js',
            'js/fileup/uploader.basic.js',
            'js/fileup/dnd.js',
            'js/fileup/uploader.js',
            'js/fileup/jquery-plugin.js',
        ),
        'output_filename': 'js_compressed/file_up.js'
    },
    'gantt': {
        'source_filenames': (
            'gantt/js/dragndrop.js',
            'gantt/js/gantt.event.block.js',
            'gantt/js/gantt.js',
            'gantt/js/gantt.thumbnail.js',
            'gantt/js/widget.js',
        ),
        'output_filename': 'js_compressed/gantt.js'
    },
    'kanban': {
        'source_filenames': (
            'kanban/js/kanban.js',
        ),
        'output_filename': 'js_compressed/kanban.js'
    },
    'user_detail': {
        'source_filenames': (
            'user_detail/js/widget.js',
            'js/jquery.bxslider.min.js',
            'js/libs/raphael-min.js',
            'js/libs/charts.js',
            'js/libs/d3.js'
        ),
        'output_filename': 'js_compressed/user_detail.js'
    }
}

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/reset.css',
            'css/external/imgareaselect-animated.css',
            'css/external/fancybox.css',
            'css/external/carousel.css',
            'css/external/bootstrap-responsive.css',
            'css/external/bootstrap3.min.css',
            'css/external/linecons/linecons.css',
            'css/styles.css',
            'css/project.edit.css',
            'css/add.css',
            'css/panel.css',
            'css/drowCanvas.css',
            'js/libs/timepicker/jquery.datetimepicker.css',
            'css/external/font-awesome.css',
        ),
        'output_filename': 'css_compressed/base.css',
    },
}