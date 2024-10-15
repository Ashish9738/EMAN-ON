from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from config import IMAGE_SIZE, BATCH_SIZE, EPOCHS, LEARNING_RATE

def build_model():
    """
    Builds and compile the CNN model
    """
    model = Sequential()
    model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)))
    model.add(Conv2D(32, (5, 5), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))
    
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(X_train, Y_train, X_val, Y_val):
    """
    Trains the model and plot the training history
    """
    model = build_model()
    
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=2, verbose=1, mode='max')
    
    hist = model.fit(X_train, Y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data=(X_val, Y_val), callbacks=[early_stopping])
    
  
    model.save('fid_image_model.keras')

    """
    Plot training history
    """
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(hist.history['loss'], label='Training Loss', color='blue')
    plt.plot(hist.history['val_loss'], label='Validation Loss', color='red')
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(hist.history['accuracy'], label='Training Accuracy', color='blue')
    plt.plot(hist.history['val_accuracy'], label='Validation Accuracy', color='red')
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()
