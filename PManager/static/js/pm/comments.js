/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 24.02.13
 * Time: 21:57
 */
var messageListManager, taskMessageClass, taskMessageViewClass;
var SYSTEM_AVATAR_SRC = '/static/images/avatar_red_eye.png';
(function ($) {
    $(function () {
        taskMessageClass = Backbone.Model.extend({
            'url': function () {
                return '/message/' + this.id + '/';
            },
            'initialize': function () {

            },
            'getFromServer': function (callback) {
                this.fetch({
                    'success': function (model, data) {
                        try {
                            data = $.parseJSON(data);
                            if (typeof(data) == typeof({}) && data.id) {
                                for (var i in data) {
                                    model.set(i, data[i]);
                                }
                            }

                            callback(data);
                        } catch (e) {
                            console.log(e);
                        }
                    },
                    'error': function (model, data) {
                        console.log('Read error: ' + data);
                    }
                });
            },
            'saveToServer': function (callback) {
                var t = this;
                this.save(null, {
                    'success': function (model, data) {
                        try {
                            data = $.parseJSON(data);
                            if (typeof(data) == typeof({}) && data.id) {
                                for (var i in data) {
                                    model.set(i, data[i]);
                                }
                            }

                            callback.call(t, data);
                        } catch (e) {
                            console.log(e);
                        }
                    },
                    'error': function (model, data) {
                        console.log('Save error: ' + data);
                    }
                });
            }
        });

        taskMessageViewClass = Backbone.View.extend({
            editMode: false,
            tagName: 'div',
            tpl: '',
            editModeSaveButtonClass: 'js-saveMessageButton',
            editModeCancelButtonClass: 'js-cancelEditMessageButton',
            textareaClass: 'js-editMessageTextarea',
            messageTextBlockClass: 'js-messageDetailText',
            events: {
                "click .js-removeTaskMessage": 'removeMessage',
                "click .js-editTaskMessage": 'startEdit',
                "click .js-saveMessageButton": 'editConfirm',
                "click .js-cancelEditMessageButton": 'editCancel',
                "click .js-cancel-author-hide": 'cancelAuthorHidden',
                "click .js-cancel-resp-hide": 'cancelRespHidden'
            },
            'initialize': function (data) {
                this.tpl = data.templateHTML;
            },
            'template': function (messageInfo) {
                var arKeys = {
                    'ID': messageInfo.id,
                    'TEXT': htmlspecialchars_decode(messageInfo.text)
                        .replace(new RegExp('&gt;&gt; (.+?)<br />', 'mig'), "<blockquote class='well'>$1</blockquote>") //quotes
                        .replace(new RegExp('&gt;&gt; (.+?)<br>', 'mig'), "<blockquote class='well'>$1</blockquote>") //quotes
                        .replace(new RegExp('&gt;&gt; ', 'mig'), ''), //other quote lines
                    'DATE_CREATE': messageInfo.date,
                    'FILE_LIST': '',
                    'AVATAR_SRC': ''
                }
                arKeys['HIDDEN_LABEL'] = '';
                if (messageInfo.hidden_from_employee) {
                    arKeys['HIDDEN_LABEL'] += 'Скрыто от персонала <a href="#"><i class="fa fa-ban js-cancel-resp-hide"></i></a>';
                }
                arKeys['AVATAR'] = '';
                if (messageInfo.author.avatar) {
                    arKeys['AVATAR'] += '<img src="' + messageInfo.author.avatar + '" width="90px" class="media-object img-thumbnail"/>';
                } else if (messageInfo.author && messageInfo.author.last_name) {
                    arKeys['AVATAR'] += '<div>'
                        + '<code style="background-color: transparent;padding: 0;">'
                        + '<svg width="90" height="90" viewBox="0 0 90 90">'
                        + '<title>' + messageInfo.author.last_name[0] + messageInfo.author.name[0] + '</title>'
                        + '<rect rx="4" ry="4" x="0" y="0" width="90" height="90" style="fill: ' + messageInfo.author.avatar_color + '"/>'
                        + '<g style="font-weight: bold; font-size: 71px;">'
                        + '<defs><mask id="textMask' + messageInfo.id + '">'
                        + '<text style="fill:white;" x="6" y="67">' + messageInfo.author.last_name[0] + messageInfo.author.name[0] + '</text>'
                        + '</mask>'
                        + '<filter id="innerShadow' + messageInfo.id + '" x="-20%" y="-20%" width="140%" height="140%">'
                        + '<feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>'
                        + '<feOffset in="blur" dx="2.5" dy="2.5"/>'
                        + '</filter>'
                        + '</defs>'
                        + '<g mask="url(#textMask' + messageInfo.id + ')">'
                        + '<rect x="0" y="0" width="90" height="90" style="fill:black"/>'
                        + '<text style="fill: ' + messageInfo.author.avatar_color + '; filter: url(#innerShadow' + messageInfo.id + ')" x="6" y="67">'
                        + messageInfo.author.last_name[0] + messageInfo.author.name[0] + '</text></g>'
                        + '</g>'
                        + '</svg>'
                        + '</code>'
                        + '</div>'
                }
                if (messageInfo.hidden) {
                    arKeys['HIDDEN_LABEL'] += 'Личное ';
                }
                if (messageInfo.hidden_from_clients) {
                    arKeys['HIDDEN_LABEL'] += 'Скрыто от клиентов <a href="#"><i class="fa fa-ban js-cancel-author-hide"></i></a>';
                }
                if (messageInfo.userTo.id) {
                    arKeys['USER_TO_NAME'] = ' для <b>' + messageInfo.userTo.name + '</b>';
                } else {
                    arKeys['USER_TO_NAME'] = '';
                }
                if (messageInfo.author.id) {
                    arKeys['AUTHOR_NAME'] = messageInfo.author.name;
                    arKeys['AUTHOR_LAST_NAME'] = messageInfo.author.last_name;
                    arKeys['AUTHOR_USERNAME'] = messageInfo.author.username;
                    arKeys['AUTHOR_ID'] = messageInfo.author.id;
                    arKeys['AUTHOR_URL'] = '/user_detail/?id=' + messageInfo.author.id;
                } else {
                    arKeys['AUTHOR_NAME'] = 'сообщение';
                    arKeys['AUTHOR_LAST_NAME'] = 'Системное';
                    arKeys['AUTHOR_USERNAME'] = '';
                }

                arKeys['TASK_LINE'] = '';
                arKeys['PROJECT_LINE'] = '';
                arKeys['CONFIRMATION'] = '';
                if (messageInfo.confirmation) arKeys['CONFIRMATION'] = messageInfo.confirmation;

                if (messageInfo.task && messageInfo.task.name) {
                    if (messageInfo.project && messageInfo.project.name) {
                        arKeys['PROJECT_LINE'] = '<a href="'+messageInfo.project.url+'" class="message-info-title">'+messageInfo.project.name+'</a>&nbsp;/&nbsp;';
                    }

                    if (messageInfo.task.parent && messageInfo.task.parent.id) {
                        var p = messageInfo.task.parent;
                        arKeys['TASK_LINE'] = arKeys['TASK_LINE'] + '/ <a href="' + p.url + '" class="message-desc-text">' + p.name + '</a> ';
                    }
                    arKeys['TASK_LINE'] = arKeys['TASK_LINE'] + '/ <a href="' + messageInfo.task.url + '" class="message-desc-text"><strong>' +
                        messageInfo.task.name + '</strong></a>';
                }


                if (messageInfo.system) {
                    arKeys.AVATAR_SRC = SYSTEM_AVATAR_SRC;
                } else if (messageInfo.avatar) {
                    arKeys.AVATAR_SRC = messageInfo.avatar;
                }

                if (messageInfo.files) {
                }

                if (!this.tpl) {
                    return '';
                }

                var t = this;
                var htmlTemplate = this.tpl;

                var k, strKey;
                for (k in arKeys) {
                    strKey = '#' + k + '#';
                    if (htmlTemplate.indexOf(strKey) > -1) {
                        htmlTemplate = htmlTemplate.replace(new RegExp(strKey, 'mig'), arKeys[k]);
                    }
                }
                return htmlTemplate;
            },
            'render': function (params) {
                if (!params)
                    params = {};

                if (this.model.get('invisible')) {
                    this.$el.hide();
                } else {
                    this.$el.show();
                }
                this.$el.html(this.template(this.model.toJSON())).addClass('task-message');
                var $messageTextBlock = this.$el.find('.js-taskMessageText');

                if (!this.model.get('text') && !this.model.get('files')) {
                    return false;
                }
                if (!this.model.get('author').id) {
                    this.$('.js-author-block').hide();
                }
//                if (!this.model.get('avatar') && this.model.get('author').id){
//                    this.$('.js-avatarBlock').hide();
//                    $messageTextBlock.removeClass('Img');
//                }
                var aFiles = this.model.get('files');

                if (aFiles) {
                    var aPictures = [], aOtherFiles = [];
                    for (var i in aFiles) {
                        var file = aFiles[i];
                        var rowTemplate;

                        if (file.is_picture) {
                            rowTemplate = '<a class="fnc" href="#URL#"><img class="img-polaroid" src="#URL_SMALL#" /></a>';
                        } else {
                            rowTemplate = '<a #ADD# href="#VIEW_URL#">#NAME#</a>&nbsp;<a href="#URL#" class="icon-download-alt icon-#EXTENSION#"></a>';
                        }
                        if (file.viewUrl) {
                            rowTemplate = rowTemplate.replace(/\#VIEW_URL\#/mgi, file.viewUrl);
                            rowTemplate = rowTemplate.replace(/\#ADD\#/mgi, 'class="fnc_ajax"');
                        } else {
                            rowTemplate = rowTemplate.replace(/\#VIEW_URL\#/mgi, file.url);
                            rowTemplate = rowTemplate.replace(/\#ADD\#/mgi, '');
                        }
                        rowTemplate = rowTemplate.replace(/\#URL\#/mgi, file.url);
                        rowTemplate = rowTemplate.replace(/\#NAME\#/mgi, file.name);
                        rowTemplate = rowTemplate.replace(/\#EXTENSION\#/mgi, file.type);
                        rowTemplate = rowTemplate.replace(/\#URL_SMALL\#/mgi, file.thumb100pxUrl);

                        if (file.is_picture) {
                            aPictures.push($(rowTemplate));
                        } else {
                            aOtherFiles.push($(rowTemplate))
                        }
                    }

                    var $pictures = $('<div></div>'),
                        $otherFiles = $('<div></div>');

                    var exist;
                    var $filesListblock = $messageTextBlock.parent().find('.js-filesList').eq(0);
                    if (aPictures) {
                        exist = false;
                        for (i in aPictures) {
                            exist = true;
                            if (aPictures.hasOwnProperty(i))
                                $pictures.append(aPictures[i]);
                        }
                        if (exist)
                            $filesListblock.append($pictures);
                    }

                    if (aOtherFiles) {
                        exist = false;
                        for (i in aOtherFiles) {
                            exist = true;
                            if (aOtherFiles.hasOwnProperty(i))
                                $otherFiles.append(aOtherFiles[i]);
                        }
                        if (exist)
                            $filesListblock.append($otherFiles);
                    }
                }

                this.$el.addClass('row-fluid show-grid js-taskMessage').data('id', this.model.id);

                if (this.model.get('canEdit')) {
                    this.$('.js-editTaskMessage').show();
                }
                if (this.model.get('canDelete')) {
                    this.$('.js-removeTaskMessage').show();
                }
                if (this.model.get('noveltyMark')) {
                    this.$el.addClass('new-message');
                }
//                this.$('.fnc').fancybox();
                this.$('.fnc_ajax').fancybox({
                    'type': 'ajax'
                });
                this.delegateEvents();

                return this;
            },
            'removeMessage': function () {
                var t = this,
                    model = this.model;
                if (confirm("Вы действительно хотите удалить сообщение?")) {
                    model.destroy({
                        'success': function (model, response) {
                            console.log(response);
                            if (response == 'Message has been deleted')
                                t.remove();
                        }
                    });
                }

                return false;
            },
            'startEdit': function () {
                var t = this;
                if (!t.editMode) {
                    t.editMode = true;

                    var $textarea = $('<textarea></textarea>').addClass('form-control ' + this.textareaClass);
                    var $messageTextBlock = this.$('.js-messageDetailText');
                    var $saveButton = $('<button></button>').text('Сохранить').addClass('btn btn-success')
                        .addClass(this.editModeSaveButtonClass);
                    var $cancelButton = $('<button></button>').text('Отмена').addClass('btn btn-danger')
                        .addClass(this.editModeCancelButtonClass);
                    var tags = new RegExp('\<[^>]+\>', 'mig');
                    $messageTextBlock.replaceWith(
                        $textarea.val(
                            $messageTextBlock.html()
                                .replace('<br>', "\r\n")
                                .replace('<br />', "\r\n")
                                .replace('<br/>', "\r\n")
                                .replace(tags, '')
                        )
                    );
                    this.$('.js-quote').hide();
                    this.$('.js-reply').hide();
                    this.$('.js-taskMessageText').append($saveButton, $cancelButton)
                }

                return false;
            },
            'editCancel': function () {
                this.editMode = false;
                this.$('.js-quote').show();
                this.$('.js-reply').show();
                this.render();
            },
            'editConfirm': function () {
                this.editMode = false;
                var $textarea = this.$('.' + this.textareaClass);
                this.$('.js-quote').show();
                this.$('.js-reply').show();
                var newText = $textarea.val().replace("\r\n", '<br />');
                var view = this;

                this.model.set('text', newText);
                this.model.saveToServer(function (data) {
                    view.render();
                });
            },
            'cancelAuthorHidden': function () {
                var view = this;
                this.model.set('hidden_from_clients', false);
                this.model.saveToServer(function (data) {
                    view.render();
                });
                return false;
            },
            'cancelRespHidden': function () {
                var view = this;
                this.model.set('hidden_from_employee', false);
                this.model.saveToServer(function (data) {
                    view.render();
                });
                return false;
            }
        });

        messageListManager = function ($element, taskId, arMessageTpl) {
            this.taskId = taskId;
            this.$commentsContainer = $element;
            if (arMessageTpl)
                this.messageTemplates = arMessageTpl;
            else
                this.messageTemplates = {'template': ''};
            this.showLast = 7;
            this.callbacks = [];
            this.addCallbacks = [];
            this.init();
        }

        messageListManager.prototype = {
            init: function () {
                var t = this;

                var collectionClass = Backbone.Collection.extend({
                    model: taskMessageClass
                });
                this.messageList = new collectionClass();
                this.messageList.url = function () {
                    return '/message';
                };

                this.messageList.on("add", function (message) {
                    if (t.taskId)
                        message.set('task', t.taskId);

                    var code = (message.get('code') + '').toLowerCase();
                    var codeTpl = t.messageTemplates[code];
                    if (!message.view) {
                        message.view = new taskMessageViewClass({
                            'model': message,
                            'templateHTML': codeTpl ?
                                codeTpl : t.messageTemplates['template']
                        });
                    }
                    message.view.render();

                    for (var i in t.addCallbacks) {
                        t.addCallbacks[i].call(message);
                    }

                    var func;
                    if (t.reversed) {
                        func = 'prepend';
                        if (message.get('userTo') && message.get('userTo')['id'] == document.mainController.userId) {
                            $.bootstrapGrowl(
                                message.view.$el.children().find('img, .js-quote, .js-answer').remove().end().html(),
                                {
                                    'delay': 0
                                }
                            );
                        }
                        knock();    
                    } else {
                        func = 'append';
                    }
                    if (message.get('userTo') && message.get('userTo')['id'] == document.mainController.userId) {
                        message.view.$el.addClass('for_current_user');
                    }

                    /* Mininimize system messages */

                    var subCode = message.get('code');
                    if (subCode == null) {
                        subCode = 'MESSAGES';
                    }

                    var $chatWindow = $('#chatWindow');

                    if (!t.$commentsContainer.find('.SUBCONTAINER:last').hasClass(subCode) || message.view.$el.hasClass('new-message')) {
                        if ((t.$commentsContainer.find('.SUBCONTAINER:last').find('.task-message').length > 1) && (!message.view.$el.hasClass('new-message'))) {
                            var containerMessages = t.$commentsContainer.find('.SUBCONTAINER:last');
                            var colMessages = (containerMessages.find('.task-message')).length - 1;
                            var msgs = containerMessages.find('.task-message');
                            var btnMinimize = $('<div class="toggle-messages minimize"><span class="btn btn-xs"><span class="fa fa-caret-down"></span>&nbsp;&nbsp;Еще ' + colMessages +'...</span></div>');
                            btnMinimize.click(function(){
                                msgs.show();
                                $(this).remove();
                            });
                            containerMessages.append(btnMinimize);
                        }
                        var containerMessages = $('<div class="' + subCode +' SUBCONTAINER"></div>');
                        if (message.view.$el.hasClass('new-message') && $('#chatWindow').length > 0) {
                            t.$commentsContainer.prepend(containerMessages);
                        } else {
                            t.$commentsContainer.append(containerMessages);
                        }
                    }

                    var codeElementLast = t.$commentsContainer.find('.SUBCONTAINER:last');
                    var codeElementFirst = t.$commentsContainer.find('.SUBCONTAINER:first');
                    codeElementLast.find('.last').removeClass('last');                
                    if (message.view.$el.hasClass('new-message') && $('#chatWindow').length > 0) {
                        codeElementFirst[func](message.view.$el);
                    } else {
                        codeElementLast[func](message.view.$el);
                    }

                    if (!message.view.$el.hasClass('new-message')) {
                        var sel = ":last";
                        if($chatWindow.length > 0){
                            sel = ":first"
                        }
                        codeElementLast.find('.task-message' + sel).addClass('last');
                        codeElementLast.find('.task-message:not(.last)').hide();
                    }

                    /* /Mininimize system messages */

                });

                this.messageList.on("remove", function (message) {
                    message.view.$el.remove();
                });

                setTimeout(function () {
                    for (var i in t.callbacks) {
                        t.callbacks[i].call(t);
                    }
                }, 0);
            },
            addMessages: function (aMessagesData) {
                var i, l = aMessagesData.length;
                if (this.showLast > 0) { //TODO: все, что в этом услови, должно быть во вьюхах
                    for (var k in aMessagesData) {
                        i++;
                        var mes = aMessagesData[k];

                        if (i < l - this.showLast) {
                            mes['invisible'] = true;
                        }

                        if (i == l - this.showLast && l > this.showLast) {
                            $('.js-show-all').show();
                        }

                        this.messageList.add([mes]);
                    }
                    $('.js-show-all').click(function () {
                        $('.js-taskMessage').show();
                        $(this).remove();
                    });
                } else {
                    this.messageList.add(aMessagesData);
                }
            },

            ready: function (callback) {
                this.callbacks.push(callback);
            },

            onAddMessage: function (callback) {
                this.addCallbacks.push(callback);
            },

            clean: function () {
                this.messageList.remove(this.messageList.models);
            }
        }
    });
})(jQuery);