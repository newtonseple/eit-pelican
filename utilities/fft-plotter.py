# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Receives serial lines with FFT bins and plots the result in real time.

"""

import serial

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

pointsY0 = [];
pwnd = pg.plot();
curveY0 = pwnd.plot(pen="y", antialias=True);

ser = serial.Serial("COM5",115200);
while(1):
    QtGui.QApplication.processEvents();
    line = ser.readline();
    nums = np.array(line.split());
    curveY0.setData(nums);
    