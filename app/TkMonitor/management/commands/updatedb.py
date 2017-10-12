from django.core.management.base import BaseCommand, CommandError
from TkMonitor.models import DataFile, FileManager

fileMgr = FileManager()

class Command(BaseCommand):
    help = 'Updates the DB with the list of rootfiles'

    def handle(self, *args, **options):
        fileMgr.UpdateDB()
        pass
