import json
import requests
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
import threading
import os

app = Flask(__name__)

# Sabitler (Constants)
DEFAULT_PRODUCT_COUNT = 24
DEFACTO_URL = f"https://www.defacto.com.tr/Catalog/PartialIndexScrollResult?page=1&SortOrder=0&pageSize={DEFAULT_PRODUCT_COUNT}&fx_c1=1&fx_c2=1413"
TIMEOUT = 15  # Bağlantı zaman aşımı süresi (saniye)
EXCEL_FILE_NAME = "urunler.xlsx"

# Global değişkenler
old_products = pd.DataFrame()
products = []

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
            color: #343a40; /* Genel metin rengi */
        }
        .container {
            max-width: 1200px; /* Maksimum genişlik */
            margin: 0 auto; /* Ortalamak için */
            padding: 20px; /* İç boşluk */
        }
        h1, h2 {
            color: #2c3e50; /* Daha belirgin başlık rengi */
            text-align: center;
            margin-bottom: 30px;
        }
        /* Form ve buton stilleri */
        .form-group {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            justify-content: center; /* Yatayda ortala */
        }
        .form-group label {
            margin-right: 10px;
            font-weight: bold; /* Etiketi daha belirgin yap */
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
            justify-content: center; /* Butonları ortala */
            margin-bottom: 20px;
        }
        button {
            background-color: #3498db; /* Canlı mavi buton rengi */
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin: 0 5px;
            transition: background-color 0.3s ease; /* Geçiş efekti */
        }
        button:hover {
            background-color: #2980b9; /* Hover efekti için daha koyu mavi */
        }
        button:active {
            background-color: #2471a3; /* Tıklandığında daha da koyu mavi */
        }
         #message {
          margin-top: 10px;
          margin-bottom: 10px;
          padding: 10px;
          border-radius: 4px;
          font-weight: bold;
          text-align: center;
          color: #27ae60; /* Mesaj rengi */
          background-color: #dff0d8; /* Mesaj arka planı */
          border: 1px solid #d0e9c6; /* Kenarlık */
        }
        /* Tablo stilleri */
        table {
            border-collapse: collapse;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Daha belirgin gölge */
            border-radius: 8px;
            overflow: hidden;
            margin-top: 20px; /* Tablo için üst boşluk */
        }
        th, td {
            text-align: left;
            padding: 15px;
            border-bottom: 1px solid #e0e0e0; /* Daha açık çizgi */
        }
        th {
            background-color: #34495e; /* Başlık arka planı */
            color: white;
            font-weight: bold; /* Başlıkları kalınlaştır */
        }
        tr:nth-child(even) {
            background-color: #f9f9f9; /* Çift satır arka plan rengi */
        }
         tr:hover {
            background-color: #ecf0f1; /* Hover rengi */
        }
        .error {
            color: red;
            text-align: center;
             margin-top: 10px;
             margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Defacto İndirimli Ürünler</h1>
        <div class="form-group">
            <label for="product_count">Kaç ürün çekmek istersiniz?</label>
            <input type="number" id="product_count" name="product_count" value="24">
        </div>
         <div class="button-group">
            <button onclick="fetchData()">İndirimli Ürünleri Çek</button>
            <button onclick="saveToExcel()">Excel'e Kaydet</button>
            <button onclick="checkForDiscounts()">İndirimleri Kontrol Et</button>
        </div>
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
        function fetchData() {
            var productCount = document.getElementById("product_count").value;
            document.getElementById("message").innerHTML = "Veriler çekiliyor...";
            fetch('/fetch_data?product_count=' + productCount)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("message").innerHTML = data.message;
                    var productList = document.getElementById("product_list");
                    productList.innerHTML = ""; // Önceki ürünleri temizle
                    data.products.forEach(product => {
                        var row = productList.insertRow();
                        var cell1 = row.insertCell();
                        var cell2 = row.insertCell();
                        var cell3 = row.insertCell();
                        cell1.innerHTML = product.name;
                        cell2.innerHTML = product.discount;
                        cell3.innerHTML = product.normalPrice;
                    });
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
            fetch('/check_for_discounts')
                .then(response => response.json())
                .then(data => {
                    document.getElementById("message").innerHTML = data.message;
                })
                .catch(error => {
                    document.getElementById("message").innerHTML = "Hata: " + error;
                });
        }
    </script>
</body>
</html>
"""

# Dosya yükleme formunu içeren HTML şablonu (AYNI KALDI)
UPLOAD_FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Excel Yükle</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            color: #343a40;
            margin-bottom: 20px;
        }
        form {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        input[type="file"] {
            margin-bottom: 15px;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        #message {
            margin-top: 20px;
            text-align: center;
            color: #28a745;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Excel Dosyası Yükle</h1>
    <form method="POST" enctype="multipart/form-data" action="/upload_excel">
        <input type="file" name="file">
        <input type="submit" value="Yükle">
    </form>
    <p id="message"></p>
    <script>
      document.querySelector('form').addEventListener('submit', function(e) {
          e.preventDefault();
          var formData = new FormData(this);
          document.getElementById("message").innerHTML = "Dosya yükleniyor...";
          fetch('/upload_excel', {
              method: 'POST',
              body: formData
          })
          .then(response => response.json())
          .then(data => {
              document.getElementById("message").innerHTML = data.message;
          })
          .catch(error => {
              document.getElementById("message").innerHTML = "Hata: " + error;
          });
      });
    </script>
</body>
</html>
"""

# Ana sayfa
@app.route("/")
def index():
    return HTML_TEMPLATE

# Veri çekme fonksiyonu
@app.route("/fetch_data")
def fetch_data():
    global products
    try:
        max_products = int(request.args.get('product_count', DEFAULT_PRODUCT_COUNT))
        url = DEFACTO_URL.replace(f"pageSize={DEFAULT_PRODUCT_COUNT}", f"pageSize={max_products}")
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
        url = DEFACTO_URL.replace(f"pageSize={DEFAULT_PRODUCT_COUNT}", f"pageSize={max_products}")
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
            if campaign and "DiscountAmount" in campaign:
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

@app.route('/upload')
def upload_form():
    return UPLOAD_FORM_HTML

if __name__ == "__main__":
    # Uygulamayı ayrı bir iş parçacığında (thread) çalıştır
    def run_app():
        app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)

    thread = threading.Thread(target=run_app)
    thread.daemon = True  # Ana iş parçacığı sonlandığında bu iş parçacığının da sonlanmasını sağla
    thread.start()

    # Pydroid3'te ana iş parçacığının çalışmaya devam etmesini sağlamak için bir döngü ekleyin
    # (Aksi takdirde uygulama hemen kapanır)
    while True:
        import time
        time.sleep(1)
