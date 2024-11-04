import json
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import *

def front_page(request):
    footer_info = Footer.objects.first() 

    return render(request, 'front_page.html', {'footer_info': footer_info})

def all_products(request):
    footer_info = Footer.objects.first()  

    # 查詢所有商品資料
    products = Product.objects.all()
    
    # 將商品資料和 footer_info 都傳遞到模板中
    context = {
        'products': products,
        'footer_info': footer_info
    }
    
    return render(request, 'all_products.html', context)

def shopcart(request):
    footer_info = Footer.objects.first()  
    
    # 將商品資料和 footer_info 都傳遞到模板中
    context = {
        'footer_info': footer_info
    }
    
    return render(request, 'shopcart.html', context)

def admin_page(request):
    footer_info = Footer.objects.first()  # footer_info
    products = Product.objects.all()  # 獲取所有商品
    admin_accounts = Admin.objects.all()
    context = {
        'footer_info': footer_info,
        'products': products,
        'accounts' : admin_accounts
    }

    # 檢查是否已經登入
    if request.session.get('is_admin_logged_in'):
        return render(request, "admin.html", context)  # 顯示管理員頁面
    else:
        # 如果未登入，顯示登入頁面
        return redirect("/admin/login/",context)

def admin_login(request):
    if request.method == "POST":
        acc_name = request.POST.get("acc_name")
        password = request.POST.get("password")

        # 驗證 acc_name 和 password 是否正確
        try:
            admin = Admin.objects.get(acc_name=acc_name, password=password)
            # 使用 session 紀錄登入狀態
            request.session['is_admin_logged_in'] = True
            return redirect("/admin/")  # 登入成功後重定向至 /admin
        except Admin.DoesNotExist:
            # 如果帳號或密碼錯誤，顯示錯誤訊息
            footer_info = Footer.objects.first()  
            context = {
                'footer_info': footer_info,
                "error_message": "Incorrect account name or password."
            }

            return render(request, "admin_login.html", context)
    else:
        footer_info = Footer.objects.first()  
        context = {
            'footer_info': footer_info,
        }
        return render(request, "admin_login.html", context)  # 顯示登入頁面

def admin_logout(request):
    request.session.flush()  # 清除 session 資訊
    return redirect('/admin/')  # 登出後重定向至登入頁面

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
        return redirect('/admin/')
    
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('/admin/')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    footer_info = Footer.objects.first()
    context = {
        'footer_info': footer_info,
        'product': product
    }
    if request.method == 'POST':
        product.product_name = request.POST['product_name']
        product.introduction = request.POST['introduction']
        product.product_quantity = request.POST['product_quantity']
        product.product_price = request.POST['product_price']
        product.save()
        return redirect('/admin/')
    
    return render(request, 'edit_product.html', context)  # 創建 edit_product.html 以便編輯

def add_account(request):
    if request.method == 'POST':
        acc_name = request.POST['acc_name']
        password = request.POST['password']
        
        # 如果需要，您可以在這裡添加密碼的哈希處理
        Admin.objects.create(
            acc_name=acc_name,
            password=password  # 這裡應考慮使用 hashed_password
        )
        return redirect('/admin/')  # 成功後重定向到管理頁面

def delete_account(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    account.delete()  # 刪除帳號
    return redirect('/admin/')  # 成功後重定向到管理頁面

def edit_account(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    footer_info = Footer.objects.first()
    context = {
        'footer_info': footer_info,
        'account': account
    }
    
    if request.method == 'POST':
        account.acc_name = request.POST['acc_name']
        account.password = request.POST['password']  # 這裡應考慮使用 hashed_password
        account.save()  # 儲存更新
        return redirect('/admin/')  # 成功後重定向到管理頁面
    
    return render(request, 'edit_account.html', context)  # 返回編輯頁面

def edit_footer(request):
    # 獲取唯一的 footer 資料
    footer = Footer.objects.first()

    if request.method == 'POST':
        # 更新 about_us 和 contact_us 資訊
        footer.about_us = request.POST.get('about_us')
        footer.contact_us = request.POST.get('contact_us')
        footer.save()
        return redirect('/admin/')

    # 如果是 GET 請求，顯示當前的 footer 資訊
    return render(request, 'admin_page.html', {'footer': footer})

def process_order(request):
    try:
        # 接收購物車數據
        data = json.loads(request.body)
        products = data.get("products", [])

        # 更新每個產品的庫存
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
    