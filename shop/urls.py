from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path("",views.home, name="home"),
    path("signup",views.signup),
    path("login/",views.login,name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("cart/",views.cart_view,name="cart"),
    path("add-to-cart/",views.add_to_cart,name="add_to_cart"),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('place-order/', views.place_order, name='place_order'),

]


