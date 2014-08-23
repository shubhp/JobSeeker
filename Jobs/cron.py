from django_cron import CronJobBase, Schedule

from datetime import datetime, timedelta
from Jobs.models import Jobs
from Jobs.script import AngelList

class RefreshJobs(CronJobBase):
  RUN_EVERY_MINS = 1
  
  schedule = Schedule(run_every_mins = RUN_EVERY_MINS)
  code = 'Jobs.cron'
  
  def do(self):
    updateTime = datetime.now() - timedelta(days = 1)
    queryStrings = Jobs.objects.filter(created_at__lt = updateTime).values('queryString','searchType').distinct()
    for queryString in queryStrings:
      searchArea = queryString['searchType']
      querystring = queryString['queryString']
      jobs = Jobs.objects.filter(queryString = querystring).delete()
      classobj = AngelList(querystring, searchArea)
      jobresults = classobj.searchApi()