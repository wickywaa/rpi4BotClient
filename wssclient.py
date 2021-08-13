import socketio, json
from botdata import botDetails

sio= socketio.Client()



sio.connect('https://db4fec263fa1.ngrok.io')


botdetails = botDetails()


newBotdata = {
    **botdetails,
    "botsurname":"guess"
    }


@sio.event
def connect():
    print('connected to warbotz')


sio.emit('register-new-bot',newBotdata)


@sio.on('bot-pre-offer')
def onPreOffer(data):
    print('got the pre offer', data)
