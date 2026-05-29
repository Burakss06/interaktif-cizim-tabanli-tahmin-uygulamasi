# tahmin_motoru.py
import os
import numpy as np
import tensorflow as tf
from PIL import Image

class TahminMotoru:
    def __init__(self):
        # prepare_dataset.py dosyasındaki tam sıralama (önemli!)
        # 0 -> cat, 1 -> house, 2 -> car, 3 -> apple, 4 -> sun
        # Kullanıcıya Türkçe göstermek için burayı Türkçe yapıyoruz ama sıra bozulmamalı.
        self.siniflar = ["Kedi", "Ev", "Araba", "Elma", "Güneş"]
        
        model_yolu = "quickdraw_model.keras"
        
        if os.path.exists(model_yolu):
            print("Yapay zeka modeli başarıyla yükleniyor...")
            self.model = tf.keras.models.load_model(model_yolu)
            print("Model yükleme tamamlandı! Tahmine hazır.")
        else:
            raise FileNotFoundError(f"Hata: '{model_yolu}' dosyası bulunamadı! Lütfen dosyanın main.py ile aynı yerde olduğundan emin olun.")

    def tahmin_et(self, arayuz_resmi):
        """
        Arayüzden (ekrandan) gelen çizimi alır, yapay zekanın anlayacağı
        28x28 formatına getirir ve gerçek tahmini döndürür.
        """
        # 1. Çizilen resmi yapay zekanın eğitim boyutuna (28x28) küçült ve Gri Tonlamaya (L) çevir
        kucuk_resim = arayuz_resmi.resize((28, 28)).convert("L")
        
        # 2. Resmi sayı matrisine (numpy array) dönüştür
        matris = np.array(kucuk_resim)
        
        # KRİTİK ADIM: Renkleri Tersine Çevirme (Invert)
        # Kullanıcı arayüzde BEYAZ arka plana SİYAH kalemle çizer (Pikseller: Arka plan 255, Çizim 0).
        # Ama Google Quick Draw verisi SİYAH arka plana BEYAZ çizimdir (Arka plan 0, Çizim 255).
        # Eğer bu tersine çevirmeyi yapmazsak model saçmalar.
        matris = 255 - matris
        
        # 3. Normalizasyon: Sayıları 0-255 arasından 0.0 - 1.0 arasına getir 
        matris = matris.astype("float32") / 255.0
        
        # 4. Boyut Ekleme: Tek bir resmi modelin beklediği (1, 28, 28, 1) formatına sokuyoruz
        # (1 adet resim, 28 genişlik, 28 yükseklik, 1 renk kanalı)
        model_girisi = matris.reshape(1, 28, 28, 1)
        
        # 5. GERÇEK YAPAY ZEKA TAHMİNİ
        tahminler = self.model.predict(model_girisi, verbose=0) # verbose=0 terminali kirletmesin diye
        
        # En yüksek olasılığa sahip sınıfın indeksini bul (Örn: 2 çıktıysa 'Araba')
        en_yuksek_indeks = np.argmax(tahminler[0])
        
        # Güven oranını yüzdeye çevir (Örn: 0.89 -> %89)
        guven_orani = int(tahminler[0][en_yuksek_indeks] * 100)
        
        tahmin_edilen_etiket = self.siniflar[en_yuksek_indeks]
        
        return tahmin_edilen_etiket, guven_orani, matris