# tahmin_motoru.py
import os
import numpy as np
import tensorflow as tf
from PIL import Image

class TahminMotoru:
    def __init__(self):
        # prepare_dataset.py dosyasındaki tam sıralama önemli
        # Kullanıcıya Türkçe göstermek için burayı Türkçe yapıyoruz ama sıra ASLA bozulmamalı.
        self.siniflar = [
            "Kedi",     # 0
            "Ev",       # 1
            "Araba",    # 2
            "Elma",     # 3
            "Güneş",    # 4
            "Kuş",      # 5
            "Ağaç",     # 6
            "Bisiklet", # 7
            "Balık",    # 8
            "Çiçek"     # 9
        ]
        
        model_yolu = "quickdraw_model.keras"
        
        if os.path.exists(model_yolu):
            print("Yapay zeka modeli başarıyla yükleniyor...")
            self.model = tf.keras.models.load_model(model_yolu)
            try:
                # Modeli sahte veriyle bir kere çalıştırarak Keras'ın modeli ısıtmasını/hazırlamasını sağlıyoruz.
                self.model(np.zeros((1, 28, 28, 1)))
            except Exception:
                pass
            print("Model yükleme tamamlandı! Tahmine hazır.")
        else:
            raise FileNotFoundError(f"Hata: '{model_yolu}' dosyası bulunamadı! Lütfen dosyanın main.py ile aynı yerde olduğundan emin olun.")

    def crop_and_pad_to_square(self, img, padding_ratio=0.15, min_size=80):
        """
        Çizimi otomatik olarak kırpar, en-boy oranını bozmadan 
        kare bir tuvalin ortasına yerleştirir ve kenar payı (padding) ekler.
        Böylece çizim boyutu ve konumundan bağımsız yüksek başarı elde edilir.
        """
        gray = img.convert("L")
        arr = np.array(gray)
        inv = 255 - arr
        
        # Çizim piksellerini bul (eşik değeriyle hafif gürültüleri filtrele)
        non_zero = np.argwhere(inv > 20)
        if len(non_zero) == 0:
            return img
            
        ymin, xmin = non_zero.min(axis=0)
        ymax, xmax = non_zero.max(axis=0)
        
        h = ymax - ymin + 1
        w = xmax - xmin + 1
        
        # Çizimin merkez noktasını bul
        cy = (ymin + ymax) // 2
        cx = (xmin + xmax) // 2
        
        # Çok küçük detay veya gürültülerin aşırı büyümesini engellemek için limit koy
        max_dim = max(h, w)
        if max_dim < min_size:
            max_dim = min_size
            
        # Yeni merkezlenmiş kırpma alanını hesapla
        half_dim = max_dim // 2
        ymin = max(0, cy - half_dim)
        ymax = min(img.height - 1, cy + half_dim)
        xmin = max(0, cx - half_dim)
        xmax = min(img.width - 1, cx + half_dim)
        
        # Resmi kırp
        cropped = img.crop((xmin, ymin, xmax + 1, ymax + 1))
        
        h_crop = ymax - ymin + 1
        w_crop = xmax - xmin + 1
        max_crop_dim = max(h_crop, w_crop)
        
        # Kenar payı hesapla (Quick Draw veri setine benzer boşluk hissi)
        padding = int(max_crop_dim * padding_ratio)
        padding = max(8, padding) # En az 8 piksel kenar boşluğu
        
        new_size = max_crop_dim + 2 * padding
        square_img = Image.new("RGB", (new_size, new_size), "white")
        
        # Kırpılan çizimi kare tuvalin ortasına yapıştır
        paste_x = padding + (max_crop_dim - w_crop) // 2
        paste_y = padding + (max_crop_dim - h_crop) // 2
        
        square_img.paste(cropped, (paste_x, paste_y))
        return square_img

    def tahmin_et(self, arayuz_resmi):
        """
        Arayüzden (ekrandan) gelen çizimi alır, yapay zekanın anlayacağı
        28x28 formatına getirir ve gerçek tahmini döndürür.
        """
        # 1. Çizimi otomatik kırp, ortala ve hizala
        islenmis_resim = self.crop_and_pad_to_square(arayuz_resmi, min_size=80)
        
        # 2. Yapay zekanın eğitim boyutuna (28x28) küçült ve Gri Tonlamaya (L) çevir
        kucuk_resim = islenmis_resim.resize((28, 28), Image.Resampling.BILINEAR).convert("L")
        
        # 2. Resmi sayı matrisine (numpy array) dönüştür
        matris = np.array(kucuk_resim)
        
        # KRİTİK ADIM: Renkleri Tersine Çevirme (Invert)
        # Kullanıcı arayüzde BEYAZ arka plana SİYAH kalemle çizer (Pikseller: Arka plan 255, Çizim 0).
        # Ama Google Quick Draw verisi SİYAH arka plana BEYAZ çizimdir (Arka plan 0, Çizim 255).
        # Eğer bu tersine çevirmeyi yapmazsak model saçmalar.
        matris = 255 - matris
        
        # 3. Normalizasyon: Sayıları 0-255 arasından 0.0 - 1.0 arasına getir
        # Maksimum piksel değerine bölerek (Max Normalization) fırça inceldiğinde bile çizim kontrastını %100 koruyoruz.
        max_val = matris.max()
        if max_val > 0:
            matris = matris.astype("float32") / max_val
        else:
            matris = matris.astype("float32") / 255.0
        
        # 4. Boyut Ekleme: Tek bir resmi modelin beklediği (1, 28, 28, 1) formatına sokuyoruz
        # (1 adet resim, 28 genişlik, 28 yükseklik, 1 renk kanalı)
        model_girisi = matris.reshape(1, 28, 28, 1)
        
        # 5. GERÇEK YAPAY ZEKA TAHMİNİ VE AKTİVASYON HARİTASI
        tahminler = self.model.predict(model_girisi, verbose=0)
        try:
            # İlk Conv2D katmanının çıktısını doğrudan alıyoruz (Eager Tensor -> Numpy)
            conv_out = self.model.layers[0](model_girisi).numpy()
            # conv_out shape: (1, 26, 26, 32) -> Kanalların ortalamasını alıp 2D yapıyoruz (26x26)
            act_map = np.mean(conv_out[0], axis=-1)
            # 0.0 - 1.0 arasına normalize et
            min_val = act_map.min()
            max_val = act_map.max()
            if max_val > min_val:
                act_map = (act_map - min_val) / (max_val - min_val)
            else:
                act_map = np.zeros_like(act_map)
        except Exception as e:
            # Aktivasyon haritası alınamazsa çizim matrisini geri dönüş olarak kullan
            act_map = matris
        
        # En yüksek olasılığa sahip sınıfın indeksini bul (Örn: 2 çıktıysa 'Araba')
        en_yuksek_indeks = np.argmax(tahminler[0])
        
        # Güven oranını yüzdeye çevir (Örn: 0.89 -> %89)
        guven_orani = int(tahminler[0][en_yuksek_indeks] * 100)
        
        tahmin_edilen_etiket = self.siniflar[en_yuksek_indeks]
        
        return tahmin_edilen_etiket, guven_orani, matris, tahminler[0], act_map