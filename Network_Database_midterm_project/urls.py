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
from django.urls import path  # 引入 path 函數來定義路由
from shop.views import *  # 匯入我們自定義的視圖模組，以便在路由中調用

urlpatterns = [
    # 首頁和索引頁面
    path('', front_page, name='front_page'),  # 預設首頁，顯示主要內容
    path('index/', front_page, name='front_page'),  # 額外的首頁路徑選項

    # 顯示所有商品的頁面
    path('all_products/', all_products, name='all_products'),

    # 購物車頁面
    path('shopcart/', shopcart, name='shopcart'),

    # 後台頁面 (若未登入則會被重導到登入頁面)
    path('admin/', admin_page, name='admin_page'),

    # 後台登入頁面
    path('admin/login/', admin_login, name='admin_login'),

    # 後台登出功能
    path('admin/logout/', admin_logout, name='admin_logout'),

    # 後台功能：管理商品
    path('admin/product/add/', add_product, name='add_product'),  # 新增商品
    path('admin/product/delete/<int:product_id>/', delete_product, name='delete_product'),  # 刪除商品
    path('admin/product/edit/<int:product_id>/', edit_product, name='edit_product'),  # 更新商品資訊

    # 後台功能：管理帳號
    path('admin/account/add/', add_account, name='add_account'),  # 新增帳號
    path('admin/account/delete/<int:account_id>/', delete_account, name='delete_account'),  # 刪除帳號
    path('admin/account/edit/<int:account_id>/', edit_account, name='edit_account'),  # 編輯帳號資訊

    # Footer 編輯頁面
    path('edit_footer/', edit_footer, name='edit_footer'),  # 允許管理員編輯網站底部資訊

    # 處理訂單的路由
    path('process_order/', process_order, name='process_order'),  # 用於處理購物車訂單
]
