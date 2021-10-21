# Data-mining-CGM-data-monitoring
Mined CGM data of a patient to analyze blood sugar levels to automate insulin injection

## Tools Used:
1. Python 
  1. Numpy
  2. Pandas
  3. Sklearn


● Engineered features of the time-series data and used Principal Component Analysis to build Logistic Regression model to classify data into ‘meal’ and ‘not meal’ data by achieving an accuracy rate of 83%

● Enhanced the performance of the model by using CNN (with pooling, conv2D and fully-connected layers) on time-series data to achieve an accuracy score of 92%

● Employed DBSCAN algorithm to cluster the CGM data to learn as to which bin (CGM range) a data point belonged to

● Extracted anomalous data points using associative rule mining to reduce diagnosis time for the doctors by 10 minutes
