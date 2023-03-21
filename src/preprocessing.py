import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import random
import os
import sys
import time
#import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from numpy import random
from scipy.fft import fft, ifft, fftfreq
import copy
import scipy
from sklearn.model_selection import train_test_split
class preprocessor():
  def __init__(self, src_X, src_Y, tar_x, tar_y, scalerChoice, File=None):
    self.src_X = src_X
    self.src_Y = src_Y
    self.tar_x = tar_x
    self.tar_y = tar_y
    self.scalerChoice = scalerChoice
  def preprocess(self):
    print(f"src_x shape {self.src_X.shape}")
    print(f"tar_x shape {self.tar_x.shape}")
    if self.scalerChoice == 0:
      self.X_scaler = MinMaxScaler()
      self.Y_scaler = MinMaxScaler()
    if self.scalerChoice == 1:
      self.X_scaler = StandardScaler()
      self.Y_scaler = StandardScaler()
    self.Y_scaler.fit(self.src_Y.reshape(-1,1))
    self.X_scaler.fit(self.src_X)
    self.src_Y_scaled = self.Y_scaler.transform(self.src_Y.reshape(-1,1))
    self.tar_y_scaled = self.Y_scaler.transform(self.tar_y.reshape(-1,1))
    #print(f"{src_y_scaled.shape}, {tar_y_scaled.shape}")
    #print(f" source columns {self.src_X.columns}")
    #print(f"target columns {self.tar_x.columns}")
    self.src_X_scaled = self.X_scaler.transform(self.src_X)
    self.tar_x_scaled = self.X_scaler.transform(self.tar_x)
    """# **Train Test validation**"""
  def train_test_val(self, test_size_, val_size, rand_state, rand_state2=0):
    X_train, X_test, y_train, y_test = train_test_split( self.src_X_scaled, self.src_Y_scaled, test_size=test_size_, random_state=rand_state, shuffle = False, stratify = None)
    src_train, src_val, src_y_train, src_y_val = train_test_split( X_train, y_train, test_size=val_size, random_state= rand_state2, shuffle = False, stratify = None)
    return X_train, y_train, src_train, src_y_train, src_val, src_y_val, X_test, y_test
  def getTargetScaled(self):
    return self.tar_x_scaled, self.tar_y_scaled
 
