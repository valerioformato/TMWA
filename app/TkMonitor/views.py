# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import json

from Utils import Singleton
from .models import DataFile, FileManager
from HomePage.views import HeaderButton, HeaderButtonManager

from ltmon import ltmon

global btnMgr
btnMgr = HeaderButtonManager()

fileMgr = FileManager()

class LTMonView( generic.TemplateView ):

    # context_object_name = 'buttonSet'
    template_name = 'TkMonitor/ltmon.html'

    def get(self, request, *args, **kwargs):
        print "Selecting LT Monitor"
        btnMgr.SelectButton("LT Monitor")
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self , **kwargs):
        context = {
          'headerButtons'  : btnMgr.headerButtons,
          'firstFile'      : fileMgr.GetFirstFile().timestamp,
          'lastFile'       : fileMgr.GetLastFile().timestamp
        }
        return context

@csrf_exempt
def GetJSONForLTMon(request):
    if request.method == 'POST':
        print request.body
        task = ltmon.getJSON.delay( request.body )
        jResponse = json.dumps({
        'task' : task.id,
        'status' : "submitted"
        })
        return HttpResponse( jResponse )
    else:
        return HttpResponse( "Only POST requests allowed" )


class RTMonView( generic.TemplateView ):

    # context_object_name = 'buttonSet'
    template_name = 'TkMonitor/rtmon.html'

    def get(self, request, *args, **kwargs):
        print "Selecting RT Monitor"
        btnMgr.SelectButton("RT Monitor")
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self , **kwargs):
        context = {
          'headerButtons'  : btnMgr.headerButtons,
        }
        return context
