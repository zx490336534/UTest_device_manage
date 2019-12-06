"""UTest_device_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='自动化设备管理平台',
        default_version='v1',  # 必传
        description='自动化测试设备管理',
        terms_of_service="http://www.zhongxin.com",
        contact=openapi.Contact(email="490336534@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # 权限类
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('device_manage.urls')),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
