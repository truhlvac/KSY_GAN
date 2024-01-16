from numpy import expand_dims
from numpy import zeros
from numpy import ones
from numpy.random import randn
from numpy.random import randint
import pandas as pd
import os
from icecream import ic
import numpy as np
import cv2

import matplotlib.pyplot as plt

def process_images(dataframe, target_size=(64, 64)):
    processed_images = []
    label_counter = np.zeros(8, dtype=int)
    labels = []
    for i, row in dataframe.iterrows():
        img_path = os.path.join("img_align_celeba", row['nameofimage'])
        if not os.path.exists(img_path):
            continue  # skip if file does not exist
        # Read the image
        if label_counter[int(row['label'])] < 2000:
            label_counter[int(row['label'])] += 1
        else:
            continue
        img = cv2.imread(img_path)

        # Resize the image
        resized_img = cv2.resize(img, target_size)
        rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
        # Append to the list
        processed_images.append(rgb_img)
        labels.append(int(row['label']))

    return np.array(processed_images), np.array(labels)

# load CUB dataset images
def load_celebs():
    # load images
    current_path = os.getcwd()
    # ic(current_path)
    # ic(os.path.join(current_path, 'CUB_200_2011', 'CUB_200_2011', 'images.txt'))
    df = pd.read_csv('filtered_file.txt', delim_whitespace=True, header=None, dtype='str')
    df.columns = df.iloc[0]

    ic(df.shape)
    # ic(data.head())

    image_data, labels = process_images(df)
    image_data = image_data.astype('float32')
    image_data = (image_data - 127.5) / 127.5
    # ic(image_data.shape)
    # ic(image_data.min(), image_data.max())
    labels = labels.astype('float32')

    ic(labels[0:70])
    ic(labels.shape)
    ic(image_data.shape)
    # if train:
    #     data = data[data.is_training_img == 1]
    # else:
    #     data = data[data.is_training_img == 0]

    return image_data, labels

image_data, labels = load_celebs()
np.save('image_data_c.npy', image_data)
np.save('labels_c.npy', labels)
