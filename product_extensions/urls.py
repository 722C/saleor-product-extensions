from django.conf.urls import url

from .dashboard_views import views as dashboard_views

urlpatterns = [
    url(r'^dashboard/product-extensions/$',
        dashboard_views.product_extension_list,
        name='product-extension-dashboard-list'),
    url(r'^dashboard/product-extensions/create/$',
        dashboard_views.product_extension_create,
        name='product-extension-dashboard-create'),
    url(r'^dashboard/product-extensions/(?P<pk>[0-9]+)/$',
        dashboard_views.product_extension_details,
        name='product-extension-dashboard-detail'),
    url(r'^dashboard/product-extensions/(?P<pk>[0-9]+)/delete/$',
        dashboard_views.product_extension_delete,
        name='product-extension-dashboard-delete'),
]
