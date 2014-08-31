from django_cron import CronJobBase, Schedule

from datetime import datetime, timedelta
from Jobs.models import Jobs
from Jobs.script import AngelList
from Jobs.views import *

class RefreshJobs(CronJobBase):
  RUN_EVERY_MINS = 1
  
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'Jobs.cron'
  
  def do(self):
    getJobstheMuse()