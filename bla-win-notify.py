from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import urllib
import json
import time
import getpass
import os.path
import wx

uid = None
user = None
sleeptime = 1

class WindowsBalloonTip:
    def __init__(self):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], 
"bla.png" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           self.hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        self.nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, 
"BlaChat Notify")
        Shell_NotifyIcon(NIM_ADD, self.nid)
        # self.show_balloon(title, msg)
        #time.sleep(10)
        #DestroyWindow(self.hwnd)

    def notify(self, title, msg):
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          self.hicon, "Bla Notification",msg,1000,title))

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

windowTools=WindowsBalloonTip()

def notification(conversation, author, msg):
  global windowTools
  windowTools.notify("Bla - " + conversation, "(" + author + ") " + msg)

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
    f = urllib.urlopen("https://www.ssl-id.de/bla.f-online.net/api/xjcp.php", params)
    result = f.read()
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
    f = urllib.urlopen("https://www.ssl-id.de/bla.f-online.net/api/xjcp.php", params)
    result = f.read()
    #print(result)
    obj = json.loads(result)
    if "id" in obj:
      print("Login successfull!")
      global uid
      uid = obj["id"]
      with open('.bla-config.json', 'w') as f:
        f.write(json.dumps({"user":user, "uid":uid}))
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
