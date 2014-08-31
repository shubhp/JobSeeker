from django.db import models

# Create your models here.
class Jobs(models.Model):
  companyName = models.CharField(max_length = 100)
  jobDescription = models.CharField(max_length = 10000, null = True, blank = True)
  jobTitle = models.CharField(max_length = 200)
  details_url = models.CharField(max_length = 300)
  logo_url = models.URLField(max_length = 300)
  minSalary = models.CharField(max_length = 15, null = True, blank = True)
  maxSalary = models.CharField(max_length = 15, null = True, blank = True)
  jobType = models.CharField(max_length = 100, null = True, blank = True)
  location = models.CharField(max_length = 100, null = True, blank = True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return self.companyName
  
class SearchTags(models.Model):
  job = models.ForeignKey(Jobs)
  tagName = models.CharField(max_length = 100)
  
  def __unicode__(self):
    return self.tagName