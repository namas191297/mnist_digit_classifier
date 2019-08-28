from tensorflow import keras

dataset = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = dataset.load_data()

train_images = train_images/255.0
test_images = test_images/255.0

model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(28,28)))
model.add(keras.layers.Dense(256, activation=keras.activations.relu))
model.add(keras.layers.Dense(10,activation=keras.activations.softmax))

model.compile(optimizer=keras.optimizers.SGD(lr=0.1), loss=keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])
model.fit(train_images,train_labels,epochs=10,validation_split=0.2)

model.save('mnist_model.h5')

