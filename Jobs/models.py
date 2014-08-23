from django.db import models

# Create your models here.
class Jobs(models.Model):
  companyName = models.CharField(max_length = 100)
  jobDescription = models.CharField(max_length = 10000, null = True, blank = True)
  jobTitle = models.CharField(max_length = 200)
  angellist_url = models.CharField(max_length = 300)
  minSalary = models.CharField(max_length = 15, null = True, blank = True)
  maxSalary = models.CharField(max_length = 15, null = True, blank = True)
  jobType = models.CharField(max_length = 100, null = True, blank = True)
  queryString = models.CharField(max_length = 100)
  searchType = models.CharField(max_length = 15)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __unicode__(self):
    return self.companyName