import urllib2, json

from Jobs.models import Jobs

#class including all functions required for api request
class AngelList(object):
  #constructor
  def __init__(self, queryString, searchType):
    self.queryString = queryString
    self.searchType = searchType
    
  #function for making api request and storing results in database
  def searchApi(self):
    #check database
    jobs = Jobs.objects.filter(queryString = self.queryString, searchType = self.searchType)
    
    #query string is not present in database
    if len(jobs) == 0:
      requesturl = 'https://api.angel.co/1/search?query='+urllib2.quote(self.queryString)+'&type='+urllib2.quote(self.searchType)
      response = urllib2.urlopen(requesturl)
      data = response.read()
      data = json.loads(data)
      ids = []
      #get all respective ids
      for row in data:
	id = row['id']
	ids.append(id)
      urls = self.getUrls(ids)
      jobs = self.getJobs(urls)
    return jobs
  
  #function to generate urls for all api requests
  def getUrls(self, ids):
    urlprefix = 'https://api.angel.co/1/'
    urlsuffix = '/jobs'
    #generate urls according to the loaction
    if self.searchType == "LocationTag":
      urls = []
      for id in ids:
	url = urlprefix + 'tags/'+str(id)+urlsuffix
	urls.append(url)
    #generate urls according to the company name
    elif self.searchType == "Startup":
      urls = []
      for id in ids:
	url = urlprefix + 'startups/'+str(id)+urlsuffix
	urls.append(url)
    return urls
  
  #function for fetching jobs through all api requests
  def getJobs(self, urls):
    jobs = []
    for url in urls:
      response = urllib2.urlopen(url)
      data = response.read()
      data = json.loads(data)
      if len(data) != 0 and self.searchType != "Startup":
	print data
	data = data['jobs']
      for obj in data:
	companyName = obj['startup']['name']
	jobDescription = obj['description']
	jobTitle = obj['title']
	angellist_url = obj['angellist_url']
	minSalary = obj['salary_min']
	maxSalary = obj['salary_max']
	jobType = obj['job_type']
	job = Jobs(companyName = companyName, jobDescription = jobDescription, jobTitle = jobTitle, angellist_url = angellist_url, minSalary = minSalary, maxSalary = maxSalary, jobType = jobType, queryString = self.queryString, searchType = self.searchType)
	job.save()
	jobs.append(job)
    return jobs