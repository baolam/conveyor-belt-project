import subprocess

def server_service():
    subprocess.run("node server.js")

import socketio
client = socketio.Client()

from .constant import *
def client_service():
    client.connect("http://localhost:3000", namespaces=[NAMESPACE])