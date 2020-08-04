"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
# from rest_framework import permissions

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Snippets API",
#         default_version='v1',
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@snippets.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # url(r'^swagger(?P<format>\.json|\.yaml)$',
    #     schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger',
    #                                        cache_timeout=0),
    #     name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc',
    #                                      cache_timeout=0),
    #     name='schema-redoc'),
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    # TODO mobile optimization
    path('privacy-policy/',
         TemplateView.as_view(template_name='privacypolicy.html')),
    path('terms-of-service/',
         TemplateView.as_view(template_name='termsofservice.html')),
    path('dabi/', TemplateView.as_view(template_name='index_dabi.html')),
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/preorder/', include('preorder.urls')),
    path('api/store/', include('store.urls')),
    path('api/publish/', include('publish.urls')),
    path('api/pick/', include('pick.urls')),
    path('api/auth/', include('rest_auth.urls')),
    path('api/core/', include('core.urls')),
    path('api/order/', include('order.urls')),
    path('api/product/', include('product.urls')),
    path('api/advertisement/', include('advertisement.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
