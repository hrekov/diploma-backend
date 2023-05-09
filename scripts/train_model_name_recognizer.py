import argparse
import os
import json

from argparse import ArgumentTypeError
from pathlib import Path

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint


IMG_WIDTH, IMG_HEIGHT = 224, 224
INPUT_SHAPE = (IMG_WIDTH, IMG_HEIGHT, 3)
BATCH_SIZE = 64
EPOCHS = 25
PROJECT_ROOT = Path('.').resolve().parent
RESOURCE_FOLDER = PROJECT_ROOT / 'resources' / 'model_recognizer'


def load_data(dataset_path: str):
    datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.2)

    train_generator = datagen.flow_from_directory(
        dataset_path,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = datagen.flow_from_directory(
        dataset_path,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    return train_generator, validation_generator


def build_model(input_shape, train_generator):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_generator.class_indices), activation='softmax'))

    return model


def compile_and_train(model, train_generator, validation_generator):
    model.compile(
        loss='categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )

    checkpoint_filepath = str(RESOURCE_FOLDER / 'model.h5')

    checkpoint = ModelCheckpoint(
        checkpoint_filepath,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )

    return model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=[checkpoint]
    )


def save_labels_to_json(train_generator, labels_json_file):
    labels_dict = train_generator.class_indices

    with open(labels_json_file, 'w') as f:
        json.dump(labels_dict, f)


def validate_folder_path(folder_path):
    """
    Validate whether the provided folder path exists.
    """
    if not os.path.exists(folder_path):
        raise ArgumentTypeError(f"{folder_path} does not exist.")

    return folder_path


def main():
    parser = argparse.ArgumentParser(description='Validate dataset folder path')
    parser.add_argument(
        'dataset_path',
        type=validate_folder_path,
        help='Path to the dataset folder',
    )

    args = parser.parse_args()

    train_generator, validation_generator = load_data(args.dataset_path)
    model = build_model(INPUT_SHAPE, train_generator)
    model.summary()
    compile_and_train(model, train_generator, validation_generator)
    save_labels_to_json(train_generator, RESOURCE_FOLDER / 'labels.json')


if __name__ == '__main__':
    main()
