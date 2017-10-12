import math
import json

import sys
sys.argv.append( '-b' )
print sys.argv

import ROOT

from TkMonitor.models import FileManager
from plotMgr import PlotManager

from TMWA.celeryapp import app
from celery import task, shared_task, current_task

from Utils import Singleton

global fileMgr
fileMgr = FileManager()

def SplitCanv( canv, n ):
    if n == 1:
        pass
    elif n == 2:
        canv.Divide(2, 1)
    elif n == 3:
        canv.Divide(3, 1)
    elif n == 4:
        canv.Divide(2, 2)


@app.task
def getJSON( jsonReq ):

    print 80*'-'
    print "getJSON called"

    req = json.loads( jsonReq )

    start = req['startdate']
    end   = req['enddate']
    filelist = fileMgr.GetFiles(start=start, end=end)
    print "DEBUG: getPlot() - {} files retrieved from DB".format(len(filelist))

    print req

    nPlots = req['nplots']

    canv = ROOT.TCanvas( True )
    SplitCanv( canv, nPlots )

    requests = []

    for iPlot in range(1, nPlots+1):
        requests.append( req['plot' + str(iPlot)] )

    print requests

    plotMgr = PlotManager(requests, filelist)
    plotMgr.SetTime(start, end)

    plots = plotMgr.GetPlots()
    print plots

    for iPlot in range(0, nPlots):
        canv.cd(iPlot+1)
        axis, plot, opt = plots[iPlot]
        plot.SetName("plot"+str(iPlot+1))

        axis.Draw('axis')
        plot.Draw(opt)

    print plots

    canv.GetListOfPrimitives().ls()

    stringResp = str(ROOT.TBufferJSON.ConvertToJSON( canv ))
    print type(stringResp)

    print 80*'-'

    return stringResp.decode('utf-8')
