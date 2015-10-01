
from flask import *
import requests
import client
import math

hackyServer = Flask(__name__)

client.volumeFunction = (lambda x: 200 + (100*(math.sin(x)))) 

@hackyServer.route('/hack')
def hack():
    client.write("play")
    return "Playing!"

if __name__=='__main__':
    hackyServer.run(port=8000, host='0.0.0.0', debug=True)


