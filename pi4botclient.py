import asyncio
import attr
import socketio

sio = socketio.AsyncClient()
botName = 'deathBot'
id = '12345678'
password = "testPassword"
location = "Berlin"
online = True
attributes = {
    "weapon" :"laser",
    "speed" : 10,
    "armour": 10,
    "seats":3
}


@sio.event
async def connect():
    print('connected to server')
    await sio.emit('registerBot',{
        "name":botName,
        "image":"image",
        "id":id,
        "password":password,
        "location":location,
        "online":online,
        "attributes":attributes
        })


@sio.event
async def disconnect():
    print('disconnected from server')


@sio.event
def hello(a, b, c):
    print(a, b, c)


async def start_server():
    await sio.connect('http://localhost:8080', auth={'token': 'my-token'})
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(start_server())