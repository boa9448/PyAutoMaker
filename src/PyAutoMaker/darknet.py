import numpy as np
import cv2

class DarknetUtil:
    DARKNET_SCALE = 0.00392
    def __init__(self, cfg_path : str, model_path : str, net_size : tuple = (416, 416)):
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, model_path)
        self.width = net_size[0]
        self.height = net_size[1]

    def __del__(self):
        pass

    def detect(self, image, thresh = 0.25):
        Height, Width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, self.DARKNET_SCALE, (self.width, self.height), (0,0,0), True, crop=False)

        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        outs = self.net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > thresh:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])


        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        retBoxes = []
        for i in indices:
            x,y,w,h = boxes[i]
            retBoxes.append({"x":x, "y":y, "w":w, "h":h, "id":class_ids[i], "thresh":confidences[i]})
        
        return retBoxes


if __name__ == "__main__":
    pass