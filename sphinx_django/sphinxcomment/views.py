# Create your views here.
from django.http import HttpResponse
from django.utils.simplejson import dumps 
from django.contrib.csrf.middleware import csrf_exempt
import django.forms as forms
from django.db import connection
from django.http import HttpResponse,Http404
from sphinxcomment.models import Comment, Element
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context
from django.template.loader import get_template
from django.utils.simplejson import dumps 
from django.conf import settings
from os.path import join, splitext
from BeautifulSoup import BeautifulSoup as bss, Tag

#placeholder_string = open('paragraph_id.py').read()
#exec placeholder_string



def dump_queries():
    # requires settings.DEBUG to be set to True in order to work
    if len(connection.queries) == 1:
        print connection.queries
    else:
        qs = {}
        for q in connection.queries:
            qs[q['sql']] = qs.setdefault(q['sql'], 0) + 1
        for q in sorted(qs.items(), key=lambda x: x[1], reverse=True):
            print q
        print len(connection.queries)

class CommentForm(forms.Form):
    name = forms.CharField(max_length=64)
    url = forms.URLField(max_length=128, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 8, 'cols': 60
        }))
    remember = forms.BooleanField(initial=True, required=False)

def comments_by_chapter(chapter):
     objs = {}

     for c in Comment.objects.filter(element__chapter_name=chapter).order_by('date'):
         objs.setdefault(c.element.paragraph_id, []).append(c)
         

             
     
     return objs


     




# def chapter(request):
#     template = get_template('comment.html')
#     resp = {}
#     for elt, comments in comments_by_chapter(chapter).iteritems():
#         print elt ,comments
#         form = CommentForm(initial={
#             'paragraph_id': elt,
#             'name': name
#             })
#         resp[elt] = template.render(Context({
#             'paragraph_id': elt,
#             'form': form,
#             'length': len(comments),
#             'query': comments,
#             }))
#     return HttpResponse(dumps(resp), mimetype='application/json')

def chapter_count(request,chapter_name):
#    print chapter_name
    chapter_name=chapter_name.split('.')[0]
    comment_objs = comments_by_chapter(chapter_name)
    resp={}
    temp_dict={}
    for elt, comments in comment_objs.iteritems():
        temp_dict[elt]=len(comments)

    resp['count']=temp_dict
      
    
#    print resp
    return HttpResponse(dumps(resp), mimetype='application/json')
    
def single(request,paragraph_id, form=None, newid=None):
    if paragraph_id[-1]=='/':
        paragraph_id=paragraph_id[:-1]
    queryset = Comment.objects.filter(element=paragraph_id)
   #  print len(queryset)
    if form is None:
        form = CommentForm(initial={
            'paragraph_id': paragraph_id,
            'name': request.session.get('name', ''),
            })
    try:
        error = form.errors[0]
    except:
        error = ''
   # print form.errors
    return render_to_response('comment.html', {
        'paragraph_id': paragraph_id,
        'form': form,
        'length': len(queryset),
        'query': queryset,
        'newid': newid or True,
        'error': error,
        })




def submit(request, paragraph_id):

    try:
        element = get_object_or_404(Element, paragraph_id=paragraph_id)
    except Http404:
        #creating chapter name from paragraph_id surely there is a better way using the context but i do not know as yet
        chapter_id='_'.join(paragraph_id.split('_')[0:-1])
        chapter_name=chapter_id[-1::-1].replace('_','/',1)[-1::-1]
        element=Element(chapter_name=chapter_name,paragraph_id=paragraph_id)
        element.save()
   # print element.chapter_name
    form = None
    newid = None
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
      #  print form.errors
        if form.is_valid():
            #print form.cleaned_data
            data = form.cleaned_data
            if data.get('remember'):
                request.session['name'] = data['name']
                request.session['url'] = data['url']
            else:
                request.session.pop('name', None)
                request.session.pop('url', None)
            c = Comment(element=element,
                        comment=data['comment'],
                        submitter_name=data['name'],
                        submitter_url=data['url'],
                        ip=request.META.get('REMOTE_ADDR'))
         #   print c
            c.save()
           
            form = None
    return single(request, paragraph_id, form,)

def test(request):
   # print request
    string="<p>test comment</p>"
    return HttpResponse(string,mimetype="text/plain")
    
def page(req, path):
    if splitext(path)[1] == '.html':
        soup = bss(open(join(settings.SPHINX_PROJECT, path)).read())
        head = soup.find('head')
        first_script = Tag(soup, 'script')
        first_script['src'] = "../_static/simplecomment.js" 
        first_script['type'] = "text/javascript"
        second_script = Tag(soup, 'script')
        second_script['src'] = "../_static/jquery.form.js" 
        second_script['type'] = "text/javascript"
        head.insert(-1, first_script)
        head.insert(-1, second_script)
        counter = 0
        page_identity = path.split('.')[0].replace('/', '_')
        for p in soup.findAll('p'):
            p['id'] = '%s_%s' %(page_identity, counter)
            counter += 1
        return HttpResponse(str(soup))
    else:
        return HttpResponse(open(join(settings.SPHINX_PROJECT, path)).read())
    
#return HttpResponse(dumps(string),mimetype="text/plain")
#test= csrf_exempt(test)

