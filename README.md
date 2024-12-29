# Defacto İndirim Takip Uygulaması

Bu proje, Defacto'nun web sitesinden indirimli ürünleri çekerek kullanıcıya sunan ve bu bilgileri Excel dosyasına kaydeden bir Flask uygulamasıdır. Ayrıca, daha önce kaydedilmiş ürünlerin indirim durumunu kontrol etme özelliği de bulunmaktadır. Bu proje [mrcbrbn5361/defacto-discount-detector](https://github.com/mrcbrbn5361/defacto-discount-detector) GitHub deposunda bulunmaktadır.

## Proje Detayları

-   **Python ve Flask Kullanılarak Geliştirildi:** Basit bir web arayüzü sunar.
-   **Veri Çekme:** Defacto'nun API'sinden indirimli ürünleri çeker.
-   **Excel Kaydetme:** Çekilen ürün bilgilerini Excel dosyasına kaydeder.
-   **İndirim Kontrolü:** Daha önce kaydedilen ürünlerin indirim durumunu kontrol eder.
-   **Çoklu Ortam Desteği:** Visual Studio Code, Pydroid3, Termux ve repl.it'te çalıştırılabilir.

## Gereksinimler

-   Python 3.6 veya daha yüksek bir sürümü
-   `requests`, `pandas`, `flask`, `openpyxl` kütüphaneleri
    ```bash
    pip install requests pandas flask openpyxl
    ```

## Kurulum ve Kullanım

### Visual Studio Code

1.  **Proje Klonlama:**
    *   GitHub'daki depoyu bilgisayarınıza klonlayın:
        ```bash
        git clone https://github.com/mrcbrbn5361/defacto-discount-detector.git
        ```
    *   Proje klasörüne gidin:
        ```bash
        cd defacto-discount-detector
        ```
2.  **Sanal Ortam Oluşturma (Önerilir):**
    *   Proje klasöründe bir sanal ortam oluşturun:
        ```bash
        python -m venv venv
        ```
    *   Sanal ortamı aktif hale getirin:
        *   Windows için: `venv\Scripts\activate`
        *   macOS/Linux için: `source venv/bin/activate`
3.  **Gerekli Kütüphaneleri Yükleme:**
    *   Sanal ortam aktifken, requirements.txt dosyasındaki kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Uygulamayı Çalıştırma:**
    *   Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:
    ```bash
    python app.py
    ```
    *   Uygulama çalıştığında, tarayıcınızda `http://0.0.0.0:8081` adresini ziyaret ederek arayüze erişebilirsiniz.

### Pydroid3

1.  **Pydroid3'ü Kurun:** Google Play Store'dan Pydroid3'ü indirin ve kurun.
2.  **Gerekli Kütüphaneleri Yükleyin:**
    *   Pydroid3 uygulamasını açın.
    *   PIP sekmesine tıklayın ve `requests`, `pandas`, `flask`, `openpyxl` kütüphanelerini kurun.
3.  **Proje Dosyalarını Pydroid3'e Aktarın:**
    *   GitHub'daki projeyi indirin (zip dosyası olarak) ve telefonunuza aktarın.
    *   Pydroid3'te `app.py` dosyasını açın.
4.  **Uygulamayı Çalıştırın:**
    *   Play (Çalıştır) butonuna tıklayın.
    *   Uygulama çalıştığında, tarayıcınızda `http://0.0.0.0:8081` adresini ziyaret ederek arayüze erişebilirsiniz.

### Termux

1.  **Termux'u Kurun:** Google Play Store'dan veya F-Droid'den Termux'u indirin ve kurun.
2.  **Gerekli Paketleri Yükleyin:**
    ```bash
    pkg update && pkg upgrade
    pkg install python git
    ```
3.  **Proje Klonlama:**
    ```bash
    git clone https://github.com/mrcbrbn5361/defacto-discount-detector.git
    cd defacto-discount-detector
    ```
4.  **Sanal Ortam Oluşturma (Önerilir):**
      ```bash
      python -m venv venv
      ```
    *   Sanal ortamı aktif hale getirin:
        ```bash
        source venv/bin/activate
        ```
5.  **Gerekli Kütüphaneleri Yükleme:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Uygulamayı Çalıştırın:**
    ```bash
    python app.py
    ```
    *   Uygulama çalıştığında, tarayıcınızda `http://<termux-ip>:8081` adresini ziyaret ederek arayüze erişebilirsiniz. (Termux'ta `ifconfig` komutu ile ip adresinizi öğrenebilirsiniz)

### repl.it

1.  **repl.it'e Giriş Yapın:** [repl.it](https://repl.it) adresine gidin ve bir hesabınızla giriş yapın veya yeni bir hesap oluşturun.
2.  **Yeni Bir Repl Oluşturun:**
    *   "Create +" butonuna tıklayın.
    *   "Python" şablonunu seçin.
    *   Projenize bir ad verin ve "Create repl" butonuna tıklayın.
3.  **Proje Dosyalarını Yükleyin:**
    *   GitHub deposundaki tüm proje dosyalarını ( `app.py`, `requirements.txt` vb.) repl.it'teki dosya bölümüne sürükleyip bırakarak yükleyin.
4.  **Gerekli Kütüphaneleri Yükleyin:**
    *   Sol taraftaki shell bölümüne aşağıdaki komutu yazarak gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Uygulamayı Çalıştırın:**
    *   Aynı shell bölümüne aşağıdaki komutu yazarak uygulamayı çalıştırın:
    ```bash
    python app.py
    ```
    *  Uygulama çalıştıktan sonra, repl.it tarafından sağlanan URL'yi tarayıcınızda açarak uygulamaya erişebilirsiniz. URL genellikle repl'in sağ üst köşesinde görünür.

## Kullanım

1.  **Ürün Sayısı Belirleme:** Arayüzdeki giriş kutusuna kaç ürün çekmek istediğinizi girin.
2.  **İndirimli Ürünleri Çek:** "İndirimli Ürünleri Çek" butonuna tıklayarak Defacto'dan güncel indirimli ürünleri çekin.
3.  **Excel'e Kaydet:** "Excel'e Kaydet" butonuna tıklayarak çekilen ürünleri `urunler.xlsx` dosyasına kaydedin.
4.  **İndirimleri Kontrol Et:**
    *   Önce Excel dosyasını yükleyin.
    *   "İndirimleri Kontrol Et" butonuna tıklayarak, kaydedilen ürünlerin indirim durumunda değişiklik olup olmadığını kontrol edin.

## Notlar

-   Uygulama, Defacto'nun web sitesinin yapısına bağlıdır. Site yapısındaki değişiklikler uygulamayı etkileyebilir.
-   İnternet bağlantınızın olduğundan emin olun.
-   Termux'ta uygulamayı çalıştırırken, Termux'un IP adresini tarayıcıya girmeniz gerekebilir.
-   Proje dosyaları arasında `requirements.txt` dosyası bulunmaktadır. Bu dosya, projenin çalışması için gerekli olan kütüphaneleri listeler.

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Hata düzeltmeleri, yeni özellikler veya iyileştirmeler için çekme istekleri (pull request) oluşturabilirsiniz. [Buradan](https://github.com/mrcbrbn5361/defacto-discount-detector/pulls) pull request oluşturabilirsiniz.

## Lisans

Bu proje MIT Lisansı altında yayınlanmıştır. Detaylar için [LICENSE](https://github.com/mrcbrbn5361/defacto-discount-detector/blob/main/LICENSE) dosyasına bakabilirsiniz.
