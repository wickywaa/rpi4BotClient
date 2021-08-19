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
peerConnection = RTCPeerConnection()
myStream  ='' 
localStream =''



async def handleBotPreOffer(data,callback):
    if(bot['botStatus'] == "vacant"):
     await   callback({
            "usersocketId":data['usernameSocketId'],
            "answer":"ACCEPTED"
            })
    else:await  callback({"answer":"REJECTED"})






async def handleBotWebRTCOffer(data,callback):
    print(data)
    offer =(data['offer'])
    await peerConnection.setRemoteDescription(RTCSessionDescription(sdp=offer['sdp'],type=offer['type']))
    answer = await peerConnection.createAnswer()
    await peerConnection.setLocalDescription(answer)
    print('this is the data sending to the function')
    answerData = {
        "answer":{
        "type":answer.type,
        "sdp":answer.sdp
        },
        "userSocketId":data
        
        
        }

    await callback(json.dumps(answerData))

async def createPeerConnection():

    await getLocalStream()
    video  = await createLocalTracks(myStream)
    print (video)
    print(peerConnection)
    


async def getLocalStream():
    myStream = io.BytesIO()
    with PiCamera() as camera:
        while True:
            camera.capture(myStream,format='jpeg',use_video_port=True)
            frame = np.fromstring(myStream.getvalue(),dtype=np.uint8)
            myStream.seek(0)
            frame = cv2.imdecode(frame,1)
            createLocalTracks(myStream)
            print(frame)
            return frame


def createLocalTracks(source):
    global relay,webcam
    player = MediaPlayer(source,options={'video_size':'640X480'})
    peerConnection = RTCPeerConnection()
    peerConnection.addTrack(player.video)
    print(player)
    
    






