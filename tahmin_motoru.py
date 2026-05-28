import numpy as np
import random
from PIL import Image

class tahmin_motoru:
    SINIFLAR = [
        "Kedi", "Köpek", "Ev", "Araba", "Bisiklet",
        "Elma", "Ağaç", "Güneş", "Balık", "Yıldız",
    ]

    def __init__(self):
        # İleride gerçek model buraya yüklenecek:
        # from tensorflow.keras.models import load_model
        # self.model = load_model("quickdraw_model.keras")
        pass

    def tahmin_et(self, sanal_resim):
        """
        Arayüzden gelen orijinal resmi alır, yapay zekaya uygun 
        28x28 boyutuna getirir ve tahmini döndürür.
        """
        # 1. Resmi 28x28 boyutuna küçült ve gri tona (L) çevir
        kucuk = sanal_resim.resize((28, 28)).convert("L")
        
        # 2. Renkleri tersine çevir (Siyah arka plan, beyaz çizim) ve normalize et
        matris = (255 - np.array(kucuk)) / 255.0
        
        # --- ŞİMDİLİK SAHTE TAHMİN (Simülasyon) ---
        tahmin_edilen_sinif = random.choice(self.SINIFLAR)
        guven_orani = random.randint(42, 97)
        # ------------------------------------------
        
        # İleride gerçek model hazır olduğunda üstteki sahte tahmin silinecek
        # ve yerine şu kodlar gelecek:
        # model_girisi = matris.reshape(1, 28, 28, 1)
        # tahminler = self.model.predict(model_girisi)
        # indeks = np.argmax(tahminler[0])
        # tahmin_edilen_sinif = self.SINIFLAR[indeks]
        # guven_orani = int(tahminler[0][indeks] * 100)
        
        return tahmin_edilen_sinif, guven_orani, matris