#!/usr/bin/env python

"""code template"""

import os
import random
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
import xml.etree.ElementTree as et
from sklearn.metrics import confusion_matrix

class_id_to_new_class_id = {"crosswalk": 2, "other": 0}

def load_data(path, path_image):
    """
    Loads data from disk.
    @param path: Path to xml file
    @param path_image: Path to image
    @return: List of dictionaries, one for every sample, with entries "image" (np.array with image) and "label" (class_id).
    """

    data = []

    for x in (os.listdir(path)):
        tree = et.parse(os.path.join(path, x))
        root = tree.getroot()

        for i in root.findall('size'):
            width = float(i.find('width').text)
            height = float(i.find('height').text)

        for y in root.findall('object'):
            classId = y.find('name').text
            if classId != 'crosswalk':
                classId = 'other'

            class_id = class_id_to_new_class_id[classId]

            for z in y.findall('bndbox'):
                x_min = int(z.find('xmin').text)
                x_max = int(z.find('xmax').text)
                y_min = int(z.find('ymin').text)
                y_max = int(z.find('ymax').text)

            image_path = os.getcwd() + '\\' + path_image + '\\' + root[1].text

            if x_max - x_min >= 0.1*width and y_max - y_min >= 0.1*height:
                image = cv2.imread(os.path.join(path, image_path))
                cutimg = image[int(y_min) : int(y_max), int(x_min) : int(x_max)]
                data.append({'image': cutimg, 'label': class_id, 'file': x,'xmin': x_min,'xmax': x_max ,'ymin': y_min,'ymax': y_max})

    return data


def learn_bovw(data):
    """
    Learns BoVW dictionary and saves it as "voc.npy" file.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image) and "label" (class_id).
    @return: Nothing
    """
    dict_size = 128
    bow = cv2.BOWKMeansTrainer(dict_size)

    sift = cv2.SIFT_create()
    for sample in data:
        kpts = sift.detect(sample['image'], None)
        kpts, desc = sift.compute(sample['image'], kpts)

        if desc is not None:
            bow.add(desc)

    vocabulary = bow.cluster()

    np.save('voc.npy', vocabulary)


def extract_features(data):
    """
    Extracts features for given data and saves it as "desc" entry.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image) and "label" (class_id).
    @return: Data with added descriptors for each sample.
    """
    sift = cv2.SIFT_create()
    flann = cv2.FlannBasedMatcher_create()
    bow = cv2.BOWImgDescriptorExtractor(sift, flann)
    vocabulary = np.load('voc.npy')
    bow.setVocabulary(vocabulary)
    for sample in data:
        kpts = sift.detect(sample['image'], None)
        desc = bow.compute(sample['image'], kpts)
        sample['desc'] = desc

    return data


def train(data):
    """
    Trains Random Forest classifier.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor).
    @return: Trained model.
    """
    descs = []
    labels = []
    for sample in data:
        if sample['desc'] is not None:
            descs.append(sample['desc'].squeeze(0))
            labels.append(sample['label'])
    rf = RandomForestClassifier()
    rf.fit(descs, labels)

    return rf

def predict(rf, data):
    """
    Predicts labels given a model and saves them as "label_pred" (int) entry for each sample.
    @param rf: Trained model.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor).
    @return: Data with added predicted labels for each sample.
    """

    for sample in data:
        if sample['desc'] is not None:
            predict = rf.predict(sample['desc'])
            sample['label_pred'] = int(predict)
    return data


def evaluate(data):
    """
    Evaluates results of classification.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor), and "label_pred".
    @return: Nothing.
    """
    correct = 0
    incorrect = 0
    eval = []
    real = []
    for sample in data:
        if sample['desc'] is not None:
            eval.append(sample['label_pred'])
            real.append(sample['label'])
            if sample['label_pred'] == sample['label']:
                correct += 1
                if sample['label_pred'] == class_id_to_new_class_id['crosswalk']:
                    print(sample['file'], sample['xmin'], sample['xmax'], sample['ymin'], sample['ymax'])
            else:
                incorrect += 1

    print('score = %.3f' % (correct / max(correct + incorrect, 1)))
    conf_matrix = confusion_matrix(real, eval)
    print(conf_matrix)
    return


def display_dataset_stats(data):
    """
    Displays statistics about dataset in a form: class_id: number_of_samples
    @param data: List of dictionaries, one for every sample, with entry "label" (class_id).
    @return: Nothing
    """
    class_to_num = {}
    for idx, sample in enumerate(data):
        class_id = sample['label']
        if class_id not in class_to_num:
            class_to_num[class_id] = 0
        class_to_num[class_id] += 1

    class_to_num = dict(sorted(class_to_num.items(), key=lambda item: item[0]))
    print(class_to_num)


def balance_dataset(data, ratio):
    """
    Subsamples dataset according to ratio.
    @param data: List of samples.
    @param ratio: Ratio of samples to be returned.
    @return: Subsampled dataset.
    """
    sampled_data = random.sample(data, int(ratio * len(data)))

    return sampled_data


def main():

    data_train = load_data('Train/annotations', 'Train/images')
    print('train dataset before balancing:')
    display_dataset_stats(data_train)
    data_train = balance_dataset(data_train, 1.0)
    print('train dataset after balancing:')
    display_dataset_stats(data_train)


    data_test = load_data('Test/annotations', 'Test/images')
    print('test dataset before balancing:')
    display_dataset_stats(data_test)
    data_test = balance_dataset(data_test, 1.0)
    print('test dataset after balancing:')
    display_dataset_stats(data_test)

    # you can comment those lines after dictionary is learned and saved to disk.
    print('learning BoVW')
    learn_bovw(data_train)

    print('extracting train features')
    data_train = extract_features(data_train)

    print('training')
    rf = train(data_train)

    print('extracting test features')
    data_test = extract_features(data_test)

    print('testing on testing dataset')
    data_test = predict(rf, data_test)
    evaluate(data_test)

    return


if __name__ == '__main__':
    main()