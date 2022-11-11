import os.path

import tensorflow as tf
import numpy as np

# Path definition
data_path = "data_right.npy"
label_path = "label_right.npy"
model_save_path = "model_right.hdf5"

# Loading data and label
data = np.load(data_path)
label = np.load(label_path)

# Splitting the dataset
TEST_SPLIT = 0.2

dataset_size = len(label)
training_split = int((1 - TEST_SPLIT) * dataset_size)

selection = np.random.permutation(dataset_size)

training_data = data[selection[:training_split]]
training_label = label[selection[:training_split]]

test_data = data[selection[training_split:]]
test_label = label[selection[training_split:]]

print(f"Training data shape : {training_data.shape}\nTest data shape : {test_data.shape}")

NUM_CLASSES = 10

# Building model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=[21, 2]),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

# Model checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    model_save_path, verbose=0, save_weights_only=False)
# Callback for early stopping
es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

# Model compilation
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    training_data,
    training_label,
    epochs=1000,
    batch_size=128,
    validation_split=0.2,
    callbacks=[cp_callback, es_callback],
    verbose=0
)

loss, acc = model.evaluate(test_data, test_label)
print(f"Loss : {loss} \t Accuracy : {acc}")

model.save(model_save_path)