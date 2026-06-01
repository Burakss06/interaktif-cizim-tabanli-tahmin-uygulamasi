import os
import numpy as np

# Quick Draw veri setinden kullanacağımız sınıflar
# Sıralama çok önemlidir çünkü model çıktıları bu sıraya göre yorumlanacaktır.
# 0 -> cat, 1 -> house, 2 -> car, 3 -> apple, 4 -> sun
# 5 -> dog, 6 -> bird, 7 -> tree, 8 -> bicycle, 9 -> clock
CLASSES = [
    "cat",
    "house",
    "car",
    "apple",
    "sun",
    "dog",
    "bird",
    "tree",
    "bicycle",
    "clock"
]

# Ham .npy dosyalarının bulunduğu klasör
RAW_DIR = "data/raw"

# Hazırlanmış train/test dosyalarının kaydedileceği klasör
PROCESSED_DIR = "data/processed"

# Her sınıftan kaç örnek alınacağı
# 10 sınıf x 3000 örnek = toplam 30000 veri
SAMPLES_PER_CLASS = 3000

# Verinin %20'si test, %80'i eğitim için ayrılacak
TEST_RATIO = 0.2

# processed klasörü yoksa oluşturulur
os.makedirs(PROCESSED_DIR, exist_ok=True)

X_list = []
y_list = []

# Her sınıf için ilgili .npy dosyasını oku
for label, class_name in enumerate(CLASSES):
    file_path = os.path.join(RAW_DIR, f"{class_name}.npy")

    print(f"{class_name}.npy okunuyor...")

    # Quick Draw verileri 28x28 çizimleri 784 uzunluklu vektörler olarak tutar
    data = np.load(file_path)

    # Eğitim süresini kısa tutmak için her sınıftan belirli sayıda örnek alıyoruz
    data = data[:SAMPLES_PER_CLASS]

    # Görseller X listesine, sınıf etiketleri y listesine eklenir
    X_list.append(data)
    y_list.append(np.full(len(data), label))

# Tüm sınıfların verileri tek bir X ve y dizisinde birleştirilir
X = np.concatenate(X_list, axis=0)
y = np.concatenate(y_list, axis=0)

# CNN modeli 28x28x1 formatında görüntü bekler.
# Ayrıca piksel değerleri 0-255 aralığından 0-1 aralığına normalize edilir.
X = X.reshape(-1, 28, 28, 1).astype("float32") / 255.0

# Veriler karıştırılır.
# Böylece model eğitim sırasında sınıfları sırayla değil, karışık şekilde görür.
indices = np.arange(len(X))
np.random.shuffle(indices)

X = X[indices]
y = y[indices]

# Test veri sayısı hesaplanır
test_size = int(len(X) * TEST_RATIO)

# Train/test ayrımı yapılır
X_test = X[:test_size]
y_test = y[:test_size]

X_train = X[test_size:]
y_train = y[test_size:]

# Hazırlanmış dosyalar kaydedilir
np.save(os.path.join(PROCESSED_DIR, "X_train.npy"), X_train)
np.save(os.path.join(PROCESSED_DIR, "X_test.npy"), X_test)
np.save(os.path.join(PROCESSED_DIR, "y_train.npy"), y_train)
np.save(os.path.join(PROCESSED_DIR, "y_test.npy"), y_test)

# Sınıf sıralaması ayrı bir txt dosyasına yazılır.
# Model entegrasyonu sırasında tahmin sonucu bu sıraya göre çevrilecektir.
with open(os.path.join(PROCESSED_DIR, "classes.txt"), "w", encoding="utf-8") as f:
    for i, class_name in enumerate(CLASSES):
        f.write(f"{i}: {class_name}\n")

print("Dataset başarıyla hazırlandı.")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)
print("Sınıflar:", CLASSES)