from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'seniors.views.seniors', name='tnq_seniors'),
    url(r'^info/', 'seniors.views.enterinfo', name='enter_senior_info'),
    #url(r'^info/', 'seniors.views.closed', name='enter_senior_info'),
    url(r'^submit/', 'seniors.views.enterinfo', name='submit_senior_info'),
    url(r'^thanks', 'seniors.views.thanks', name='senior_success'),
    url(r'^email/', 'seniors.views.email', name="senior_email"),
    url(r'^email/submit/', 'seniors.views.email', name="submit_senior_email"),
    url(r'^emailsent/', 'seniors.views.emailsent', name="senior_email_sent"),
    url(r'^noinfo/', 'seniors.views.noinfo', name="no_senior_info"),
)
