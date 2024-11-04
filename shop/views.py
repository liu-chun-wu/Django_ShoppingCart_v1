import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *

# 顯示首頁
def front_page(request):
    footer_info = Footer.objects.first()  # 獲取唯一的 footer 資訊
    return render(request, 'front_page.html', {'footer_info': footer_info})

# 顯示所有商品的頁面
def all_products(request):
    footer_info = Footer.objects.first()  # 獲取 footer 資訊
    products = Product.objects.all()  # 查詢所有商品
    context = {
        'products': products,
        'footer_info': footer_info
    }
    return render(request, 'all_products.html', context)

# 顯示購物車頁面
def shopcart(request):
    footer_info = Footer.objects.first()  # 獲取 footer 資訊
    context = {
        'footer_info': footer_info
    }
    return render(request, 'shopcart.html', context)

# 顯示管理員頁面
def admin_page(request):
    footer_info = Footer.objects.first()  # 獲取 footer 資訊
    products = Product.objects.all()  # 獲取所有商品
    admin_accounts = Admin.objects.all()  # 獲取所有管理員帳號
    context = {
        'footer_info': footer_info,
        'products': products,
        'accounts': admin_accounts
    }

    # 檢查是否已經登入
    if request.session.get('is_admin_logged_in'):
        return render(request, "admin.html", context)  # 已登入，顯示管理員頁面
    else:
        return redirect("/admin/login/", context)  # 未登入，重定向至登入頁面

# 管理員登入功能
def admin_login(request):
    if request.method == "POST":
        acc_name = request.POST.get("acc_name")
        password = request.POST.get("password")

        try:
            # 驗證帳號和密碼
            admin = Admin.objects.get(acc_name=acc_name, password=password)
            request.session['is_admin_logged_in'] = True  # 使用 session 紀錄登入狀態
            return redirect("/admin/")  # 登入成功，重定向至 /admin
        except Admin.DoesNotExist:
            footer_info = Footer.objects.first()
            context = {
                'footer_info': footer_info,
                "error_message": "Incorrect account name or password."
            }
            return render(request, "admin_login.html", context)  # 顯示錯誤訊息
    else:
        footer_info = Footer.objects.first()
        context = {
            'footer_info': footer_info,
        }
        return render(request, "admin_login.html", context)  # 顯示登入頁面

# 管理員登出功能
def admin_logout(request):
    request.session.flush()  # 清除 session 資訊
    return redirect('/admin/')  # 登出後重定向至登入頁面

# 新增商品
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        introduction = request.POST['introduction']
        product_quantity = request.POST['product_quantity']
        product_price = request.POST['product_price']
        
        Product.objects.create(
            product_name=product_name,
            introduction=introduction,
            product_quantity=product_quantity,
            product_price=product_price
        )
        return redirect('/admin/')  # 新增成功後重定向到管理頁面

# 刪除商品
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()  # 刪除商品
    return redirect('/admin/')  # 刪除成功後重定向到管理頁面

# 編輯商品
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    footer_info = Footer.objects.first()
    context = {
        'footer_info': footer_info,
        'product': product
    }
    
    if request.method == 'POST':
        # 更新商品資訊
        product.product_name = request.POST['product_name']
        product.introduction = request.POST['introduction']
        product.product_quantity = request.POST['product_quantity']
        product.product_price = request.POST['product_price']
        product.save()  # 儲存更改
        return redirect('/admin/')  # 更新成功後重定向到管理頁面
    
    return render(request, 'edit_product.html', context)  # 顯示編輯頁面

# 新增管理員帳號
def add_account(request):
    if request.method == 'POST':
        acc_name = request.POST['acc_name']
        password = request.POST['password']
        
        # 此處應考慮使用密碼哈希
        Admin.objects.create(
            acc_name=acc_name,
            password=password
        )
        return redirect('/admin/')  # 新增成功後重定向到管理頁面

# 刪除管理員帳號
def delete_account(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    account.delete()  # 刪除帳號
    return redirect('/admin/')  # 刪除成功後重定向到管理頁面

# 編輯管理員帳號
def edit_account(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    footer_info = Footer.objects.first()
    context = {
        'footer_info': footer_info,
        'account': account
    }
    
    if request.method == 'POST':
        # 更新帳號資訊
        account.acc_name = request.POST['acc_name']
        account.password = request.POST['password']  # 此處應考慮密碼哈希
        account.save()  # 儲存更新
        return redirect('/admin/')  # 更新成功後重定向到管理頁面
    
    return render(request, 'edit_account.html', context)  # 顯示編輯頁面

# 編輯頁尾資訊
def edit_footer(request):
    footer = Footer.objects.first()  # 獲取唯一的 footer 資訊

    if request.method == 'POST':
        # 更新頁尾內容
        footer.about_us = request.POST.get('about_us')
        footer.contact_us = request.POST.get('contact_us')
        footer.save()  # 儲存更改
        return redirect('/admin/')  # 更新成功後重定向到管理頁面

    return render(request, 'admin_page.html', {'footer': footer})  # 顯示編輯頁面

# 處理訂單並更新庫存
def process_order(request):
    try:
        data = json.loads(request.body)  # 接收購物車數據
        products = data.get("products", [])

        for product in products:
            product_name = product.get("name")
            quantity_purchased = int(product.get("quantity"))
            
            # 查詢並更新產品庫存
            prod = Product.objects.get(product_name=product_name)
            if prod.product_quantity >= quantity_purchased:
                prod.product_quantity -= quantity_purchased
                prod.save()
            else:
                return JsonResponse({"status": "failed", "message": f"{prod.product_name} 的庫存不足"}, status=400)

        return JsonResponse({"status": "success", "message": "庫存已更新，交易成功"})
    except Product.DoesNotExist:
        return JsonResponse({"status": "failed", "message": "無此商品"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "failed", "message": str(e)}, status=500)
