from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection
import matplotlib.pyplot as plt
import cv2

classes = ["Japanese_castle","Europe_castle","Chinese_castle"]
num_classes = len(classes)
image_size = 50

def scratch_image(img, flip=True, thr=True, filt=True, resize=True, erode=True):
    methods = [flip, thr, filt, resize, erode]
    img_size = img.shape
    filter1 = np.ones((3, 3))
    images = [img]
    scratch = np.array([
        lambda x: cv2.flip(x, 1),
        lambda x: cv2.threshold(x, 100, 255, cv2.THRESH_TOZERO)[1],
        lambda x: cv2.GaussianBlur(x, (5, 5), 0),
        lambda x: cv2.resize(cv2.resize(
                       x, (img_size[1] // 5, img_size[0] // 5)
                    ),(img_size[1], img_size[0])),
        lambda x: cv2.erode(x, filter1)
    ])
    
    doubling_images = lambda f, imag: (imag + [f(i) for i in imag])
    for func in scratch[methods]:
        images = doubling_images(func, images)
    
    return images


X = []
Y = []
for index, classlabel in enumerate(classes):
    photos_dir = "castle/{}".format(classlabel)
    files = glob.glob(photos_dir + "/*.jpg")
    print(files)
    for i, file in enumerate(files):
        if i >= 200: break
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))
        data = np.asarray(image)
        data = scratch_image(data)


        if not os.path.exists("castle/{}".format(classlabel)+"_images"):
            os.mkdir("castle/{}".format(classlabel)+"_images")
        for num, im in enumerate(data):
            cv2.imwrite("castle/{}".format(classlabel)+"_images/" + str(i)+"_"+str(num) + ".jpg" ,im)