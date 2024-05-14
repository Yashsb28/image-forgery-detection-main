import numpy as np
from keras.models import load_model
from ela import convert_to_ela_image


def prepare_image(inp_img):
    image_size = (128, 128)
    return (
        np.array(convert_to_ela_image(inp_img, 90).resize(image_size)).flatten()
        / 255.0
    )  # return ela_image as a numpy array


def predict_result(image):
    model = load_model("trained_model.h5")  # load the trained model
    class_names = ["Forged", "Authentic"]  # classification outputs
    test_image = prepare_image(image)
    temptest_image = test_image.reshape(-1, 128, 128, 3)

    y_pred = model.predict(temptest_image)
    y_pred_class = round(y_pred[0][0])

    prediction = class_names[y_pred_class]
    if y_pred <= 0.5:
        confidence = f"{(1-(y_pred[0][0])) * 100:0.2f}"
    else:
        confidence = f"{(y_pred[0][0]) * 100:0.2f}"
    return (prediction, confidence)