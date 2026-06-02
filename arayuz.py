import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
from PIL import Image, ImageDraw, ImageTk
from tahmin_motoru import TahminMotoru

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<Button-1>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 8
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() - 25) // 2
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Tema renklerini al
        bg = "#1e1e2e"
        fg = "#cdd6f4"
        try:
            app = self.widget.winfo_toplevel()
            if hasattr(app, "aktif_tema"):
                bg = app.aktif_tema["kutu_bg"]
                fg = app.aktif_tema["yazi_ana"]
        except Exception:
            pass

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background=bg, foreground=fg,
                         relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 10, "bold"), padx=6, pady=4)
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# 8 Gelişmiş Tema Özelleştirmesi için Catppuccin ve Retro Renk Paletleri
THEMES = {
    "Catppuccin Mocha": {
        "mode": "dark",
        "pencere_bg": "#1e1e2e",
        "kutu_bg": "#181825",
        "alan_bg": "#11111b",
        "border_renk": "#313244",
        "yazi_ana": "#cdd6f4",
        "yazi_yardimci": "#89b4fa",
        "yazi_aciklama": "#6c7086",
        "yesil": "#a6e3a1",
        "mavi": "#89b4fa",
        "mavi_hover": "#74c7ec",
        "kirmizi": "#f38ba8",
        "sari": "#f9e2af",
        "turuncu": "#fab387",
        "surface0": "#313244",
        "btn_text": "#11111b"
    },
    "Catppuccin Latte": {
        "mode": "light",
        "pencere_bg": "#eff1f5",
        "kutu_bg": "#e6e9ef",
        "alan_bg": "#dce0e8",
        "border_renk": "#ccd0da",
        "yazi_ana": "#4c4f69",
        "yazi_yardimci": "#1e66f5",
        "yazi_aciklama": "#9ca0b0",
        "yesil": "#40a02b",
        "mavi": "#1e66f5",
        "mavi_hover": "#1a5fb4",
        "kirmizi": "#d20f39",
        "sari": "#df8e1d",
        "turuncu": "#fe640b",
        "surface0": "#ccd0da",
        "btn_text": "#ffffff"
    },
    "Siberpunk (Neon)": {
        "mode": "dark",
        "pencere_bg": "#0f051d",
        "kutu_bg": "#140b24",
        "alan_bg": "#1a0f30",
        "border_renk": "#ff007f",
        "yazi_ana": "#00ffff",
        "yazi_yardimci": "#ff007f",
        "yazi_aciklama": "#a19fb0",
        "yesil": "#39ff14",
        "mavi": "#00ffff",
        "mavi_hover": "#00b3b3",
        "kirmizi": "#ff003c",
        "sari": "#ffff00",
        "turuncu": "#ff5e00",
        "surface0": "#251642",
        "btn_text": "#000000"
    },
    "Dracula": {
        "mode": "dark",
        "pencere_bg": "#282a36",
        "kutu_bg": "#21222c",
        "alan_bg": "#1e1f29",
        "border_renk": "#44475a",
        "yazi_ana": "#f8f8f2",
        "yazi_yardimci": "#bd93f9",
        "yazi_aciklama": "#6272a4",
        "yesil": "#50fa7b",
        "mavi": "#8be9fd",
        "mavi_hover": "#bd93f9",
        "kirmizi": "#ff5555",
        "sari": "#f1fa8c",
        "turuncu": "#ffb86c",
        "surface0": "#44475a",
        "btn_text": "#282a36"
    },
    "Nord": {
        "mode": "dark",
        "pencere_bg": "#2e3440",
        "kutu_bg": "#3b4252",
        "alan_bg": "#242933",
        "border_renk": "#4c566a",
        "yazi_ana": "#eceff4",
        "yazi_yardimci": "#88c0d0",
        "yazi_aciklama": "#d8dee9",
        "yesil": "#a3be8c",
        "mavi": "#81a1c1",
        "mavi_hover": "#5e81ac",
        "kirmizi": "#bf616a",
        "sari": "#ebcb8b",
        "turuncu": "#d08770",
        "surface0": "#434c5e",
        "btn_text": "#2e3440"
    },
    "Akvaryum (Ocean)": {
        "mode": "dark",
        "pencere_bg": "#0c1b2a",
        "kutu_bg": "#0f2338",
        "alan_bg": "#08121e",
        "border_renk": "#1b4965",
        "yazi_ana": "#e0f2fe",
        "yazi_yardimci": "#64dfdf",
        "yazi_aciklama": "#8ecae6",
        "yesil": "#52b788",
        "mavi": "#48cae4",
        "mavi_hover": "#0096c7",
        "kirmizi": "#e63946",
        "sari": "#ffb703",
        "turuncu": "#fb8500",
        "surface0": "#1b4965",
        "btn_text": "#0c1b2a"
    },
    "Retro Kehribar": {
        "mode": "dark",
        "pencere_bg": "#120c02",
        "kutu_bg": "#1c1405",
        "alan_bg": "#080501",
        "border_renk": "#805300",
        "yazi_ana": "#ffb000",
        "yazi_yardimci": "#ff8000",
        "yazi_aciklama": "#b37b00",
        "yesil": "#99ff33",
        "mavi": "#ffcc00",
        "mavi_hover": "#e69500",
        "kirmizi": "#ff3300",
        "sari": "#ffea00",
        "turuncu": "#ffaa00",
        "surface0": "#2e1f07",
        "btn_text": "#120c02"
    },
    "Zümrüt Ormanı": {
        "mode": "dark",
        "pencere_bg": "#0a1c15",
        "kutu_bg": "#0e261d",
        "alan_bg": "#06120e",
        "border_renk": "#1c4e3a",
        "yazi_ana": "#e6f4f0",
        "yazi_yardimci": "#2ec4b6",
        "yazi_aciklama": "#a3d9c9",
        "yesil": "#4ad66d",
        "mavi": "#2ec4b6",
        "mavi_hover": "#208b82",
        "kirmizi": "#e63946",
        "sari": "#ffb703",
        "turuncu": "#fb8500",
        "surface0": "#1b4e3b",
        "btn_text": "#0a1c15"
    },
    "Gül Yaprağı (Rose Pine)": {
        "mode": "dark",
        "pencere_bg": "#191724",
        "kutu_bg": "#1f1d2e",
        "alan_bg": "#12101a",
        "border_renk": "#403d52",
        "yazi_ana": "#e0def4",
        "yazi_yardimci": "#ebbcba",
        "yazi_aciklama": "#908caa",
        "yesil": "#9ccfd8",
        "mavi": "#c4a7e7",
        "mavi_hover": "#b38fe3",
        "kirmizi": "#eb6f92",
        "sari": "#f6c177",
        "turuncu": "#ea9a97",
        "surface0": "#2a2837",
        "btn_text": "#191724"
    },
    "Gruvbox Retro": {
        "mode": "dark",
        "pencere_bg": "#282828",
        "kutu_bg": "#3c3836",
        "alan_bg": "#1d2021",
        "border_renk": "#504945",
        "yazi_ana": "#fbf1c7",
        "yazi_yardimci": "#d65d0e",
        "yazi_aciklama": "#a89984",
        "yesil": "#b8bb26",
        "mavi": "#83a598",
        "mavi_hover": "#458588",
        "kirmizi": "#fb4934",
        "sari": "#fabd2f",
        "turuncu": "#fe8019",
        "surface0": "#504945",
        "btn_text": "#282828"
    },
    "Lavanta Bahçesi": {
        "mode": "light",
        "pencere_bg": "#f3f0fc",
        "kutu_bg": "#e8e3f7",
        "alan_bg": "#ded7f2",
        "border_renk": "#c5b9e8",
        "yazi_ana": "#4a3b70",
        "yazi_yardimci": "#7c4dff",
        "yazi_aciklama": "#8a7fa6",
        "yesil": "#00b0ff",
        "mavi": "#7c4dff",
        "mavi_hover": "#651fff",
        "kirmizi": "#ff1744",
        "sari": "#ff9100",
        "turuncu": "#ff3d00",
        "surface0": "#d1c4e9",
        "btn_text": "#ffffff"
    },
    "Buzul Kıyameti (Glacier)": {
        "mode": "dark",
        "pencere_bg": "#050e14",
        "kutu_bg": "#0b1c28",
        "alan_bg": "#03070b",
        "border_renk": "#1a3d54",
        "yazi_ana": "#e1f5fe",
        "yazi_yardimci": "#00e5ff",
        "yazi_aciklama": "#80deea",
        "yesil": "#00e676",
        "mavi": "#00b0ff",
        "mavi_hover": "#0091ea",
        "kirmizi": "#ff1744",
        "sari": "#ffea00",
        "turuncu": "#ff9100",
        "surface0": "#15354b",
        "btn_text": "#050e14"
    }
}

class CizimTahminArayuzu:
    ONIZLEME_PX = 140

    def __init__(self, pencere: ctk.CTk):
        self.pencere = pencere
        self.pencere.title("CNN — İnteraktif Çizim Tanıma")
        self.pencere.geometry("1100x700")
        self.pencere.minsize(1050, 650)
        self.pencere.resizable(True, True)
        
        self.aktif_tema = THEMES["Catppuccin Mocha"]
        self.pencere.configure(fg_color=self.aktif_tema["pencere_bg"])

        # F11 tuşu ile tam ekran geçişi
        self.pencere.bind("<F11>", self.tam_ekran_tetikle)
        self.tam_ekran_durumu = False

        self.tuval_boyutu = 360
        self.ai = TahminMotoru()

        # Serbest Çizim Ayarları (Ayrı State)
        self.serbest_kalem_kalinligi = 14
        self.serbest_silgi_kalinligi = 20
        self.serbest_firca_kalinligi = self.serbest_kalem_kalinligi
        self.serbest_secilen_renk = "black"
        self.serbest_silgi_modu = False
        
        # Mücadele Oyunu Ayarları (Ayrı State)
        self.oyun_kalem_kalinligi = 14
        self.oyun_silgi_kalinligi = 20
        self.oyun_firca_kalinligi = self.oyun_kalem_kalinligi
        self.oyun_secilen_renk = "black"
        self.oyun_silgi_modu = False
        
        self.sidebar_acik = True
        
        # Son fare konumları (Silgi halkasını güncellemek için)
        self.son_fare_x = 180
        self.son_fare_y = 180

        # Modelin besleneceği sanal (görünmez) tuval (Her zaman 500x500 sabit boyutta tutulur)
        self.sanal_boyut = 500
        self.sanal_resim = Image.new("RGB", (self.sanal_boyut, self.sanal_boyut), "white")
        self.cizici      = ImageDraw.Draw(self.sanal_resim)
        
        # Mücadele Oyunu için sanal tuval
        self.oyun_sanal_resim = Image.new("RGB", (self.sanal_boyut, self.sanal_boyut), "white")
        self.oyun_cizici      = ImageDraw.Draw(self.oyun_sanal_resim)

        self.onceki_x    = None
        self.onceki_y    = None
        self.oyun_onceki_x = None
        self.oyun_onceki_y = None
        self.tk_gorsel   = None
        self.tk_buyuk_gorsel = None
        self.tahmin_timer = None
        self.oyun_timer_id = None
        self.tuval_resize_timer = None
        self.oyun_resize_timer = None

        # Geri Al / İleri Al Hafıza Yığınları
        self.serbest_undo_stack = [self.sanal_resim.copy()]
        self.serbest_redo_stack = []
        self.oyun_undo_stack = [self.oyun_sanal_resim.copy()]
        self.oyun_redo_stack = []

        # Kısayol Tuşları (Ctrl+Z: Geri Al, Ctrl+Y: İleri Al)
        self.pencere.bind("<Control-z>", self.klavye_geri_al)
        self.pencere.bind("<Control-y>", self.klavye_ileri_al)

        self.barlar = {}
        self.yuzde_etiketleri = {}
        self.sonuc_barlar = {}
        self.sonuc_yuzde_etiketleri = {}

        # Skor, Kombo ve Zorluk Ayarları
        self.aktif_zorluk = "Orta"
        self.oyun_sure_limiti = 15
        self.oyun_skor = 0
        self.oyun_kombo = 0
        self.rekorlar = self.high_scores_yukle()
        self.konfeti_partikulleri = []
        self.konfeti_aktif = False

        self._arayuzu_olustur()
        self.temayi_uygula("Catppuccin Mocha")
        self.sayfa_sec("tuval")

        # Arka Plan Görsel Efekt Döngüleri
        self.glow_efekti_guncelle()
        self.pulse_tahmin_guncelle()

    def _arayuzu_olustur(self):
        # ==========================================
        # 1. SOL SIDEBAR PANELİ
        # ==========================================
        self.sidebar = ctk.CTkFrame(self.pencere, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.logo_lbl = ctk.CTkLabel(self.sidebar, text="🎨 Çizim AI", font=("Segoe UI", 22, "bold"))
        self.logo_lbl.rol = "logo"
        self.logo_lbl.pack(pady=(25, 5), padx=20)
        
        # Menü Açma/Kapama Butonu
        self.btn_sidebar_toggle = ctk.CTkButton(self.sidebar, text="◀ Menüyü Kapat", font=("Segoe UI", 11, "bold"), height=30,
                                                fg_color="transparent", border_width=0, command=self.sidebar_toggle)
        self.btn_sidebar_toggle.pack(pady=(5, 15), padx=15, fill="x")
        self.btn_sidebar_toggle.rol = "pasif_sekme"
        
        self.sidebar_butonlar = {}
        
        tabs = [
            ("tuval", "✏️ Serbest Çizim"),
            ("oyun", "🎮 Mücadele Oyunu"),
            ("temalar", "🎨 Tema Seçimi")
        ]
        
        for name, label in tabs:
            btn = ctk.CTkButton(self.sidebar, text=label, anchor="w", height=40, font=("Segoe UI", 12, "bold"),
                                 fg_color="transparent", command=lambda n=name: self.sayfa_sec(n))
            btn.pack(fill="x", padx=15, pady=5)
            self.sidebar_butonlar[name] = btn
            btn.rol = "pasif_sekme"

        # ToolTip'leri Ekle
        ToolTip(self.sidebar_butonlar["tuval"], "✏️ Serbest Çizim")
        ToolTip(self.sidebar_butonlar["oyun"], "🎮 Mücadele Oyunu")
        ToolTip(self.sidebar_butonlar["temalar"], "🎨 Tema Seçimi")
        ToolTip(self.btn_sidebar_toggle, "☰ Menüyü Kapat/Aç")

        # ==========================================
        # 2. SAĞ İÇERİK ALANI (Tüm ekranların griddendiği alan)
        # ==========================================
        self.icerik_alani = ctk.CTkFrame(self.pencere, fg_color="transparent")
        self.icerik_alani.pack(side="right", fill="both", expand=True)
        
        self.ana_icerik = ctk.CTkFrame(self.icerik_alani, fg_color="transparent")
        self.ana_icerik.pack(fill="both", expand=True)
        self.ana_icerik.rowconfigure(0, weight=1)
        self.ana_icerik.columnconfigure(0, weight=1)
        
        # Ekran çerçeveleri
        self.cizim_frame = ctk.CTkFrame(self.ana_icerik, fg_color="transparent")
        self.sonuc_frame = ctk.CTkFrame(self.ana_icerik, fg_color="transparent")
        self.oyun_frame  = ctk.CTkFrame(self.ana_icerik, fg_color="transparent")
        self.temalar_frame = ctk.CTkFrame(self.ana_icerik, fg_color="transparent")
        
        # Grid stacking (Raise ile geçiş sağlanacak - sıfır titreşim/flicker)
        for frame in [self.cizim_frame, self.sonuc_frame, self.oyun_frame, self.temalar_frame]:
            frame.grid(row=0, column=0, sticky="nsew")
            
        self._cizim_ekranini_olustur()
        self._sonuc_ekranini_olustur()
        self._oyun_ekranini_olustur()
        self._temalar_ekranini_olustur()

    def _cizim_ekranini_olustur(self):
        self.cizim_frame.rowconfigure(0, weight=1)
        # Tuval alanının daha büyük olması için sol kolona biraz daha fazla ağırlık veriyoruz (yarı yarıyaya yakın ama tuval odaklı)
        self.cizim_frame.columnconfigure(0, weight=12, uniform="cizim_esit") # Sol Yarı (Tuval)
        self.cizim_frame.columnconfigure(1, weight=10, uniform="cizim_esit") # Sağ Yarı (Yapay Zeka Paneli)

        # Sol Bölüm: Çizim alanı ve araçlar (Kare kilitli esnek yerleşim)
        self.sol_panel = ctk.CTkFrame(self.cizim_frame, fg_color="transparent")
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sol_panel.bind("<Configure>", self.sol_panel_boyutlandirildi)
        
        # Grid weights to center content vertically and horizontally inside the column
        self.sol_panel.rowconfigure(0, weight=1)
        self.sol_panel.columnconfigure(0, weight=1)
        
        self.sol_panel_icerik = ctk.CTkFrame(self.sol_panel, fg_color="transparent")
        self.sol_panel_icerik.grid(row=0, column=0)

        # Başlık ve tuval üst hizalama için anchor="center"
        self.sol_baslik = ctk.CTkLabel(self.sol_panel_icerik, text="Çizim Alanı", font=("Segoe UI", 15, "bold"), anchor="center")
        self.sol_baslik.rol = "yazi_ana"
        self.sol_baslik.pack(side="top", pady=(5, 5))

        # Orta Düzen (Dikey İkon Barı + Tuval Çerçevesi)
        self.orta_layout_frame = ctk.CTkFrame(self.sol_panel_icerik, fg_color="transparent")
        self.orta_layout_frame.pack(side="top", pady=5)

        # 1. Dikey Araç Çubuğu (Toolbar)
        self.arac_bari = ctk.CTkFrame(self.orta_layout_frame, corner_radius=10)
        self.arac_bari.rol = "dis"
        self.arac_bari.pack(side="left", fill="y", padx=(0, 10), pady=2)

        # Kalem Butonu
        self.btn_kalem = ctk.CTkButton(self.arac_bari, text="✏️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                       border_width=0, command=lambda: self.arac_degistir("Kalem ✏️"))
        self.btn_kalem.pack(side="top", padx=6, pady=4)
        self.btn_kalem.rol = "aktif_sekme"
        
        # Silgi Butonu
        self.btn_silgi = ctk.CTkButton(self.arac_bari, text="🧼", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                       border_width=0, command=lambda: self.arac_degistir("Silgi 🧼"))
        self.btn_silgi.pack(side="top", padx=6, pady=4)
        self.btn_silgi.rol = "pasif_sekme"

        # Ayırıcı Hat
        spacer = ctk.CTkFrame(self.arac_bari, height=2, width=30, fg_color="#44475a")
        spacer.rol = "border"
        spacer.pack(side="top", pady=6)

        # Geri Al Butonu
        self.btn_undo = ctk.CTkButton(self.arac_bari, text="↩️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                      fg_color="transparent", border_width=0, command=self.serbest_geri_al)
        self.btn_undo.pack(side="top", padx=6, pady=4)
        self.btn_undo.rol = "pasif_sekme"

        # İleri Al Butonu
        self.btn_redo = ctk.CTkButton(self.arac_bari, text="↪️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                      fg_color="transparent", border_width=0, command=self.serbest_ileri_al)
        self.btn_redo.pack(side="top", padx=6, pady=4)
        self.btn_redo.rol = "pasif_sekme"

        # Temizle Butonu
        self.btn_temizle = ctk.CTkButton(self.arac_bari, text="🧹", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                         border_width=0, command=self.tuvali_temizle)
        self.btn_temizle.pack(side="top", padx=6, pady=4)
        self.btn_temizle.rol = "temizle"

        # ToolTip'leri Ekle
        ToolTip(self.btn_kalem, "✏️ Kalem Modu")
        ToolTip(self.btn_silgi, "🧼 Silgi Modu")
        ToolTip(self.btn_undo, "↩️ Geri Al (Ctrl+Z)")
        ToolTip(self.btn_redo, "↪️ İleri Al (Ctrl+Y)")
        ToolTip(self.btn_temizle, "🧹 Tuvali Temizle")

        # 2. Çizim tuvali çerçevesi
        self.cerceve = ctk.CTkFrame(self.orta_layout_frame, corner_radius=10, border_width=2)
        self.cerceve.rol = "cerceve"
        self.cerceve.pack_propagate(False)
        self.cerceve.pack(side="left")

        self.tuval = tk.Canvas(self.cerceve, bg="white", highlightthickness=0)
        self.tuval.pack(padx=2, pady=2, fill="both", expand=True)
        self.tuval.configure(cursor="pencil")
        
        # Olay bağlamaları
        self.tuval.bind("<Button-1>",        self.cizime_basla)
        self.tuval.bind("<B1-Motion>",       self.cizimi_surdur)
        self.tuval.bind("<ButtonRelease-1>", self.cizimi_bitir)
        self.tuval.bind("<Motion>",          self.imlec_guncelle)
        self.tuval.bind("<Leave>",           lambda e: self.tuval.delete("silgi_imleci"))
        self.tuval.bind("<Configure>",       self.tuval_boyutlandirildi)

        # Kontrol Paneli (Sadece Kalınlık Slider'ı)
        self.kontrol_frame = ctk.CTkFrame(self.sol_panel_icerik, corner_radius=10)
        self.kontrol_frame.pack(side="top", pady=(5, 5))

        # Slider Etiket Grubu
        slider_etiket = ctk.CTkFrame(self.kontrol_frame, fg_color="transparent")
        slider_etiket.pack(fill="x", padx=15, pady=(5, 2))
        
        self.slider_title = ctk.CTkLabel(slider_etiket, text="Çizgi Kalınlığı:", font=("Segoe UI", 12, "bold"))
        self.slider_title.rol = "yazi_ana"
        self.slider_title.pack(side="left")
        
        self.slider_deger = ctk.CTkLabel(slider_etiket, text="14 px", font=("Segoe UI", 12))
        self.slider_deger.rol = "yesil"
        self.slider_deger.pack(side="right")

        self.slider = ctk.CTkSlider(self.kontrol_frame, from_=5, to=40, number_of_steps=35, command=self.firca_kalinligi_degisti)
        self.slider.set(14)
        self.slider.pack(fill="x", padx=15, pady=(0, 10))

        # Sağ Bölüm: Yapay Zeka Canlı Panel
        sag = ctk.CTkFrame(self.cizim_frame, fg_color="transparent")
        sag.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)

        lbl_pre = ctk.CTkLabel(sag, text="Ön İşlenmiş Giriş (28×28)", font=("Segoe UI", 15, "bold"))
        lbl_pre.rol = "yazi_ana"
        lbl_pre.pack(anchor="w", pady=(0, 6))

        onizleme_ve_sonuc = ctk.CTkFrame(sag, fg_color="transparent")
        onizleme_ve_sonuc.pack(fill="x", pady=5)

        onizleme_dis = ctk.CTkFrame(onizleme_ve_sonuc, corner_radius=10, border_width=2)
        onizleme_dis.pack(side="left", anchor="w")
        onizleme_dis.rol = "dis"

        onizleme_ic = ctk.CTkFrame(onizleme_dis, width=self.ONIZLEME_PX, height=self.ONIZLEME_PX, corner_radius=8)
        onizleme_ic.pack(padx=1, pady=1)
        onizleme_ic.pack_propagate(False)
        onizleme_ic.rol = "ic"

        self.veri_ekrani = ctk.CTkLabel(onizleme_ic, text="")
        self.veri_ekrani.place(x=0, y=0)

        sonuc_kont = ctk.CTkFrame(onizleme_ve_sonuc, corner_radius=10, border_width=1)
        sonuc_kont.pack(side="right", fill="both", expand=True, padx=(10, 0), ipady=6)

        self.tahmin_etiketi = ctk.CTkLabel(sonuc_kont, text="—", font=("Segoe UI", 26, "bold"))
        self.tahmin_etiketi.rol = "mavi"
        self.tahmin_etiketi.pack(pady=(12, 0))

        self.guven_etiketi = ctk.CTkLabel(sonuc_kont, text="", font=("Segoe UI", 14, "bold"))
        self.guven_etiketi.rol = "yesil"
        self.guven_etiketi.pack(pady=(2, 0))

        self.bilgi_etiketi = ctk.CTkLabel(sonuc_kont, text="Çizmeye başlayın, tahmin edilecektir.", font=("Segoe UI", 9))
        self.bilgi_etiketi.rol = "yazi_aciklama"
        self.bilgi_etiketi.pack(pady=(4, 8))

        olasilik_kont = ctk.CTkFrame(sag, corner_radius=10, border_width=1)
        olasilik_kont.pack(fill="both", expand=True, pady=(12, 0), ipady=8)
        
        lbl_probs = ctk.CTkLabel(olasilik_kont, text="Canlı Sınıf Olasılıkları", font=("Segoe UI", 13, "bold"))
        lbl_probs.rol = "yazi_ana"
        lbl_probs.pack(anchor="w", padx=15, pady=(8, 4))

        olasilik_konteyner = ctk.CTkFrame(olasilik_kont, fg_color="transparent")
        olasilik_konteyner.pack(fill="both", expand=True, padx=10, pady=2)

        sol_barlar_frame = ctk.CTkFrame(olasilik_konteyner, fg_color="transparent")
        sol_barlar_frame.pack(side="left", fill="both", expand=True)

        sag_barlar_frame = ctk.CTkFrame(olasilik_konteyner, fg_color="transparent")
        sag_barlar_frame.pack(side="right", fill="both", expand=True)

        for idx, sinif_adi in enumerate(self.ai.siniflar):
            hedef_frame = sol_barlar_frame if idx < 5 else sag_barlar_frame
            
            satir = ctk.CTkFrame(hedef_frame, fg_color="transparent")
            satir.pack(fill="x", padx=8, pady=2)
            
            lbl = ctk.CTkLabel(satir, text=sinif_adi, font=("Segoe UI", 10, "bold"), width=55, anchor="w")
            lbl.rol = "yazi_ana"
            lbl.pack(side="left")
            
            yuzde = ctk.CTkLabel(satir, text="%0", font=("Segoe UI", 10), width=30, anchor="e")
            yuzde.rol = "yesil"
            yuzde.pack(side="right")
            self.yuzde_etiketleri[sinif_adi] = yuzde

            bar = ctk.CTkProgressBar(satir, height=8, corner_radius=4)
            bar.rol = "mavi"
            bar.set(0.0)
            bar.pack(side="left", fill="x", expand=True, padx=5)
            self.barlar[sinif_adi] = bar

        buton_grubu = ctk.CTkFrame(sag, fg_color="transparent")
        buton_grubu.pack(fill="x", pady=(15, 0))

        self.btn_tahmin = ctk.CTkButton(buton_grubu, text="Tahmin Et", font=("Segoe UI", 12, "bold"), height=40,
                                         command=self.tahmin_butonuna_basildi)
        self.btn_tahmin.pack(fill="x", expand=True)

    def _sonuc_ekranini_olustur(self):
        self.sonuc_frame.rowconfigure(0, weight=1)
        # Tuval alanının daha büyük olması için sol kolona biraz daha fazla ağırlık veriyoruz
        self.sonuc_frame.columnconfigure(0, weight=12, uniform="sonuc_esit")
        self.sonuc_frame.columnconfigure(1, weight=10, uniform="sonuc_esit")

        self.sonuc_sol = ctk.CTkFrame(self.sonuc_frame, corner_radius=10, border_width=2)
        self.sonuc_sol.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        lbl_res = ctk.CTkLabel(self.sonuc_sol, text="Çizdiğiniz Resim", font=("Segoe UI", 15, "bold"))
        lbl_res.rol = "mavi"
        lbl_res.pack(pady=10)
        
        self.sonuc_gorsel_label = ctk.CTkLabel(self.sonuc_sol, text="")
        self.sonuc_gorsel_label.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.sonuc_sol.bind("<Configure>", self.sonuc_gorsel_boyutlandirildi)

        sonuc_sag = ctk.CTkFrame(self.sonuc_frame, corner_radius=10, border_width=2)
        sonuc_sag.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        lbl_highest = ctk.CTkLabel(sonuc_sag, text="En Yüksek Tahmin", font=("Segoe UI", 14, "bold"))
        lbl_highest.rol = "yazi_ana"
        lbl_highest.pack(pady=(15, 2))

        self.sonuc_tahmin_etiketi = ctk.CTkLabel(sonuc_sag, text="—", font=("Segoe UI", 38, "bold"))
        self.sonuc_tahmin_etiketi.rol = "yesil"
        self.sonuc_tahmin_etiketi.pack(pady=2)

        self.sonuc_guven_etiketi = ctk.CTkLabel(sonuc_sag, text="", font=("Segoe UI", 16, "bold"))
        self.sonuc_guven_etiketi.rol = "yesil"
        self.sonuc_guven_etiketi.pack(pady=(0, 12))

        detay_olasilik = ctk.CTkFrame(sonuc_sag, corner_radius=8)
        detay_olasilik.rol = "ic"
        detay_olasilik.pack(fill="both", expand=True, padx=15, pady=10, ipady=6)

        lbl_dist = ctk.CTkLabel(detay_olasilik, text="Sınıf Dağılımları", font=("Segoe UI", 12, "bold"))
        lbl_dist.rol = "yazi_ana"
        lbl_dist.pack(anchor="w", padx=15, pady=(8, 4))

        detay_olasilik_konteyner = ctk.CTkFrame(detay_olasilik, fg_color="transparent")
        detay_olasilik_konteyner.pack(fill="both", expand=True, padx=10, pady=2)

        sonuc_sol_barlar = ctk.CTkFrame(detay_olasilik_konteyner, fg_color="transparent")
        sonuc_sol_barlar.pack(side="left", fill="both", expand=True)

        sonuc_sag_barlar = ctk.CTkFrame(detay_olasilik_konteyner, fg_color="transparent")
        sonuc_sag_barlar.pack(side="right", fill="both", expand=True)

        for idx, sinif_adi in enumerate(self.ai.siniflar):
            hedef_frame = sonuc_sol_barlar if idx < 5 else sonuc_sag_barlar
            
            satir = ctk.CTkFrame(hedef_frame, fg_color="transparent")
            satir.pack(fill="x", padx=8, pady=4)
            
            lbl = ctk.CTkLabel(satir, text=sinif_adi, font=("Segoe UI", 11, "bold"), width=55, anchor="w")
            lbl.rol = "yazi_ana"
            lbl.pack(side="left")
            
            yuzde = ctk.CTkLabel(satir, text="%0", font=("Segoe UI", 11), width=35, anchor="e")
            yuzde.rol = "yesil"
            yuzde.pack(side="right")
            self.sonuc_yuzde_etiketleri[sinif_adi] = yuzde

            bar = ctk.CTkProgressBar(satir, height=10, corner_radius=5)
            bar.rol = "yesil"
            bar.set(0.0)
            bar.pack(side="left", fill="x", expand=True, padx=5)
            self.sonuc_barlar[sinif_adi] = bar

        sonuc_buton_grubu = ctk.CTkFrame(sonuc_sag, fg_color="transparent")
        sonuc_buton_grubu.pack(fill="x", side="bottom", padx=15, pady=(10, 15))

        self.btn_geri_don = ctk.CTkButton(sonuc_buton_grubu, text="Düzenlemeye Geri Dön ✏️", font=("Segoe UI", 12, "bold"), height=40,
                                           command=lambda: self.ekran_degistir("cizim"))
        self.btn_geri_don.rol = "temizle"
        self.btn_geri_don.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_yeni_cizim = ctk.CTkButton(sonuc_buton_grubu, text="Yeni Çizim Başlat 🧹", font=("Segoe UI", 12, "bold"), height=40,
                                             command=self.yeni_cizim_baslat)
        self.btn_yeni_cizim.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def _oyun_ekranini_olustur(self):
        # Mücadele frame'inin genişleme davranışını ayarlıyoruz ki pencereler ekranı tam doldursun
        self.oyun_frame.rowconfigure(0, weight=1)
        self.oyun_frame.columnconfigure(0, weight=1)

        # 1. Mücadele aktif oyun alanı
        self.oyun_aktif_frame = ctk.CTkFrame(self.oyun_frame, fg_color="transparent")
        self.oyun_aktif_frame.grid(row=0, column=0, sticky="nsew")
        
        self.oyun_aktif_frame.rowconfigure(0, weight=1)
        # Tuval alanının daha büyük olması için sol kolona biraz daha fazla ağırlık veriyoruz
        self.oyun_aktif_frame.columnconfigure(0, weight=12, uniform="oyun_esit")
        self.oyun_aktif_frame.columnconfigure(1, weight=10, uniform="oyun_esit")

        # Sol Panel (Tuval)
        self.oyun_sol_panel = ctk.CTkFrame(self.oyun_aktif_frame, fg_color="transparent")
        self.oyun_sol_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.oyun_sol_panel.bind("<Configure>", self.oyun_sol_panel_boyutlandirildi)
        
        # Grid weights to center content vertically and horizontally inside the column
        self.oyun_sol_panel.rowconfigure(0, weight=1)
        self.oyun_sol_panel.columnconfigure(0, weight=1)
        
        self.oyun_sol_panel_icerik = ctk.CTkFrame(self.oyun_sol_panel, fg_color="transparent")
        self.oyun_sol_panel_icerik.grid(row=0, column=0)

        self.oyun_baslik = ctk.CTkLabel(self.oyun_sol_panel_icerik, text="Çizim Alanı (Mücadele)", font=("Segoe UI", 15, "bold"), anchor="center")
        self.oyun_baslik.rol = "yazi_ana"
        self.oyun_baslik.pack(side="top", pady=(5, 5))

        # Orta Düzen (Dikey İkon Barı + Tuval Çerçevesi)
        self.oyun_orta_layout_frame = ctk.CTkFrame(self.oyun_sol_panel_icerik, fg_color="transparent")
        self.oyun_orta_layout_frame.pack(side="top", pady=5)

        # 1. Dikey Araç Çubuğu (Toolbar - Oyun)
        self.oyun_arac_bari = ctk.CTkFrame(self.oyun_orta_layout_frame, corner_radius=10)
        self.oyun_arac_bari.rol = "dis"
        self.oyun_arac_bari.pack(side="left", fill="y", padx=(0, 10), pady=2)

        # Kalem Butonu (Oyun)
        self.btn_oyun_kalem = ctk.CTkButton(self.oyun_arac_bari, text="✏️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                            border_width=0, command=lambda: self.oyun_arac_degistir("Kalem ✏️"))
        self.btn_oyun_kalem.pack(side="top", padx=6, pady=4)
        self.btn_oyun_kalem.rol = "aktif_sekme"
        
        # Silgi Butonu (Oyun)
        self.btn_oyun_silgi = ctk.CTkButton(self.oyun_arac_bari, text="🧼", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                            border_width=0, command=lambda: self.oyun_arac_degistir("Silgi 🧼"))
        self.btn_oyun_silgi.pack(side="top", padx=6, pady=4)
        self.btn_oyun_silgi.rol = "pasif_sekme"

        # Ayırıcı Hat
        Spacer_oyun = ctk.CTkFrame(self.oyun_arac_bari, height=2, width=30, fg_color="#44475a")
        Spacer_oyun.rol = "border"
        Spacer_oyun.pack(side="top", pady=6)

        # Geri Al Butonu (Oyun)
        self.btn_oyun_undo = ctk.CTkButton(self.oyun_arac_bari, text="↩️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                           fg_color="transparent", border_width=0, command=self.oyun_geri_al)
        self.btn_oyun_undo.pack(side="top", padx=6, pady=4)
        self.btn_oyun_undo.rol = "pasif_sekme"

        # İleri Al Butonu (Oyun)
        self.btn_oyun_redo = ctk.CTkButton(self.oyun_arac_bari, text="↪️", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                           fg_color="transparent", border_width=0, command=self.oyun_ileri_al)
        self.btn_oyun_redo.pack(side="top", padx=6, pady=4)
        self.btn_oyun_redo.rol = "pasif_sekme"

        # Temizle Butonu (Oyun)
        self.btn_oyun_temizle = ctk.CTkButton(self.oyun_arac_bari, text="🧹", font=("Segoe UI", 16, "bold"), width=42, height=42,
                                              border_width=0, command=self.oyun_tuvali_temizle)
        self.btn_oyun_temizle.pack(side="top", padx=6, pady=4)
        self.btn_oyun_temizle.rol = "temizle"

        # ToolTip'leri Ekle
        ToolTip(self.btn_oyun_kalem, "✏️ Kalem Modu")
        ToolTip(self.btn_oyun_silgi, "🧼 Silgi Modu")
        ToolTip(self.btn_oyun_undo, "↩️ Geri Al (Ctrl+Z)")
        ToolTip(self.btn_oyun_redo, "↪️ İleri Al (Ctrl+Y)")
        ToolTip(self.btn_oyun_temizle, "🧹 Tuvali Temizle")

        # 2. Çizim tuvali çerçevesi (Oyun)
        self.oyun_cerceve = ctk.CTkFrame(self.oyun_orta_layout_frame, corner_radius=10, border_width=2)
        self.oyun_cerceve.rol = "cerceve"
        self.oyun_cerceve.pack_propagate(False)
        self.oyun_cerceve.pack(side="left")

        self.oyun_tuval = tk.Canvas(self.oyun_cerceve, bg="white", highlightthickness=0)
        self.oyun_tuval.pack(padx=2, pady=2, fill="both", expand=True)
        self.oyun_tuval.configure(cursor="pencil")
        
        self.oyun_tuval.bind("<Button-1>",        self.oyun_cizime_basla)
        self.oyun_tuval.bind("<B1-Motion>",       self.oyun_cizimi_surdur)
        self.oyun_tuval.bind("<ButtonRelease-1>", self.oyun_cizimi_bitir)
        self.oyun_tuval.bind("<Motion>",          self.oyun_imlec_guncelle)
        self.oyun_tuval.bind("<Leave>",           lambda e: self.oyun_tuval.delete("silgi_imleci"))
        self.oyun_tuval.bind("<Configure>",       self.oyun_tuval_boyutlandirildi)

        # Kontrol Paneli (Oyun - Sadece Kalınlık Slider'ı)
        self.oyun_kontrol_frame = ctk.CTkFrame(self.oyun_sol_panel_icerik, corner_radius=10)
        self.oyun_kontrol_frame.pack(side="top", pady=(5, 5))

        slider_etiket = ctk.CTkFrame(self.oyun_kontrol_frame, fg_color="transparent")
        slider_etiket.pack(fill="x", padx=15, pady=(5, 2))
        
        self.oyun_slider_title = ctk.CTkLabel(slider_etiket, text="Çizgi Kalınlığı:", font=("Segoe UI", 12, "bold"))
        self.oyun_slider_title.rol = "yazi_ana"
        self.oyun_slider_title.pack(side="left")
        
        self.oyun_slider_deger = ctk.CTkLabel(slider_etiket, text="14 px", font=("Segoe UI", 12))
        self.oyun_slider_deger.rol = "yesil"
        self.oyun_slider_deger.pack(side="right")

        self.oyun_slider = ctk.CTkSlider(self.oyun_kontrol_frame, from_=5, to=40, number_of_steps=35, command=self.oyun_firca_kalinligi_degisti)
        self.oyun_slider.set(14)
        self.oyun_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Sağ Oyun Paneli
        self.oyun_sag_panel = ctk.CTkFrame(self.oyun_aktif_frame, corner_radius=10, border_width=2)
        self.oyun_sag_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        lbl_title = ctk.CTkLabel(self.oyun_sag_panel, text="Mücadele Modu", font=("Segoe UI", 18, "bold"))
        lbl_title.rol = "yazi_yardimci"
        lbl_title.pack(pady=(15, 2))

        # Skor ve Kombo Göstergesi
        self.skor_frame = ctk.CTkFrame(self.oyun_sag_panel, fg_color="transparent")
        self.skor_frame.pack(fill="x", padx=20, pady=(2, 5))
        
        self.lbl_skor = ctk.CTkLabel(self.skor_frame, text="Skor: 0", font=("Segoe UI", 13, "bold"))
        self.lbl_skor.rol = "yesil"
        self.lbl_skor.pack(side="left")
        
        self.lbl_kombo = ctk.CTkLabel(self.skor_frame, text="Kombo: x0", font=("Segoe UI", 13, "bold"))
        self.lbl_kombo.rol = "turuncu"
        self.lbl_kombo.pack(side="right")

        # Kelime Kutusu
        self.hedef_kelime_kutu = ctk.CTkFrame(self.oyun_sag_panel, corner_radius=12)
        self.hedef_kelime_kutu.rol = "ic"
        self.hedef_kelime_kutu.pack(fill="x", padx=20, pady=10, ipady=8)

        lbl_prompt = ctk.CTkLabel(self.hedef_kelime_kutu, text="Lütfen Şunu Çizin:", font=("Segoe UI", 12, "bold"))
        lbl_prompt.rol = "yazi_aciklama"
        lbl_prompt.pack(pady=(8, 2))

        self.oyun_kelime_label = ctk.CTkLabel(self.hedef_kelime_kutu, text="...", font=("Segoe UI", 34, "bold"))
        self.oyun_kelime_label.rol = "yazi_ana"
        self.oyun_kelime_label.pack(pady=4)

        # Süre Çubuğu
        self.oyun_sure_label = ctk.CTkLabel(self.oyun_sag_panel, text="Kalan Süre: 20 sn", font=("Segoe UI", 15, "bold"))
        self.oyun_sure_label.rol = "yazi_ana"
        self.oyun_sure_label.pack(pady=(10, 2))

        self.oyun_sure_bar = ctk.CTkProgressBar(self.oyun_sag_panel, height=12)
        self.oyun_sure_bar.rol = "yesil"
        self.oyun_sure_bar.set(1.0)
        self.oyun_sure_bar.pack(fill="x", padx=40, pady=(2, 10))

        self.oyun_durum_label = ctk.CTkLabel(self.oyun_sag_panel, text="Yükleniyor...", font=("Segoe UI", 13, "italic"))
        self.oyun_durum_label.rol = "yazi_ana"
        self.oyun_durum_label.pack(pady=5)

        # Canlı En Yakın Tahminler
        game_pred_kont = ctk.CTkFrame(self.oyun_sag_panel, corner_radius=8)
        game_pred_kont.rol = "ic"
        game_pred_kont.pack(fill="both", expand=True, padx=20, pady=10, ipady=6)

        lbl_real = ctk.CTkLabel(game_pred_kont, text="En Yakın Canlı Tahminler", font=("Segoe UI", 12, "bold"))
        lbl_real.rol = "yazi_ana"
        lbl_real.pack(anchor="w", padx=15, pady=(8, 4))

        self.oyun_tahmin_satirlari = []
        for i in range(3):
            satir = ctk.CTkFrame(game_pred_kont, fg_color="transparent")
            satir.pack(fill="x", padx=15, pady=4)
            
            lbl_name = ctk.CTkLabel(satir, text="—", font=("Segoe UI", 11, "bold"), width=70, anchor="w")
            lbl_name.rol = "yazi_ana"
            lbl_name.pack(side="left")
            
            lbl_val = ctk.CTkLabel(satir, text="%0", font=("Segoe UI", 11), width=35, anchor="e")
            lbl_val.rol = "yesil"
            lbl_val.pack(side="right")
            
            bar = ctk.CTkProgressBar(satir, height=10, corner_radius=5)
            bar.rol = "mavi"
            bar.set(0.0)
            bar.pack(side="left", fill="x", expand=True, padx=5)
            
            self.oyun_tahmin_satirlari.append({"lbl": lbl_name, "bar": bar, "val": lbl_val})

        game_btn_grubu = ctk.CTkFrame(self.oyun_sag_panel, fg_color="transparent")
        game_btn_grubu.pack(fill="x", side="bottom", padx=20, pady=(10, 20))

        self.btn_oyun_yeni = ctk.CTkButton(game_btn_grubu, text="Yeni Kelimeye Geç ➡️", font=("Segoe UI", 12, "bold"), height=40,
                                            command=self.yeni_oyun_baslat)
        self.btn_oyun_yeni.pack(fill="x", expand=True)

        # 2. Mücadele giriş ekranı (Ekranı tam dolduracak esnek 50/50 panel)
        self.oyun_giris_frame = ctk.CTkFrame(self.oyun_frame, fg_color="transparent")
        self.oyun_giris_frame.grid(row=0, column=0, sticky="nsew")
        self._oyun_giris_ekranini_olustur()

    def _oyun_giris_ekranini_olustur(self):
        # 1. Başlık
        title_lbl = ctk.CTkLabel(self.oyun_giris_frame, text="🤖 Yapay Zeka Çizim Mücadelesi", font=("Segoe UI", 24, "bold"))
        title_lbl.rol = "logo"
        title_lbl.pack(pady=(40, 20))
        
        # 2. Esnek Orta Bölüm (Kurallar ve Nesneler Yan Yana)
        middle_frame = ctk.CTkFrame(self.oyun_giris_frame, fg_color="transparent")
        middle_frame.pack(fill="both", expand=True, padx=40, pady=10)
        
        middle_frame.rowconfigure(0, weight=1)
        middle_frame.columnconfigure(0, weight=1, uniform="lobby_split")
        middle_frame.columnconfigure(1, weight=1, uniform="lobby_split")
        
        # Sol taraf: Kurallar kartı
        rules_frame = ctk.CTkFrame(middle_frame, corner_radius=15, border_width=1)
        rules_frame.rol = "dis"
        rules_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=10)
        
        lbl_rules_title = ctk.CTkLabel(rules_frame, text="Nasıl Oynanır?", font=("Segoe UI", 16, "bold"))
        lbl_rules_title.rol = "yazi_yardimci"
        lbl_rules_title.pack(anchor="w", padx=25, pady=(20, 10))
        
        rules_text = (
            "• Yapay zeka listeden zorluğa göre rastgele bir nesne seçecektir.\n"
            "• Çizim yapmak için kalan süreniz zorluk seviyesine bağlıdır.\n"
            "• Çiziminiz yapay zeka tarafından süre bitmeden önce doğru\n"
            "  tahmin edilirse turu kazanıp puan toplarsınız.\n"
            "• Üst üste kazandıkça puanınızı artıran Kombo Çarpanı devreye girer!"
        )
        lbl_rules = ctk.CTkLabel(rules_frame, text=rules_text, font=("Segoe UI", 11.5), justify="left", anchor="nw")
        lbl_rules.rol = "yazi_ana"
        lbl_rules.pack(fill="x", padx=25, pady=(5, 5))

        # Zorluk Seçimi
        lbl_diff_title = ctk.CTkLabel(rules_frame, text="Zorluk Derecesi Seçin:", font=("Segoe UI", 12, "bold"))
        lbl_diff_title.rol = "yazi_yardimci"
        lbl_diff_title.pack(anchor="w", padx=25, pady=(5, 2))

        self.seg_zorluk = ctk.CTkSegmentedButton(rules_frame, values=["Kolay", "Orta", "Zor"],
                                                command=self.zorluk_secildi)
        self.seg_zorluk.set(self.aktif_zorluk)
        self.seg_zorluk.pack(fill="x", padx=25, pady=(2, 10))

        # Rekorlar Tablosu
        lbl_hs_title = ctk.CTkLabel(rules_frame, text="🏆 En Yüksek Skorlarınız (Rekorlar):", font=("Segoe UI", 12, "bold"))
        lbl_hs_title.rol = "yazi_yardimci"
        lbl_hs_title.pack(anchor="w", padx=25, pady=(10, 2))

        self.hs_frame = ctk.CTkFrame(rules_frame, corner_radius=8)
        self.hs_frame.rol = "ic"
        self.hs_frame.pack(fill="x", padx=25, pady=(2, 15), ipady=4)

        self.lbl_record_kolay = ctk.CTkLabel(self.hs_frame, text=f"🟢 Kolay: {self.rekorlar.get('Kolay', 0)} P", font=("Segoe UI", 10, "bold"))
        self.lbl_record_kolay.rol = "yazi_ana"
        self.lbl_record_kolay.pack(side="left", expand=True)

        self.lbl_record_orta = ctk.CTkLabel(self.hs_frame, text=f"🟡 Orta: {self.rekorlar.get('Orta', 0)} P", font=("Segoe UI", 10, "bold"))
        self.lbl_record_orta.rol = "yazi_ana"
        self.lbl_record_orta.pack(side="left", expand=True)

        self.lbl_record_zor = ctk.CTkLabel(self.hs_frame, text=f"🔴 Zor: {self.rekorlar.get('Zor', 0)} P", font=("Segoe UI", 10, "bold"))
        self.lbl_record_zor.rol = "yazi_ana"
        self.lbl_record_zor.pack(side="left", expand=True)
        
        # Sağ taraf: Kelime listesi kartı
        word_list_frame = ctk.CTkFrame(middle_frame, corner_radius=15, border_width=1)
        word_list_frame.rol = "dis"
        word_list_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=10)
        
        lbl_words_title = ctk.CTkLabel(word_list_frame, text=f"Tahmin Edilebilir Sınıflar ({len(self.ai.siniflar)} Adet):", font=("Segoe UI", 16, "bold"))
        lbl_words_title.rol = "yazi_yardimci"
        lbl_words_title.pack(anchor="w", padx=25, pady=(20, 10))
        
        grid_frame = ctk.CTkFrame(word_list_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        grid_frame.rowconfigure((0,1,2,3,4), weight=1)
        grid_frame.columnconfigure((0,1), weight=1)
        
        for idx, sinif in enumerate(self.ai.siniflar):
            row = idx % 5
            col = idx // 5
            badge = ctk.CTkLabel(grid_frame, text=sinif, font=("Segoe UI", 12, "bold"), corner_radius=8, height=35)
            badge.rol = "rozet"
            badge.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
        # 3. Alt Başlat Butonu
        start_btn = ctk.CTkButton(self.oyun_giris_frame, text="Mücadeleyi Başlat 🚀", font=("Segoe UI", 14, "bold"), height=46,
                                  command=self.oyunu_resmen_baslat)
        start_btn.pack(pady=(20, 35), padx=40, fill="x")

    def oyunu_resmen_baslat(self):
        self.oyun_aktif_frame.tkraise()
        self.yeni_oyun_baslat()
        self.pencere.after(50, self.oyun_tuval_yeniden_ciz)

    def _temalar_ekranini_olustur(self):
        for child in self.temalar_frame.winfo_children():
            child.destroy()
            
        baslik_lbl = ctk.CTkLabel(self.temalar_frame, text="Tema Galerisi", font=("Segoe UI", 22, "bold"))
        baslik_lbl.rol = "yazi_ana"
        baslik_lbl.pack(anchor="w", padx=25, pady=(20, 5))
        
        alt_lbl = ctk.CTkLabel(self.temalar_frame, text="Arayüz görünümünü dilediğiniz Catppuccin veya retro renklerle özelleştirin.", font=("Segoe UI", 12))
        alt_lbl.rol = "yazi_aciklama"
        alt_lbl.pack(anchor="w", padx=25, pady=(0, 20))
        
        self.temalar_scroll = ctk.CTkScrollableFrame(self.temalar_frame, fg_color="transparent")
        self.temalar_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.temalar_scroll.columnconfigure(0, weight=1)
        self.temalar_scroll.columnconfigure(1, weight=1)
        
        for idx, (tema_adi, renkler) in enumerate(THEMES.items()):
            row = idx // 2
            col = idx % 2
            
            card = ctk.CTkFrame(self.temalar_scroll, fg_color=renkler["kutu_bg"], border_width=1, border_color=renkler["border_renk"], corner_radius=12)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            t_lbl = ctk.CTkLabel(card, text=tema_adi, font=("Segoe UI", 16, "bold"), text_color=renkler["yazi_ana"])
            t_lbl.pack(anchor="w", padx=15, pady=(12, 5))
            
            dots_frame = ctk.CTkFrame(card, fg_color="transparent")
            dots_frame.pack(anchor="w", padx=15, pady=5)
            
            for color_key in ["pencere_bg", "mavi", "yesil", "yazi_ana"]:
                dot = ctk.CTkLabel(dots_frame, text="", width=20, height=20, corner_radius=10, fg_color=renkler[color_key])
                dot.pack(side="left", padx=3)
            
            btn = ctk.CTkButton(card, text="Uygula", font=("Segoe UI", 11, "bold"), 
                                 fg_color=renkler["mavi"], hover_color=renkler["mavi_hover"], text_color=renkler["btn_text"],
                                 command=lambda name=tema_adi: self.temayi_uygula(name))
            btn.pack(anchor="e", padx=15, pady=(10, 12))

    def temayi_uygula(self, tema_adi):
        self.aktif_tema = THEMES[tema_adi]
        
        # Sadece mod değiştiğinde (light -> dark veya dark -> light) set_appearance_mode çağır (Ağır bir işlemdir)
        mevcut_mod = ctk.get_appearance_mode().lower()
        hedef_mod = self.aktif_tema["mode"].lower()
        if mevcut_mod != hedef_mod:
            ctk.set_appearance_mode(self.aktif_tema["mode"])
        
        self.pencere.configure(fg_color=self.aktif_tema["pencere_bg"])
        self._widget_renklendir(self.pencere, self.aktif_tema)

    def _widget_renklendir(self, parent, tema):
        if hasattr(self, "temalar_scroll") and parent == self.temalar_scroll:
            return
            
        for child in parent.winfo_children():
            if hasattr(self, "temalar_scroll") and (child == self.temalar_scroll or str(child).startswith(str(self.temalar_scroll))):
                continue
                
            w_type = child.__class__.__name__
            
            if w_type == "CTkFrame":
                current_fg = child.cget("fg_color")
                if current_fg != "transparent" and current_fg is not None:
                    if child == self.sidebar:
                        child.configure(fg_color=tema["kutu_bg"])
                    elif child in [self.cizim_frame, self.sonuc_frame, self.oyun_frame, self.temalar_frame, self.oyun_giris_frame, self.oyun_aktif_frame]:
                        child.configure(fg_color="transparent")
                    elif hasattr(child, "rol"):
                        if child.rol == "dis":
                            child.configure(fg_color=tema["kutu_bg"])
                        elif child.rol == "ic":
                            child.configure(fg_color=tema["alan_bg"])
                        elif child.rol == "cerceve":
                            child.configure(fg_color=tema["surface0"])
                        elif child.rol == "border":
                            child.configure(fg_color=tema["border_renk"])
                    else:
                        child.configure(fg_color=tema["kutu_bg"])
                
                try:
                    if child.cget("border_width") > 0:
                        if hasattr(child, "rol") and child.rol == "cerceve":
                            child.configure(border_color=tema["mavi"])
                        else:
                            child.configure(border_color=tema["border_renk"])
                except Exception:
                    pass
                    
            elif w_type == "CTkLabel":
                if hasattr(child, "rol"):
                    rol = child.rol
                    if rol == "yazi_ana":
                        child.configure(text_color=tema["yazi_ana"])
                    elif rol == "yazi_yardimci":
                        child.configure(text_color=tema["yazi_yardimci"])
                    elif rol == "yazi_aciklama":
                        child.configure(text_color=tema["yazi_aciklama"])
                    elif rol == "logo":
                        child.configure(text_color=tema["mavi"])
                    elif rol == "yesil":
                        child.configure(text_color=tema["yesil"])
                    elif rol == "mavi":
                        child.configure(text_color=tema["mavi"])
                    elif rol == "rozet":
                        child.configure(text_color=tema["yazi_ana"], fg_color=tema["surface0"])
                else:
                    child.configure(text_color=tema["yazi_ana"])
                    
            elif w_type == "CTkButton":
                if hasattr(child, "rol"):
                    if child.rol == "temizle":
                        child.configure(fg_color=tema["surface0"], hover_color=tema["border_renk"], text_color=tema["kirmizi"])
                    elif child.rol == "aktif_sekme":
                        child.configure(fg_color=tema["mavi"], text_color=tema["btn_text"], hover_color=tema["mavi_hover"])
                    elif child.rol == "pasif_sekme":
                        child.configure(fg_color="transparent", text_color=tema["yazi_ana"], hover_color=tema["surface0"])
                else:
                    child.configure(fg_color=tema["mavi"], hover_color=tema["mavi_hover"], text_color=tema["btn_text"])
                    
            elif w_type == "CTkProgressBar":
                p_color = tema["mavi"] if (hasattr(child, "rol") and child.rol == "mavi") else tema["yesil"]
                child.configure(progress_color=p_color, fg_color=tema["surface0"])
                
            elif w_type == "CTkSlider":
                child.configure(button_color=tema["mavi"], button_hover_color=tema["mavi_hover"], fg_color=tema["surface0"], progress_color=tema["mavi"])
                
            elif w_type == "CTkSegmentedButton":
                child.configure(selected_color=tema["mavi"], selected_hover_color=tema["mavi_hover"])
                
            elif w_type == "CTkOptionMenu":
                child.configure(fg_color=tema["surface0"], button_color=tema["surface0"], button_hover_color=tema["border_renk"], 
                                dropdown_fg_color=tema["kutu_bg"], dropdown_text_color=tema["yazi_ana"], text_color=tema["yazi_ana"])
            
            elif w_type == "Canvas":
                child.configure(bg="white")
                
            self._widget_renklendir(child, tema)

    def sidebar_toggle(self):
        self.sidebar_acik = not getattr(self, "sidebar_acik", True)
        if self.sidebar_acik:
            self.sidebar.configure(width=200)
            self.logo_lbl.configure(text="🎨 Çizim AI", font=("Segoe UI", 22, "bold"))
            self.btn_sidebar_toggle.configure(text="◀ Menüyü Kapat")
            
            self.sidebar_butonlar["tuval"].configure(text="✏️ Serbest Çizim", anchor="w")
            self.sidebar_butonlar["oyun"].configure(text="🎮 Mücadele Oyunu", anchor="w")
            self.sidebar_butonlar["temalar"].configure(text="🎨 Tema Seçimi", anchor="w")
            
            self.btn_sidebar_toggle.pack_configure(padx=15)
            for btn in self.sidebar_butonlar.values():
                btn.pack_configure(padx=15)
        else:
            self.sidebar.configure(width=60)
            self.logo_lbl.configure(text="🎨", font=("Segoe UI", 24, "bold"))
            self.btn_sidebar_toggle.configure(text="☰")
            
            self.sidebar_butonlar["tuval"].configure(text="✏️", anchor="center")
            self.sidebar_butonlar["oyun"].configure(text="🎮", anchor="center")
            self.sidebar_butonlar["temalar"].configure(text="🎨", anchor="center")
            
            self.btn_sidebar_toggle.pack_configure(padx=5)
            for btn in self.sidebar_butonlar.values():
                btn.pack_configure(padx=5)

    def sayfa_sec(self, sayfa_adi):
        self.aktif_sekme = sayfa_adi
        
        # Oyun sayfasından çıkılırken oyun döngüsünü durdur
        if sayfa_adi != "oyun":
            if hasattr(self, "oyun_aktif") and self.oyun_aktif:
                self.oyun_aktif = False
                if hasattr(self, "oyun_timer_id") and self.oyun_timer_id:
                    self.pencere.after_cancel(self.oyun_timer_id)
                    self.oyun_timer_id = None
        
        # Sidebar aktif buton stilini güncelle
        for btn_name, btn in self.sidebar_butonlar.items():
            if btn_name == sayfa_adi:
                btn.configure(fg_color=self.aktif_tema["mavi"], text_color=self.aktif_tema["btn_text"], hover_color=self.aktif_tema["mavi_hover"])
                btn.rol = "aktif_sekme"
            else:
                btn.configure(fg_color="transparent", text_color=self.aktif_tema["yazi_ana"], hover_color=self.aktif_tema["surface0"])
                btn.rol = "pasif_sekme"
                
        if sayfa_adi == "tuval":
            self.ekran_degistir("cizim")
            self.arac_degistir("Silgi 🧼" if self.serbest_silgi_modu else "Kalem ✏️")
            self.pencere.after(50, self.tuval_yeniden_ciz)
        elif sayfa_adi == "oyun":
            self.ekran_degistir("oyun")
            self.oyun_giris_frame.tkraise()
        elif sayfa_adi == "temalar":
            self.ekran_degistir("temalar")

    def ekran_degistir(self, hedef_ekran):
        # Grid raise kullanarak ekranları sıfır parlama ve anında geçişle değiştiriyoruz
        if hedef_ekran == "cizim":
            self.cizim_frame.tkraise()
        elif hedef_ekran == "sonuc":
            self.sonuc_frame.tkraise()
        elif hedef_ekran == "oyun":
            self.oyun_frame.tkraise()
        elif hedef_ekran == "temalar":
            self.temalar_frame.tkraise()

    def arac_degistir(self, value):
        if value == "Kalem ✏️":
            self.serbest_silgi_modu = False
            self.serbest_secilen_renk = "black"
            self.tuval.configure(cursor="pencil")
            self.slider_title.configure(text="Çizgi Kalınlığı:")
            self.slider.configure(from_=5, to=40, number_of_steps=35)
            self.slider.set(self.serbest_kalem_kalinligi)
            self.serbest_firca_kalinligi = self.serbest_kalem_kalinligi
            self.slider_deger.configure(text=f"{self.serbest_firca_kalinligi} px")
            self.btn_kalem.rol = "aktif_sekme"
            self.btn_silgi.rol = "pasif_sekme"
        else:
            self.serbest_silgi_modu = True
            self.serbest_secilen_renk = "white"
            self.tuval.configure(cursor="none")
            self.slider_title.configure(text="Silgi Kalınlığı:")
            self.slider.configure(from_=5, to=80, number_of_steps=75)
            self.slider.set(self.serbest_silgi_kalinligi)
            self.serbest_firca_kalinligi = self.serbest_silgi_kalinligi
            self.slider_deger.configure(text=f"{self.serbest_firca_kalinligi} px")
            self.btn_silgi.rol = "aktif_sekme"
            self.btn_kalem.rol = "pasif_sekme"
        self._widget_renklendir(self.arac_bari, self.aktif_tema)
        self.imlec_guncelle()

    def firca_kalinligi_degisti(self, value):
        val = int(value)
        if self.serbest_silgi_modu:
            self.serbest_silgi_kalinligi = val
            self.serbest_firca_kalinligi = val
        else:
            self.serbest_kalem_kalinligi = val
            self.serbest_firca_kalinligi = val
        self.slider_deger.configure(text=f"{self.serbest_firca_kalinligi} px")
        self.imlec_guncelle()

    def tam_ekran_tetikle(self, event=None):
        self.tam_ekran_durumu = not self.tam_ekran_durumu
        self.pencere.attributes("-fullscreen", self.tam_ekran_durumu)
        if not self.tam_ekran_durumu:
            self.pencere.geometry("1100x700")

    def sol_panel_boyutlandirildi(self, event):
        # Alt widget'lardan gelen configure tetiklenmelerini engelliyoruz
        # CustomTkinter'da CTkFrame olayları iç canvas üzerinden tetiklenir
        if event.widget != self.sol_panel._canvas:
            return
            
        parent_w = self.cizim_frame.winfo_width()
        parent_h = self.cizim_frame.winfo_height()
        
        if parent_w < 100 or parent_h < 100:
            return
            
        baslik_h = 30
        slider_h = 45
        bosluk = 12
        toolbar_w = 54
        
        # Column 0 width is parent_w * 12 / 22
        col0_w = parent_w * 12 / 22
        
        mevcut_h = parent_h - baslik_h - slider_h - (bosluk * 3) - 30
        mevcut_w = col0_w - toolbar_w - (bosluk * 2) - 30
        
        # Keep the canvas a perfect square
        boyut = min(mevcut_w, mevcut_h)
        boyut = max(200, boyut)
        
        self.sol_baslik.configure(width=boyut + toolbar_w + 10)
        self.cerceve.configure(width=boyut, height=boyut)
        self.kontrol_frame.configure(width=boyut + toolbar_w + 10)

    def oyun_sol_panel_boyutlandirildi(self, event):
        # Alt widget'lardan gelen configure tetiklenmelerini engelliyoruz
        if event.widget != self.oyun_sol_panel._canvas:
            return
            
        parent_w = self.oyun_aktif_frame.winfo_width()
        parent_h = self.oyun_aktif_frame.winfo_height()
        
        if parent_w < 100 or parent_h < 100:
            return
            
        baslik_h = 30
        slider_h = 45
        bosluk = 12
        toolbar_w = 54
        
        # Column 0 width is parent_w * 12 / 22
        col0_w = parent_w * 12 / 22
        
        mevcut_h = parent_h - baslik_h - slider_h - (bosluk * 3) - 30
        mevcut_w = col0_w - toolbar_w - (bosluk * 2) - 30
        
        # Keep the canvas a perfect square
        boyut = min(mevcut_w, mevcut_h)
        boyut = max(200, boyut)
        
        self.oyun_baslik.configure(width=boyut + toolbar_w + 10)
        self.oyun_cerceve.configure(width=boyut, height=boyut)
        self.oyun_kontrol_frame.configure(width=boyut + toolbar_w + 10)

    def tuval_boyutlandirildi(self, event):
        if event.widget != self.tuval:
            return
        if hasattr(self, "tuval_resize_timer") and self.tuval_resize_timer:
            self.pencere.after_cancel(self.tuval_resize_timer)
        self.tuval_resize_timer = self.pencere.after(80, self.tuval_yeniden_ciz)

    def oyun_tuval_boyutlandirildi(self, event):
        if event.widget != self.oyun_tuval:
            return
        if hasattr(self, "oyun_resize_timer") and self.oyun_resize_timer:
            self.pencere.after_cancel(self.oyun_resize_timer)
        self.oyun_resize_timer = self.pencere.after(80, self.oyun_tuval_yeniden_ciz)

    def tuval_yeniden_ciz(self):
        w = self.tuval.winfo_width()
        h = self.tuval.winfo_height()
        if w > 10 and h > 10:
            olcekli = self.sanal_resim.resize((w, h), Image.Resampling.BILINEAR)
            self.tk_tuval_resim = ImageTk.PhotoImage(olcekli)
            if hasattr(self, "bg_img_id") and self.bg_img_id in self.tuval.find_all():
                self.tuval.itemconfig(self.bg_img_id, image=self.tk_tuval_resim)
                self.tuval.tag_lower(self.bg_img_id)
                self.tuval.delete("cizgi")
            else:
                self.tuval.delete("all")
                self.bg_img_id = self.tuval.create_image(0, 0, anchor="nw", image=self.tk_tuval_resim)

    def oyun_tuval_yeniden_ciz(self):
        w = self.oyun_tuval.winfo_width()
        h = self.oyun_tuval.winfo_height()
        if w > 10 and h > 10:
            olcekli = self.oyun_sanal_resim.resize((w, h), Image.Resampling.BILINEAR)
            self.tk_oyun_tuval_resim = ImageTk.PhotoImage(olcekli)
            if hasattr(self, "oyun_bg_img_id") and self.oyun_bg_img_id in self.oyun_tuval.find_all():
                self.oyun_tuval.itemconfig(self.oyun_bg_img_id, image=self.tk_oyun_tuval_resim)
                self.oyun_tuval.tag_lower(self.oyun_bg_img_id)
                self.oyun_tuval.delete("cizgi")
            else:
                self.oyun_tuval.delete("all")
                self.oyun_bg_img_id = self.oyun_tuval.create_image(0, 0, anchor="nw", image=self.tk_oyun_tuval_resim)

    def sonuc_gorsel_boyutlandirildi(self, event):
        if event.widget != self.sonuc_sol._canvas:
            return
        if hasattr(self, "sanal_resim") and self.tk_buyuk_gorsel:
            max_boyut = 360
            w = min(max_boyut, event.width - 40, event.height - 80)
            w = max(100, w)
            gorsel_copy = self.sanal_resim.copy()
            self.tk_buyuk_gorsel = ctk.CTkImage(light_image=gorsel_copy, dark_image=gorsel_copy, size=(w, w))
            self.sonuc_gorsel_label.configure(image=self.tk_buyuk_gorsel)


    def imlec_guncelle(self, event=None):
        self.tuval.delete("silgi_imleci")
        if event:
            self.son_fare_x = event.x
            self.son_fare_y = event.y
        if self.serbest_silgi_modu:
            r = self.serbest_firca_kalinligi / 2
            outline_color = "#d20f39" if ctk.get_appearance_mode() == "light" else "#f38ba8"
            self.tuval.create_oval(self.son_fare_x - r, self.son_fare_y - r, 
                                   self.son_fare_x + r, self.son_fare_y + r,
                                   outline=outline_color, width=1.5, tags="silgi_imleci")

    def oyun_imlec_guncelle(self, event=None):
        self.oyun_tuval.delete("silgi_imleci")
        if event:
            self.son_fare_x = event.x
            self.son_fare_y = event.y
        if self.oyun_silgi_modu:
            r = self.oyun_firca_kalinligi / 2
            outline_color = "#d20f39" if ctk.get_appearance_mode() == "light" else "#f38ba8"
            self.oyun_tuval.create_oval(self.son_fare_x - r, self.son_fare_y - r, 
                                        self.son_fare_x + r, self.son_fare_y + r,
                                        outline=outline_color, width=1.5, tags="silgi_imleci")

    def cizime_basla(self, event):
        self.onceki_x, self.onceki_y = event.x, event.y

    def oyun_cizime_basla(self, event):
        self.oyun_onceki_x, self.oyun_onceki_y = event.x, event.y

    def cizimi_surdur(self, event):
        if self.onceki_x is not None:
            self.tuval.create_line(self.onceki_x, self.onceki_y, event.x, event.y,
                                   width=self.serbest_firca_kalinligi, fill=self.serbest_secilen_renk,
                                   capstyle=tk.ROUND, tags="cizgi")
            
            canvas_w = self.tuval.winfo_width()
            canvas_h = self.tuval.winfo_height()
            
            w_ratio = self.sanal_boyut / max(1, canvas_w)
            h_ratio = self.sanal_boyut / max(1, canvas_h)
            
            sanal_x1 = self.onceki_x * w_ratio
            sanal_y1 = self.onceki_y * h_ratio
            sanal_x2 = event.x * w_ratio
            sanal_y2 = event.y * h_ratio
            
            sanal_kalinlik = max(1, int(round(self.serbest_firca_kalinligi * min(w_ratio, h_ratio))))
            sanal_cizim_rengi = "white" if self.serbest_silgi_modu else "black"
            
            self.cizici.line([sanal_x1, sanal_y1, sanal_x2, sanal_y2],
                             fill=sanal_cizim_rengi, width=sanal_kalinlik, joint="curve")
            
            self.onceki_x, self.onceki_y = event.x, event.y
            self.imlec_guncelle(event)

            if self.tahmin_timer:
                self.pencere.after_cancel(self.tahmin_timer)
            self.tahmin_timer = self.pencere.after(250, self.canli_tahmin_yap)

    def oyun_cizimi_surdur(self, event):
        if self.oyun_onceki_x is not None:
            self.oyun_tuval.create_line(self.oyun_onceki_x, self.oyun_onceki_y, event.x, event.y,
                                        width=self.oyun_firca_kalinligi, fill=self.oyun_secilen_renk,
                                        capstyle=tk.ROUND, tags="cizgi")
            
            canvas_w = self.oyun_tuval.winfo_width()
            canvas_h = self.oyun_tuval.winfo_height()
            
            w_ratio = self.sanal_boyut / max(1, canvas_w)
            h_ratio = self.sanal_boyut / max(1, canvas_h)
            
            sanal_x1 = self.oyun_onceki_x * w_ratio
            sanal_y1 = self.oyun_onceki_y * h_ratio
            sanal_x2 = event.x * w_ratio
            sanal_y2 = event.y * h_ratio
            
            sanal_kalinlik = max(1, int(round(self.oyun_firca_kalinligi * min(w_ratio, h_ratio))))
            sanal_cizim_rengi = "white" if self.oyun_silgi_modu else "black"
            
            self.oyun_cizici.line([sanal_x1, sanal_y1, sanal_x2, sanal_y2],
                                  fill=sanal_cizim_rengi, width=sanal_kalinlik, joint="curve")
            
            self.oyun_onceki_x, self.oyun_onceki_y = event.x, event.y
            self.oyun_imlec_guncelle(event)

            if self.tahmin_timer:
                self.pencere.after_cancel(self.tahmin_timer)
            self.tahmin_timer = self.pencere.after(250, self.oyun_tahmin_yap)

    def cizimi_bitir(self, event):
        self.onceki_x = self.onceki_y = None
        if self.tahmin_timer:
            self.pencere.after_cancel(self.tahmin_timer)
        self.canli_tahmin_yap()
        self.tuval_yeniden_ciz()
        self.serbest_durum_kaydet()

    def oyun_cizimi_bitir(self, event):
        self.oyun_onceki_x = self.oyun_onceki_y = None
        if self.tahmin_timer:
            self.pencere.after_cancel(self.tahmin_timer)
        self.oyun_tahmin_yap()
        self.oyun_tuval_yeniden_ciz()
        self.oyun_durum_kaydet()

    def tuvali_temizle(self):
        self.tuval.delete("cizgi", "silgi_imleci")
        self.sanal_resim = Image.new("RGB", (self.sanal_boyut, self.sanal_boyut), "white")
        self.cizici      = ImageDraw.Draw(self.sanal_resim)
        self.tuval_yeniden_ciz()
        self.veri_ekrani.configure(image=None)
        self.tk_gorsel   = None
        self.tahmin_etiketi.configure(text="—", text_color=self.aktif_tema["mavi"])
        self.guven_etiketi.configure(text="")
        self.bilgi_etiketi.configure(text="Çizmeye başlayın, tahmin edilecektir.", text_color=self.aktif_tema["yazi_aciklama"])
        
        for sinif in self.ai.siniflar:
            self.barlar[sinif].set(0.0)
            self.yuzde_etiketleri[sinif].configure(text="%0")

        self.serbest_undo_stack.append(self.sanal_resim.copy())
        self.serbest_redo_stack.clear()

    def oyun_tuvali_temizle(self):
        self.oyun_tuval.delete("cizgi", "silgi_imleci")
        self.oyun_sanal_resim = Image.new("RGB", (self.sanal_boyut, self.sanal_boyut), "white")
        self.oyun_cizici      = ImageDraw.Draw(self.oyun_sanal_resim)
        self.oyun_tuval_yeniden_ciz()
        for row in self.oyun_tahmin_satirlari:
            row["lbl"].configure(text="—")
            row["bar"].set(0.0)
            row["val"].configure(text="%0")

        self.oyun_undo_stack.append(self.oyun_sanal_resim.copy())
        self.oyun_redo_stack.clear()

    # ==========================================
    # GERİ AL / İLERİ AL (UNDO / REDO) MANTISI
    # ==========================================
    def klavye_geri_al(self, event=None):
        if self.aktif_sekme == "tuval":
            self.serbest_geri_al()
        elif self.aktif_sekme == "oyun":
            self.oyun_geri_al()

    def klavye_ileri_al(self, event=None):
        if self.aktif_sekme == "tuval":
            self.serbest_ileri_al()
        elif self.aktif_sekme == "oyun":
            self.oyun_ileri_al()

    def serbest_durum_kaydet(self):
        self.serbest_undo_stack.append(self.sanal_resim.copy())
        self.serbest_redo_stack.clear()
        if len(self.serbest_undo_stack) > 31:
            self.serbest_undo_stack.pop(0)

    def oyun_durum_kaydet(self):
        self.oyun_undo_stack.append(self.oyun_sanal_resim.copy())
        self.oyun_redo_stack.clear()
        if len(self.oyun_undo_stack) > 31:
            self.oyun_undo_stack.pop(0)

    def serbest_geri_al(self):
        if len(self.serbest_undo_stack) > 1:
            son_durum = self.serbest_undo_stack.pop()
            self.serbest_redo_stack.append(son_durum)
            
            self.sanal_resim = self.serbest_undo_stack[-1].copy()
            self.cizici = ImageDraw.Draw(self.sanal_resim)
            
            self.tuval_yeniden_ciz()
            self.canli_tahmin_yap()

    def serbest_ileri_al(self):
        if len(self.serbest_redo_stack) > 0:
            durum = self.serbest_redo_stack.pop()
            self.serbest_undo_stack.append(durum)
            
            self.sanal_resim = durum.copy()
            self.cizici = ImageDraw.Draw(self.sanal_resim)
            
            self.tuval_yeniden_ciz()
            self.canli_tahmin_yap()

    def oyun_geri_al(self):
        if len(self.oyun_undo_stack) > 1:
            son_durum = self.oyun_undo_stack.pop()
            self.oyun_redo_stack.append(son_durum)
            
            self.oyun_sanal_resim = self.oyun_undo_stack[-1].copy()
            self.oyun_cizici = ImageDraw.Draw(self.oyun_sanal_resim)
            
            self.oyun_tuval_yeniden_ciz()
            self.oyun_tahmin_yap()

    def oyun_ileri_al(self):
        if len(self.oyun_redo_stack) > 0:
            durum = self.oyun_redo_stack.pop()
            self.oyun_undo_stack.append(durum)
            
            self.oyun_sanal_resim = durum.copy()
            self.oyun_cizici = ImageDraw.Draw(self.oyun_sanal_resim)
            
            self.oyun_tuval_yeniden_ciz()
            self.oyun_tahmin_yap()

    def tahmin_butonuna_basildi(self):
        gri_matris = np.array(self.sanal_resim.convert("L"))
        if np.min(gri_matris) == 255:
            messagebox.showwarning("Boş Çizim Uyarısı", "Lütfen tahmin etmeden önce çizim alanına bir şeyler çizin!")
            self.bilgi_etiketi.configure(text="Uyarı: Boş tuval tahmin edilemez!", text_color=self.aktif_tema["kirmizi"])
            return

        tahmin, guven, matris, olasiliklar, act_map = self.ai.tahmin_et(self.sanal_resim)

        gorsel_copy = self.sanal_resim.copy()
        self.tk_buyuk_gorsel = ctk.CTkImage(light_image=gorsel_copy, dark_image=gorsel_copy, size=(280, 280))
        self.sonuc_gorsel_label.configure(image=self.tk_buyuk_gorsel)

        renk = (self.aktif_tema["yesil"] if guven >= 75 else
                self.aktif_tema["sari"] if guven >= 55 else
                self.aktif_tema["turuncu"])
        self.sonuc_tahmin_etiketi.configure(text=f"Bu bir {tahmin}!", text_color=renk)
        self.sonuc_guven_etiketi.configure(text=f"%{guven} Doğruluk Olasılığı", text_color=renk)

        for i, sinif_adi in enumerate(self.ai.siniflar):
            olasılık = float(olasiliklar[i])
            self.sonuc_barlar[sinif_adi].set(olasılık)
            self.sonuc_yuzde_etiketleri[sinif_adi].configure(text=f"%{int(olasılık * 100)}")

        self.ekran_degistir("sonuc")

    def yeni_cizim_baslat(self):
        self.tuvali_temizle()
        self.ekran_degistir("cizim")

    def canli_tahmin_yap(self):
        gri_matris = np.array(self.sanal_resim.convert("L"))
        
        if np.min(gri_matris) == 255:
            self.tahmin_etiketi.configure(text="—", text_color=self.aktif_tema["mavi"])
            self.guven_etiketi.configure(text="")
            self.bilgi_etiketi.configure(text="Çizmeye başlayın, otomatik tahmin edilecektir.", text_color=self.aktif_tema["yazi_aciklama"])
            self.veri_ekrani.configure(image=None)
            self.tk_gorsel = None
            for sinif in self.ai.siniflar:
                self.barlar[sinif].set(0.0)
                self.yuzde_etiketleri[sinif].configure(text="%0")
            return

        tahmin, guven, matris, olasiliklar, act_map = self.ai.tahmin_et(self.sanal_resim)

        # Termal Isı Haritası (Heatmap) Oluşturma
        lut = []
        for i in range(256):
            v = i / 255.0
            r = int(min(1.0, v * 1.5) * 255)
            g = int(max(0.0, min(1.0, (v - 0.3) * 1.5)) * 255)
            b = int(max(0.0, min(1.0, (v - 0.6) * 2.5)) * 255)
            lut.extend([r, g, b])
            
        act_img = Image.fromarray((act_map * 255).astype(np.uint8), mode="L")
        act_img = act_img.resize((self.ONIZLEME_PX, self.ONIZLEME_PX), Image.Resampling.BILINEAR)
        act_img = act_img.convert("P")
        act_img.putpalette(lut)
        act_img = act_img.convert("RGB")

        self.tk_gorsel = ctk.CTkImage(light_image=act_img, dark_image=act_img, size=(self.ONIZLEME_PX, self.ONIZLEME_PX))
        self.veri_ekrani.configure(image=self.tk_gorsel)

        renk = (self.aktif_tema["yesil"] if guven >= 75 else
                self.aktif_tema["sari"] if guven >= 55 else
                self.aktif_tema["turuncu"])

        self.tahmin_etiketi.configure(text=tahmin, text_color=renk)
        self.guven_etiketi.configure(text=f"%{guven} güven", text_color=renk)
        self.bilgi_etiketi.configure(
            text=f"CNN Aktivasyon Haritası | Güven: %{guven}",
            text_color=self.aktif_tema["yazi_aciklama"])

        for i, sinif_adi in enumerate(self.ai.siniflar):
            olasılık = float(olasiliklar[i])
            self.barlar[sinif_adi].set(olasılık)
            self.yuzde_etiketleri[sinif_adi].configure(text=f"%{int(olasılık * 100)}")

    def oyun_arac_degistir(self, value):
        if value == "Kalem ✏️":
            self.oyun_silgi_modu = False
            self.oyun_secilen_renk = "black"
            self.oyun_tuval.configure(cursor="pencil")
            self.oyun_slider_title.configure(text="Çizgi Kalınlığı:")
            self.oyun_slider.configure(from_=5, to=40, number_of_steps=35)
            self.oyun_slider.set(self.oyun_kalem_kalinligi)
            self.oyun_firca_kalinligi = self.oyun_kalem_kalinligi
            self.oyun_slider_deger.configure(text=f"{self.oyun_firca_kalinligi} px")
            self.btn_oyun_kalem.rol = "aktif_sekme"
            self.btn_oyun_silgi.rol = "pasif_sekme"
        else:
            self.oyun_silgi_modu = True
            self.oyun_secilen_renk = "white"
            self.oyun_tuval.configure(cursor="none")
            self.oyun_slider_title.configure(text="Silgi Kalınlığı:")
            self.oyun_slider.configure(from_=5, to=80, number_of_steps=75)
            self.oyun_slider.set(self.oyun_silgi_kalinligi)
            self.oyun_firca_kalinligi = self.oyun_silgi_kalinligi
            self.oyun_slider_deger.configure(text=f"{self.oyun_firca_kalinligi} px")
            self.btn_oyun_silgi.rol = "aktif_sekme"
            self.btn_oyun_kalem.rol = "pasif_sekme"
        self._widget_renklendir(self.oyun_arac_bari, self.aktif_tema)
        self.oyun_imlec_guncelle()

    def oyun_firca_kalinligi_degisti(self, value):
        val = int(value)
        if self.oyun_silgi_modu:
            self.oyun_silgi_kalinligi = val
            self.oyun_firca_kalinligi = val
        else:
            self.oyun_kalem_kalinligi = val
            self.oyun_firca_kalinligi = val
        self.oyun_slider_deger.configure(text=f"{self.oyun_firca_kalinligi} px")
        self.oyun_imlec_guncelle()

    def yeni_oyun_baslat(self):
        if hasattr(self, "oyun_timer_id") and self.oyun_timer_id:
            self.pencere.after_cancel(self.oyun_timer_id)
            self.oyun_timer_id = None
            
        import random
        # Zorluk seviyesine göre kelime havuzunu filtrele
        if self.aktif_zorluk == "Kolay":
            pool = ["Ev", "Elma", "Güneş", "Ağaç", "Çiçek"]
            self.oyun_sure_limiti = 25
        elif self.aktif_zorluk == "Orta":
            pool = ["Kedi", "Araba", "Kuş", "Balık", "Ev", "Elma", "Güneş", "Ağaç", "Çiçek"]
            self.oyun_sure_limiti = 15
        else: # Zor
            pool = ["Bisiklet", "Kedi", "Araba", "Kuş", "Balık"]
            self.oyun_sure_limiti = 10
            
        self.hedef_kelime = random.choice(pool)
        self.oyun_sure = self.oyun_sure_limiti
        self.oyun_aktif = True
        
        self.oyun_tuvali_temizle()
        
        self.oyun_kelime_label.configure(text=self.hedef_kelime, text_color=self.aktif_tema["mavi"])
        self.oyun_durum_label.configure(text="Çiziminizi yapın...", text_color=self.aktif_tema["yazi_ana"])
        self.oyun_sure_guncelle()
        
        self.lbl_skor.configure(text=f"Skor: {self.oyun_skor}")
        self.lbl_kombo.configure(text=f"Kombo: x{self.oyun_kombo}")
        
        # Reset tool inside game screen back to current game state tab choices
        self.oyun_arac_degistir("Silgi 🧼" if self.oyun_silgi_modu else "Kalem ✏️")
        
        self.oyun_dongusu()

    def oyun_dongusu(self):
        if hasattr(self, "oyun_aktif") and self.oyun_aktif:
            if self.oyun_sure > 0:
                self.oyun_sure -= 1
                self.oyun_sure_guncelle()
                self.oyun_timer_id = self.pencere.after(1000, self.oyun_dongusu)
            else:
                self.oyun_kaybettin()

    def oyun_sure_guncelle(self):
        self.oyun_sure_label.configure(text=f"Kalan Süre: {self.oyun_sure} sn")
        progress = self.oyun_sure / float(self.oyun_sure_limiti)
        self.oyun_sure_bar.set(progress)
        
        if progress > 0.5:
            self.oyun_sure_bar.configure(progress_color=self.aktif_tema["yesil"])
        elif progress > 0.25:
            self.oyun_sure_bar.configure(progress_color=self.aktif_tema["sari"])
        else:
            self.oyun_sure_bar.configure(progress_color=self.aktif_tema["kirmizi"])

    def oyun_tahmin_yap(self):
        if not hasattr(self, "oyun_aktif") or not self.oyun_aktif:
            return
            
        gri_matris = np.array(self.oyun_sanal_resim.convert("L"))
        if np.min(gri_matris) == 255:
            for row in self.oyun_tahmin_satirlari:
                row["lbl"].configure(text="—")
                row["bar"].set(0.0)
                row["val"].configure(text="%0")
            return
            
        tahmin, guven, matris, olasiliklar, act_map = self.ai.tahmin_et(self.oyun_sanal_resim)
        
        # En yüksek olasılıkları sırala
        sorted_indices = np.argsort(olasiliklar)[::-1]
        
        for i in range(3):
            idx = sorted_indices[i]
            label_text = self.ai.siniflar[idx]
            val_pct = int(olasiliklar[idx] * 100)
            
            row = self.oyun_tahmin_satirlari[i]
            row["lbl"].configure(text=label_text)
            row["bar"].set(olasiliklar[idx])
            row["val"].configure(text=f"%{val_pct}")
            
        # Hedef kelime doğru ve yeterli güvenle tahmin edildiyse kazan
        if tahmin == self.hedef_kelime and guven >= 45:
            self.oyun_kazandin(guven)

    def oyun_kazandin(self, guven):
        self.oyun_aktif = False
        if hasattr(self, "oyun_timer_id") and self.oyun_timer_id:
            self.pencere.after_cancel(self.oyun_timer_id)
            self.oyun_timer_id = None
            
        # Puanlama ve Kombo çarpanı hesaplama
        self.oyun_kombo += 1
        sure_yuzde = self.oyun_sure / float(self.oyun_sure_limiti)
        temel_puan = int(sure_yuzde * 100)
        if temel_puan < 15:
            temel_puan = 15 # En az 15 taban puan
            
        # Zorluk çarpanı
        zorluk_katsayisi = 1.0 if self.aktif_zorluk == "Kolay" else 1.5 if self.aktif_zorluk == "Orta" else 2.5
        kazanilan_puan = int(temel_puan * self.oyun_kombo * zorluk_katsayisi)
        
        self.oyun_skor += kazanilan_puan
        self.lbl_skor.configure(text=f"Skor: {self.oyun_skor}")
        self.lbl_kombo.configure(text=f"Kombo: x{self.oyun_kombo}")
        
        # Rekor kaydet
        self.high_score_kaydet(self.aktif_zorluk, self.oyun_skor)
        
        self.oyun_kelime_label.configure(text_color=self.aktif_tema["yesil"])
        self.oyun_durum_label.configure(
            text=f"Tebrikler! +{kazanilan_puan} Puan (Kombo x{self.oyun_kombo}) 🎉", 
            text_color=self.aktif_tema["yesil"]
        )
        
        # Konfeti patlat
        self.konfeti_animasyonu_baslat()

    def oyun_kaybettin(self):
        self.oyun_aktif = False
        self.oyun_kombo = 0
        self.lbl_kombo.configure(text="Kombo: x0")
        
        self.oyun_kelime_label.configure(text_color=self.aktif_tema["kirmizi"])
        self.oyun_durum_label.configure(text="Zaman doldu! Kombo Sıfırlandı. 😢", text_color=self.aktif_tema["kirmizi"])

    # ==========================================
    # 🏆 REKORLAR, ZORLUK, KONFETİ VE GÖRSEL DÖNGÜLER
    # ==========================================
    def high_scores_yukle(self):
        import json
        import os
        self.high_score_dosyası = "high_scores.json"
        try:
            if os.path.exists(self.high_score_dosyası):
                with open(self.high_score_dosyası, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"Kolay": 0, "Orta": 0, "Zor": 0}

    def high_score_kaydet(self, zorluk, skor):
        import json
        scores = self.high_scores_yukle()
        if skor > scores.get(zorluk, 0):
            scores[zorluk] = skor
            self.rekorlar = scores
            try:
                with open(self.high_score_dosyası, "w", encoding="utf-8") as f:
                    json.dump(scores, f, indent=4)
                # Lobideki rekor yazılarını anlık güncelle
                if hasattr(self, "lbl_record_kolay") and self.lbl_record_kolay.winfo_exists():
                    self.lbl_record_kolay.configure(text=f"🟢 Kolay: {scores.get('Kolay', 0)} P")
                    self.lbl_record_orta.configure(text=f"🟡 Orta: {scores.get('Orta', 0)} P")
                    self.lbl_record_zor.configure(text=f"🔴 Zor: {scores.get('Zor', 0)} P")
            except Exception:
                pass

    def zorluk_secildi(self, value):
        self.aktif_zorluk = value
        if value == "Kolay":
            self.oyun_sure_limiti = 25
        elif value == "Orta":
            self.oyun_sure_limiti = 15
        else: # Zor
            self.oyun_sure_limiti = 10

    def konfeti_animasyonu_baslat(self):
        if hasattr(self, "konfeti_timer_id") and self.konfeti_timer_id:
            self.pencere.after_cancel(self.konfeti_timer_id)
            self.konfeti_timer_id = None
            
        self.oyun_tuval.delete("konfeti")
        self.konfeti_partikulleri = []
        self.konfeti_sayac = 0
        self.konfeti_aktif = True
        
        w = max(300, self.oyun_tuval.winfo_width())
        colors = ["#ff007f", "#00ffff", "#39ff14", "#ffff00", "#ffaa00", "#bd93f9", "#ff5555"]
        
        for _ in range(70):
            self.konfeti_partikulleri.append({
                "x": np.random.randint(0, w),
                "y": np.random.randint(-150, 0),
                "size_w": np.random.randint(5, 12),
                "size_h": np.random.randint(5, 12),
                "color": np.random.choice(colors),
                "speed_y": np.random.uniform(3.0, 7.0),
                "speed_x": np.random.uniform(-2.0, 2.0),
                "angle": np.random.uniform(0, 360),
                "spin": np.random.uniform(-8.0, 8.0)
            })
            
        self.konfeti_animasyonu_dongusu()

    def konfeti_animasyonu_dongusu(self):
        if not hasattr(self, "konfeti_aktif") or not self.konfeti_aktif:
            return
            
        self.oyun_tuval.delete("konfeti")
        h = self.oyun_tuval.winfo_height()
        
        still_alive = False
        for p in self.konfeti_partikulleri:
            p["y"] += p["speed_y"]
            p["x"] += p["speed_x"]
            p["angle"] += p["spin"]
            
            if p["y"] < h + 20:
                still_alive = True
                rad = np.radians(p["angle"])
                dw = p["size_w"] * np.cos(rad)
                dh = p["size_h"] * np.sin(rad)
                
                # Çift yönlü dönen poligon (kağıt) efekti
                self.oyun_tuval.create_polygon(
                    p["x"] - dw, p["y"] - dh,
                    p["x"] + dw, p["y"] - dh,
                    p["x"] + dw, p["y"] + dh,
                    p["x"] - dw, p["y"] + dh,
                    fill=p["color"], tags="konfeti"
                )
                
        self.konfeti_sayac += 1
        if self.konfeti_sayac < 60 and still_alive and self.aktif_sekme == "oyun":
            self.konfeti_timer_id = self.pencere.after(30, self.konfeti_animasyonu_dongusu)
        else:
            self.konfeti_aktif = False
            self.oyun_tuval.delete("konfeti")

    def glow_efekti_guncelle(self):
        if not hasattr(self, "glow_sayac"):
            self.glow_sayac = 0.0
        self.glow_sayac += 0.15
        
        # Seçili temanın mavi ve border renklerini alıp aralarında yumuşakça pulse yaptırıyoruz
        c1 = self.aktif_tema["border_renk"]
        c2 = self.aktif_tema["mavi"]
        
        try:
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            
            factor = (np.sin(self.glow_sayac) + 1.0) / 2.0 # 0.0 ile 1.0 arası sinüs
            
            r = int(r1 + (r2 - r1) * factor)
            g = int(g1 + (g2 - g1) * factor)
            b = int(b1 + (b2 - b1) * factor)
            
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            
            if hasattr(self, "cerceve") and self.cerceve.winfo_exists():
                self.cerceve.configure(border_color=color_hex)
            if hasattr(self, "oyun_cerceve") and self.oyun_cerceve.winfo_exists():
                self.oyun_cerceve.configure(border_color=color_hex)
        except Exception:
            pass
            
        self.pencere.after(80, self.glow_efekti_guncelle)

    def pulse_tahmin_guncelle(self):
        if not hasattr(self, "pulse_sayac"):
            self.pulse_sayac = 0.0
        self.pulse_sayac += 0.25
        
        factor = (np.sin(self.pulse_sayac) + 1.0) / 2.0
        
        try:
            # En yüksek olasılıklı sınıfın barını neon yeşil/mavi arası parlat
            tahmin_sinif = self.tahmin_etiketi.cget("text")
            if tahmin_sinif and tahmin_sinif != "—":
                c_mavi = self.aktif_tema["mavi"]
                c_yesil = self.aktif_tema["yesil"]
                
                r1, g1, b1 = int(c_mavi[1:3], 16), int(c_mavi[3:5], 16), int(c_mavi[5:7], 16)
                r2, g2, b2 = int(c_yesil[1:3], 16), int(c_yesil[3:5], 16), int(c_yesil[5:7], 16)
                
                r = int(r1 + (r2 - r1) * factor)
                g = int(g1 + (g2 - g1) * factor)
                b = int(b1 + (b2 - b1) * factor)
                color_hex = f"#{r:02x}{g:02x}{b:02x}"
                
                if tahmin_sinif in self.barlar:
                    self.barlar[tahmin_sinif].configure(progress_color=color_hex)
            
            # Mücadele oyununda kazanıldığında kelime etiketini pulse et
            if hasattr(self, "oyun_aktif") and not self.oyun_aktif and self.oyun_kelime_label.cget("text_color") == self.aktif_tema["yesil"]:
                c_yesil = self.aktif_tema["yesil"]
                c_yazi = self.aktif_tema["yazi_ana"]
                r1, g1, b1 = int(c_yesil[1:3], 16), int(c_yesil[3:5], 16), int(c_yesil[5:7], 16)
                r2, g2, b2 = int(c_yazi[1:3], 16), int(c_yazi[3:5], 16), int(c_yazi[5:7], 16)
                
                r = int(r1 + (r2 - r1) * factor)
                g = int(g1 + (g2 - g1) * factor)
                b = int(b1 + (b2 - b1) * factor)
                color_hex = f"#{r:02x}{g:02x}{b:02x}"
                
                self.oyun_kelime_label.configure(text_color=color_hex)
                self.oyun_durum_label.configure(text_color=color_hex)
        except Exception:
            pass
            
        self.pencere.after(100, self.pulse_tahmin_guncelle)