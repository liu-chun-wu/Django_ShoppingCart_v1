網路與資料庫程式設計期中project
===
題目 : 簡易購物網站
---
# 功能說明
- 網站上方有導覽列，分別為首頁,所有商品,購物車,管理員登入，按下按鈕會到相對應的頁面:
    - 所有商品 : 列出所有商品及其資訊(介紹、名稱、價格、數量)
    - 購物車 : 列出顧客已經選購的商品，可以結帳(會減少商品庫存)和清空購物車
    - 後台登入 : 管理員可以登入後台修改商品、帳號、footer

# 實作技術
- 框架 : Django
- 語言 : Python
- 資料表 : 
  - admin   : acc_name(unique),password -- 帳號名稱,密碼
  - product : introduction,product_name(unique),product_quantity,product_price -- 產品介紹,名稱,數量,價格
  - footer  : about_us,contact_us -- 頁尾資訊,關於我們,聯絡我們
- 其他概念:
    1. html(網頁架構),css(排版、顏色等等),javascript(互動性功能)
    2. cookie(購物車)、session(登入狀態)
    3. 後台路徑管制: 利用session檢查登入狀態，如果沒登入就導到登入頁面，無法直接用/admin進去
    4. 結帳功能 : AJAX
        1. 獲取 CSRF Token: 確保在 AJAX 請求中傳遞 CSRF token
        2. 發送請求: 當用戶按下結帳按鈕時，構建包含所選商品的 JSON 請求，並將其發送到後端 API。
        3. 處理響應: 根據後端返回的狀態顯示適當的消息。
