import flask
import threading
import time
from discord import *
import json
client=Client(intents=Intents.all())
app=flask.Flask(__name__)

important=json.loads(open('./important.json','r').read())
timesout=(60*2)+30
messages={}

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
        msgs.append({'auth':message.author.display_name,'color':str(message.author.color.to_rgb()),'avatar':message.author.guild_avatar,'content':message.content})


@app.route('/')
def home():
    return 'haiii!! >w<'

@app.route('/waitformessage',methods=['POST'])
def giveMessage():
    payload:dict=flask.request.get_json()
    
    if not 'key' in payload:
        return 'invalid key'
    elif not payload.get('key') in important['apiKeys']:
        return 'invalid key'
    
    elif not 'server-id' in payload:
        return 'invalid server-id'
    
    else:
        start=time.time()
        sid:int=int(payload.get('server-id'))
        msgs:list=False
        
        while not msgs:
            print('awaiting list')
            if sid in messages:
                msgs=messages.get(sid)
        
        if msgs:
            while len(msgs)==0:
                print('awaiting messages')
                continue
            if (time.time()-start)>timesout:
                return 'TIMEOUT'
            msg=msgs.pop(0)
            if len(msgs)==0:
                del messages[sid]
            return msg

@client.event
async def on_ready():
    print('running')
    threading.Thread(target=app.run).start()

client.run(important['token'])


"""
local http=game.HttpService
local resp=http:PostAsync('http://127.0.0.1:5000/waitformessage',http:JSONEncode({key='2',['server-id']=1234567}))
print(http:JSONDecode(resp))
"""
