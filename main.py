import tkinter as tk
from arayuz import CizimTahminArayuzu

if __name__ == "__main__":
    # Ana Tkinter penceresini başlatıyoruz
    kutu = tk.Tk()
    
    # Arayüzümüzü bu pencereye yüklüyoruz
    CizimTahminArayuzu(kutu)
    
    # Pencerenin açık kalmasını sağlıyoruz
    kutu.mainloop()