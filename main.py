
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
import numpy as np

import pickle
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler


# In[2]:


insulin_data = pd.DataFrame(pd.read_csv('insulinData.csv'))


# In[3]:


cgm_data = pd.DataFrame(pd.read_csv('CGMData.csv'))


# In[4]:


match_time = []
match_date = []
intake = []
for i in range(len(insulin_data)):
    if((not(math.isnan(insulin_data.loc[i, 'BWZ Carb Input (grams)']))) and (insulin_data.loc[i, 'BWZ Carb Input (grams)'] != 0)):
        match_date.append(insulin_data.loc[i, 'Date'])
        match_time.append(insulin_data.loc[i, 'Time'])
        intake.append(insulin_data.loc[i, 'BWZ Carb Input (grams)'])


# In[5]:


dtl = []
for i in range(len(match_date)):
    dtl.append(str(match_date[i]) + ' ' + str(match_time[i]))


# In[6]:


dtl_in = []
for i in range(len(intake)):
    dtl_in.append(intake[i])


# In[7]:


insulin_data = insulin_data.iloc[::-1]


# In[8]:


cgm_data = cgm_data[::-1]


# In[9]:


for i in range(len(dtl)):
    dtl[i] = datetime.strptime(str(match_date[i]) + ' ' + str(match_time[i]), '%m/%d/%Y %H:%M:%S')


# In[10]:


dtl = dtl[::-1]


# In[11]:


dtl_in = dtl_in[::-1]


# In[12]:


meal_data_dt = []
meal_data_dt_in = []
for i in range(len(dtl)-1):
    if((dtl[i] + timedelta(hours = 2)) < dtl[i+1]):
        meal_data_dt.append(dtl[i])
        meal_data_dt_in.append(dtl_in[i])
    if((dtl[i] + timedelta(hours = 2)) == dtl[i+1]):
        meal_data_dt.append(dtl[i+1] + timedelta(hours = -0.5))
        meal_data_dt_in.append(dtl_in[i+1])
    


# In[13]:


cgm_data_dt = []
for i in range(len(cgm_data)):
    cgm_data_dt.append(datetime.strptime(str(cgm_data.loc[i, 'Date']) + ' ' + str(cgm_data.loc[i, 'Time']), '%m/%d/%Y %H:%M:%S'))


# # meal data datetime of cgm
# 

# In[14]:


cgm_tm_match_meal = []
cgm_tm_match_meal_in = []
for i in range(len(meal_data_dt)):
    for j in range(len(cgm_data_dt)):
        if(cgm_data_dt[j] < meal_data_dt[i] + timedelta(minutes = 5)):
            cgm_tm_match_meal.append((cgm_data_dt[j]))
            cgm_tm_match_meal_in.append(meal_data_dt_in[i])
            break


# In[15]:


cgm_data['timestamp'] = cgm_data_dt[::-1]


# # Meal data cgm values

# In[16]:


temp_index_list = []
temp_index_list_in = []
for i in range(len(cgm_tm_match_meal)):
    temp_index_list.append(cgm_data[cgm_data['timestamp'] == cgm_tm_match_meal[i]].index[0])
    temp_index_list_in.append(cgm_tm_match_meal_in[i])


# In[17]:


cgm_value_stretch_meal = []
cgm_value_stretch_meal_in = []
for i in range(1,len(temp_index_list)):
    cgm_value_one_stretch_meal = []
    for j in range(30):
        cgm_value_one_stretch_meal.append(cgm_data.loc[(temp_index_list[i] + 6 - j),'Sensor Glucose (mg/dL)'])
    if(not(np.isnan(cgm_value_one_stretch_meal).all())):
        cgm_value_stretch_meal.append(cgm_value_one_stretch_meal)
        cgm_value_stretch_meal_in.append(temp_index_list_in[i])


# In[18]:


for i in range(len(cgm_value_stretch_meal)):
    for j in range(len(cgm_value_stretch_meal[i])):
        if(np.isnan(cgm_value_stretch_meal[i][j])):
            cgm_value_stretch_meal[i][j] = int(np.nanmean(cgm_value_stretch_meal[i]))


# In[19]:


cgm_value_stretch_meal_df = pd.DataFrame(cgm_value_stretch_meal)


# # Feature Engineering

# # CGM Velocity, tmax

# In[20]:


cgm_velocity_meal_p1 = np.diff(cgm_value_stretch_meal_df)


# In[21]:


max_cgm_velocity_meal_p1 = []
for i in range(len(cgm_velocity_meal_p1)):
    max_cgm_velocity_meal_p1.append([max(cgm_velocity_meal_p1[i]), np.argmax(cgm_velocity_meal_p1[i])*5])


# # CGMmax - CGMmin

# In[22]:


cgm_range_meal_p1 = cgm_value_stretch_meal_df.max(axis = 1) - cgm_value_stretch_meal_df.min(axis = 1)


# # Important duration

# In[23]:


imp_duration_meal_p1 = (cgm_value_stretch_meal_df.idxmax(axis = 1))*5


# # FFT

# In[24]:


fft_meal_p1 = []
temp1 = []
#for i in range(len(cgm_value_stretch_meal_df)):
temp1 = abs(np.fft.fft(cgm_value_stretch_meal_df)) #[i:i+1])).flatten()
for i in range(len(temp1)):
    temp1[i].sort()
    fft_meal_p1.append([temp1[i][-2], temp1[i][-4]])


# # windowed mean

# In[25]:


win_mean_meal_p1 = []
win_mean_meal_p1.append([cgm_value_stretch_meal_df.rolling(3, win_type='triang', axis = 1).mean()[8], cgm_value_stretch_meal_df.rolling(3, win_type='triang', axis = 1).mean()[11], cgm_value_stretch_meal_df.rolling(3, win_type='triang', axis = 1).mean()[14], cgm_value_stretch_meal_df.rolling(3, win_type='triang', axis = 1).mean()[17], cgm_value_stretch_meal_df.rolling(3, win_type='triang', axis = 1).mean()[20]])


# In[26]:


feat_win_meal_p1 = []
for j in range(5):
    temp = []
    for i in range(len(win_mean_meal_p1[0][j])):
        temp.append(win_mean_meal_p1[0][j][i])
    feat_win_meal_p1.append(temp)
feat_win_meal_p1 = np.array(feat_win_meal_p1).T


# # Creating feature matrix

# In[27]:


'''max_cgm_velocity_meal_p1 = []
for i in range(len(cgm_velocity_meal_p1)):
    max_cgm_velocity_meal_p1.append([max(cgm_velocity_meal_p1[i]), np.argmax(cgm_velocity_meal_p1[i])*5])'''
final_feature_matrix = []
feature_matrix = []
feature_matrix.append(max_cgm_velocity_meal_p1)
final_feature_matrix.append(feature_matrix[0])
final_feature_matrix = final_feature_matrix[0]


# In[28]:


for i in range(len(final_feature_matrix)):
    final_feature_matrix[i].append(cgm_range_meal_p1[i])


# # important duration for test

# In[29]:


for i in range(len(final_feature_matrix)):
    final_feature_matrix[i].append(imp_duration_meal_p1[i])


# In[30]:


for i in range(len(final_feature_matrix)):
    final_feature_matrix[i].append(fft_meal_p1[i][0])
    final_feature_matrix[i].append(fft_meal_p1[i][1])


# In[31]:


for i in range(len(final_feature_matrix)):
    for j in range(5):
        final_feature_matrix[i].append(feat_win_meal_p1[i][j])


# In[32]:


final_feature_matrix = (np.array(final_feature_matrix).T).T


# In[33]:


final_feature_df = pd.DataFrame(final_feature_matrix, columns=['Max CGM velocity', 'time at max vel', 'CGM max-min', 'Important duration', 'FFT1', 'FFT2', 'Win_mean1', 'Win_mean2', 'Win_mean3', 'Win_mean4', 'Win_mean5'])


# In[34]:


final_feature_df['intake'] = cgm_value_stretch_meal_in


# In[35]:


n_bins = math.ceil((np.max(final_feature_df['intake']) - np.min(final_feature_df['intake']))/ 20 )


# In[36]:


class_list = []
for i in range(len(final_feature_df)):
    for j in range(1, n_bins):
        if(np.min(final_feature_df['intake']) <= final_feature_df['intake'][i] < (np.min(final_feature_df['intake']) + (20*1))):
            class_list.append(1)
            break
        if((np.min(final_feature_df['intake']) + (20 * j)) <= final_feature_df['intake'][i] < (np.min(final_feature_df['intake']) + (20*(j+1)))):
            class_list.append(j+1)
            break
        
            


# In[37]:


final_feature_df['class'] = class_list


# In[38]:


X = final_feature_df.iloc[:,:-2]


# In[39]:


stscaler = StandardScaler().fit(X)
X = stscaler.transform(X)




# # K-MEANS

# In[42]:


Xkm = X


# In[43]:


kmeans = KMeans(n_clusters=7, random_state=50).fit(Xkm)


# In[44]:


kmeans.labels_ = kmeans.labels_+1


# In[45]:


count = 0
count_list1 = []
for j in range(1,8):
    temp_list = []
    for k in range(1,8):
        for i in range(len(class_list)):
            if((kmeans.labels_[i] == j) and (class_list[i] == k)):
                count += 1
        temp_list.append(count)
        count = 0
    count_list1.append(temp_list)

    


# # DBSCAN

# In[46]:


m = DBSCAN(eps=1.21, min_samples=4)
m.fit(X)


# In[47]:


m.labels_ = m.labels_+1


# In[48]:


count = 0
count_list2 = []
for j in range(1,8):
    temp_list = []
    for k in range(1,8):
        for i in range(len(class_list)):
            if((m.labels_[i] == j) and (class_list[i] == k)):
                count += 1
        temp_list.append(count)
        count = 0
    count_list2.append(temp_list)

for i in range(len(class_list)):
    if((m.labels_[i] == 0)):
        count_list2[1][1] += 1


# # K-means sse, entropy, purity 

# In[49]:


Entropy = []
Purity = []
for i in range(7):
    Entropy.append(np.nansum(np.multiply((count_list1[i]/np.sum(count_list1[i])*-1) , np.log(count_list1[i]/np.sum(count_list1[i]))/np.log(2))))
    Purity.append(np.max(count_list1[i])/np.sum(count_list1[i]))

sum_TotalP = np.sum(count_list1)
WholeEntropy_km = 0
WholePurity_km = 0
for i in range(7):
    WholeEntropy_km = WholeEntropy_km + ((np.sum(count_list1[i]))/(sum_TotalP))*Entropy[i]
    WholePurity_km = WholePurity_km + ((np.sum(count_list1[i]))/(sum_TotalP))*Purity[i]


# # DBSCAN sse, entropy ,purity

# In[53]:


Entropy = []
Purity = []
for i in range(7):
    Entropy.append(np.nansum(np.multiply((count_list2[i]/np.sum(count_list2[i])*-1) , np.log(count_list2[i]/np.sum(count_list2[i]))/np.log(2))))
    Purity.append(np.max(count_list2[i])/np.sum(count_list2[i]))

sum_TotalP = np.sum(count_list2)
WholeEntropy_db = 0
WholePurity_db = 0
for i in range(7):
    WholeEntropy_db = WholeEntropy_db + ((np.sum(count_list2[i]))/(sum_TotalP))*Entropy[i]
    WholePurity_db = WholePurity_db + ((np.sum(count_list2[i]))/(sum_TotalP))*Purity[i]


# In[56]:


sse = 0
for i in range(len(class_list)):
    sse += (m.labels_[i] - class_list[i])**2


# In[58]:


final_list=[]
final_list.append(kmeans.inertia_)
final_list.append(sse)
final_list.append(WholeEntropy_km)
final_list.append(WholeEntropy_db)
final_list.append(WholePurity_km)
final_list.append(WholePurity_db)


# In[60]:


temp_df = pd.DataFrame(final_list, columns = None)


# In[61]:


temp_df = temp_df.T


# In[67]:


temp_df.to_csv(r'.\Results.csv', index=False, columns = None)


# In[68]:


final_df = pd.read_csv("Results.csv", encoding="utf-8", skiprows=1)


# In[69]:


final_df.to_csv(r'.\Results.csv', index=False)

