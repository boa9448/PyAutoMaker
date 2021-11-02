import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras


tf.config.set_visible_devices ([], 'GPU')
class TeachableUtil:
    def __init__(self, modelPath, labelPath):
        # Disable scientific notation for clarity
        #np.set_printoptions(suppress=True)
        self.model = tensorflow.keras.models.load_model(modelPath)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.names = []
        
        with open(labelPath, "rt") as f:
            names = f.readlines()
            names = [name.replace("\n", "") for name in names]
            self.names = names

    def predict(self, img):
        image_array = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) if img.shape[-1] == 4 else img
        image_array = cv2.resize(image_array, (224, 224))
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        self.data[0] = normalized_image_array

        # run the inference
        prediction = self.model.predict(self.data)
        ret = np.argmax(prediction)
        
        return self.names[ret], prediction[0][ret], ret


if __name__ == "__main__":
    pass
