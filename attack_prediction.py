import pandas as pd
import numpy as np
import pickle
import warnings
from tensorflow.keras.models import load_model
warnings.filterwarnings("ignore")


model = load_model('models/ConvolutionalLongShortTermMemory_model.h5')

with open(file='models/Scaler.pkl', mode='rb') as file:
    scaler = pickle.load(file=file)

labels = ['normal','dos','r2l','probe','u2r']


def predict():
    filename = 'in_folder/test.xlsx'
    df = pd.read_excel(filename)
    scaled_data = scaler.transform(df.values)
    model_input = pd.DataFrame(data=scaled_data, columns=df.columns)
    prediction = model.predict(model_input.values, verbose=1)
    label = np.argmax(prediction[0])
    res = labels[label]
    print("res", res)
    return res
