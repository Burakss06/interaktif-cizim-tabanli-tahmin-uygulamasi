# interaktif-cizim-tabanli-tahmin-uygulamasi
NumPy ve PIL kütüphaneleri kullanılarak geliştirilen, kullanıcı çizimlerini gerçek zamanlı olarak sınıflandıran interaktif tahmin uygulaması.
## Dataset Hazırlama

Bu projede Google Quick Draw veri setinin `numpy_bitmap` formatındaki `.npy` dosyaları kullanılmıştır.

Kullanılan sınıflar:

- cat
- house
- car
- apple
- sun

Ham veriler `data/raw/` klasöründe tutulmaktadır.

Veri hazırlama işlemi `prepare_dataset.py` dosyası ile yapılmaktadır. Bu dosya:

- Her sınıftan 3000 örnek alır.
- Verileri 28x28x1 formatına dönüştürür.
- Piksel değerlerini 0-255 aralığından 0-1 aralığına normalize eder.
- Verileri karıştırır.
- %80 eğitim, %20 test olacak şekilde ayırır.
- Hazırlanmış verileri `data/processed/` klasörüne kaydeder.

Oluşan dosyalar:

- `X_train.npy`
- `X_test.npy`
- `y_train.npy`
- `y_test.npy`
- `classes.txt`

Model eğitimi sırasında `data/processed/` klasöründeki dosyalar kullanılacaktır.
