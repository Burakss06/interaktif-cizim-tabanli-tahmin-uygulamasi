import tkinter as tk
import numpy as np
import random
import os

from PIL import Image, ImageDraw, ImageTk
from tahmin_motoru import tahmin_motoru  # Diğer dosyayı içeri aktarıyoruz

class CizimTahminArayuzu:
    ONIZLEME_PX = 140

    def __init__(self, pencere: tk.Tk):
        self.pencere = pencere
        self.pencere.title("CNN — Çizim Tanıma Simülatörü")
        self.pencere.resizable(False, False)
        self.pencere.configure(bg="#1e1e2e")

        self.tuval_boyutu = 360
        
        # Model yardımcısını buraya bağlıyoruz
        self.ai = tahmin_motoru()

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

        # Sağ: kontrol paneli
        sag = tk.Frame(self.pencere, bg="#1e1e2e")
        sag.pack(side=tk.RIGHT, padx=(12, PAD), pady=PAD, fill=tk.Y)

        tk.Label(sag, text="Ön İşlenmiş Giriş (28×28)",
                 font=("Consolas", 10, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(anchor="w", pady=(0, 4))

        onizleme_dis = tk.Frame(sag, bg="#313244", padx=1, pady=1)
        onizleme_dis.pack(anchor="w")

        onizleme_ic = tk.Frame(onizleme_dis, bg="#11111b",
                               width=self.ONIZLEME_PX, height=self.ONIZLEME_PX)
        onizleme_ic.pack()
        onizleme_ic.pack_propagate(False)

        self.veri_ekrani = tk.Label(onizleme_ic, bg="#11111b")
        self.veri_ekrani.place(x=0, y=0, width=self.ONIZLEME_PX, height=self.ONIZLEME_PX)

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
                  command=self.tahmin_butonuna_basildi,
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

    def tahmin_butonuna_basildi(self):
        # Orijinal resmi model yardımcısına gönderip sonuçları alıyoruz
        tahmin, guven, matris = self.ai.tahmin_et(self.sanal_resim)

        # Gelen matrisi sağdaki küçük 28x28 önizleme kutusuna basıyoruz (UI İşlemi)
        gorsel_matris = (matris * 255).astype(np.uint8)
        gorsel = Image.fromarray(gorsel_matris).resize(
            (self.ONIZLEME_PX, self.ONIZLEME_PX), Image.NEAREST)
        self.tk_gorsel = ImageTk.PhotoImage(image=gorsel)
        self.veri_ekrani.config(image=self.tk_gorsel)

        # Renkleri güven oranına göre ayarlıyoruz
        renk = ("#a6e3a1" if guven >= 75 else
                "#f9e2af" if guven >= 55 else
                "#fab387")

        # Ekrana yazdırma işlemleri
        self.tahmin_etiketi.config(text=tahmin,            fg=renk)
        self.guven_etiketi.config( text=f"%{guven} güven", fg=renk)
        self.bilgi_etiketi.config(
            text=f"shape={matris.shape}  |  dtype={matris.dtype}\n"
                 f"min={matris.min():.2f}  max={matris.max():.2f}")