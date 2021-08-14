from botdata import botDetails
bot = botDetails() 



def handleBotPreOffer(data,callback):
    if(bot['botStatus'] == "vacant"):
        callback({
            "usersocketId":data['usernameSocketId'],
            "answer":"ACCEPTED"
            })
    else:callback({"answer":"REJECTED"})
