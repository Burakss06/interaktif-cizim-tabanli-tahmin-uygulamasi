# İnteraktif Çizim Tabanlı Tahmin Uygulaması (Interactive Drawing-Based Prediction Application)

Bu proje, **Bursa Uludağ Üniversitesi Mühendislik Fakültesi Bilgisayar Mühendisliği Bölümü Python Programlamaya Giriş Dersi (2026)** kapsamında hazırlanmış final projesidir. 

Proje, Google'ın **Quick Draw** veri setini kullanarak eğittiği bir **Evrişimli Sinir Ağı (CNN - Convolutional Neural Network)** modeli ile kullanıcının arayüzde çizdiği resimleri gerçek zamanlı olarak sınıflandıran interaktif bir masaüstü uygulamasıdır.

---

## 🚀 Proje Özellikleri

* **Gerçek Zamanlı Sınıflandırma:** Kullanıcı çizim yaparken, çizimler arka planda eş zamanlı olarak analiz edilir ve en olası 10 sınıf arasından tahmin yapılır.
* **Modern Arayüz (GUI):** `customtkinter` kütüphanesi ile modern, karanlık mod destekli ve dinamik bir arayüz tasarlanmıştır.
* **Yapay Zeka Görselleştirmesi:** Çizimin yapay zeka modelindeki ilk evrişim (convolution) katmanındaki aktivasyon haritaları (activation maps) görselleştirilerek yapay zekanın çizimin hangi bölgelerine odaklandığı canlı olarak gösterilir.
* **Gelişmiş Ön İşleme (Preprocessing):** Çizimler otomatik olarak kırpılır, en-boy oranı korunarak kare bir matrisin ortasına yerleştirilir ve normalize edilir.
* **Yüksek Skorlar (High Scores):** Kullanıcının hızlı ve doğru tahminler yaparak puan topladığı ve bu puanların yerel olarak kaydedildiği bir mini oyun mekanizması barındırır.

---

## 🛠️ Donanım ve Yazılım Gereksinimleri

### Yazılım Gereksinimleri
* **İşletim Sistemi:** Windows, macOS veya Linux
* **Python Sürümü:** Python 3.10 veya üzeri (Python 3.13 ile test edilmiştir)
* **Temel Kütüphaneler:** TensorFlow/Keras, NumPy, Pillow (PIL), CustomTkinter, Matplotlib

### Donanım Gereksinimleri
* **İşlemci:** Intel Core i3 / AMD Ryzen 3 veya daha iyi işlemci
* **Bellek (RAM):** Minimum 4 GB RAM (Eğitim için 8 GB tavsiye edilir)
* **Depolama:** Minimum 3 GB boş disk alanı (Veri setleri ve eğitilmiş modeller için)

---

## 📦 Kurulum Adımları

1. **Projeyi Klonlayın veya İndirin:**
   ```bash
   git clone <github-repo-linki>
   cd interaktif-cizim-tabanli-tahmin-uygulamasi-main
   ```

2. **Sanal Ortam Oluşturun (Tavsiye Edilir):**
   ```bash
   python -m venv venv
   # Windows için:
   .\venv\Scripts\activate
   # macOS/Linux için:
   source venv/bin/activate
   ```

3. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📂 Klasör Yapısı

```text
interaktif-cizim-tabanli-tahmin-uygulamasi-main/
│
├── data/
│   ├── raw/                  # Google Quick Draw ham .npy dosyaları (cat.npy, house.npy vb.)
│   └── processed/            # prepare_dataset.py ile üretilen eğitim/test verileri (X_train.npy vb.)
│
├── main.py                   # Uygulamanın ana giriş noktası (arayüzü başlatır)
├── arayuz.py                 # CustomTkinter arayüz bileşenleri ve çizim tahtası mantığı
├── tahmin_motoru.py          # Çizimleri ön-işleme, normalize etme ve model tahmini
├── prepare_dataset.py        # Ham verileri okuyup normalize ederek eğitim setini hazırlayan betik
├── train_model.py            # CNN model mimarisini kurup eğiten betik (train_model dosyası .py olarak da kullanılabilir)
├── visualize_samples.py      # Eğitim verilerinden örnekleri görselleştiren test aracı
├── quickdraw_model.keras     # Eğitilmiş Keras model dosyası (Yaklaşık 93.5% doğruluk oranına sahip)
├── high_scores.json          # Arayüzdeki oyun skorlarının yerel olarak kaydedildiği dosya
├── requirements.txt          # Gerekli bağımlılıklar listesi
├── LICENSE                   # Proje lisans dosyası
└── README.md                 # Proje açıklama ve kurulum dosyası (Bu dosya)
```

---

## 📊 Veri Seti ve Hazırlanması

Projede Google Quick Draw datasetinin `numpy_bitmap` formatındaki `.npy` dosyaları kullanılmıştır. 

### Kullanılan 10 Sınıf:
1. Kedi (cat)
2. Ev (house)
3. Araba (car)
4. Elma (apple)
5. Güneş (sun)
6. Kuş (bird)
7. Ağaç (tree)
8. Bisiklet (bicycle)
9. Balık (fish)
10. Çiçek (flower)

### Veri Seti İndirme Linki:
Ham veri setlerine Google Cloud Storage üzerinden erişebilirsiniz:
[Google Quick Draw Dataset - numpy_bitmap](https://console.cloud.google.com/gstorage/browser/quickdraw_dataset/full/numpy_bitmap)

### Verileri Hazırlama ve Model Eğitme Adımları:
1. `data/raw/` adında bir klasör oluşturun ve yukarıdaki linkten indirdiğiniz 10 sınıfın `.npy` dosyalarını bu klasöre kaydedin (Örn: `cat.npy`, `house.npy` vb.).
2. Veri hazırlama betiğini çalıştırın:
   ```bash
   python prepare_dataset.py
   ```
   *Bu betik her sınıftan 3000 örnek çeker, 28x28x1 formatına getirir, normalize eder ve %80 eğitim - %20 test verisi olarak `data/processed/` klasörüne kaydeder.*
   
3. Model eğitimi başlatın:
   ```bash
   python train_model.py
   ```
   *Bu betik CNN modelini kurar, 20 epoch boyunca eğitir ve modeli `quickdraw_model.keras` adıyla kaydeder.*

---

## 💻 Uygulamayı Çalıştırma

Model eğitildikten veya `quickdraw_model.keras` ana dizine yerleştirildikten sonra arayüzü başlatmak için şu komutu çalıştırın:

```bash
python main.py
```

---

## 🔬 Model Mimarisi ve Doğruluk (Accuracy)

Projede uygulanan Evrişimli Sinir Ağı (CNN) yapısı:
* **Conv2D (32 filtre, 3x3)** + MaxPooling (2x2) + Dropout (0.25)
* **Conv2D (64 filtre, 3x3)** + MaxPooling (2x2) + Dropout (0.25)
* **Flatten** + Dense (128) + Dropout (0.5)
* **Dense (10, Softmax çıktısı)**

Model **20 Epoch** sonunda test setinde **%93.58 doğruluk (accuracy)** oranına ulaşmıştır.

---

## 👥 Proje Ekibi & Görev Dağılımı

*(Formda belirtilen görev dağılımı doğrultusunda burayı doldurunuz)*
* **Öğrenci 1:** [Numara - İsim Soyisim] - Model Eğitimi, Tahmin Motoru & Veri Ön İşleme
* **Öğrenci 2:** [Numara - İsim Soyisim] - GUI Geliştirme (CustomTkinter), Raporlama & Dokümantasyon

---
*Bu proje Bursa Uludağ Üniversitesi Bilgisayar Mühendisliği Python Programlama Dersi final projesi teslim kurallarına uygun olarak hazırlanmıştır.*
