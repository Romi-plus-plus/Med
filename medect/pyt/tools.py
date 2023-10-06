import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import threading
import time
import scipy
import scipy.signal 
from scipy.signal import savgol_filter



# 点可视化，将其绘制至底图
def draw_points(image, points):
    image2 = np.copy(image)
    for p in points:
        x,y = np.int64(p[0]), np.int64(p[1])
        cv2.circle(image2, (x,y), 5, (255,255,255), 5)
        cv2.circle(image2, (x,y), 5, 255, 3)
    return image2

# 特征点可视化，将其绘制至底图
def draw_keypoints(image, keypoints):
    points = [keypoint.pt for keypoint in keypoints]
    return draw_points(image, points)

# 转为灰度
def get_gray_image(image):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return result

# BGR(opencv默认色彩空间)转为RGB(pyplot默认色彩空间)
def get_bgr2rgb_image(image):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return result

def get_orb_feature(image):
    orb = cv2.ORB_create(200, 2.0)
    kp = orb.detect(image, None)
    kp2, des = orb.compute(image, kp)
    return kp2, des

def get_sift_feature(image):
    sift = cv2.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    return kp, des

def get_hog_feature(image):
    #在这里设置参数
    winSize = (128,128)
    blockSize = (64,64)
    blockStride = (8,8)
    cellSize = (16,16)
    nbins = 9

    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    kp, des = hog.detect(image, None)
    return kp, des

# 主要有效
def get_gftt_feature(image):
    orb = cv2.ORB_create()
    ptrGFTT = cv2.GFTTDetector_create(
        maxCorners=0, qualityLevel=0.01, minDistance=20,
        blockSize=20, useHarrisDetector=True, k=0.04)
    kp = ptrGFTT.detect(image, None)
    kp2, des = orb.compute(image, kp)
    return kp2, des

    
# # 更新相对评估位置
# def update_static_frame(frame):
#     global dists, dists_savgol, states
#     frames += [frame]
#     if t % 10 == 0 and t > 10:
#         static_frame = frames[np.argmin(dists[-50:])]
#         keypoints0, descriptors0 = get_orb_feature(static_img)

# 返回特征子匹配平均距离
def get_ave_distance(keypoints1, descriptor1, keypoints2, descriptor2):
    if len(keypoints1) == 0 or len(keypoints2) == 0:
        return -1
    
    if descriptor1.dtype == np.dtype('uint8'):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    else:
        bf = cv2.FlannBasedMatcher()
    matches = bf.match(descriptor1, descriptor2)
    # dist = [m.distance ** 2 for m in matches]
    # print(dist)
    # ave_dist = np.mean(dist)
    matches = sorted(matches, key = lambda x : x.distance)
    n = len(matches)
    if n == 0:
        return -1
    sum1 = 0
    for i in range(0, n):
        a1 = keypoints1[matches[i].queryIdx].pt[0]
        b1 = keypoints1[matches[i].queryIdx].pt[1]
        a2 = keypoints2[matches[i].trainIdx].pt[0]
        b2 = keypoints2[matches[i].trainIdx].pt[1]

        sum1 += pow((a1-a2)*(a1-a2)+(b1-b2)*(b1-b2), 1/2)
        #print(sum1)
    ave_dist = sum1 / n
    
    return ave_dist


def lucas_kanade_ave_distance(p0, p1):
    s = 0
    for j in range(0, len(p1 - p0)):
        # print((p1-p0)[j,0,0])
        s += (p1 - p0)[j, 0, 0] * (p1 - p0)[j, 0, 0] + (p1 - p0)[j, 0, 1] * (p1 - p0)[j, 0, 1]
    s = pow(s, 1 / 2)
    ave_distance = s / len(p1 - p0)

    return ave_distance