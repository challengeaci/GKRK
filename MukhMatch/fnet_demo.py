import tensorflow as tf
import numpy as np
import facenet
from align import detect_face
import cv2
import os
from xlwt import Workbook

wb = Workbook()
sheet1 = wb.add_sheet('Sheet1')

# Default constants for FaceNet suggested by Google
minimum_size = 20
threshold = [0.6, 0.7, 0.7]
factor = 0.709
margin = 44
ii_size = 160

sess = tf.Session()

# OSS implementation of high level CNN
pnet, rnet, onet = detect_face.create_mtcnn(sess, 'align')

# Pre-trained model for high precision results
facenet.load_model("20170512-110547/20170512-110547.pb")

images_ = tf.get_default_graph().get_tensor_by_name("input:0")
embeds = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_ = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embed_size = embeds.get_shape()[1]


def get_face(img):
    faces = []
    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes = detect_face.detect_face(img, minimum_size, pnet, rnet, onet, threshold, factor)[0]
    if not len(bounding_boxes) == 0:
        for face in bounding_boxes:
            if face[4] > 0.50:
                det = np.squeeze(face[0:4])
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = np.maximum(det[0] - margin / 2, 0)
                bb[1] = np.maximum(det[1] - margin / 2, 0)
                bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
                resized = cv2.resize(cropped, (ii_size, ii_size), interpolation=cv2.INTER_CUBIC)
                prewhitened = facenet.prewhiten(resized)
                faces.append(
                    {'face': resized, 'rect': [bb[0], bb[1], bb[2], bb[3]], 'embedding': embed(prewhitened)})
    return faces


def embed(resized):
    reshaped = resized.reshape(-1, ii_size, ii_size, 3)
    feed_dict = {images_: reshaped, phase_train_: False}
    embedding = sess.run(embeds, feed_dict=feed_dict)
    return embedding


def compare_faces(face1, face2):
    face1 = get_face(face1)
    face2 = get_face(face2)
    if face1 and face2:
        distance = np.sqrt(np.sum(np.square(np.subtract(face1[0]['embedding'], face2[0]['embedding']))))
        return distance
    return -1


def match(face1, face2):
    img1 = cv2.imread(face1)
    img2 = cv2.imread(face2)
    distance = compare_faces(img1, img2)
    threshold = 0.9
    return distance <= threshold

def update_attendance(name, status):
    with open("attendance.json", 'a') as f:
        f.write({name: status})

def match_db(face):
    for f in os.listdir(r'Faces/'):
        try:
            if match(face, 'Faces\\' + f):
                sheet1.write(1,0,f.split(".")[0])
                wb.save('D:\\Sample.xls')
                return f.split(".")[0]
        except Exception as e:
            -1
    return "Mismatch"


'''
OSS mentions: https://www.python36.com/face-detection-matching-using-facenet/
                https://medium.freecodecamp.org/making-your-own-face-recognition-system-29a8e728107c
'''
