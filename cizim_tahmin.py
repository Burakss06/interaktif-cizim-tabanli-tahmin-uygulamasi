# Başlangıç Kodu
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import random


class CizimTahminArayuzu:
    """
    Makine Öğrenimi modelleri için veri toplama ve ön işleme (preprocessing)
    işlemlerini simüle eden interaktif çizim arayüzü.

    Mevcut durum : model.predict() yerine rastgele sınıf döndürülüyor.
    İleride      : veriyi_on_isle() çıktısı gerçek modele verilecek.
    """

    SINIFLAR = [
        "Kedi", "Köpek", "Ev", "Araba", "Bisiklet",
        "Elma", "Ağaç", "Güneş", "Balık", "Yıldız",
    ]
    ONIZLEME_PX = 140

    def __init__(self, pencere: tk.Tk):
        self.pencere = pencere
        self.pencere.title("CNN — Çizim Tanıma Simülatörü")
        self.pencere.resizable(False, False)
        self.pencere.configure(bg="#1e1e2e")

        self.tuval_boyutu = 360
        self.model_girdi  = 28

        self.sanal_resim = Image.new("RGB", (self.tuval_boyutu, self.tuval_boyutu), "white")
        self.cizici      = ImageDraw.Draw(self.sanal_resim)
        self.onceki_x    = None
        self.onceki_y    = None
        self.tk_gorsel   = None

        self._arayuzu_olustur()

    def _arayuzu_olustur(self):
        PAD = 20

        # Sol: çizim alanı
        sol = tk.Frame(self.pencere, bg="#1e1e2e")
        sol.pack(side=tk.LEFT, padx=(PAD, 12), pady=PAD)

        tk.Label(sol, text="Çizim Alanı",
                 font=("Consolas", 11, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", pady=(0, 6))

        cerceve = tk.Frame(sol, bg="#89b4fa", padx=2, pady=2)
        cerceve.pack()

        self.tuval = tk.Canvas(cerceve,
                               width=self.tuval_boyutu, height=self.tuval_boyutu,
                               bg="white", cursor="pencil", highlightthickness=0)
        self.tuval.pack()
        self.tuval.bind("<Button-1>",        self.cizime_basla)
        self.tuval.bind("<B1-Motion>",       self.cizimi_surdur)
        self.tuval.bind("<ButtonRelease-1>", self.cizimi_bitir)

        # ── Sağ: kontrol paneli ───────────────
        sag = tk.Frame(self.pencere, bg="#1e1e2e")
        sag.pack(side=tk.RIGHT, padx=(12, PAD), pady=PAD, fill=tk.Y)

        tk.Label(sag, text="Ön İşlenmiş Giriş (28×28)",
                 font=("Consolas", 10, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", pady=(0, 4))

        # Ön izleme: sabit piksel kutusu (pack_propagate=False çocuk label'ın
        # kutuyu genişletmesini engeller — karakter-birimi sorununu düzeltir)
        onizleme_dis = tk.Frame(sag, bg="#313244", padx=1, pady=1)
        onizleme_dis.pack(anchor="w")

        onizleme_ic = tk.Frame(onizleme_dis, bg="#11111b",
                               width=self.ONIZLEME_PX, height=self.ONIZLEME_PX)
        onizleme_ic.pack()
        onizleme_ic.pack_propagate(False)   # ← kritik

        self.veri_ekrani = tk.Label(onizleme_ic, bg="#11111b")
        self.veri_ekrani.place(x=0, y=0,
                               width=self.ONIZLEME_PX,
                               height=self.ONIZLEME_PX)

        # Sonuç kutusu
        sonuc_kont = tk.Frame(sag, bg="#181825", padx=12, pady=8)
        sonuc_kont.pack(fill=tk.X, pady=(12, 0))

        self.tahmin_etiketi = tk.Label(sonuc_kont, text="—",
                                       font=("Consolas", 22, "bold"),
                                       bg="#181825", fg="#89b4fa")
        self.tahmin_etiketi.pack()

        self.guven_etiketi = tk.Label(sonuc_kont, text="",
                                      font=("Consolas", 12, "bold"),
                                      bg="#181825", fg="#a6e3a1")
        self.guven_etiketi.pack(pady=(2, 0))

        self.bilgi_etiketi = tk.Label(sonuc_kont,
                                      text="Çizin ve tahmin ettirin.",
                                      font=("Consolas", 8),
                                      bg="#181825", fg="#6c7086",
                                      justify="center")
        self.bilgi_etiketi.pack(pady=(4, 0))

        # Butonlar
        tk.Button(sag, text="Tahmin Et",
                  command=self.tahmin_simulasyonu,
                  bg="#89b4fa", fg="#1e1e2e",
                  font=("Consolas", 10, "bold"),
                  relief=tk.FLAT, width=20, height=2,
                  cursor="hand2",
                  activebackground="#b4d0ff",
                  activeforeground="#1e1e2e").pack(pady=(10, 4))

        tk.Button(sag, text="Temizle",
                  command=self.tuvali_temizle,
                  bg="#313244", fg="#f38ba8",
                  font=("Consolas", 10, "bold"),
                  relief=tk.FLAT, width=20, height=2,
                  cursor="hand2",
                  activebackground="#45475a",
                  activeforeground="#f38ba8").pack()

    # ── Çizim ────────────────────────────────
    def cizime_basla(self, event):
        self.onceki_x, self.onceki_y = event.x, event.y

    def cizimi_surdur(self, event):
        if self.onceki_x is not None:
            self.tuval.create_line(self.onceki_x, self.onceki_y, event.x, event.y,
                                   width=14, fill="black",
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
            self.cizici.line([self.onceki_x, self.onceki_y, event.x, event.y],
                             fill="black", width=14, joint="curve")
            self.onceki_x, self.onceki_y = event.x, event.y

    def cizimi_bitir(self, event):
        self.onceki_x = self.onceki_y = None

    def tuvali_temizle(self):
        self.tuval.delete("all")
        self.sanal_resim = Image.new("RGB", (self.tuval_boyutu, self.tuval_boyutu), "white")
        self.cizici      = ImageDraw.Draw(self.sanal_resim)
        self.veri_ekrani.config(image="")
        self.tk_gorsel   = None
        self.tahmin_etiketi.config(text="—",  fg="#89b4fa")
        self.guven_etiketi.config( text="")
        self.bilgi_etiketi.config( text="Çizin ve tahmin ettirin.")

    # ── Ön işleme ────────────────────────────
    def veriyi_on_isle(self) -> np.ndarray:
        """
        1. 28×28'e yeniden boyutlandır
        2. Gri tonlamaya çevir (Grayscale)
        3. Rengi ters çevir  → siyah zemin, beyaz çizgi
        4. [0, 1] aralığına normalize et
        """
        kucuk  = self.sanal_resim.resize((self.model_girdi, self.model_girdi)).convert("L")
        matris = 255 - np.array(kucuk)

        gorsel = Image.fromarray(matris).resize(
            (self.ONIZLEME_PX, self.ONIZLEME_PX), Image.NEAREST)
        self.tk_gorsel = ImageTk.PhotoImage(image=gorsel)
        self.veri_ekrani.config(image=self.tk_gorsel)

        return matris / 255.0

    # ── Tahmin simülasyonu ────────────────────
    def tahmin_simulasyonu(self):
        """
        TODO: sahte_tahmin satırını  model.predict(veri.reshape(1,28,28,1))  ile değiştir.
        """
        veri = self.veriyi_on_isle()

        # ── İleride buraya gerçek model gelecek ──────────────────────────
        sahte_tahmin = random.choice(self.SINIFLAR)
        sahte_guven  = random.randint(42, 97)
        # ─────────────────────────────────────────────────────────────────

        renk = ("#a6e3a1" if sahte_guven >= 75 else
                "#f9e2af" if sahte_guven >= 55 else
                "#fab387")

        self.tahmin_etiketi.config(text=sahte_tahmin,            fg=renk)
        self.guven_etiketi.config( text=f"%{sahte_guven} güven", fg=renk)
        self.bilgi_etiketi.config(
            text=f"shape={veri.shape}  |  dtype={veri.dtype}\n"
                 f"min={veri.min():.2f}  max={veri.max():.2f}")


if __name__ == "__main__":
    kutu = tk.Tk()
    CizimTahminArayuzu(kutu)
    kutu.mainloop()
# Başlangıç Kodunun Sonu
