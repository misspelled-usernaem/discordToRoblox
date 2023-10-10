import flask
import requests
from discord import *
client=Client(Intents=Intents.all())
app=flask.Flask(__name__)

@app.route('/')
def home():
    return 'haiii!! >w<'
@app.route('/waitformessage')
def giveMessage():

    return

