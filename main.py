import customtkinter as ctk
from arayuz import CizimTahminArayuzu

if __name__ == "__main__":
    # CustomTkinter görünüm ayarları
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Ana pencereyi başlatıyoruz
    kutu = ctk.CTk()
    
    # Arayüzümüzü bu pencereye yüklüyoruz
    CizimTahminArayuzu(kutu)
    
    # Pencerenin açık kalmasını sağlıyoruz
    kutu.mainloop()