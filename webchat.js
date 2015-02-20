function WebChat(socket_url, client_id, callback_onmessage) {
    var ws = new WebSocket("ws://"+ socket_url +"/webchat/" + client_id);
    var callback_onmessage = callback_onmessage;

    this.sendMessage = function(message_payload) {
        ws.send(JSON.stringify(message_payload));
    }

    this.close = function() {
        ws.close();
    }

    ws.onmessage = function(e) {
        callback_onmessage( JSON.parse(e.data) );
    }
}