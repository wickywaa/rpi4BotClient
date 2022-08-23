import asyncio
import attr
import socketio

sio = socketio.AsyncClient()
id = '12345678'
password = "testPassword"
location = "Berlin"
online = True



@sio.event
async def connect():
    print('connected to server')
    await sio.emit('registerBot',{
        "id":id,
        "password":password,
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