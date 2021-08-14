import socketio, json
from botdata import botDetails
from webRTCHandler import handleBotPreOffer
sio= socketio.Client()



sio.connect('https://f4e6d6297bde.ngrok.io')


botdetails = botDetails()


newBotdata = {
    **botdetails,
    "botsurname":"guess"
    }




@sio.event
def connect():
    print('connected to warbotz')


sio.emit('register-new-bot',newBotdata)


def preOfferAnswer(data):
    sio.emit('bot-pre-offer-answer',data)


@sio.on('bot-pre-offer')
def onPreOffer(data):
    print('got the pre offer', data)
    handleBotPreOffer(data,preOfferAnswer)



    
