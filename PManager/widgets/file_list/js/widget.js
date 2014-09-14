var fileList = new widgetObject({'id':'file_list'});

$.extend(fileList,{
    'currentFolder':0,
    'replaceMode':false,
    'version_of':0,
    '$selectedFile':{},
    '$fileInfoContainer':{},
    'ajax_url':'/files_ajax/',
    'lang':{
        'replaceButtonTitle':'Перенести',
        'replaceModeTitle':'Выберите папку'
    },
    'renderBreadCrumbs': function($currentfolder){
        var str = $currentfolder.text(),
            curFolder = false;
        while (curFolder = $currentfolder.closest('ul').closest('li').find('a').get(0)){
            $currentfolder = $(curFolder);
            str = '<a href="#">' + $currentfolder.text() + '</a> > ' + str;
        }
        return str;
    },
    'disableFileButtons': function (){
        this.$fileButtons.attr('disabled','disabled');
    },
    'enableFileButtons': function (){
        this.$fileButtons.attr('disabled',false);
    },
    'collectSelectedFiles': function(){
        var aFilesId = [];
        this.container.find('input[name=files]:checked').each(function(){
            aFilesId.push($(this).val());
        });
        return aFilesId;
    },
    'enableReplaceMode': function(){
        var $icon = this.$replaceButton.find('i').clone();
        fileList.replaceMode = true;
        this.$replaceButton.text(fileList.lang.replaceModeTitle + ' ').append($icon);
    },
    'disableReplaceMode': function(){
        var $icon = this.$replaceButton.find('i').clone();
        fileList.replaceMode = false;
        this.$replaceButton.text(fileList.lang.replaceButtonTitle + ' ').append($icon);
    },
    'addOrRenameCategory': function(inputData){
        return this.ajaxRequest({
            'action':(inputData.$lnk.data('id')?'renameCategory':'addCategory'),
            'name':inputData.name,
            'section_id':inputData.$lnk.data('id'),
            'parent':inputData.$lnk.data('parent')
        },function(data){
            inputData.$lnk.attr('data-id',data.id);
            if (inputData.$delete_lnk)
                inputData.$delete_lnk.attr('data-dir_id',data.id);
        });
    },
    'showSelectedFileInfo': function(){
        var oDataSet = this.$selectedFile.data();
        for (var key in oDataSet){
            if (oDataSet[key]) {
                var oContainer = $('.js-file_' + key);
                if (oContainer.get(0)) {
                    if (oContainer.is('img')) {
                        var sImgSrc = this.$selectedFile.find('a').attr('href');
                        oContainer.attr('src', oDataSet[key]).closest('a').attr('href', sImgSrc);
                    } else if (key == 'src') {
                        oContainer.attr('href', oDataSet[key]);
                    } else {
                        oContainer.text(oDataSet[key]);
                    }
                    oContainer.closest('.js-infoRow').show();
                }
            }
        }
        if (oDataSet['versionsexist'] == 'Y'){
            var t = this;
            this.getFileVersions(oDataSet['id'], function(files){
                t.constructVersionsList(files);
            });
        }
    },
    'getFileVersions':function(fileId, callback){
        return this.ajaxRequest({
            'file_id':fileId,
            'action':'getVersionsList'
        },callback);
    },
    'constructVersionsList': function(files){
        this.$fileVersionsContainer.empty();
        if (files.length > 0){
            for (var i in files){
                var file = files[i];
                var $fileBlock = $('<li></li>');
                var $fileLink = $('<a></a>').attr('href',file.url).text(file.name);
                $fileBlock.text(' '+file.date_create).prepend($fileLink);
                this.$fileVersionsContainer.append($fileBlock)
            }
            this.$fileVersionsBlock.show();
        }
    },
    'ajaxRequest':function(data,callback){
        return PM_AjaxPost(this.ajax_url,data,callback,'json');
    },
    'getElementOfCurrentFolder': function(){
        if (this.currentFolder){
            return $('.dir_name[data-id='+this.currentFolder+']').closest('li');
        }
        return false;
    },
    'appendFile': function(oFile){
        this.$fileListContainer.append(oFile.getTemplateRow(this.fileTpl));
    },
    'prependFile': function(oFile){
        this.$fileListContainer.prepend(oFile.getTemplateRow(this.fileTpl));
    }
});
fileList.init = function(){
    this.$fileListContainer = $('.js-file-list');
    this.$fileInfoContainer = $('.js-fileInfo');
    this.$fileVersionsContainer = $('.js-fileVersionsList');
    this.$fileVersionsBlock = $('.js-fileVersionsBlock');
    this.$fileButtons = $('.js-fileButtonsGrp button');
    this.$replaceButton = $('.js-replaceFiles');
    this.container = $('.widget.file_list');
    this.directoryLinksSelector = 'span.folder div.dir_name, span.root a';
    this.fileTpl = widget_file_list_file_tpl;
    this.aStartFileList = widget_file_list_arFiles;
    var t = this;

    for (var i in this.aStartFileList){
        this.appendFile(new fileObject(this.aStartFileList[i]));
    }
    $('#create_new_folder').click(function(e){
        var name = 'Новая папка',
            $lnk = $('<div class="dir_name" style="display:inline;margin-left: 22px;"></div>').text(name).attr('contenteditable','true'),
            $list_item = $('<li></li>').append('<div class="tree-row"></div>'),
            $delete_lnk = $('<a href="#" class="del_dir js-delete_dir" ><i title="Удалить папку" class="fa fa-times-circle"></i></a>');

        $list_item.find('.tree-row')
            .append($('<span class="folder"></span>').append($lnk).append($delete_lnk));
        if (fileList.currentFolder){
            $lnk.data('parent',fileList.currentFolder);
            var $curFolderElem = fileList.getElementOfCurrentFolder();
            var $listOfFolders = $curFolderElem.find('ul');
            if (!$listOfFolders.get(0)){
                $listOfFolders = $('<ul></ul>').appendTo($curFolderElem);
            }
        }else{
            $listOfFolders = $('ul.folder-list')
        }
        $listOfFolders.append($list_item);

        var addCategoryLocal = function(e){
            $lnk.attr('contenteditable',false).trigger('blur');
            fileList.addOrRenameCategory({
                'name':$lnk.text(),
                '$lnk':$lnk,
                '$delete_lnk':$delete_lnk
            });
            return false;
        }

        $lnk.focus().selectText().enterPressed(function(e){addCategoryLocal(e)});
        $(document).one('click', function(e){addCategoryLocal(e)});

        e.stopPropagation();
        return false;
    });

    this.container.on('click', fileList.directoryLinksSelector, function(){
        var t = this;
        if (fileList.replaceMode){
            if (!$(t).closest('li').hasClass('active')){
                if (confirm('Вы действительнто хотите перенести эти файлы в папку "' + $(t).text() + '"?')){
                    var aFilesId = fileList.collectSelectedFiles();
                    fileList.ajaxRequest({
                        'action':'replaceFiles',
                        'files':aFilesId,
                        'section_id':$(t).data('id')
                    },function(aReplacedFiles){
                        for (var i in aReplacedFiles){
                            $('input[name=files][value=' + aReplacedFiles[i] + ']')
                                .closest('li').remove();
                        }
                    });
                    fileList.disableReplaceMode();
                }
            }
        }else{
            $('ul.folder-list li').removeClass('active');
            if (!$(t).closest('.root').get(0)){
                $(t).closest('li').addClass('active');
            }
            $('.js-breadcrumb').html(fileList.renderBreadCrumbs($(this)));
            fileList.currentFolder = $(t).data('id');
            fileList.disableFileButtons();
            //TODO: сделать через historyManager
            document.location.hash = $(this).attr('href');
            fileList.ajaxRequest({
                'action':'getFileList',
                'section_id':fileList.currentFolder
            },function(aFiles){
                fileList.$fileListContainer.empty();
                for (var i in aFiles){
                    var obFile = new fileObject(aFiles[i]);
                    fileList.appendFile(obFile);
                }
            });
        }
        //return false;
    })
    .on('mouseup',fileList.directoryLinksSelector,function(e){
        var t = this;
        if ($(t).closest('li').hasClass('active')){
            $(t).setEditable(function(){
                var t = this;
                fileList.addOrRenameCategory({
                    'name':t.text(),
                    '$lnk':t
                });
            });
        }
        e.stopPropagation();
        return false;
    });

    this.$fileListContainer.on('click', 'li.file', function(){
        t.$selectedFile = $(this);
        $(this).addClass('selected').siblings().removeClass('selected');
        t.$fileInfoContainer.find('div.js-infoRow').hide();
        t.showSelectedFileInfo();
    });

    this.$fileListContainer.on('click', 'input[name=files]', function(e){
        if ($('input[name=files]:checked').get(0)){
            fileList.enableFileButtons()
        }else{
            fileList.disableFileButtons();
        }
        e.stopPropagation();
    });

    $('.folder-list').on('click', '.js-delete_dir', function(){
        if (confirm("Вы действительно хотите удалить эту папку?")){
            var oCurLink = this;
            fileList.ajaxRequest({
                'action':'deleteDir',
                'dirId':$(oCurLink).data('dir_id')
            },function(oResult){
                if (oResult.success == 'Y'){
                    $(oCurLink).closest('li').remove();
                }
                $('span.root a').trigger('click'); //перейдем в корень проекта
            });

            return false;
        }
    });

    var $delButton = $('.js-deleteFiles');
    $delButton.click(function(){
        if (confirm("Вы действительно хотите удалить эти файлы?")){
            var aFilesId = fileList.collectSelectedFiles();
            fileList.ajaxRequest({
                'action':'deleteFiles',
                'files':aFilesId
            },function(aDeletedFiles){
                for (var i in aDeletedFiles){
                    $('input[name=files][value=' + aDeletedFiles[i] + ']')
                        .closest('li').remove();
                }
            });
        }
    });

    this.$replaceButton.click(function(){
        if (fileList.replaceMode){
            fileList.disableReplaceMode();
        }else{
            fileList.enableReplaceMode();
        }
    });

    this.container.on('click', '.jsAddNewVersion', function(e){
        t.version_of = $(this).data('file_id');
        t.container.find('input:file').bind('click.silent',function(e){e.stopPropagation();}).trigger('click').unbind('click.silent');

        e.stopPropagation();
        return false;
    });

    $(document).click(function(){
        fileList.version_of = 0;
    });

    this.initFileUpload();

    $('.tmp_script').remove();

    if (document.location.hash) {
        $('[href='+document.location.hash+']').trigger('click');
    }
}

fileList.initFileUpload = function(){
    var errorHandler = function(){
        alert('Не удалось загрузить файл');
    }

    $('.filelist-file-upload').fineUploader({
        debug: false,
        button: $('.file_upload_button').get(0),
        request: {
            endpoint: "/upload/receiver",
            paramsInBody: true
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
            forceConfirm: false
            //params: {foo: "bar"}
        },
        display: {
            completeFileDelete: true,
            fileSizeOnSubmit: true
        }
        ,
        paste: {
            targetElement: $(document)
        }
    })
        .on('error', errorHandler)
        .on('uploadChunk resume', function(event, id, fileName, chunkData) {
            qq.log('on' + event.type + ' -  ID: ' + id + ", FILENAME: " + fileName + ", PARTINDEX: " + chunkData.partIndex + ", STARTBYTE: " + chunkData.startByte + ", ENDBYTE: " + chunkData.endByte + ", PARTCOUNT: " + chunkData.totalParts);
        })
        .on("upload", function(event, id, filename) {
            $(this).fineUploader('setParams', {"section_id": fileList.currentFolder, "version_of": fileList.version_of}, id);
        })
        .on("complete",function(event,id,filename,data){
            if (data.id){
                $(this).fineUploader('setDeleteFileParams', {"file_id": data.id}, id);
                var oFile = new fileObject(data);
                fileList.prependFile(oFile);
            }
        });
}

$(function(){
    fileList.init();
});

var fileObject = function(data){
    if (!data) data = {};
    for (var i in data){
        if (!this[i]){
            this[i] = data[i];
        }
    }

    return this;
}

fileObject.prototype = {
    getTemplateRow:function(tpl){
        var t = this;
        for (var i in t){
            if (t.hasOwnProperty(i) && !(t[i] instanceof Function)){
                var strRegExp = '#'+i+'#';
                tpl = tpl.replace(new RegExp(strRegExp,'mig'),t[i]);
            }
        }
        this.$content = $(tpl);

        for (var key in t){
            if (!(t[key] instanceof Function) && !((t[key] instanceof Object))){
                this.$content.attr('data-'+key, t[key]);
            }
        }
        return this.$content;
    }
}