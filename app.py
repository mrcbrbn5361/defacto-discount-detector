import json
import requests
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
import threading
import os

app = Flask(__name__)

# Sabitler (Constants)
DEFAULT_PRODUCT_COUNT = 24
TIMEOUT = 15 # Bağlantı zaman aşımı süresi (saniye)
EXCEL_FILE_NAME = "urunler.xlsx"

# Kategori Linkleri ve ID'leri
CATEGORY_LINKS = {
 "Kadın": {
 "Tüm Kadın Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1",
 "Tişört": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1413",
 "Gömlek": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1414",
 "Bluz": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1415",
 "Elbise": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1416",
 "Pantolon": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1417",
 "Etek": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1418",
 "Şort": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1419",
 "Ceket": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1420",
 "Hırka & Triko": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1421",
 "Sweatshirt": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1422",
 "Mont": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1423",
 "Trençkot": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1718",
 "Jean": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1424",
 "Tayt": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1730",
 "Tulum": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1459",
 "İç Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1430",
 "Pijama & Ev Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1432",
 "Mayo & Bikini": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1431",
 "Büyük Beden": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1451",
 "Hamile Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1658",
 "Aksesuar": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1434",
 "Ayakkabı": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1674",
 "Çanta": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1435",
 "Spor Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1610",
 "Abiye": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=1&fx_c2=1741"
 },
 "Erkek": {
 "Tüm Erkek Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2",
 "Tişört": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1438",
 "Gömlek": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1439",
 "Polo Yaka Tişört": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1440",
 "Pantolon": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1441",
 "Şort": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1442",
 "Ceket": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1443",
 "Hırka & Triko": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1444",
 "Sweatshirt": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1445",
 "Mont": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1446",
 "Jean": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1447",
 "İç Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1449",
 "Pijama & Ev Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1450",
 "Aksesuar": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1452",
 "Ayakkabı": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1676",
 "Spor Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1611",
 "Büyük Beden": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=2&fx_c2=1672"
 },
 "Çocuk": {
 "Tüm Çocuk Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3",
 "Bebek (0-24 Ay) Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1454",
 "Kız Çocuk Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1455",
 "Erkek Çocuk Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1456",
 "İç Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1457",
 "Pijama & Ev Giyim": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1458",
 "Ayakkabı": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1678",
 "Aksesuar": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1460",
 "Okul Koleksiyonu": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1700",
 "Lisanslı Ürünler": "https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder={sortOrder}&pageSize={pageSize}&fx_c1=3&fx_c2=1733"
 }
}

# Sıralama Seçenekleri
SORT_OPTIONS = {
 "Varsayılan": 0,
 "En Düşük Fiyat": 1,
 "En Yüksek Fiyat": 2,
 "Çok Satanlar": 4,
 "Yeni Eklenenler": 5
}

# Global değişkenler
old_products = pd.DataFrame()
products = []
selected_category_link = None
selected_sort_order = 0

# HTML şablonu (index.html) - GÜNCELLENDİ
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
 <title>Defacto İndirim Takip</title>
 <style>
 body {
 font-family: 'Roboto', sans-serif;
 margin: 20px;
 background-color: #f8f9fa;
 color: #343a40;
 }
 .container {
 max-width: 1200px;
 margin: 0 auto;
 padding: 20px;
 }
 h1, h2 {
 color: #2c3e50;
 text-align: center;
 margin-bottom: 30px;
 }
 /* Form ve buton stilleri */
 .form-group {
 display: flex;
 align-items: center;
 margin-bottom: 15px;
 justify-content: center;
 }
 .form-group label {
 margin-right: 10px;
 font-weight: bold;
 }
 input[type="number"] {
 width: 80px;
 padding: 8px;
 border: 1px solid #ced4da;
 border-radius: 4px;
 text-align: center;
 }
 .button-group {
 display: flex;
 justify-content: center;
 margin-bottom: 20px;
 gap: 10px;
 }
 .button-group button {
 background-color: #3498db;
 color: white;
 padding: 12px 24px;
 border: none;
 border-radius: 6px;
 cursor: pointer;
 transition: background-color 0.3s ease;
 }
 .button-group button:hover {
 background-color: #2980b9;
 }
 .button-group button:active {
 background-color: #2471a3;
 }
 #message {
 margin-top: 10px;
 margin-bottom: 10px;
 padding: 10px;
 border-radius: 4px;
 font-weight: bold;
 text-align: center;
 color: #27ae60;
 background-color: #dff0d8;
 border: 1px solid #d0e9c6;
 }
 /* Tablo stilleri */
 table {
 border-collapse: collapse;
 width: 100%;
 box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
 border-radius: 8px;
 overflow: hidden;
 margin-top: 20px;
 }
 th, td {
 text-align: left;
 padding: 15px;
 border-bottom: 1px solid #e0e0e0;
 }
 th {
 background-color: #34495e;
 color: white;
 font-weight: bold;
 }
 tr:nth-child(even) {
 background-color: #f9f9f9;
 }
 tr:hover {
 background-color: #ecf0f1;
 }
 .error {
 color: red;
 text-align: center;
 margin-top: 10px;
 margin-bottom: 10px;
 }
 /* Dosya Yükleme Stili */
 #fileInput {
 display: none; /* Dosya seçme alanını gizle */
 }
 #upload-message {
 margin-top: 10px;
 margin-bottom: 10px;
 padding: 10px;
 border-radius: 4px;
 font-weight: bold;
 text-align: center;
 color: #27ae60;
 background-color: #dff0d8;
 border: 1px solid #d0e9c6;
 }

 /* Kategori Seçimi Stili */
 .select-group {
 display: flex;
 justify-content: center;
 margin-bottom: 20px;
 }
 .select-group select {
 padding: 10px;
 border: 1px solid #ced4da;
 border-radius: 4px;
 }
 /* Seçenek stili */
 select option {
 padding: 8px;
 }

 select option:hover {
 background-color: #e2e6ea; /* Seçenek üzerine gelindiğinde */
 }
 /* Sıralama Seçimi Stili */
 .sort-group {
 display: flex;
 justify-content: center;
 margin-bottom: 20px;
 }
 .sort-group select {
 padding: 10px;
 border: 1px solid #ced4da;
 border-radius: 4px;
 }

 </style>
</head>
<body>
 <div class="container">
 <h1>Defacto İndirimli Ürünler</h1>
 <div class="select-group">
 <label for="categorySelect">Kategori Seç:</label>
 <select id="categorySelect">
 <optgroup label="Kadın">
 {% for category, link in category_links['Kadın'].items() %}
 <option value="{{link}}">{{category}}</option>
 {% endfor %}
 </optgroup>
 <optgroup label="Erkek">
 {% for category, link in category_links['Erkek'].items() %}
 <option value="{{link}}">{{category}}</option>
 {% endfor %}
 </optgroup>
 <optgroup label="Çocuk">
 {% for category, link in category_links['Çocuk'].items() %}
 <option value="{{link}}">{{category}}</option>
 {% endfor %}
 </optgroup>
 </select>
 </div>
 <div class="sort-group">
 <label for="sortSelect">Sıralama Seç:</label>
 <select id="sortSelect">
 {% for key, value in sort_options.items() %}
 <option value="{{value}}">{{key}}</option>
 {% endfor %}
 </select>
 </div>
 <div class="form-group">
 <label for="product_count">Kaç ürün çekmek istersiniz?</label>
 <input type="number" id="product_count" name="product_count" value="24">
 </div>
 <div class="button-group">
 <button onclick="fetchData()">İndirimli Ürünleri Çek</button>
 <button onclick="saveToExcel()">Excel'e Kaydet</button>
 <button onclick="uploadExcel()">Excel Dosyasını Yükle</button>
 <button onclick="checkForDiscounts()">İndirimleri Kontrol Et</button>
 </div>
 <input type="file" name="file" id="fileInput">
 <p id="upload-message"></p>
 <p id="message"></p>
 <div id="products">
 <h2>Ürünler</h2>
 <table>
 <thead>
 <tr>
 <th>Ürün Adı</th>
 <th>İndirim</th>
 <th>Normal Fiyat</th>
 </tr>
 </thead>
 <tbody id="product_list">
 <!-- Ürünler buraya eklenecek -->
 </tbody>
 </table>
 </div>

 </div>

 <script>
 let selectedCategoryLink = null;
 let selectedSortOrder = 0;
 document.addEventListener('DOMContentLoaded', function() {
 const categorySelect = document.getElementById('categorySelect');
 const sortSelect = document.getElementById('sortSelect');
 selectedCategoryLink = categorySelect.value; // Default value
 selectedSortOrder = sortSelect.value;
 categorySelect.addEventListener('change', function() {
 selectedCategoryLink = this.value;
 });
 sortSelect.addEventListener('change', function() {
 selectedSortOrder = this.value;
 });
 });
 function fetchData() {
 if (!selectedCategoryLink) {
 document.getElementById("message").innerHTML = "Lütfen bir kategori seçin.";
 return;
 }

 var productCount = document.getElementById("product_count").value;
 document.getElementById("message").innerHTML = "Veriler çekiliyor...";
 fetch('/fetch_data?product_count=' + productCount + '&category_link=' + encodeURIComponent(selectedCategoryLink)+ '&sort_order=' + encodeURIComponent(selectedSortOrder))
 .then(response => response.json())
 .then(data => {
 document.getElementById("message").innerHTML = data.message;
 var productList = document.getElementById("product_list");
 productList.innerHTML = "";
 if (data.products && data.products.length > 0) {
 data.products.forEach(product => {
 var row = productList.insertRow();
 var cell1 = row.insertCell();
 var cell2 = row.insertCell();
 var cell3 = row.insertCell();
 cell1.innerHTML = product.name;
 cell2.innerHTML = product.discount;
 cell3.innerHTML = product.normalPrice;
 });
 } else{
 document.getElementById("message").innerHTML = "Seçilen kategoride indirimli ürün bulunamadı.";
 }
 })
 .catch(error => {
 document.getElementById("message").innerHTML = "Hata: " + error;
 });
 }

 function saveToExcel() {
 document.getElementById("message").innerHTML = "Excel'e kaydediliyor...";
 fetch('/save_to_excel')
 .then(response => response.json())
 .then(data => {
 document.getElementById("message").innerHTML = data.message;
 })
 .catch(error => {
 document.getElementById("message").innerHTML = "Hata: " + error;
 });
 }

 function checkForDiscounts() {
 document.getElementById("message").innerHTML = "İndirimler kontrol ediliyor...";
 fetch('/check_for_discounts?category_link=' + encodeURIComponent(selectedCategoryLink)+ '&sort_order=' + encodeURIComponent(selectedSortOrder))
 .then(response => response.json())
 .then(data => {
 document.getElementById("message").innerHTML = data.message;
 })
 .catch(error => {
 document.getElementById("message").innerHTML = "Hata: " + error;
 });
 }
 function uploadExcel() {
 document.getElementById('fileInput').click(); // Dosya seçme alanını tetikle
 }

 document.getElementById('fileInput').addEventListener('change', function() {
 var file = this.files[0];
 var formData = new FormData();
 formData.append('file', file);
 document.getElementById("upload-message").innerHTML = "Dosya yükleniyor...";
 fetch('/upload_excel', {
 method: 'POST',
 body: formData
 })
 .then(response => response.json())
 .then(data => {
 document.getElementById("upload-message").innerHTML = data.message;
 if (!data.error){
 checkForDiscounts();
 }

 })
 .catch(error => {
 document.getElementById("upload-message").innerHTML = "Hata: " + error;
 });

 });
 </script>
</body>
</html>
"""

# Dosya yükleme formu ve ana sayfa artık aynı yerde
@app.route("/")
def index():
 return render_template_string(HTML_TEMPLATE, category_links=CATEGORY_LINKS,sort_options = SORT_OPTIONS)

# Veri çekme fonksiyonu
@app.route("/fetch_data")
def fetch_data():
 global products
 try:
 max_products = int(request.args.get('product_count', DEFAULT_PRODUCT_COUNT))
 category_link = request.args.get('category_link')
 sort_order = int(request.args.get('sort_order', 0))

 if not category_link:
 return {"message": "Kategori linki bulunamadı.", "products": []}

 url = category_link.replace("{pageSize}", str(max_products)).replace("{sortOrder}",str(sort_order))

 response = requests.get(url, timeout=TIMEOUT)
 response.raise_for_status()
 api_response = response.json()
 products = filter_discounted_products(api_response, max_products)

 return {"message": "Veriler çekildi.", "products": products}
 except (ValueError, requests.exceptions.RequestException, json.JSONDecodeError) as e:
 return {"message": f"Hata: {e}", "products": []}

# Excel'e kaydetme fonksiyonu
@app.route("/save_to_excel")
def save_to_excel():
 global products
 try:
 if products:
 df = pd.DataFrame(products)
 df.to_excel(EXCEL_FILE_NAME, index=False)
 return {"message": f"Veriler {EXCEL_FILE_NAME} dosyasına kaydedildi."}
 else:
 return {"message": "Kaydedilecek veri yok.", "error": True}
 except Exception as e:
 return {"message": f"Kaydetme hatası: {e}", "error": True}

# İndirim kontrol fonksiyonu
@app.route("/check_for_discounts")
def check_for_discounts():
 global old_products
 if old_products.empty:
 return {"message": "Lütfen önce Excel dosyasını yükleyin.", "error": True}

 try:
 max_products = int(request.args.get('product_count', DEFAULT_PRODUCT_COUNT))
 category_link = request.args.get('category_link', None)
 sort_order = int(request.args.get('sort_order', 0))
 if not category_link:
 return {"message": "Lütfen bir kategori seçin.", "error": True}

 url = category_link.replace("{pageSize}", str(max_products)).replace("{sortOrder}",str(sort_order))
 response = requests.get(url, timeout=TIMEOUT)
 response.raise_for_status()
 current_products = filter_discounted_products(response.json(), max_products)

 changes_message = ""
 for old_product in old_products.to_dict('records'):
 if matching_current_product := next((p for p in current_products if p['name'] == old_product['name']), None):
 if matching_current_product['discount'] > 0:
 changes_message += (f"Ürün: {old_product['name']}\n"
 f"Eski Fiyat: {old_product['normalPrice']}\n"
 f"Güncel İndirim: {matching_current_product['discount']}\n\n")

 if changes_message:
 return {"message": changes_message}
 else:
 return {"message": "İndirim değişikliği bulunamadı."}

 except (ValueError, requests.exceptions.RequestException, json.JSONDecodeError) as e:
 return {"message": f"Hata: {e}", "error": True}
 except Exception as e:
 return {"message": f"Bir hata oluştu: {e}", "error": True}

# İndirimli ürünleri filtreleyen fonksiyon - GÜNCELLENDİ
def filter_discounted_products(api_data, max_products):
 discounted_products = []
 product_count = 0
 if "Data" in api_data and "SearchResponse" in api_data["Data"]:
 for product in api_data["Data"]["SearchResponse"]["Documents"]:
 if product_count >= max_products:
 break
 campaign = product.get("CampaignBadge")
 if campaign and campaign and "DiscountAmount" in campaign:
 discounted_products.append({
 "name": product.get("ProductName", "Unknown"),
 "discount": campaign["DiscountAmount"],
 "normalPrice": product.get("ProductPriceInclTax", 0)
 })
 product_count += 1
 return discounted_products

# Excel dosyasını yükleme fonksiyonu
@app.route('/upload_excel', methods=['POST'])
def upload_excel():
 global old_products
 try:
 if 'file' not in request.files:
 return {"message": "Dosya seçilmedi.", "error": True}
 file = request.files['file']
 if file.filename == '':
 return {"message": "Dosya seçilmedi.", "error": True}
 if file:
 old_products = pd.read_excel(file)
 if not {'name', 'normalPrice'}.issubset(old_products.columns):
 return {"message": "Excel dosyasında 'name' ve 'normalPrice' sütunları bulunamadı.", "error": True}
 return {"message": "Excel dosyası başarıyla yüklendi."}
 except Exception as e:
 return {"message": f"Excel dosyası yüklenirken bir hata oluştu: {e}", "error": True}

from flask import render_template_string

if __name__ == "__main__":
 # Uygulamayı ayrı bir iş parçacığında (thread) çalıştır
 def run_app():
 app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)

 thread = threading.Thread(target=run_app)
 thread.daemon = True # Ana iş parçacığı sonlandığında bu iş parçacığının da sonlanmasını sağla
 thread.start()

 # Pydroid3'te ana iş parçacığının çalışmaya devam etmesini sağlamak için bir döngü ekleyin
 # (Aksi takdirde uygulama hemen kapanır)
 while True:
 import time
 time.sleep(1)
