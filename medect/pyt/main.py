# 主程序：获取帧画面并处理
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mahotas.features import surf
import cv2
import glob
import os
from datetime import datetime
import shutil
import PySimpleGUI as sg
import time
import matplotlib.pyplot as plt
from math import *
import scipy
import zmq
import threading
import sys

import tools

flag = True
time_t = time.perf_counter()

# plt.rcParams['figure.figsize'] = (12.0, 8.0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams['font.size'] = 8

# 背景色
# sg.theme('DarkAmber')

# 定义窗口布局
layout = [
    # [sg.Image(key='image', size=(100, 100))],
    [
        sg.Text('正面设备号'), sg.Combo(['0', '1', '2'], default_value='0', key='combo_cap_idx0'),
        sg.Text('左耳设备号'), sg.Combo(['0', '1', '2'], default_value='0', key='combo_cap_idx1'),
        sg.Text('右耳设备号'), sg.Combo(['0', '1', '2'], default_value='0', key='combo_cap_idx2'),
        sg.Button('重设', key='set_cap_idx', size=(10, 1))
    ],
    [sg.Slider(range=(0, 15), orientation='h', size=(40, 15), default_value=6, key='threshold1')],
    [sg.Slider(range=(0, 15), orientation='h', size=(40, 15), default_value=6, key='threshold2')],
    [sg.Text('阈值1'), sg.Text(size=(20, 1), key='label_threshold1'), sg.Text('阈值1'),
     sg.Text(size=(20, 1), key='label_threshold2')],
    [sg.Text('当前FPS'), sg.Text(size=(20, 1), key='label_fps')],
    [sg.Text('左耳动'), sg.Text(size=(20, 1), key='left_ear_count')],
    [sg.Text('右耳动'), sg.Text(size=(20, 1), key='right_ear_count')],
    [
        sg.Button('关闭图像预览', key='close_image', size=(20, 1)),
        sg.Button('开始测试', key='start_test', size=(20, 1)),
    ], [
        sg.Button('开始进行通信', key='start_communication', size=(20, 1)),
        sg.Button('停止进程通信', key='stop_communication', size=(20, 1))
    ], [
        sg.Button('Exit', size=(20, 1))
    ],
    [sg.Text('时间'), sg.Text(size=(20,1), key='time_t')]
]


# tcp通信
def server_communication():
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # try:
    while True:
        # message = socket.recv()
        message = socket.recv()
        print("Received request: %s" % message)
        if len(states1) > 0 and len(states2) > 0:
            send_message = b'%d,%d' % (int(states1[-1]), int(states2[-1]))
        else:
            send_message = b'%d,%d' % (0, 0)
        socket.send(send_message)

    # socket.send(b'%d, %d' % (states1[-1], states2[-1]))


# except:
# 	pass


def server_stop():
    global context
    context.destroy()
    context = zmq.Context()


# 记录dist，并处理得到state
def signal_process(dist1, dist2):
    global dists1, dists2, dists1_savgol, dists2_savgol, states1, states2, left_ear_count, right_ear_count
    # 记录
    if dist1 == -1:
        if len(dists1) > 0:
            dist1 = dists1[-1]
        else:
            dist1 = 0

    if dist2 == -1:
        if len(dists1) > 0:
            dist2 = dists2[-1]
        else:
            dist2 = 0

    dists1 += [dist1]
    dists2 += [dist2]
    if len(dists1) > 7:
        dists1_savgol = scipy.signal.savgol_filter(dists1, 7, 5)  # 平滑化（小幅度平滑）
    if len(dists2) > 7:
        dists2_savgol = scipy.signal.savgol_filter(dists2, 7, 5)  # 平滑化（小幅度平滑）
    # 信号处理
    state1 = False if dist1 < threshold1 else True
    state2 = False if dist2 < threshold2 else True
    states1 += [state1]
    states2 += [state2]
    if dist1 > threshold1:
        left_ear_count += 1
    if dist2 > threshold2:
        right_ear_count += 1

# # 更新相对评估位置
# def update_static_frame(frame):
# 	global dists, dists_savgol, states
# 	frames += [frame]
# 	if t % 10 == 0 and t > 10:
# 		static_frame = frames[np.argmin(dists[-50:])]
# 		keypoints0, descriptors0 = get_orb_feature(static_img)

# 初始化
def init_record():
    global dists1, dists2, dists1_savgol, dists2_savgol, states1, states2
    t = 0
    dists1, dists2 = [], []
    dists1_savgol, dists2_savgol = [], []
    states1, states2 = [], []


#
context = zmq.Context()

# 打开内置摄像头
cap_idx0 = 0
cap_idx1 = 0
cap_idx2 = 0

cap = [cv2.VideoCapture(0), cv2.VideoCapture(1), cv2.VideoCapture(2)]
# cap0 = cv2.VideoCapture(cap_idx0)
# cap1 = cv2.VideoCapture(cap_idx1)
# cap2 = cv2.VideoCapture(cap_idx2)
# ret1, frame1 = cap1.read()
# ret2, frame2 = cap2.read()

is_static_frame_saved = False
is_testing = False
is_communication = True

# static_frame1 = None
# static_frame2 = None
# static_keypoints1, static_descriptors1 = None, None
# static_keypoints2, static_descriptors2 = None, None

# 信号
# 全局变量记录
t = 0
window_size = 100
dists1, dists2 = [], []
frames1, frames2 = [], []
dists1_savgol, dists1_savgol = [], []
states1, states2 = [], []
left_ear_count = 0
right_ear_count = 0
threshold1, threshold2 = 60, 60
image_show = 1

# 窗口设计
window = sg.Window(
    'Ear Moving Tracer',
    layout,
    # location=(800, 50),
    font=("Microsoft Yahei", 10),
    finalize=True,
)

while True:
    t += 1
    event, values = window.read(timeout=0.1, timeout_key='timeout')

    # 读取内窥镜画面
    # ret0, frame0 = cap[cap_idx0].read()
    ret1, old_frame1 = cap[cap_idx1].read()
    ret2, old_frame2 = cap[cap_idx2].read()
    ret1, base_frame1 = cap[cap_idx1].read()
    ret2, base_frame2 = cap[cap_idx2].read()

    #一直更新初始帧
    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    color = np.random.randint(0, 255, (100, 3))
    old_gray1 = cv2.cvtColor(old_frame1, cv2.COLOR_BGR2GRAY)
    old_gray2 = cv2.cvtColor(old_frame2, cv2.COLOR_BGR2GRAY)

    p0_1 = cv2.goodFeaturesToTrack(old_gray1, mask=None, **feature_params)
    p0_2 = cv2.goodFeaturesToTrack(old_gray2, mask=None, **feature_params)

    if is_testing:
        ret1, frame1 = cap[cap_idx1].read()
        ret2, frame2 = cap[cap_idx2].read()
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        if p0_1 is not None and p0_2 is not None:

            p1_1, st_1, err_1 = cv2.calcOpticalFlowPyrLK(old_gray1, frame1_gray, p0_1, None, **lk_params)
            p1_2, st_2, err_2 = cv2.calcOpticalFlowPyrLK(old_gray2, frame2_gray, p0_2, None, **lk_params)# 计算新的一副图像中相应的特征点额位置
            #dist1 = tools.get_ave_distance(static_keypoints1, static_descriptors1, keypoints1, descriptors1)
            #dist2 = tools.get_ave_distance(static_keypoints2, static_descriptors2, keypoints2, descriptors2)
            dist1 = tools.lucas_kanade_ave_distance(p0_1, p1_1)
            dist2 = tools.lucas_kanade_ave_distance(p0_2, p1_2)
        else:
            dist1 = dist2 = 0
        signal_process(dist1, dist2)
        
    if image_show == 1:
    # 更新GUI: 内窥镜获取的画面
    #frame1_drawed = tools.draw_keypoints(frame1, keypoints1)
    #frame2_drawed = tools.draw_keypoints(frame2, keypoints2)
        # cv2.namedWindow("Monitor Yourself", 0);
        # cv2.imshow('Monitor Yourself', frame0)
        cv2.namedWindow("Monitor Left Ear", 0);
        cv2.imshow('Monitor Left Ear', base_frame1)
        cv2.namedWindow("Monitor Right Ear", 0);
        cv2.imshow('Monitor Right Ear', base_frame2)


    # 更新GUI: 信号波动
    if flag:
         if is_testing and t % 20 == 0:
            plt.clf()  # 清空画布上的所有内容
            plt.subplot(4, 1, 1)
            plt.axhline(y=threshold1, c="orange")
            plt.plot(dists1_savgol)
        
            plt.subplot(4, 1, 2)
            plt.axhline(y=threshold2, c="orange")
            plt.plot(dists2_savgol)
        
            plt.subplot(4, 1, 3)
            plt.plot(states1, color='orange')
            plt.subplot(4, 1, 4)
            plt.plot(states2, color='orange')
        
            plt.pause(0.01)
            #pass
        # 更新GUI: 文字标签

    fps = cap[cap_idx1].get(cv2.CAP_PROP_FPS)
    window['label_fps'].update(fps)
    #window['label_static_frame'].update(str(is_static_frame_saved))

    threshold1 = values['threshold1']
    threshold2 = values['threshold2']
    window['left_ear_count'].update(left_ear_count)
    window['right_ear_count'].update(right_ear_count)
    window['label_threshold1'].update(str(threshold1))
    window['label_threshold2'].update(str(threshold2))
    window['time_t'].update(str(time.perf_counter() - time_t))
    time_t = time.perf_counter()


    # 按钮事件
    if event == 'close_image':
        # static_frame1 = frame1
        # static_frame2 = frame2
        # static_keypoints1, static_descriptors1 = tools.get_orb_feature(static_frame1)
        # static_keypoints2, static_descriptors2 = tools.get_orb_feature(static_frame2)
        # is_static_frame_saved = True
        image_show = 0
        cv2.destroyAllWindows()
    elif event == 'start_test':
        # if not is_static_frame_saved:
        #     sg.popup_ok('先存比对帧', modal=True, keep_on_top=True, grab_anywhere=False, font=("Microsoft Yahei", 10), )
        #
        # else:
        is_testing = True
        # 记录初始化
        init_record()
        # plt画布窗体准备
        if flag:
            plt.ion()
            plt.figure(1)

    elif event == 'start_communication':
        thread_server = threading.Thread(target=server_communication)
        thread_server.start()
        print('start communication')

    elif event == 'stop_communication':
        server_stop()

    # 重设左右耳设备号
    elif event == 'set_cap_idx':
        print(int(values['combo_cap_idx0']), int(values['combo_cap_idx1']), int(values['combo_cap_idx2']))
        cap_idx0 = int(values['combo_cap_idx0'])
        cap_idx1 = int(values['combo_cap_idx1'])
        cap_idx2 = int(values['combo_cap_idx2'])

    # cap0 = cv2.VideoCapture(cap_idx0)
    # cap1 = cv2.VideoCapture(cap_idx1)
    # cap2 = cv2.VideoCapture(cap_idx2)

    elif event == 'Exit' or event is None:
        socket.close()
        context.term()
        sys.exit(0)
        break

window.close()
sys.exit(0)