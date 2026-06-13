# train_model.py
import os
import numpy as np
import tensorflow as tf

# 1. Verileri yüklüyoruz
PROCESSED_DIR = "data/processed"

X_train = np.load(os.path.join(PROCESSED_DIR, "X_train.npy"))
X_test = np.load(os.path.join(PROCESSED_DIR, "X_test.npy"))
y_train = np.load(os.path.join(PROCESSED_DIR, "y_train.npy"))
y_test = np.load(os.path.join(PROCESSED_DIR, "y_test.npy"))

print("Veriler yüklendi...")
print(f"Eğitim seti boyutu: {X_train.shape}")
print(f"Test seti boyutu: {X_test.shape}")

# 2. CNN Mimarisi
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    
    tf.keras.layers.Dense(10, activation='softmax')
])

# 3. Modeli Derleme 
# Etiketlerimiz (y) direkt sayısal (0, 1, 2..) olduğu için sparse_categorical_crossentropy kullanıyoruz
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Model eğitimi (train)
# epochs=10: Verilerin üzerinden 10 tur geçerek öğrenecek
print("\nModel eğitimi başlıyor...")
history = model.fit(X_train, y_train,
                    epochs=20,
                    batch_size=64,
                    validation_data=(X_test, y_test))

# Eğitilen modeli kaydediyoruz
model.save("quickdraw_model.keras")
print("\nTebrikler! Model başarıyla eğitildi ve 'quickdraw_model.keras' olarak kaydedildi.")

"""
Veriler yüklendi...
Eğitim seti boyutu: (24000, 28, 28, 1)
Test seti boyutu: (6000, 28, 28, 1)

Model: "sequential_1"

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ conv2d_2 (Conv2D)               │ (None, 26, 26, 32)     │           320 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_2 (MaxPooling2D)  │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_3 (Dropout)             │ (None, 13, 13, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_3 (Conv2D)               │ (None, 11, 11, 64)     │        18,496 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_3 (MaxPooling2D)  │ (None, 5, 5, 64)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_4 (Dropout)             │ (None, 5, 5, 64)       │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten_1 (Flatten)             │ (None, 1600)           │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_2 (Dense)                 │ (None, 128)            │       204,928 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_5 (Dropout)             │ (None, 128)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_3 (Dense)                 │ (None, 10)             │         1,290 │
└─────────────────────────────────┴────────────────────────┴───────────────┘

 Total params: 225,034 (879.04 KB)

 Trainable params: 225,034 (879.04 KB)

 Non-trainable params: 0 (0.00 B)


Model eğitimi başlıyor...
Epoch 1/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 23s 57ms/step - accuracy: 0.6770 - loss: 0.9787 - val_accuracy: 0.8572 - val_loss: 0.4752
Epoch 2/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 21s 56ms/step - accuracy: 0.8307 - loss: 0.5427 - val_accuracy: 0.8807 - val_loss: 0.3823
Epoch 3/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 40s 54ms/step - accuracy: 0.8588 - loss: 0.4490 - val_accuracy: 0.8993 - val_loss: 0.3320
Epoch 4/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.8770 - loss: 0.3969 - val_accuracy: 0.9043 - val_loss: 0.2962
Epoch 5/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 21s 57ms/step - accuracy: 0.8892 - loss: 0.3614 - val_accuracy: 0.9128 - val_loss: 0.2778
Epoch 6/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 41s 58ms/step - accuracy: 0.8961 - loss: 0.3348 - val_accuracy: 0.9120 - val_loss: 0.2712
Epoch 7/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.8996 - loss: 0.3118 - val_accuracy: 0.9202 - val_loss: 0.2457
Epoch 8/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 20s 54ms/step - accuracy: 0.9083 - loss: 0.2934 - val_accuracy: 0.9240 - val_loss: 0.2433
Epoch 9/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.9136 - loss: 0.2730 - val_accuracy: 0.9287 - val_loss: 0.2317
Epoch 10/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 41s 58ms/step - accuracy: 0.9181 - loss: 0.2588 - val_accuracy: 0.9268 - val_loss: 0.2254
Epoch 11/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 40s 54ms/step - accuracy: 0.9208 - loss: 0.2511 - val_accuracy: 0.9252 - val_loss: 0.2353
Epoch 12/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.9262 - loss: 0.2354 - val_accuracy: 0.9297 - val_loss: 0.2220
Epoch 13/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.9264 - loss: 0.2274 - val_accuracy: 0.9290 - val_loss: 0.2203
Epoch 14/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 41s 58ms/step - accuracy: 0.9295 - loss: 0.2173 - val_accuracy: 0.9312 - val_loss: 0.2182
Epoch 15/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 20s 54ms/step - accuracy: 0.9310 - loss: 0.2076 - val_accuracy: 0.9325 - val_loss: 0.2142
Epoch 16/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.9341 - loss: 0.1987 - val_accuracy: 0.9343 - val_loss: 0.2084
Epoch 17/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 23s 60ms/step - accuracy: 0.9344 - loss: 0.2001 - val_accuracy: 0.9337 - val_loss: 0.2101
Epoch 18/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 20s 54ms/step - accuracy: 0.9358 - loss: 0.1927 - val_accuracy: 0.9358 - val_loss: 0.2032
Epoch 19/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 22s 58ms/step - accuracy: 0.9378 - loss: 0.1849 - val_accuracy: 0.9350 - val_loss: 0.2059
Epoch 20/20
375/375 ━━━━━━━━━━━━━━━━━━━━ 40s 54ms/step - accuracy: 0.9413 - loss: 0.1760 - val_accuracy: 0.9358 - val_loss: 0.2042

Tebrikler! Model başarıyla eğitildi ve 'quickdraw_model.keras' olarak kaydedildi.

"""