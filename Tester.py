
# coding: utf-8

# In[53]:


import pickle
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))


# In[54]:

import sklearn
import pandas as pd
import numpy as np


# In[55]:


dft = pd.read_csv('testa4.csv', header = None)


# # Feature extraction

# In[56]:


cgm_velocity_test = np.diff(dft)


# # max CGM velocity with tm

# In[57]:


max_cgm_velocity_test = []
for i in range(len(cgm_velocity_test)):
    max_cgm_velocity_test.append([max(cgm_velocity_test[i]), np.argmax(cgm_velocity_test[i])*5])


# # CGMmax-CGMmin

# In[58]:


cgm_range_test = dft.max(axis = 1) - dft.min(axis = 1)


# # Important duration

# In[59]:


imp_duration_test = (dft.idxmax(axis = 1))*5


# # FFT

# In[60]:


fft_test = []
temp1 = []
temp1 = abs(np.fft.fft(dft))
for i in range(len(temp1)):
    temp1[i].sort()
    fft_test.append([temp1[i][-2], temp1[i][-4]])


# # Windowed mean

# In[61]:


win_mean_test = []
win_mean_test.append([dft.rolling(3, win_type='triang', axis = 1).mean()[8], dft.rolling(3, win_type='triang', axis = 1).mean()[11], dft.rolling(3, win_type='triang', axis = 1).mean()[14], dft.rolling(3, win_type='triang', axis = 1).mean()[17], dft.rolling(3, win_type='triang', axis = 1).mean()[20]])


# In[62]:


feat_win_test = []
for j in range(5):
    temp = []
    for i in range(len(win_mean_test[0][j])):
        temp.append(win_mean_test[0][j][i])
    feat_win_test.append(temp)
feat_win_test = np.array(feat_win_test).T


# # Build feature matrix

# In[63]:


new_test_feature_matrix = []
new_test_matrix = []
new_test_matrix.append(max_cgm_velocity_test)
new_test_feature_matrix.append(new_test_matrix[0])
new_test_feature_matrix = new_test_feature_matrix[0]


# In[64]:


for i in range(len(new_test_feature_matrix)):
    new_test_feature_matrix[i].append(cgm_range_test[i])


# In[65]:


for i in range(len(new_test_feature_matrix)):
    new_test_feature_matrix[i].append(imp_duration_test[i])


# In[66]:


for i in range(len(new_test_feature_matrix)):
    new_test_feature_matrix[i].append(fft_test[i][0])
    new_test_feature_matrix[i].append(fft_test[i][1])


# In[67]:


for i in range(len(new_test_feature_matrix)):
    for j in range(5):
        new_test_feature_matrix[i].append(feat_win_test[i][j])


# In[68]:


new_test_feature_matrix = (np.array(new_test_feature_matrix).T).T


# In[69]:


test_feature_df = pd.DataFrame(new_test_feature_matrix, columns=['Max CGM velocity', 'time at max vel', 'CGM max-min', 'Important duration', 'FFT1', 'FFT2', 'Win_mean1', 'Win_mean2', 'Win_mean3', 'Win_mean4', 'Win_mean5'])


# In[70]:


y_pred = loaded_model.predict(test_feature_df)


# In[ ]:


y_pred = pd.DataFrame(y_pred)


# In[ ]:


y_pred.to_csv('results.csv', index=False, header = False)

