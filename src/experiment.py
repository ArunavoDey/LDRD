# -*- coding: utf-8 -*-
"""analysis_w_paper_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EZTRUg9Hg-sofoig8vkJjhp_09YQnn_G
"""
#!pip install optuna
import optuna
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
import random
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation, Dropout, Flatten, Input, Dense, concatenate 
from sklearn.metrics import accuracy_score, precision_score, recall_score, r2_score, mean_squared_error
from tensorflow.keras.models import Model, Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import preprocessing
import dataloader
from preprocessing import preprocessor
from dataloader import dataLoader
import sys
import os
import csv
import ensemRegressor
#np.random.seed(1)  
#tf.random.set_seed(2)

def compute_rse(y,yhat):
  #y = y.ravel()
  yhat = yhat.ravel()
  yhat = tf.cast(yhat, dtype=tf.float64)
  mu = np.mean(y)
  return np.sqrt(np.sum((y-yhat)**2))/np.sqrt(np.sum((y-mu)**2))
def compute_smape(y,yhat):
  #y = y.ravel()
  #yhat = yhat.ravel()
  n = len(y)
  nr = np.abs(y - yhat)
  dr = 0.5*(np.abs(y) + np.abs(yhat))
  return (100./n)*np.sum(nr/dr)
def plot_graphs(history, string, filename):
  matplotlib.rcParams['mathtext.fontset'] = 'stix'
  matplotlib.rcParams['font.family'] = 'STIXGeneral'
  plt.plot(history.history[string])
  plt.plot(history.history['val_'+string])
  plt.xticks(fontsize=32)
  plt.yticks(fontsize=32)
  plt.xlabel("Epochs")
  plt.ylabel(string)
  plt.savefig(filename)

"""
def create_model3(
                 neurons_input = 1, num_of_layers_1=1,
                  lr=0.01, moment = 0.5, actF="relu", lossF="mean_squared_error"):

  model = Sequential()
  for i in range(num_of_layers_1):
    layer = Dense(units=neurons_input, activation=actF)
    layer2 = BatchNormalization(momentum=moment)
    if i >= 3:
      #(num_of_layers_1-1):
      layer.trainable=False
      layer2.trainable=False
   
    model.add(layer)
    model.add(layer2)
    #model.add(Dropout(0.4))
  finalLayer = Dense(units=1)
  #finalLayer.trainable=False
  model.add(finalLayer)
  #, kernel_regularizer=tf.keras.regularizers.l1(0.01),
  #                            activity_regularizer=tf.keras.regularizers.l2(0.01)))
  opt1 = tf.keras.optimizers.Nadam(learning_rate=lr)
  model.compile(loss=lossF, optimizer=opt1, metrics=['mse','mae','mape'])
  return model
"""

def create_model4(
                 neurons_input = 1, num_of_layers_1=1, neurons_output = 1,
                  lr=0.01, moment = 0.5, actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers = 0):

  model = Sequential()
  for i in range(num_of_layers_1):
    layer = Dense(units=neurons_input, activation=actF)
    layer2 = BatchNormalization(momentum=moment)
    if transfer == True and i< frozen_layers:
      #(num_of_layers_1-1):
      layer.trainable=False
      layer2.trainable=False
    model.add(layer)
    model.add(layer2)
    #model.add(Dropout(0.4))
  finalLayer = Dense(units=neurons_output)
  #finalLayer.trainable=False
  model.add(finalLayer)
  #, kernel_regularizer=tf.keras.regularizers.l1(0.01),
  #                            activity_regularizer=tf.keras.regularizers.l2(0.01)))
  opt1 = tf.keras.optimizers.Nadam(learning_rate=lr)
  model.compile(loss=lossF, optimizer=opt1, metrics=['mse','mae','mape'])
  return model





def scheduler(epoch, lr):
  if epoch < 20:
    return lr
  else:
    return lr * tf.math.exp(-0.1)
import optunannPOD
if __name__ == "__main__":
  #path_to_module = '/content/drive/MyDrive/'
  #np.random.seed(1)  
  #tf.random.set_seed(2)
  os.chdir("../../../")
  ep1 = int(sys.argv[1])
  trials = int(sys.argv[2])
  #shot = sys.argv[5]
  #fold = int(sys.argv[6])
  stdy = sys.argv[3]
  storageN = sys.argv[4]
  n = float(sys.argv[5])
  path = sys.argv[6]
  target_app = sys.argv[7]
  use_case = sys.argv[8]
  src_path = os.getcwd()+sys.argv[9]
  tar_path = os.getcwd()+sys.argv[10]
  result_path = os.getcwd()+sys.argv[11]
  model_path = os.getcwd()+sys.argv[12]
  chck_path = os.getcwd()+sys.argv[13]
  target_label = sys.argv[14]
  test_split = float(sys.argv[15])
  val_split = float(sys.argv[16])
  rand_state = int(sys.argv[17])
  rand_state2 = int(sys.argv[18])
  num_of_frozen_layers = int(sys.argv[19])
  idx = int(n*100)
  #fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-results.csv", "w")
  #writer = csv.writer(fileI)
  #workbook = xlsxwriter.Workbook(f"pervar-finetuning-results-{n}.xlsx")
  #worksheet = workbook.add_worksheet()
  loader = dataLoader(src_path, tar_path)
  loader.loadData()
  #src_x, src_y, tar_x, tar_y = loader.getXY("ccgrid", None, "","teps",['graph_name','kernel_time','d2h_time','h2d_time','device','teps'])
  src_x, src_y, tar_x, tar_y = loader.getXY("", "",target_label)
  print("Src x shape before preprocessing")
  print(src_x.shape)
  print("Tar_x shape before preprocessing")
  print(tar_x.shape)
  #print(f"{tar_x.shape}, {tar_y.shape}")
  p = preprocessor(src_x, src_y, tar_x, tar_y, 0)
  p.preprocess()
  tar_x_scaled, tar_y_scaled = p.getTargetScaled()
  """# **Train Test validation**"""
  X_train, y_train, src_train, src_y_train, src_val, src_y_val, X_test, y_test = p.train_test_val( test_split, val_split, rand_state, rand_state2)
  try:
    with tf.device('/gpu:0'):
      n = len(tar_x_scaled)/10
      """
      """
      #tar_x_scaled = tf.convert_to_tensor(tar_x_scaled, dtype = tf.float64)
      #tar_y_scaled = tf.convert_to_tensor(tar_y_scaled, dtype = tf.float64)
      if use_case == "train":
        nnparameters = optunannPOD.finder(X_train, y_train, epochs= ep1, checkpoint_path=f"{chck_path}{target_app}/", num_of_trials=trials, fold=10, stname=stdy, storageName =storageN )  #/content/MyDrive/SimpleNN/
        #predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), moment = float(nnparameters.params['Momentum']), actF="relu", lossF="mean_squared_error")
        f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "w")
        print("Neurons ")
        print(nnparameters.params['neuron'])
        f.write(f"{nnparameters.params['neuron']}")
        f.write(" ")
        print("Number of layers")
        print(nnparameters.params['num_layers'])
        f.write(f"{nnparameters.params['num_layers']}")
        f.write(" ")
        print("Learning rate")
        print(nnparameters.params['lr2'])
        f.write(f"{nnparameters.params['lr2']}")
        f.write(" ")
        print("Best Trial Number")
        print(nnparameters.number)
        print("batch_size")
        print(nnparameters.params['batch_size'])
        f.write(f"{nnparameters.params['batch_size']}")
        f.write(" ")
        print("Momentum")
        print(nnparameters.params['Momentum'])
        f.write(f"{nnparameters.params['Momentum']}")
        f.write(" ")
        f.close()
        #for i in range(5):
        #X_train, y_train, src_train, src_y_train, src_val, src_y_val, X_test, y_test = p.train_test_val( 0.20, 0.25, (i*35), (i*71))
        #model = create_model3(neurons_input= 600, num_of_layers_1= 9, lr=0.06, moment = 0.5000000000000001, actF="relu", lossF="mean_squared_error")
        model = create_model4(neurons_input = nnparameters.params['neuron'] , num_of_layers_1= nnparameters.params['num_layers'] , lr= nnparameters.params['lr2'] , moment = nnparameters.params['Momentum'] , actF="relu", lossF="mean_squared_error")
        #model = create_model3(neurons_input = 740, num_of_layers_1= 1 , lr=0.0013461782513436136 , moment = 0.076 , actF="relu", lossF="mean_squared_error")
        callback = tf.keras.callbacks.LearningRateScheduler(scheduler)
        callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=20)
    
        """# **Num of samples splitting and model fitting**"""
        history = model.fit(X_train, y_train, batch_size = nnparameters.params['batch_size'] , epochs=1000, callbacks=[ callback2])
        """# **Model Performance on Source**""" 
        predictions = model.predict(X_test)
        matplotlib.rcParams['mathtext.fontset'] = 'stix'
        matplotlib.rcParams['font.family'] = 'STIXGeneral'
        plt.figure(figsize=(10,10))
        plt.scatter(y_test, predictions.ravel())
        mse,r2 = mean_squared_error(y_test#.reshape(-1,1)
		, predictions), r2_score(y_test#.reshape(-1,1)
				, predictions)
        plt.xlabel('Actual Labels', fontsize=32)
        plt.ylabel('Predicted Labels', fontsize=32)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        #plt.title(f'MSE: {mse}, R2: {r2}-Source for x-{target_app}')
        plt.savefig(f"{result_path}figs/Source-model-on-x-{target_app}.pdf")
        """# **Model Saving and Loading**"""
        model.save_weights(f"{model_path}x-{target_app}-SourceModel")
      elif use_case == "train-test":
        nnparameters = optunannPOD.finder(X_train, y_train, epochs= ep1, checkpoint_path=f"chck_path{target_app}/", num_of_trials=trials, fold=10, stname=stdy, storageName =storageN )  #/content/MyDrive/SimpleNN/
        #predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), moment = float(nnparameters.params['Momentum']), actF="relu", lossF="mean_squared_error")

        f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "w")
        print("Neurons ")
        print(nnparameters.params['neuron'])
        f.write(f"{nnparameters.params['neuron']}")
        f.write(" ")
        print("Number of layers")
        print(nnparameters.params['num_layers'])
        f.write(f"{nnparameters.params['num_layers']}")
        f.write(" ")
        print("Learning rate")
        print(nnparameters.params['lr2'])
        f.write(f"{nnparameters.params['lr2']}")
        f.write(" ")
        print("Best Trial Number")
        print(nnparameters.number)
        print("batch_size")
        print(nnparameters.params['batch_size'])
        f.write(f"{nnparameters.params['batch_size']}")
        f.write(" ")
        print("Momentum")
        print(nnparameters.params['Momentum'])
        f.write(f"{nnparameters.params['Momentum']}")
        f.write(" ")
        f.close()

        #for i in range(5):
        #X_train, y_train, src_train, src_y_train, src_val, src_y_val, X_test, y_test = p.train_test_val( 0.20, 0.25, (i*35), (i*71))
        #model = create_model3(neurons_input= 600, num_of_layers_1= 9, lr=0.06, moment = 0.5000000000000001, actF="relu", lossF="mean_squared_error")
        model = create_model4(neurons_input = nnparameters.params['neuron'] , num_of_layers_1= nnparameters.params['num_layers'] , lr= nnparameters.params['lr2'] , moment = nnparameters.params['Momentum'] , actF="relu", lossF="mean_squared_error")
        #model = create_model3(neurons_input = 740, num_of_layers_1= 1 , lr=0.0013461782513436136 , moment = 0.076 , actF="relu", lossF="mean_squared_error")
        callback = tf.keras.callbacks.LearningRateScheduler(scheduler)
        callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=20)
    
        """# **Num of samples splitting and model fitting**"""
        #model.load_weights("/home1/08389/hcs77/NewModels/PerfvarSourceModel") 
        history = model.fit(X_train, y_train, batch_size = nnparameters.params['batch_size'] , epochs=1000, callbacks=[ callback2],validation_split=0.2, shuffle= True)
        #model.save_weights(f"{model_path}x-{target_app}-SourceModel")
        #model.summary()
        #model.fit(tar_x_scaled[0:int((n*6))], tar_y_scaled[0:int((n*6))], batch_size = 100 , epochs=1000, callbacks=[ callback2])
        matplotlib.rcParams['mathtext.fontset'] = 'stix'
        matplotlib.rcParams['font.family'] = 'STIXGeneral'
        """# **Model Performance on Source**"""
        predictions = model.predict(X_test)
        plt.figure(figsize=(10,10))
        plt.scatter(y_test, predictions.ravel())
        mse,r2 = mean_squared_error(y_test#.reshape(-1,1)
                , predictions), r2_score(y_test#.reshape(-1,1)
                                , predictions)
        print(f"Train mse is {mse}")
        #print(f"Train rse is {rse}")
        plt.xlabel('Actual Labels', fontsize=32)
        plt.ylabel('Predicted Labels', fontsize=32)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        #plt.title(f'MSE: {mse}, R2: {r2}-Source on source')
        plt.savefig(f"{result_path}figs/Source-model-on-source-{target_app}.pdf")
        """""" 
        tar_pred_scaled = model.predict(tar_x_scaled)
        plt.figure(figsize=(10,10))
        plt.scatter(tar_y_scaled, tar_pred_scaled.ravel())
        mse,r2 = mean_squared_error(tar_y_scaled#.reshape(-1,1)
                        , tar_pred_scaled), r2_score(tar_y_scaled#.reshape(-1,1)
                        , tar_pred_scaled)
        plt.xlabel('Actual Labels', fontsize=32)
        plt.ylabel('Predicted Labels', fontsize=32)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        plt.title(f'MSE: {mse}, R2: {r2}-sample')
        mse = mean_squared_error(tar_y_scaled, tar_pred_scaled)
        rse = compute_rse(tar_y_scaled, tar_pred_scaled)
        print(f"Test mse is {mse}")
        print(f"Test rse is {rse}")
        plt.savefig(f"{result_path}figs/source-model-on-target-{target_app}.pdf")
        plot_graphs(history, "loss", f"{result_path}figs/Source-model-on-source-{target_app}-train-val-loss.pdf")
        """# **Model Performane on Target**"""
      elif use_case == "source_only":
        f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "r")
        nums = f.readlines()
        nums = nums[0].split(" ")
        f.close()
        model = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error")
        #model = create_model3(neurons_input = 740, num_of_layers_1= 1 , lr=0.0013461782513436136 , moment = 0.076 , actF="relu", lossF="mean_squared_error")
        callback = tf.keras.callbacks.LearningRateScheduler(scheduler)
        callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=40)

        """# **Model Loading**"""
        history = model.fit(X_train, y_train, batch_size = int(nums[3]) , epochs=1000, callbacks=[ callback2], validation_split=0.2, shuffle= True)
        model.save_weights(f"{model_path}x-{target_app}-SourceModel")
        #model.load_weights(f"{model_path}x-{target_app}-SourceModel-2")
        #model.fit(X_train, y_train, batch_size = int(nums[3]) , epochs=1000, callbacks=[ callback2])
        matplotlib.rcParams['mathtext.fontset'] = 'stix'
        matplotlib.rcParams['font.family'] = 'STIXGeneral'
        """# testing model on Source data"""
        predictions = model.predict(X_test)
        plt.figure(figsize=(10,10))
        plt.scatter(y_test, predictions.ravel())
        mse,r2 = mean_squared_error(y_test#.reshape(-1,1)
                , predictions), r2_score(y_test#.reshape(-1,1)
                                , predictions)
        print(f"source mse is {mse}")
        plt.xlabel('Actual Labels', fontsize=32)
        plt.ylabel('Predicted Labels', fontsize=32)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        plt.title(f'MSE: {mse}, R2: {r2}-Source on source')
        plt.savefig(f"{result_path}figs/Testing-Source-model-on-source-{target_app}.pdf")
 
        """#testing model on target data"""
        tar_pred_scaled = model.predict(tar_x_scaled)
        plt.figure(figsize=(10,10))
        plt.scatter(tar_y_scaled, tar_pred_scaled.ravel())
        mse,r2 = mean_squared_error(tar_y_scaled#.reshape(-1,1)
			, tar_pred_scaled), r2_score(tar_y_scaled#.reshape(-1,1)
			, tar_pred_scaled)
        plt.xlabel('Actual Labels', fontsize=32)
        plt.ylabel('Predicted Labels', fontsize=32)
        plt.xticks(fontsize=32)
        plt.yticks(fontsize=32)
        plt.title(f'MSE: {mse}, R2: {r2}-sample')
        mse = mean_squared_error(tar_y_scaled, tar_pred_scaled)
        #rse = compute_rse(tar_y_scaled, tar_pred_scaled)   
        print(f"mse is {mse}")
        #print(f"rse is {rse}")
        plt.savefig(f"{result_path}figs/Testing-Source-model-on-target-{target_app}.pdf")
        plot_graphs(history, "loss", f"{result_path}figs/Source-model-on-source-{target_app}-train-val-loss.pdf")
      elif use_case == "linear_probing":
        for i in range(5):
          fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-LP{num_of_frozen_layers}-results-{i}.csv", "w")
          writer = csv.writer(fileI)
          for j in range(1,10):
            n = j/10
            tar_x_scaled, tar_y_scaled = p.getTargetScaled()
            num_of_samples = int(n*len(tar_x_scaled))
            if num_of_frozen_layers == 1:
              indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "w" )
              readModeOn = False
            elif num_of_frozen_layers >1:
              indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "r" )
              readModeOn = True
            dropIndices = []
            rowArr = []
            x2 =[]
            lb2 = []
            totallen = len(tar_x_scaled)
            if readModeOn == True:
              loaded_indices = indices.readlines()
            z = 0
            for k in range(num_of_samples):
              #print(f"len of tar_x_scaled is now {len(tar_x_scaled)}")
              if readModeOn ==True:
                index =  int(loaded_indices[z]) #
              else:
                index = random.randint(0, totallen-1 ) #int(nums[i])
                indices.write(str(index))
                indices.write(" ")
                indices.write("\n")
              #print(index)
              dropIndices.append(index)
              z = z + 1
            x2.append(tar_x_scaled[index:index+1])
            lb2.append(tar_y_scaled[index:index+1])
            tar_x_scaled = np.delete(tar_x_scaled, index, 0)
            tar_y_scaled = np.delete(tar_y_scaled, index, 0)
            totallen -= 1
            indices.close()
            
            x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
            lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
            x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
            lb2 = tf.reshape(lb2, (lb2.shape[0], lb2.shape[2]))
            
            f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "r")
            nums = f.readlines()
            nums = nums[0].split(" ")
            f.close()
            model = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=True, frozen_layers= num_of_frozen_layers )
            model1 = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers=0 )
            callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=40)
            model.fit(x2, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2])
            model1.fit(x2, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2]) 
            model1.load_weights(f"{model_path}x-{target_app}-SourceModel")
            ii = 0
            while (ii) < len(model1.layers):
              print(ii)
              model.layers[ii].set_weights(model1.layers[ii].get_weights())
              ii += 1

            predictions0 = model.predict(tar_x_scaled)
            mse0 = mean_squared_error(tar_y_scaled, predictions0)
            rowArr.append(mse0)
            model.fit(x2, lb2, batch_size = int(nums[3]), epochs=ep1, callbacks = [callback2])
            predictions2 = model.predict(tar_x_scaled)
            mse2 = mean_squared_error(tar_y_scaled, predictions2)
            rowArr.append(mse2)
            writer.writerow(rowArr)
          fileI.close()
      elif use_case == "fine_tuning":
        for i in range(5):
          fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-FT-results-{i}.csv", "w")
          writer = csv.writer(fileI)
          for j in range(1,10):
            n = j/10
            tar_x_scaled, tar_y_scaled = p.getTargetScaled()
            num_of_samples = int(n*len(tar_x_scaled))
            indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "r" )
            dropIndices = []
            rowArr = []
            x2 =[]
            lb2 = []
            totallen = len(tar_x_scaled)
            loaded_indices = indices.readlines()
            z = 0
            for k in range(num_of_samples):
              #print(f"len of tar_x_scaled is now {len(tar_x_scaled)}")
              index = int(loaded_indices[z]) #random.randint(0, totallen-1 ) #int(nums[i])
              #print(index)
              dropIndices.append(index)
              """
              indices.write(str(index))
              indices.write(" ")
              indices.write("\n")
              """
              z = z + 1
            x2.append(tar_x_scaled[index:index+1])
            lb2.append(tar_y_scaled[index:index+1])
            tar_x_scaled = np.delete(tar_x_scaled, index, 0)
            tar_y_scaled = np.delete(tar_y_scaled, index, 0)
            totallen -= 1
            indices.close()
            
            x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
            lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
            x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
            lb2 = tf.reshape(lb2, (lb2.shape[0], lb2.shape[2]))
            
            f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "r")
            nums = f.readlines()
            nums = nums[0].split(" ")
            f.close()
            model = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=40)
            model.fit(x2, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2])
            model.load_weights(f"{model_path}x-{target_app}-SourceModel")
            predictions0 = model.predict(tar_x_scaled)
            mse0 = mean_squared_error(tar_y_scaled, predictions0)
            rowArr.append(mse0)
            model.fit(x2, lb2, batch_size = int(nums[3]), epochs=ep1, callbacks = [callback2])
            predictions2 = model.predict(tar_x_scaled)
            mse2 = mean_squared_error(tar_y_scaled, predictions2)
            rowArr.append(mse2)
            writer.writerow(rowArr)
          fileI.close()
      elif use_case == "stacked_model":
        for i in range(5):
          fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-SM-results-{i}.csv", "w")
          writer = csv.writer(fileI)
          for j in range(1,10):
            n = j/10
            tar_x_scaled, tar_y_scaled = p.getTargetScaled()
            num_of_samples = int(n*len(tar_x_scaled))
            indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "r" )
            dropIndices = []
            rowArr = []
            x2 =[]
            lb2 = []
            totallen = len(tar_x_scaled)
            loaded_indices = indices.readlines()
            z = 0
            for k in range(num_of_samples):
              index = int(loaded_indices[z]) #random.randint(0, totallen-1 ) #int(nums[i])
              dropIndices.append(index)
              z = z + 1
            x2.append(tar_x_scaled[index:index+1])
            lb2.append(tar_y_scaled[index:index+1])
            tar_x_scaled = np.delete(tar_x_scaled, index, 0)
            tar_y_scaled = np.delete(tar_y_scaled, index, 0)
            totallen -= 1
            indices.close()

            x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
            lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
            x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
            lb2 = tf.reshape(lb2, (lb2.shape[0], lb2.shape[2]))

            f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "r")
            nums = f.readlines()
            nums = nums[0].split(" ")
            f.close()
            model = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=40)
            model.fit(x2, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2])
            model.load_weights(f"{model_path}x-{target_app}-SourceModel")
            predictions0 = model.predict(tar_x_scaled)
            pp0 = np.nan_to_num(predictions0)# tf.cast(predictions0, dtype = tf.float32)
            mse0 = mean_squared_error(tar_y_scaled, pp0)
            rowArr.append(mse0)
            #model.fit(x2, lb2, batch_size = int(nums[3]), epochs=ep1, callbacks = [callback2])
            combinedModel = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            predictions0S = model.predict(x2)
            t2 = tf.cast(predictions0S, dtype = tf.float64)
            t2 = tf.reshape(t2, (t2.shape[0],1))
            new_Input = tf.concat([x2, t2], 1)
            combinedModel.fit(new_Input, lb2, batch_size =int(nums[3]) , epochs=ep1, callbacks = [callback2])
            ii = 1
            while (ii) <= (int(nums[1])+1):
              combinedModel.layers[ii].set_weights(model.layers[ii].get_weights())
              ii += 1
            combinedModel.fit(new_Input, lb2, batch_size = 100, epochs=50, callbacks = [callback2])
            t2_prime = tf.cast(predictions0, dtype = tf.float64)
            t2_prime = tf.reshape(t2_prime, (t2_prime.shape[0],1))
            new_test_Input = tf.concat([tar_x_scaled, t2_prime], 1)
            predictions2 = combinedModel.predict(new_test_Input)
            pp2 = np.nan_to_num(predictions2) #pp2 = tf.cast(predictions2, dtype = tf.float32)
            mse1 = mean_squared_error(tar_y_scaled, pp2)
            rowArr.append(mse1)
            FinalModel = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            predictions2S = combinedModel.predict(new_Input)
            t3 = tf.convert_to_tensor(predictions2S, dtype = tf.float64)
            final_Input = tf.concat([x2, t2, t3], 1)
            FinalModel.fit(final_Input, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2])
            ii = 1
            while (ii) <= (int(nums[1])+1):
              FinalModel.layers[ii].set_weights(model.layers[ii].get_weights())
              ii += 1
            FinalModel.fit(final_Input, lb2, batch_size =int(nums[3]), epochs=ep1, callbacks = [callback2])
            t3_prime = tf.convert_to_tensor(predictions2, dtype = tf.float64)
            final_test_Input = tf.concat([tar_x_scaled, t2_prime, t3_prime], 1)
            predictions3 = FinalModel.predict(final_test_Input)
            pp3 = np.nan_to_num(predictions3) #tf.cast(predictions3, dtype = tf.float32)
            mse3 = mean_squared_error(tar_y_scaled, pp3)
            rowArr.append(mse3)
            writer.writerow(rowArr)
          fileI.close()
      elif use_case == "k_regressor":
        for i in range(5):
          fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-KR-results-{i}.csv", "w")
          writer = csv.writer(fileI)
          for j in range(1,10):
            n = j/10
            tar_x_scaled, tar_y_scaled = p.getTargetScaled()
            num_of_samples = int(n*len(tar_x_scaled))
            indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "r" )
            dropIndices = []
            rowArr = []
            x2 =[] 
            lb2 = []
            totallen = len(tar_x_scaled)
            loaded_indices = indices.readlines()
            z = 0 
            for k in range(num_of_samples):
              index = int(loaded_indices[z]) #random.randint(0, totallen-1 ) #int(nums[i])
              dropIndices.append(index)
              z = z + 1 
            x2.append(tar_x_scaled[index:index+1])
            lb2.append(tar_y_scaled[index:index+1])
            tar_x_scaled = np.delete(tar_x_scaled, index, 0)
            tar_y_scaled = np.delete(tar_y_scaled, index, 0)
            totallen -= 1
            indices.close()

            x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
            lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
            x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
            lb2 = tf.reshape(lb2, (lb2.shape[0], lb2.shape[2]))

            f = open(f"{result_path}txt/Source-model-on-target-{target_app}-parameters.txt", "r")
            nums = f.readlines()
            nums = nums[0].split(" ")
            f.close()
            
            n_o_samples = int(len(X_train))
            Ensemble = ensemRegressor.EnsembleOfRegressor( int(nums[0]) , int(nums[1]) , float(nums[2]), float(nums[4]), "relu", "mean_squared_error", x2.shape[1])
            Ensemble.fitData(X_train, y_train, ep1, int(nums[3]) )
            best = Ensemble.getBestRegressor(X_test, y_test)
            model = Ensemble.getModel()
            weights_list = Ensemble.regressors[best].get_weights()
            reg = Ensemble.regressors[best]          
            predictions0 = model.predict(tar_x_scaled)
            predictions0 = tf.transpose(predictions0)
            predictions0 = predictions0[best]
            mse0 = mean_squared_error(tar_y_scaled, predictions0)
            rowArr.append(mse0)

            callback2 = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=40)
            combinedModel = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            predictions0S = model.predict(x2)
            predictions0S = tf.transpose(predictions0S)
            predictions0S = predictions0S[best]
            t2 = tf.cast(predictions0S, dtype = tf.float64)
            t2 = tf.reshape(t2, (t2.shape[0],1))
            new_Input = tf.concat([x2, t2], 1)
            combinedModel.fit(new_Input, lb2, batch_size =int(nums[3]) , epochs=ep1, callbacks = [callback2])
            print("***Combined Model***")
            print(combinedModel.layers)
            print("***Reg Layers***")
            print(reg.layers)
            ii = 1 
            while (ii) <= ((int(nums[1]))-2):
              combinedModel.layers[ii].set_weights(reg.layers[ii].get_weights())
              ii += 1
            combinedModel.fit(new_Input, lb2, batch_size = 100, epochs=50, callbacks = [callback2])
            t2_prime = tf.cast(predictions0, dtype = tf.float64)
            t2_prime = tf.reshape(t2_prime, (t2_prime.shape[0],1))
            new_test_Input = tf.concat([tar_x_scaled, t2_prime], 1)
            predictions2 = combinedModel.predict(new_test_Input)
            mse1 = mean_squared_error(tar_y_scaled, predictions2)
            rowArr.append(mse1)
            FinalModel = create_model4(neurons_input = int(nums[0]) , num_of_layers_1= int(nums[1]), lr= float(nums[2]) , moment = float(nums[4]) , actF="relu", lossF="mean_squared_error", transfer=False, frozen_layers= num_of_frozen_layers)
            predictions2S = combinedModel.predict(new_Input)
            t3 = tf.convert_to_tensor(predictions2S, dtype = tf.float64)
            final_Input = tf.concat([x2, t2, t3], 1)
            FinalModel.fit(final_Input, lb2, batch_size = int(nums[3]), epochs=50, callbacks = [callback2])
            ii = 1 
            while (ii) <= (int(nums[1])-2):
              FinalModel.layers[ii].set_weights(reg.layers[ii].get_weights())
              ii += 1
            FinalModel.fit(final_Input, lb2, batch_size =int(nums[3]), epochs=ep1, callbacks = [callback2])
            t3_prime = tf.convert_to_tensor(predictions2, dtype = tf.float64)
            final_test_Input = tf.concat([tar_x_scaled, t2_prime, t3_prime], 1)
            predictions3 = FinalModel.predict(final_test_Input)
            mse3 = mean_squared_error(tar_y_scaled, predictions3)
            rowArr.append(mse3)
            writer.writerow(rowArr)
          fileI.close()
      elif use_case == "random_forrest":
        for i in range(5):
          fileI = open(f"{result_path}csv/Source-model-on-target-{target_app}-RF-results-{i}.csv", "w")
          writer = csv.writer(fileI)
          for j in range(1,10):
            n = j/10
            tar_x_scaled, tar_y_scaled = p.getTargetScaled()
            num_of_samples = int(n*len(tar_x_scaled))
            indices = open(f"{result_path}indices/Source-model-on-target-{target_app}-LP-1-indices-{i}-{j}-percent.csv", "r" )
            dropIndices = []
            rowArr = []
            x2 =[]
            lb2 = []
            totallen = len(tar_x_scaled)
            loaded_indices = indices.readlines()
            z = 0
            for k in range(num_of_samples):
              index = int(loaded_indices[z]) #random.randint(0, totallen-1 ) #int(nums[i])
              dropIndices.append(index)
              z = z + 1
            x2.append(tar_x_scaled[index:index+1])
            lb2.append(tar_y_scaled[index:index+1])
            tar_x_scaled = np.delete(tar_x_scaled, index, 0)
            tar_y_scaled = np.delete(tar_y_scaled, index, 0)
            totallen -= 1
            indices.close()

            x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
            lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
            x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
            lb2 = tf.reshape(lb2, (lb2.shape[0], lb2.shape[2]))

            clf1 = RandomForestRegressor(n_estimators=100)
            clf1.fit(X_train, y_train.ravel())
            """
            train_pred = clf1.predict(X_train)
            clf2 = RandomForestRegressor(n_estimators=100)
            t2_prime = tf.cast(train_pred , dtype = tf.float64)
            t2_prime = tf.reshape(t2_prime, (t2_prime.shape[0],1))
            new_test_Input = tf.concat([X_train, t2_prime], 1)
            clf2.fit(new_test_Input, y_train.ravel())
            """
            clf1.fit(x2,lb2)
            predictions0 = clf1.predict(tar_x_scaled)
            mse0 = mean_squared_error(tar_y_scaled, predictions0)
            rowArr.append(mse0)
            writer.writerow(rowArr)
          fileI.close()                
      else:
        print("sorry no match")
  except RuntimeError as e:
    print(e)
