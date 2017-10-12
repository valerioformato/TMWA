from channels import Group
from channels.sessions import channel_session

import json
from TMWA.celeryapp import app
from celery import task, shared_task, current_task
from celery.result import AsyncResult

from Utils import Singleton

from ltmon import ltmon
import threading, time

celeryLock = threading.Lock()

class ConnectionManager:
    __metaclass__ = Singleton

    def __init__(self):
        self.openConnections = {}

    def AddNewConnection(self, _id, reply_channel):
        print "DEBUG: ConnectionManager - Adding a new connection with id:", _id
        self.openConnections.update({ str(_id) : reply_channel })
        print self.openConnections
        pass

    def CloseConnection(self, _id):
        print self.openConnections
        print "DEBUG: ConnectionManager - Removing connection with id:", _id
        del self.openConnections[_id]
        pass

    def UpdateConnection(self, _id, _taskid):
        print "Request to update connection", _id, _taskid
        _task = AsyncResult(_taskid)
        thread = threading.Thread(target=self.SendTaskStatus, args=(_id, _task,))
        thread.start()
        pass

    def SendTaskStatus(self, _id, _task):
        print "Starting update thread for connection", _id
        while _task.state in ["PENDING", "PROGRESS"]:
            celeryLock.acquire()
            print _id, _task.id, _task.state, _task.info
            message = {
            u'text' : json.dumps({
              u'state' : _task.state,
              u'progress' : _task.info['process_percent'] if (_task and _task.info and 'process_percent' in _task.info) else 0
              })
            }
            self.openConnections[_id].send(message)
            celeryLock.release()
            time.sleep(0.1)
            pass
        if _task.state == "SUCCESS":
            self.openConnections[_id].send({
            u'text' : json.dumps({
              u'state' : _task.state,
              u'result' : _task.info
              })
            })
            print "Result sent", _id, _task.id
        pass

global connMgr
connMgr = ConnectionManager()

@channel_session
def ws_connect(message):
    print "in ws_connect"
    print message['path']
    prefix, label, sessionId = message['path'].strip('/').split('/')
    print prefix, label, sessionId
    message.channel_session['sessionId'] = sessionId
    message.reply_channel.send({"accept": True})
    connMgr.AddNewConnection(sessionId, message.reply_channel)

@channel_session
def ws_receive(message):
    print "in ws_receive"
    jReq = message['text']
    print jReq
    task = ltmon.getJSON.delay( jReq )
    connMgr.UpdateConnection(message.channel_session['sessionId'], task.id)

@channel_session
def ws_disconnect(message):
    print "in ws_disconnect"
    connMgr.CloseConnection(message.channel_session['sessionId'])

# @csrf_exempt
# def GetPlotStatus(request):
#     print request.body
#     taskId = request['id']
#     task = AsyncResult(taskId)
#     print task
#     jResponse = json.dumps({
#     'task' : task.id,
#     'status' : task.state
#     })
