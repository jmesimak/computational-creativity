import os
import skimage.io
import sklearn.ensemble
import numpy as np
from sklearn.externals import joblib

def read_images(folder, ext):
    files = os.listdir(folder)
    images = []
    for f in files:
        images.append(skimage.io.imread(folder+"/"+f, True))
    return np.array(images, np.uint16)

def read_samples(pos_folder, neg_folder, ext=".pgm"):
    pos_images = read_images(pos_folder, ext)
    neg_images = read_images(neg_folder, ext)
    return pos_images, neg_images

def extract_features(image, types=['pixels']):
    flattened = []
    for arr in image:
        for pix in arr:
            flattened.append(pix)
    return np.array(flattened, np.uint16)

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

    pnp16 = np.array(positives, np.uint16)
    nnp16 = np.array(negatives, np.uint16)

    poslabels = []
    neglabels = []
    for i in pnp16:
        poslabels.append(1)
    for i in nnp16:
        neglabels.append(0)

    poslabels = np.array(poslabels, np.uint8)
    neglabels = np.array(neglabels, np.uint8)

    concatnp16 = np.concatenate([pnp16, nnp16])
    concatlabels = np.concatenate([poslabels, neglabels])
    shuffled = shuffle_in_unison(concatnp16, concatlabels)
    shufflednp16 = shuffled[0]
    shuffledlabels = shuffled[1]

    joblib.dump(sklearn.ensemble.AdaBoostClassifier().fit(shufflednp16, shuffledlabels), 'pickle/pixclassifier.pkl')


def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


train('faces/train/face', 'faces/train/non-face')
