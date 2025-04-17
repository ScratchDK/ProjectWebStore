import catalog.views as views
from django.urls import path
from catalog.apps import CatalogConfig
from django.views.generic import TemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.ProductsListView.as_view(), name="home"),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('contact_success/', TemplateView.as_view(template_name='contact_success.html'), name='contact_success'),
    path("create_product/", views.ProductCreateView.as_view(), name="create_product"),
    path("update_product/<int:id>/", views.ProductUpdateView.as_view(), name="update_product"),
    path("delete_product/<int:id>/", views.ProductDeleteView.as_view(), name="delete_product"),
]
