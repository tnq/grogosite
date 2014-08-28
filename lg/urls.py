from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Example:
    # (r'^orders/', include('orders.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='tnq_site/lg.html'), name='tnq_lg'),
    url(r'^signup/', 'lg.views.lgform', name='lg_signup'),
    url(r'^success/', TemplateView.as_view(template_name='tnq_site/lg/lg_success.html'), name='lg_success'),
)
