# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Receives serial lines with FFT bins and plots the result in real time.

"""

import serial

import numpy as np
#import pyqtgraph as pg
#from pyqtgraph.Qt import QtGui, QtCore

from threading import Thread
from queue import Queue

class Barryvox:
    # TODO unify state in a single model.
    bins = {6:"turn",
            9:"normal",
            11:"close",
            12:"close",
            13:"close",
            14:"close",
            15:"close",
            16:"close",
            17:"close",
            20:"ahead",
            #12:"error",
            }
    bins_distance = {6:8,
            9:7,
            11:6,
            12:5,
            13:4,
            14:3,
            15:2,
            16:1,
            17:0,
            20:7,
            #12:"error",
            }
    def __init__(self, tty, baud):
        self.state = "nosignal"
        self.distance = 7 # 7 = normal, 6-0 = close
        self.ser = serial.Serial(tty,baud)
        self.spectrum = np.array(np.zeros(128), dtype=np.float32)
        self.timer = 0;
    def set_state(self, newstate):
        if self.state != newstate:
            self.state = newstate
            #print("STATE CHANGE: " + self.state)
    def process_signal(self, bin, amplitude):
        if bin in self.bins:
            self.set_state(self.bins[bin])
        if bin in self.bins_distance:
            self.distance = self.bins_distance[bin]
            
        #print("Status: " + str(self.get_status()))
    
    def check_serial(self):
        line = self.ser.readline()
        #print(line)
        try: # in case of parse error
            self.spectrum = np.array(line.split(), dtype=np.float32)
        except:
            print("Barryvox:parse error")
        if np.max(self.spectrum) > 0.05:
            self.process_signal(np.argmax(self.spectrum),np.max(self.spectrum))
            self.timer = 0; # Reset timer for no signal
            #print (str(np.argmax(nums)) + "\t" +  str(np.max(nums)))
        elif self.timer > 2.0 / 0.020: # Timeout 2 seconds, go to nosignal
            self.set_state("nosignal")
        else:
            self.timer += 1
    def spin(self):
        while(1):
            self.check_serial()
    def get_status(self):
        # returns (bool signal, string state, int distance)
        if self.state in ("normal", "close", "ahead", "turn"):
            signal = True
            distance = self.distance
        else:
            signal = False
            distance = 9
        return (signal, self.state, distance)

class BarryvoxThread(Thread):
    def run(self):
        self.barryvox = Barryvox(self.tty,self.baud)
        last_status = None
        while(1):
            #print("BarryvoxThread:spun")
            self.barryvox.check_serial()
            #print(self.barryvox.spectrum)
            status = self.barryvox.get_status()
            if status != last_status:
                #print("STATE CHANGE:",last_status,status)
                self.queue.put(status)
            last_status = status

    def __init__(self, queue, tty="COM5", baud=115200):
        super(BarryvoxThread, self).__init__()
        
        self.tty = tty
        self.baud = baud
        self.queue = queue
        #self.thread = Thread(target=self._spin)
        #self.thread.start()

if __name__ == "__main__":
    #barryvox = Barryvox("COM5",115200)
    queue = Queue()
    barryvoxThread = BarryvoxThread(queue,"COM5",115200)
    barryvoxThread.daemon = True
    barryvoxThread.start()

    print("main:BarryvoxThread started")
    
    #ointsY0 = [];
    #pwnd = pg.plot();
    #curveY0 = pwnd.plot(pen="y", antialias=True);
    
    while(1):
        #QtGui.QApplication.processEvents();
        #curveY0.setData(barryvox.spectrum);
        print(queue.get())

# snu 6bin
# vanlig 9bin (0.1amp siden, 0.3amp vanlig)
# nær 9-17bin
# rett frem 20bin 
# error 12bin 0.52amp