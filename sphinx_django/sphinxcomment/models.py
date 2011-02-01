from django.db import models

# Create your models here.
from django.db import models


mutable = True

class Element(models.Model):
    paragraph_id = models.CharField('Paragraph Id', max_length=100, editable=False, primary_key=True) 
    chapter_name = models.CharField('Chapter name', max_length=100, editable=False,db_index=True)
    

    def __unicode__(self):
        return self.paragraph_id
    
class Comment(models.Model):
    element = models.ForeignKey(Element,
        help_text='ID of paragraph that was commented on')
    comment = models.TextField(editable=mutable,
        help_text='Text of submitted comment (please do not modify)')
    submitter_name = models.CharField('Submitter', max_length=64,
        help_text='Self-reported name of submitter (may be bogus)')
    submitter_url = models.URLField('URL', blank=True, editable=mutable,
        help_text='Self-reported URL of submitter (may be empty or bogus)')
    ip = models.IPAddressField('IP address', editable=mutable,
        help_text='IP address from which comment was submitted')
    date = models.DateTimeField('date submitted', auto_now=True,
                                auto_now_add=True)

    def __unicode__(self):
        return self.comment[:32]

    
