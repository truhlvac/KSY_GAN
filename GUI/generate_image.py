import random
from numpy import asarray
from numpy.random import randn
from numpy.random import randint
from keras.models import load_model
import numpy as np
 
def generate_latent_points_birds(latent_dim, n_samples):
    x_input = randn(latent_dim * n_samples)
    z_input = x_input.reshape(n_samples, latent_dim)
    labels = randint(1, 11, n_samples)
    return [z_input, labels]

def generate_latent_points_celebs(latent_dim, n_samples):
    x_input = randn(latent_dim * n_samples)
    z_input = x_input.reshape(n_samples, latent_dim)
    labels = randint(0, 8, n_samples)
    return [z_input, labels]

def image_generator(dataset, selected_class):
    print("generating image for: ", dataset)
    n_samples = 1
    if dataset == "Birds":
        model = load_model('birds_generator.h5')
        latent_points, labels = generate_latent_points_birds(latent_dim=100, n_samples=n_samples)
    else:
        model = load_model('celebs_generator.keras')
        latent_points, labels = generate_latent_points_celebs(latent_dim=100, n_samples=n_samples)
    # specify labels
    labels = np.zeros(1, dtype=int)
    labels[0] = selected_class
    # generate image
    X  = model.predict([latent_points, labels])
    X = (X + 1) * 127.5

    return X[0]
