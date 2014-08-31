from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

import urllib2
import json
import re

from forms import searchForm
from script import AngelList
from models import *

def home(request):
  if request.method == "GET":
    form = searchForm()
    return render_to_response('homepage.html',{'form':form}, context_instance = RequestContext(request))
  elif request.method == "POST":
    form = searchForm(request.POST)
    #form validation
    queryString = form['queryString'].value()
    location = form['location'].value()
    message = ''
    jobResults = []
    if location and queryString:
      jobResults = getJobsByKeyword(queryString)
      if jobResults:
	jobResults = getJobsByLocation(location, jobResults)
	queryString = queryString + " in " + location
    elif location:
      jobResults = getJobsByLocation(location)
      queryString = location
      data = {
	  'queryString' : '',
	  'location' : location
	}
      form = searchForm(data)
    elif queryString:
      jobResults = getJobsByKeyword(queryString)
    else:
      message = "Enter either keyword or location"
    if jobResults:
      if len(jobResults) > 50:
	jobResults = jobResults[0:51]
    else:
      message = "No jobs found, try another keyword or location"
  return render_to_response('homepage.html', {'message' : message, 'form' : form, 'jobs' : jobResults, 'queryString' : queryString}, context_instance = RequestContext(request))

#function which will get all jobs from themuse api
def getJobstheMuse():
  urlprefix = 'https://www.themuse.com/api/v1/jobs?page='
  urlsuffix = '&descending=false'
  first_url = urlprefix + str(1) + urlsuffix
  
  response = urllib2.urlopen(first_url)
  jobs = response.read()
  jobs = json.loads(jobs)
  
  total_pages = int(jobs['page_count'])+1
  jobs = jobs['results']
  storeJobstheMuse(jobs)
  print "start"
  for i in range(2, total_pages):
    print i
    url = urlprefix + str(i) + urlsuffix
    
    response = urllib2.urlopen(url)
    jobs = response.read()
    jobs = json.loads(jobs)
    jobs = jobs['results']
    
    print "response"
    storeJobstheMuse(jobs)

#function to store jobs in database for themuse api
def storeJobstheMuse(jobs):
  for job in jobs:
    try:
      locations = job['locations']
      categories = job['categories']
      companyName = job['company_name']
      details_url = job['external_apply_link']
      jobDescription = job['full_description']
      jobTitle = job['title']
      jobType = job['type']
      for location in locations:
	try:
	  jobsobject = Jobs(companyName = companyName, jobDescription = jobDescription, jobTitle = jobTitle, details_url = details_url, jobType = jobType, location = location)
	  jobsobject.save()
	  for category in categories:
	    searchTagObject = SearchTags(job = jobsobject, tagName = category)
	    searchTagObject.save()
	except:
	  continue
    except:
      continue

#function which will get all jobs from angel.co api
def getJobsAngel():
  url = 'https://api.angel.co/1/jobs'
  urlsuffix = '?page='
  response = urllib2.urlopen(url)
  jobs = response.read()
  jobs = json.loads(jobs)
  total_pages = int(jobs['last_page'])+1
  total_pages = min(total_pages, 51)
  jobs = jobs['jobs']
  storeJobsAngel(jobs)
  for i in range(2, total_pages):
    print i
    requestUrl = url + urlsuffix + str(i)
    response = urllib2.urlopen(requestUrl)
    print "response"
    jobs = response.read()
    jobs = json.loads(jobs)
    jobs = jobs['jobs']
    storeJobsAngel(jobs)
  
#function to store jobs in database for angel.co api
def storeJobsAngel(jobs):
  for job in jobs:
    try:
      tags = job['tags']
      companyName = job['startup']['name']
      jobDescription = job['description']
      jobTitle = job['title']
      details_url = job['angellist_url']
      minSalary = job['salary_min']
      maxSalary = job['salary_max']
      jobType = job['job_type']
      try:
	jobsobject = Jobs(companyName = companyName, jobDescription = jobDescription, jobTitle = jobTitle, details_url = details_url, minSalary = minSalary, maxSalary = maxSalary, jobType = jobType)
	jobsobject.save()
      except:
	continue
      for tag in tags:
	try:
	  tagName = tag['name']
	  tagType = tag['tag_type']
	  if tagType == "LocationTag":
	    jobsobject.location = tagName
	    jobsobject.save()
	  else:
	    searchTagObject = SearchTags(job = jobsobject, tagName = tagName)
	    searchTagObject.save()
	except:
	  continue
    except:
      continue
    
def getJobsByBoth(queryString, location):
  queryString = re.compile("\W").split(queryString)
  print queryString
    
def getJobsByLocation(location, jobResults = ''):
  if jobResults:
    jobs = []
    for job in jobResults:
      if location.lower() in str(job.location).lower():
	jobs.append(job)
  else:
    jobs = Jobs.objects.filter(location__icontains = location)
  return jobs

def getJobsByKeyword(queryString):
  jobs = SearchTags.objects.filter(tagName__icontains = queryString).values('job').distinct()
  jobResults = []
  for job in jobs:
    jobResults.append(Jobs.objects.get(id = job['job']))
  return jobResults