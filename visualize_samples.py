import numpy as np
import matplotlib.pyplot as plt

# Hazırlanmış train verisini yükle
X_train = np.load("data/processed/X_train.npy")
y_train = np.load("data/processed/y_train.npy")

# Sınıf isimleri
CLASSES = ["cat", "house", "car", "apple", "sun", "bird", "tree", "bicycle", "fish", "flower"]

# İlk örneği seç
image = X_train[0]
label = y_train[0]

# Görseli göster
plt.imshow(image.squeeze(), cmap="gray")
plt.title(f"Class: {CLASSES[label]}")
plt.axis("off")

plt.show()