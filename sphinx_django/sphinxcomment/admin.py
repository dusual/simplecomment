from django.contrib import admin
from sphinx_django.sphinxcomment.models import Comment, Element

class CommentAdmin(admin.ModelAdmin):
    list_display = ['element', 'submitter_name', 'comment', 'date']
    search_fields = ['comment']
    date_hierarchy = 'date'
    list_filter = ['date', 'submitter_name']
    search_fields = ['title', 'submitter_name', 'submitter_url']
    fieldsets = (
        (None, {'fields': ('submitter_name', 'element', 'comment')}),
               ('Other info', {'fields': ('submitter_url', 'ip')}),
        )
    # XXX: adding 'date' to the 'Other info' fieldset results in a
    # ImproperlyConfigured error. :S

class ElementAdmin(admin.ModelAdmin):
    search_fields = ['chapter_name']
    list_filter = ['chapter_name']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Element, ElementAdmin)
