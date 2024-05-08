from django.contrib import admin
from django.urls import path
from mastercard import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Documentation for your API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('criar-usuario/', views.criar_usuario, name='criar_usuario'),
    path('cadastrar-cartao/', views.CadastrarCartaoView.as_view(), name='cadastrar_cartao'),
    path('cadastrar-lote/', views.CadastrarLoteView.as_view(), name='cadastrar_lote'),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
