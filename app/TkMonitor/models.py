# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

import glob, re, math, sys
import cProfile
from Utils import Singleton

# Create your models here.
class DataFile( models.Model ):
    filename = models.CharField(max_length=200)
    timestamp = models.IntegerField()

    def __str__(self):
        return self.filename


class FileManager():
    __metaclass__ = Singleton
    def __init__(self):
        self.basepath = settings.ROOTFILES
        print "DEBUG: Init FileManager with path", self.basepath

    def GetFirstFile(self):
        return DataFile.objects.order_by("timestamp")[0]
    def GetLastFile(self):
        return DataFile.objects.order_by("-timestamp")[0]

    def GetFiles(self, **kwargs):
        for key in kwargs:
            print "keyword arg: %s: %s" % (key, kwargs[key])

        start = self.GetFirstFile().timestamp if not kwargs['start'] else kwargs['start']
        end   = self.GetLastFile().timestamp  if not kwargs['end']   else kwargs['end']

        print "DEBUG: FileManager::GetFiles: from {} to {}".format(start, end)

        return [ x.filename for x in DataFile.objects.filter(timestamp__gte=start, timestamp__lte=end) ]

    def UpdateDB(self):
        filelist = glob.glob(self.basepath+"/*.root")
        print "DEBUG: Found {} files".format(len(filelist))
        print "DEBUG: {} entries in the DB".format(len(DataFile.objects.all()))
        count = 0
        totfiles = len(filelist)
        dbentries = DataFile.objects.all()
        timestamps = [ x.timestamp for x in dbentries ]
        for _file in filelist:
            count += 1
            timestamp = int(re.search('\D*(\d+)\.root', _file).group(1))

            if timestamp not in timestamps:
                obj = DataFile(filename=_file, timestamp=timestamp)
                obj.save()
                if math.fmod(count, 1000) == 0:
                    print "Inserted file {}/{} \r".format(count, totfiles),
                    sys.stdout.flush()
            else:
                timestamps.remove(timestamp)
                # print "DEBUG calibration {} already in the DB".format(timestamp)
        print "DEBUG: DB updated.\n{} entries in the DB".format(len(DataFile.objects.all()))

        print "Last file:", DataFile.objects.order_by("-timestamp")[0]

        pass
