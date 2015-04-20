/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 25.03.13
 * Time: 13:07
 */
var baseConnectorClass = function(data){
    this.socket = false;
    this.url = data.url;
    this.init();
}

baseConnectorClass.prototype = {
    'init': function(){
        var t = this;
        this.socket = io.connect(this.url);

        this.addListener('connect', function () {
            this.open = true;
            this.emit("connect", {
                    sessionid: $.cookie("sessionid")
                }, function(data){
//                    console.log(data);
            });
        });
    },
    'addListener': function(event_name,func){
        var jsonParseFunc = function(data){
            if (data && (typeof data == 'string' || typeof data == 'String')){
                if (data.indexOf('{') > -1 || data.indexOf('[') > -1){
                    data = $.parseJSON(data);
                }
            }

            return func.call(this, data);
        }

        this.socket.on(event_name, jsonParseFunc);
    },
    'once': function(event_name,func){
        this.socket.once(event_name,func);
    },
    'send': function(message, data, callback){
        this.socket.emit(message, data, callback);
    },
    'closeConnection': function(){
        this.socket = null;
        io.disconnect()
    }
};

var baseConnector = {};

$(function(){
    baseConnector = new baseConnectorClass({
        'url':'http://heliard.ru:8082'
//       'url':'http://heliard.dev:8081'
    });
});
(function($){
    $('body').unload(function(e){
        window.unloadPage = true;
        baseConnector.closeConnection();
    });
})(jQuery);