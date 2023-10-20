import flask
import threading
import time
from discord import *
import json
import requests
client=Client(intents=Intents.all())
app=flask.Flask(__name__)

important:dict=json.loads(open('./etc/secrets/important.json','r').read())
timesout=(60*2)+30
messages={}
channels={}

@client.event
async def on_message(message:Message):
    category=message.channel.category
    if category and category.id==1164837537697763441:
        msgs:list=False
        servid=int(message.channel.name)
        if not servid in messages:
            messages.setdefault(servid,[])
            msgs=messages.get(servid)
        else:
            msgs=messages.get(servid)
        msgs.append({'status':'ok','auth':message.author.display_name,'color':str(message.author.color.to_rgb()),'avatar':message.author.display_avatar.url,'content':message.content})
    elif message.channel.id==1112815909048942655 and message.author.bot:
        sid=int(message.author.display_name)
        if not sid in channels:
            category=message.channel.guild.get_channel(1164837537697763441)
            channel=await message.channel.guild.create_text_channel(str(sid),category=category)
            whook:Webhook=await channel.create_webhook(name='cute')
            channels.setdefault(sid,{'channel':channel,'webhook':whook})
        else:
            await channels.get(sid)['channel'].delete()

def isAllowed(payload):
    if not 'key' in payload:
        return False,{'status':'invalid key'}
    elif not payload.get('key') in list(important['apikeys']):
        return False,{'status':'invalid key'}
    elif not 'server-id' in payload:
        return [False,{'status':'invalid server-id'}]
    else:
        return [True,{}]
    

@app.route('/')
def home():
    return 'haiii!! >w<'

@app.route('/message',methods=['POST'])
def sendMessage():
    payload:dict=flask.request.get_json()
    t=isAllowed(payload)
    allowed,resp=t[0],t[1]
    sid=payload.get('server-id')
    if not payload.get('content') or not payload.get('from') or not payload.get('avatar'):
        return {'status':'invalid messagedata'}
    elif not allowed:
        return resp
    else:
        ct=channels.get(sid)
        whook:Webhook=ct.get('webhook')
        print(channels,ct)
        requests.post(important.get('webhook'),{'content':payload.get('content'),'username':payload.get('from'),'avatar_url':payload.get('avatar')})
        async def x():
            whook.send(payload.get('content'),username=payload.get('from'),avatar_url=payload.get('avatar'))
        x()
        


@app.route('/waitformessage',methods=['POST'])
def giveMessage():
    payload:dict=flask.request.get_json()
    t=isAllowed(payload)
    allowed,resp=t[0],t[1]
    if not allowed:
        return resp
    else:
        start=time.time()
        sid:int=int(payload.get('server-id'))
        msgs:list=False
        
        while not msgs:
            #print('awaiting list')
            if sid in messages:
                msgs=messages.get(sid)
        
        if msgs:
            while len(msgs)==0:
                #print('awaiting messages')
                continue
            if (time.time()-start)>timesout:
                return {'status':'TIMEOUT'}
            msg=msgs.pop(0)
            if len(msgs)==0:
                del messages[sid]
            return msg

@client.event
async def on_ready():
    print('running')
    #threading.Thread(target=app.run).start()

client.run(important['token'])


"""
local http=game.HttpService
local resp=http:PostAsync('http://127.0.0.1:5000/waitformessage',http:JSONEncode({key='2',['server-id']=1234567}))
print(http:JSONDecode(resp))
"""
