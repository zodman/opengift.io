/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 25.03.13
 * Time: 13:07
 */
var FancyWebSocket = function(url, obj){
  var conn = new WebSocket(url);

  var callbacks = {};

  this.bind = function(event_name, callback){
    callbacks[event_name] = callbacks[event_name] || [];
    callbacks[event_name].push(callback);
    return this;// chainable
  };

  this.send = function(event_name, event_data){
    var payload = JSON.stringify({event:event_name, data: event_data});
    conn.send( payload ); // <= send JSON data to socket server
    return this;
  };

  // dispatch to the right handlers
  conn.onmessage = function(evt){
    var json = JSON.parse(evt.data);
    dispatch(json.event, json.data);
  };

  conn.onclose = function(){dispatch('close',null)};
  conn.onopen = function(){dispatch('open',null)};

  var dispatch = function(event_name, message){
    var chain = callbacks[event_name];
    if(typeof chain == 'undefined') return; // no callbacks for this event
    for(var i = 0; i < chain.length; i++){
      chain[i].call( obj, message )
    }
  }
};

var baseConnectorClass = function(data){
    this.socket = false;
    this.url = data.url;
    this.events = {};
    this.init();
};

baseConnectorClass.prototype = {
    'init': function() {
        var t = this;
        var prot = (document.location.protocol == 'https:' ? 'wss://' : 'ws://');
        this.socket = new FancyWebSocket((prot + this.url), this);

        this.addListener('connect', function () {
            this.open = true;
            this.send('connect', {
                sessionid: $.cookie("sessionid")
            });
            if(window.timerID){
               window.clearInterval(window.timerID);
               window.timerID=0;
            }
        });

        this.addListener('close', function() {
            if(!window.timerID) {
              window.timerID = setInterval(function(){t.init()}, 5000);
            }
        })
    },
    'addListener': function(event_name, func){
        this.socket.bind(event_name, func);
    },
    'send': function(message, data, func){
        this.socket.send(message, data);
        if (func) func();
    },
    'closeConnection': function(){
        this.socket.onclose = function () {};
        this.socket.close();
    }
};

var baseConnector = {};

$(function(){
    baseConnector = new baseConnectorClass({
        'url': (window.heliardSettings['SOCKET_SERVER_ADDRESS'] + ':8081')
    });
});
(function($){
    window.onbeforeunload = function(e) {
        window.unloadPage = true;
        baseConnector.closeConnection();
    }
})(jQuery);
