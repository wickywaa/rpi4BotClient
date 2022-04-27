from botdata import botDetails
from picamera.array import PiRGBArray
from picamera.encoders import PiVideoFrame
from picamera import PiCamera
import json
import time
import numpy as np
import asyncio
import io
from aiortc import (RTCIceCandidate,RTCPeerConnection,RTCSessionDescription,VideoStreamTrack)
import cv2
from aiortc.contrib.media import MediaPlayer, MediaRelay

bot = botDetails()
peerConnection = 'hllo'
myStream  ='' 
localStream =''
player =''


async def handleBotPreOffer(data,callback):
    await  createPeerConnection()
    if(bot['botStatus'] == "vacant"):
     await   callback({
            "usersocketId":data['usernameSocketId'],
            "answer":"ACCEPTED"
            })

    else:await  callback({"answer":"REJECTED"})






async def handleBotWebRTCOffer(data,callback):
    global peerConnection
    offer =(data['offer'])
    await peerConnection.setRemoteDescription(RTCSessionDescription(sdp=offer['sdp'],type=offer['type']))
    answer = await peerConnection.createAnswer()
    await peerConnection.setLocalDescription(answer)

    print('this is the data sending to the function',data)
    answerData = {
        "answer":{
        "type":answer.type,
        "sdp":answer.sdp
        },
        "userSocketId":data['userSocket'],
        "botCallingSocketId":data['botCallingSocketId']
        
        
        }

        
    await callback(json.dumps(answerData))

async def createPeerConnection():
    global peerConnection
    peerConnection= RTCPeerConnection()
    peerConnection.addTransceiver('video',direction='sendrecv')
    webcam  = MediaPlayer("/dev/video0")
    print(" here is the webcam stee",webcam)
    peerConnection.addTrack(webcam.video)
    print("attributes for pc",dir(peerConnection)
    print("tts for ice", dir(peerConnection))



    @peerConnection.on('connectionstatechange')
    async def on_connectionstatechange():
        print('Connection state is %s' % peerConnection.connectionState)
        if peerConnection.connectionState == 'failed' :
           await peerConnection.close()

    @peerConnection.on("iceconectionstatechange")
    async def on_IceGatheringstate():
        print('Ice connection state', peerConnection.IceConnectionState)
    

 




async def handleBotWebRTCCandidate(data):

    class candidate:
        candidate = data['candidate'],
        sdpMid =data['sdpMid'],
        sdpMLineIndex =data['sdpMLineIndex']

    print('print',peerConnection.connectionState)


async def getLocalStream():
    myStream = io.BytesIO()
    with PiCamera() as camera:
        while True:
            camera.capture(myStream,format='jpeg',use_video_port=True)
            frame = np.fromstring(myStream.getvalue(),dtype=np.uint8)
            myStream.seek(0)
            frame = cv2.imdecode(frame,1)
            player =   createLocalTracks(frame)
            print('this is the frame',(frame))
            print('here is the player 2')
            return player 


def createLocalTracks(source):
    global relay,webcam
    player = MediaPlayer(source,options={'video_size':'640X480'})
    return player 
    
    






