import os
import skimage.io

def read_images(folder, ext):
    files = os.listdir(folder)
    images = []
    for f in files:
        images.append(skimage.io.imread(folder+"/"+f, True))
    return images

def read_samples(pos_folder, neg_folder, ext=".pgm"):
    pos_images = read_images(pos_folder, ext)
    neg_images = read_images(neg_folder, ext)
    return pos_images, neg_images

def extract_features(image, types=['pixels']):
    flattened = []
    for arr in image:
        for pix in arr:
            flattened.append(pix)
    return flattened

def train(pos_folder, neg_folder, ext='.pgm', feature_types=['pixels']):
    samples = read_samples(pos_folder, neg_folder, ext)
    pos = samples[0]
    neg = samples[1]
    positives = []
    negatives = []
    for img in pos:
        positives.append(extract_features(img, feature_types))
    for img in neg:
        negatives.append(extract_features(img, feature_types))



train('faces/train/face', 'faces/train/non-face')
