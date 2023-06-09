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
class dataLoader():
  def __init__(self, src_path, tar_path):
    self.src_path = src_path
    self.tar_path = tar_path
  def loadData(self):
    i = 0
    for filename in os.listdir(self.src_path):
      df = pd.read_csv(self.src_path+filename)
      df = df.dropna()
      ff = filename.split(".")
      df["Domain"] = ff[0]
      if i==0:
        self.src_data = df
      else:
        self.src_data = pd.concat([self.src_data, df], axis=0)
      i = i+1
    self.src_data.reset_index(drop=True, inplace=True)
    j = 0
    for filename in os.listdir(self.tar_path):
      df = pd.read_csv(self.tar_path+filename)
      df = df.dropna()
      ff = filename.split(".")
      df["Domain"] = ff[0]
      #print(df)
      if j==0:
        self.tar_data = df
      else:
        self.tar_data = pd.concat([self.tar_data, df], axis=0) 
      j = j + 1
    self.tar_data.reset_index(drop=True, inplace=True)
  def getData(self):
    return self.src_data, self.tar_data

  def getXY(self, colName, rowName, targetColumn, specialColumns):
    #if datasetName == "perfvar":
    #  application = rowName
    #  self.src_data = self.src_data.loc[self.src_data['application']!= application]
    #  self.tar_data = self.tar_data.loc[self.tar_data['application']== application]
    s_arr = self.src_data["Domain"].unique()
    t_arr = self.tar_data["Domain"].unique()
    for name in t_arr:
      dat = []
      for i in range(len(self.src_data.columns)):
        dat.append(0)
      dat[-1]=name
      self.src_data.loc[len(self.src_data.index)] = dat
    for name in s_arr:
      dat = []
      for i in range(len(self.tar_data.columns)):
        dat.append(0)
      dat[-1]=name
      self.tar_data.loc[len(self.tar_data.index)] = dat

    ##one hot encoding
    self.src_data = pd.get_dummies(self.src_data, columns=["Domain"], drop_first=False)
    self.tar_data = pd.get_dummies(self.tar_data, columns=["Domain"], drop_first=False)
    ##remove extra inserted rows
    for name in t_arr:
        self.src_data = self.src_data.drop([len(self.src_data.index)-1])
    for name in s_arr:
        self.tar_data = self.tar_data.drop([len(self.tar_data.index)-1])
    ##listing rest string valued columns in source
    strColumnsValues = {}
    srcStringColumns = []
    for i in range(len(self.src_data.columns)):
      if self.src_data.columns[i] not in specialColumns:
        if self.src_data[self.src_data.columns[i]].dtypes == "object":
          srcStringColumns.append(self.src_data.columns[i])
          strColumnsValues[self.src_data.columns[i]] = []
          for value in self.src_data[self.src_data.columns[i]].unique():
            strColumnsValues[self.src_data.columns[i]].append(value)
    
    ##listing similar or unique string valued columns in target
    tarStringColumns = []
    for i in range(len(self.tar_data.columns)):
      if self.tar_data.columns[i] not in specialColumns:
        if self.tar_data[self.tar_data.columns[i]].dtypes == "object":
          tarStringColumns.append(self.tar_data.columns[i])
          if self.tar_data.columns[i] not in strColumnsValues:
            strColumnsValues[self.tar_data.columns[i]] = []
          for value in self.tar_data[self.tar_data.columns[i]].unique():
            if value not in strColumnsValues[self.tar_data.columns[i]]:
              strColumnsValues[self.src_data.columns[i]].append(value)
   
    for columnName in list(strColumnsValues.keys()):
      new_src_d = pd.DataFrame()
      new_tar_d = pd.DataFrame()
      for pos in range(len(self.src_data)):
        src_row = self.src_data[pos:pos+1]
        for columnValue in strColumnsValues[columnName]:
          if str(src_row[columnName]) == str(columnValue):
            new_src_d.at[pos,columnValue] = 1
          else:
            new_src_d.at[pos,columnValue] = 0
      for pos in range(len(self.tar_data)):
        tar_row = self.tar_data[pos:pos+1]
        for columnValue in strColumnsValues[columnName]:
          if str(tar_row[columnName]) == str(columnValue):
            new_tar_d.at[pos,columnValue] = 1
          else:
            new_tar_d.at[pos,columnValue] = 0
      self.src_data = self.src_data.drop([columnName], axis=1)
      self.tar_data = self.tar_data.drop([columnName], axis=1)
      self.src_data = pd.concat([self.src_data, new_src_d], axis=1)
      self.tar_data = pd.concat([self.tar_data, new_tar_d], axis=1)


    ##apply one hot encoding to other string columns on source
    """
    print(f"src string columns {stringColumns}")
    print(self.src_data)
    self.src_data = pd.get_dummies(self.src_data, columns = stringColumns, drop_first=False)
    """
    #Columns to be omitted
    omitColumns = []
    omitColumns.append(targetColumn)
    self.src_y = self.src_data.loc[:, targetColumn].values
    #inds = [i for i,f in enumerate(self.src_data.columns) if f not in omitColumns]
    #print(inds)
    self.src_data = self.src_data.drop([targetColumn], axis=1)
    self.src_x = self.src_data.values

    ##listing other string valued columns in target
    """
    stringColumns = []
    for i in range(len(self.tar_data.columns)):
      if self.tar_data.columns[i] not in specialColumns:
        if self.tar_data[self.tar_data.columns[i]].dtypes == "object":
          stringColumns.append(self.tar_data.columns[i])
    """
    ##apply one hot encoding to other string columns on source
    #self.tar_data = pd.get_dummies(self.tar_data, columns = stringColumns, drop_first=False)
    #Columns to be omitted
    omitColumns = []
    omitColumns.append(targetColumn)
    self.tar_y = self.tar_data.loc[:, targetColumn].values
    #inds = [i for i,f in enumerate(self.tar_data.columns) if f not in omitColumns]
    #print(inds)
    self.tar_data = self.tar_data.drop([targetColumn], axis =1)
    self.tar_x = self.tar_data.values

    #print(omitColumns)
    print(self.src_data.columns)
    print(self.tar_data.columns)
    #print("src_x shape {self.src_x.shape
    print(self.src_x.shape)
    print(self.tar_x.shape)
    return self.src_x, self.src_y, self.tar_x, self.tar_y
    
 
