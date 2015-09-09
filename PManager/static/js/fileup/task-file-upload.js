function taskFileUpload() {
    var errorHandler = function(){
        alert('Не удалось загрузить файл');
    };

    $('.task-file-upload').fineUploader({
        debug: false,
        button: $('.file_upload_button').get(0),
        request: {
            endpoint: "/upload/receiver",
            paramsInBody: true,
            customHeaders: {
                "X-CSRFToken": $.cookie('csrftoken')
            }
        },
        text: {
            cancelButton:'Отмена',
            retryButton:'Повторить',
            deleteButton:'Удалить'
        },
        chunking: {
            enabled: true
        },
        resume: {
            enabled: true
        },
        retry: {
            enableAuto: true,
            showButton: true
        },
        deleteFile: {
            enabled: true,
            endpoint: '/upload/receiver',
            forceConfirm: false,
            customHeaders: {
                "X-CSRFToken": $.cookie('csrftoken')
            }
        },
        display: {
            completeFileDelete: false,
            fileSizeOnSubmit: true
        }
    })
    .on('error', errorHandler)
    .on('uploadChunk resume', function(event, id, fileName, chunkData) {
        qq.log('on' + event.type + ' -  ID: ' + id + ", FILENAME: " + fileName + ", PARTINDEX: " + chunkData.partIndex + ", STARTBYTE: " + chunkData.startByte + ", ENDBYTE: " + chunkData.endByte + ", PARTCOUNT: " + chunkData.totalParts);
    })
    .on("upload", function(event, id, fileame) {
        $(this).fineUploader('setParams', {"hey": "ho"}, id);
    })
    .on("complete",function(event,id,filename,data){
        if (data.id){
            $('<input type="hidden" name="files" />').val(data.id).appendTo($('.task-file-upload'));
            $(this).fineUploader('setDeleteFileParams', {"file_id": data.id}, id);
        }
    });
}