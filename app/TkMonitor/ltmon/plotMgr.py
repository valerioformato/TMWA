import math

import ROOT

from celery import task, shared_task, current_task

from Utils import Singleton

from tkidmap import tkidmap

sides = ["X", "Y", "XY"]

def SetXaxisTimeHist( hist ):
    hist.GetXaxis().SetTimeDisplay(1)
    hist.GetXaxis().SetNdivisions(-612)
    hist.GetXaxis().SetTimeOffset(0,"gmt")
    hist.GetXaxis().SetLabelOffset(0.04)
    hist.GetXaxis().SetLabelSize(0.04)
    hist.GetXaxis().SetTimeFormat("%d/%m/%y")


class PlotManager():

    def __init__(self, plotRequests, fileList):
        self.plotRequests = []
        self.fileList = []
        self.start = 0
        self.end = 0
        self.objects = []
        self.titles = []
        self.data = []

        self.plotRequests = plotRequests
        self.fileList = fileList
        pass

    def SetTime(self, start, end):
        self.start = start
        self.end   = end
        pass

    def InitPlots(self):

        for request in self.plotRequests:
            isMean = bool(request['mean'])

            reqindex = self.plotRequests.index(request)

            vartype = type( self.data[reqindex][0][1] )

            ymin = ymax = 0

            if not request['min']:
                if vartype == int:
                    ymin = math.floor(0.95 * min( [x[1] for x in self.data[reqindex]] ))-1.5
                else:
                    ymin = 0.95 * min( [x[1] for x in self.data[reqindex]] )
            else:
                ymin = int(request['min'])

            if not request['max']:
                if vartype == int:
                    ymax = math.ceil(1.05 * max( [x[1] for x in self.data[reqindex]] ))+1.5
                else:
                    ymax = 1.05 * max( [x[1] for x in self.data[reqindex]] )
            else:
                ymax = int(request['max'])

            if vartype == int:
                nbins = int(ymax-ymin)
            else:
                nbins = 100


            print "ymin =", ymin, "ymax =", ymax
            hist = ROOT.TH2D("hist{}".format(reqindex), self.titles[reqindex], 100, self.start, self.end, nbins, ymin, ymax)

            SetXaxisTimeHist( hist )
            hist.SetStats(0)

            opt = "lp" if isMean else "colz"
            self.objects.append( [hist, opt] )
            pass

        pass

    def ReadData(self):

        ladders = []
        for request in self.plotRequests:
            self.data.append([])
            if request['type'] == "tkid":
                ladders.append([x for x in tkidmap if x[1]==int(request['num'])])
                self.titles.append("TkId " + str(request['num']) + " - Side " + sides[int(request['side'])] + ";;"+ request['var'])
            elif request['type'] == "plane":
                ladders.append([x for x in tkidmap if x[0]==int(request['num'])])
                self.titles.append("Plane " + str(request['num']) + " - Side " + sides[int(request['side'])] + ";;"+ request['var'])
            elif request['type'] == "tracker":
                ladders.append(tkidmap)
                self.titles.append("Whole Tracker - Side " + sides[int(request['side'])] + ";;"+ request['var'])

            pass

        bufferToPlot = []
        for rfile in self.fileList:
            process_percent = float(self.fileList.index(rfile))/len(self.fileList)
            current_task.update_state(state='PROGRESS',
                meta={'process_percent': process_percent})
            infile = ROOT.TFile(rfile, "OPEN")
            tree = infile.Get("CalPar")
            tree.GetEntry(0)

            for cal in tree:
                thisvar = 0;
                for request in self.plotRequests:
                    reqindex = self.plotRequests.index(request)
                    thisvar = 0
                    for ladder in ladders[reqindex]:
                        index = ladder[2]
                        pyndex = 2*index + int(request['side'])

                        queryvar = "tree."+request['var']+'['+str(pyndex)+']'
                        thisvar += eval(queryvar)
                        pass

                    self.data[reqindex].append( [cal.Time, thisvar/len(ladders[reqindex])] )
                    pass
                pass
            infile.Close()
            pass
        pass

    def FillPlots(self):

        returnBuffer = []

        for request in self.plotRequests:
            isMean = bool(request['mean'])

            reqindex = self.plotRequests.index(request)

            hist = self.objects[reqindex][0]
            opt  = self.objects[reqindex][1]

            for data in self.data[reqindex]:
                hist.Fill( data[0], data[1] )
                pass

            if isMean:
                print "Getting mean"
                graph = ROOT.TGraphErrors()

                ymin = hist.GetYaxis().GetBinLowEdge(1)
                ymax = hist.GetYaxis().GetBinLowEdge(hist.GetNbinsY()+1)
                for xbin in range(0, hist.GetNbinsX()):
                    graph.SetPoint(xbin, hist.GetXaxis().GetBinCenter(xbin), hist.ProjectionY("dummy", xbin, xbin).GetMean())
                    graph.SetPointError(xbin, 0, hist.ProjectionY("dummy", xbin, xbin).GetStdDev())

                    pass

                graph.SetMarkerStyle(20)
                graph.GetYaxis().SetRangeUser(ymin, ymax)
                SetXaxisTimeHist( graph )

                pass

                returnBuffer.append([hist, graph, "lp"])
            else:
                returnBuffer.append([hist, hist, "colz"])

        return returnBuffer

    def GetPlots(self):
        self.ReadData()
        self.InitPlots()
        return self.FillPlots()
