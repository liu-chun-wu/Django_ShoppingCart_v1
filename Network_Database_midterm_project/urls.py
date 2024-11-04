"""week8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path , re_path  #要include這個模組才能使用re_path
from shop.views import *  #要include這個我們自己定義的模組才能使用


urlpatterns = [
    # 首頁
    path('', front_page, name='front_page'),                                                
    path('index/', front_page, name='front_page'),    
                                          
    # 所有商品                                                                        
    path('all_products/', all_products, name='all_products'),     

    # 購物車                          
    path('shopcart/', shopcart, name='shopcart'),       

    # 後台(未登入會導到登入頁面)                                   
    path('admin/', admin_page, name='admin_page'),  
    # 後台登入                                       
    path('admin/login/',admin_login,name='admin_login'),                                 
    # 後台登出
    path('admin/logout/', admin_logout, name='admin_logout'),  

    # 新增商品
    path('admin/product/add/', add_product, name='add_product'),
    # 刪除商品
    path('admin/product/delete/<int:product_id>/', delete_product, name='delete_product'),
    # 更新商品
    path('admin/product/edit/<int:product_id>/', edit_product, name='edit_product'),

    # 新增帳號
    path('admin/account/add/', add_account, name='add_account'),
    # 刪除帳號
    path('admin/account/delete/<int:account_id>/', delete_account, name='delete_account'),
    # 編輯帳號
    path('admin/account/edit/<int:account_id>/', edit_account, name='edit_account'),

    # 編輯footer
    path('edit_footer/', edit_footer, name='edit_footer'),

    # 處理購物車的訂單
    path('process_order/', process_order, name='process_order'),

]