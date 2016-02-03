from gi.repository import Notify
import urllib
import json
import time
import getpass
import os.path
import wx

uid = None
user = None
sleeptime = 1

def notification(conversation, author, message):
    Notify.init ("Bla Chat")
    MsgNotification=Notify.Notification.new ("Bla - " + conversation,
                               "(" + author + ") " + message,
                               "dialog-information")
    MsgNotification.show ()

app = wx.App()
app.MainLoop()

def ask(parent=None, message='', default_value=''):
    dlg = wx.TextEntryDialog(parent, message, defaultValue=default_value)
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    return result

def askLogin():
    global user
    user = ask(message="Username")
    password = ask(message="Password")
    #user = raw_input("Username: ").lower()
    #password = getpass.getpass("Password: ")
    login(user, password)

def pollEventLoop():
    global sleeptime
    while True:
        time.sleep(sleeptime)
        sleeptime = sleeptime + 1
        if sleeptime > 30:
            sleeptime = 30
        pollEvents()

def pollEvents():
    msg = json.dumps({"id":uid})
    params = urllib.urlencode({"msg":msg})
    api = urllib.urlopen("https://www.ssl-id.de/bla.f-online.net/api/xjcp.php", params)
    result = api.read()
    #print(result)
    obj = json.loads(result)
    handleEvents(obj)

def handleEvents(data):
    global sleeptime
    if "events" in data:
        for e in data["events"]:
            if e["type"] == "onMessage" and not e["nick"] == user:
                notification(e["msg"], e["author"], e["text"])
                sleeptime = 1

def login(user, password):
    msg = json.dumps({"user":user, "pw":password})
    params = urllib.urlencode({"msg":msg})
    api = urllib.urlopen("https://www.ssl-id.de/bla.f-online.net/api/xjcp.php", params)
    result = api.read()
    #print(result)
    obj = json.loads(result)
    if "id" in obj:
        print("Login successfull!")
        global uid
        uid = obj["id"]
        with open('.bla-config.json', 'w') as conf:
            conf.write(json.dumps({"user":user, "uid":uid}))
        handleEvents(obj)
        pollEventLoop()
    else:
        print("Username or password wrong!")
        askLogin()

def initialize():
    #notification("Info", "System", "Listening for notifications.")
    global user
    global uid
    if os.path.exists('.bla-config.json'):
        with open('.bla-config.json', 'r') as f:
            data = json.loads(f.read())
            if "user" in data:
                user = data["user"]
            if "uid" in data:
                uid = data["uid"]
    if user is not None and uid is not None:
        pollEventLoop()
    else:
        notification("Login", "System", "No valid login availible.")
        askLogin()


initialize()
