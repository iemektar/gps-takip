"""from channels.channel import Group
import json

def ws_connect(message):
    Group('test').add(message.reply_channel)
    message.reply_channel.send({"accept":True,"text":"İşlem Başarılı."})

def ws_disconnect(message):
    Group('test').discard(message.reply_channel)
    Group('test').send(
        {
            "close": True,
        }
    )"""