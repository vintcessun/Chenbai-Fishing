from keras.models import load_model
import cv2
import numpy as np

number_tag={0:"none",
1:"normal",
2:"perfect"
}

def get_result(predicted):
    predicted = list(predicted)
    return number_tag[predicted.index(max(predicted))]

load_model = load_model("model")
unknown_none = cv2.imread('imgs\\none.png').reshape(256,256,3) / 255.0
unknown_normal = cv2.imread('imgs\\normal.png').reshape(256,256,3) / 255.0
unknown_perfect = cv2.imread('imgs\\perfect.png').reshape(256,256,3) / 255.0
unknown_test = cv2.imread("imgs\\test.png").reshape(256,256,3) / 255.0
unknown_test = np.asarray([unknown_test], np.float32)
unknown = np.asarray([unknown_none,unknown_normal,unknown_perfect], np.float32)
predicted = load_model.predict(unknown)
unknown_test = load_model.predict(unknown_test)
print(predicted)
print(unknown_test)
predicted_none = get_result(predicted[0])
predicted_normal = get_result(predicted[1])
predicted_perfect = get_result(predicted[2])
predicted_test = get_result(unknown_test[0])
print(f"none.png => {predicted_none}")
print(f"normal.png => {predicted_normal}")
print(f"perfect.png => {predicted_perfect}")
print(f"test.png => {predicted_test}")

"""
print(f"none.png =>{predicted_none}")
print(f"normal.png =>{predicted_normal}")
print(f"perfect.png =>{predicted_perfect}")
"""