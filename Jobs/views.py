from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from forms import searchForm
from script import AngelList

def home(request):
  if request.method == "GET":
    form = searchForm()
    return render_to_response('homepage.html',{'form':form}, context_instance = RequestContext(request))
  elif request.method == "POST":
    form = searchForm(request.POST)
    #form validation
    if form.is_valid():
      queryString = form['queryString'].value()
      searchArea = form['searchArea'].value()
      classobj = AngelList(queryString, searchArea)
      jobResults = classobj.searchApi()
      return render_to_response('homepage.html', {'jobs' : jobResults}, context_instance = RequestContext(request))
    else:
      return render_to_response('homepage.html', {'form' : form}, context_instance = RequestContext(request))