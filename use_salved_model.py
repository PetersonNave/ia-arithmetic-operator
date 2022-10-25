import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

import numpy as np
from time import sleep
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from mlforkids import MLforKidsImageProject

training_class = MLforKidsImageProject('')


class UseSalvedModel:
    def __get_class_lookup(self, training_image_data):
        class_labels = [None]*training_image_data.num_classes
        class_names = training_image_data.class_indices.keys()
        for classname in class_names:
            class_labels[training_image_data.class_indices[classname]] = classname
        return class_labels

    def __get_training_images_generator(self):
            print("Starting your saved model")
            cachedir = "~/.keras/"
            cachelocation = os.path.join("datasets", "mlforkids", "0b9bc1f0-4446-11ed-9c85-e9175b095422a46f8bf5-ac45-4c45-8d5e-344a7aa7139e")
            projectcachedir = str(os.path.expanduser(os.path.join(cachedir, cachelocation)))
            return ImageDataGenerator().flow_from_directory(str(projectcachedir),
                                                            target_size=MLforKidsImageProject.IMAGESIZE)

    def get_params(self):
        self.training_images = self.__get_training_images_generator()
        self.ml_class_names = self.__get_class_lookup(self.training_images)

    def load_model(self):
        model_path = './tmp/keras_save'
        self.model = tf.keras.models.load_model(model_path)
        self.get_params()

    def prediction(self, image_location: str):
        # self.model.summary()
        testimg = image.load_img(image_location, target_size=MLforKidsImageProject.IMAGESIZE)
        testimg = image.img_to_array(testimg)
        testimg = np.expand_dims(testimg, axis=0)
        predictions = self.model.predict(testimg)
        topprediction = predictions[0]
        topanswer = np.argmax(topprediction)
        return {
            "class_name": self.ml_class_names[topanswer],
            "confidence": 100 * np.max(tf.nn.softmax(topprediction))
        }