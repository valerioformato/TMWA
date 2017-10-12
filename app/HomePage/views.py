# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
from django.views import generic

from Utils import Singleton

import json

class HeaderButton:
    def __init__( self, name, link ):
        self.name     = name
        self.link     = link
        self.selected = False

class HeaderButtonManager:
    __metaclass__ = Singleton
    def __init__( self ):
        self.headerButtons = []
        self.SetupHeaderButtons()

    def SetupHeaderButtons(self):
        buttons = [
            ["Home", "/"],
            ["LT Monitor", "/ltmon/"],
            ["RT Monitor", "/rtmon/"],
            ["Contact", "/contact/"]
        ]
        for button in buttons:
            self.headerButtons.append( HeaderButton(button[0], button[1]) )

    def SelectButton( self, btnName ):
        for button in self.headerButtons:
            if btnName == button.name:
                button.selected = True
            else:
                button.selected = False
        pass

global btnMgr
btnMgr = HeaderButtonManager()

class IndexView( generic.TemplateView ):

    template_name = 'HomePage/index.html'

    def get(self, request, *args, **kwargs):
        print "Selecting HOME"
        btnMgr.SelectButton("Home")
        context = self.get_context_data()
        return self.render_to_response(context)


    def get_context_data(self , **kwargs):
        context = {
          'headerButtons'  : btnMgr.headerButtons,
        }
        return context


class ContactsView( generic.TemplateView ):

    template_name = 'HomePage/contact.html'

    def get(self, request, *args, **kwargs):
        print "Selecting Contact"
        btnMgr.SelectButton("Contact")
        context = self.get_context_data()
        return self.render_to_response(context)


    def get_context_data(self , **kwargs):
        context = {
          'headerButtons'  : btnMgr.headerButtons,
        }
        return context


# Create your views here.
def task_state(request):
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
