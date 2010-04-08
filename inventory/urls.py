from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object

from inventory.tracker.models import Product
from inventory.tracker.forms import ProductForm
from inventory.tracker.views import update_qty, qtys_before, qtys_on, \
                                    delete_product

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^inventory/', include('inventory.foo.urls')),

    (r'^$', object_list, {'queryset': Product.objects.all()}),

    url(r'^new/$', create_object, {'form_class': ProductForm,
        'post_save_redirect': '/'}, name='create_product'),

    url(r'^edit/(?P<object_id>\d+)/$', update_object,
        {'form_class': ProductForm, 'post_save_redirect': '/'},
        name='update_product'),

    url(r'del/$', delete_product, name='del'),
    url(r'^update_qty/(?P<product_id>\d+)/(?P<qty>\d+)$', update_qty),
    url(r'^update_qty/', lambda x:None, name='update_qty'),
    url(r'^qtys_before/(?P<days_before>\d+)$', qtys_before),
    url(r'^qtys_before/', lambda x:None, name='qtys_before'),
    url(r'^qtys_on/(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)$', qtys_on),
    url(r'^qtys_on/', lambda x:None, name='qtys_on'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^inventory/media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
