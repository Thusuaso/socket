from flask import Flask
from flask_socketio import SocketIO,emit,send
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,logger=True, engineio_logger=True,cors_allowed_origins="*")

@socketio.on('connect')
def connect():
    emit('başarıyla bağlandı')
    
#Socket IO Customer#
@socketio.on('production_update_emit')
def production_update_emit():
    emit('production_update_on',broadcast=True)

@socketio.on('cards_update_emit')
def cards_update_emit():
    emit('cards_update_on',broadcast=True)
    
@socketio.on('offers_updated_emit')
def offers_updated_emit(payload):
    emit('offers_updated_on',payload,broadcast=True)

@socketio.on('offers_deleted_emit')
def offers_deleted_emit(offerId):
    emit('offers_deleted_on',offerId,broadcast=True)

@socketio.on('supplier_list_emit')
def supplier_list_emit():
    emit('supplier_list_on',broadcast=True)

@socketio.on('customer_list_emit')
def customer_list_emit():
    emit('customer_list_on',broadcast=True)


if __name__ == '__main__':
    socketio.run(app,port=5001)