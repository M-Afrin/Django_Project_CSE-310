"""
URL configuration for Thrifting_Store project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SecondSpin.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', SignUp, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
  
    # Seller URLs
    path('user_profile/', user_profile, name='user_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('products/', seller_products, name='seller_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    # path('orders/', ordered_items, name='ordered_items'),

    # Shop URLs
    path('shop/', shop, name='shop'),
    path('shop/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/<str:action>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:cart_item_id>/', update_cart_item, name='remove_cart_item'),
    path('checkout/',checkout, name='checkout'),
    path('confirm-order/<int:order_id>/', confirm_order, name='confirm_order'), 
    path('orders/',orders, name='orders'),
    path('orders/<int:order_id>/',order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', cancel_order, name='cancel_order'),

    path('About/', About, name='About'),
    path('Contact/', Contact, name='Contact'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()