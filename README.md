# Data-mining-CGM-data-monitoring
Mined CGM data of a patient to analyze blood sugar levels to automate insulin injection

## Tools Used:
1. Python 
2. Numpy
3. Keras
4. TensorFlow (backend)
5. Pandas
6. Sklearn
7. Timedelta

# Quick Summary:

● Engineered features of the time-series data and used Principal Component Analysis to build Logistic Regression model to classify data into ‘meal’ and ‘not meal’ data by achieving an accuracy rate of 83%

● Enhanced the performance of the model by using CNN (with pooling, conv2D and fully-connected layers) on time-series data to achieve an accuracy score of 92%

● Employed DBSCAN algorithm to cluster the CGM data to learn as to which bin (CGM range) a data point belonged to

● Extracted anomalous data points using associative rule mining to reduce diagnosis time for the doctors by 10 minutes

# Detailed explanation

## STEP 1: Data Cleaning

1. As there were two datasets involved in the project, I used 5-minute time proximity rule to sync the two time-series datasets to do further analysis.

2. Used the synced dataset for all later analyses and model building

2. Used 'fillna' and 'interpolate' functions to impute the missing values.
 
## STEP 2: Exploratory data Analysis

1. Used percentage values of the amount of time a patient's glucose levels lied in a particular range (such as 70-100 mg/L,...) to analyze overall health condition of the patient.

2. Plotted the graph to show these percentage values using matplotlib

![image](https://user-images.githubusercontent.com/64389100/138208737-2e33ca1b-775e-4749-a949-73b146e51c51.png)


2. Stored the results in the 'Results_EDA.csv' file for two different reading modes - Automatic and Manual

## STEP 3: Logistic Regression to build a baseline classification model

1. Engineered the time-series data by using tools like FFT and moving average, in order to make it time-independent before using Logistic Regression

2. Used Logisitic regression to classify the data points into 'meal' and 'non-meal' data, to check if the patient had consumed a meal or not in the past 30 minutes, in order to detect mismatch between patient-provided information and the model-extracted results.

3. Used K-fold (10-fold) cross validation technique to get the accuracy score and also generated the confusion matrix and the precion score.

![image](https://user-images.githubusercontent.com/64389100/138205419-a7d5f764-44dc-48f9-9a09-2323bcd4f3ac.png)

## STEP 4: Convolutional Neural Network (CNN) to build better model on top of the baseline model.

Used CNN as the dataset was structured and also in time-series format 

1. Used Padding, Pooling, Conv2D, ReLU, Fully Connected and Softmax layers to predict the claas-affinity of each observation

2. Achieved accuracy score of 93% for the dataset

## STEP 5: Clustering using K-Means and DBSCAN

1. Used Clustering techniques like K-Means and DBSCAN to segregate data points into 3 patient-health categories: Normal, deteriorating, severely deteriorating  

2. Obtained purity scores of 0.52 for K-Means and 0.64 for DBSCAN algorithm.

3. Finalized the DBSCAN model as the purity score was comparitively higher as it dealt better with outliers

## STEP 6: Anomalous data-point detection using Associative Rule Mining (ARM)

Used ARM to obtain the confidence values of seeing an unseen observation in the trained dataset and used a threshold value of 0.15 to identify anomalous data points in order to raise an alarm, to request doctor's attention.


The overall model can be used as an anomaly-detection system to montor patient health, so that the doctors do not waste time by checking the data manually or missing important information regarding the patient's health.
