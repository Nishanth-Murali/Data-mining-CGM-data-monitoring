
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


insulin_data = pd.DataFrame(pd.read_csv('insulinData.csv'))


# In[3]:


cgm_data = pd.DataFrame(pd.read_csv('CGMData.csv'))


# In[4]:


for i in range(len(insulin_data)):
    if(insulin_data.loc[i, 'Alarm'] == 'AUTO MODE ACTIVE PLGM OFF'):
        final_date, match_time = insulin_data.loc[i, 'Date'], insulin_data.loc[i, 'Time']


# In[5]:


from datetime import datetime 


# In[6]:


match_time = datetime.strptime(match_time, '%H:%M:%S').time()


# In[7]:


match_time = str(match_time)


# In[8]:


h,m,s = match_time.split(':')
time_sec = h+m+s


# In[9]:


new_times = []
for i in range(len(cgm_data)):
    h_int, m_int, s_int = cgm_data['Time'][i].split(':')
    new_times.append(h_int+m_int+s_int)


# In[10]:


final_times = []
for i in range(len(new_times)):
    final_times.append(int(new_times[i]))


# In[11]:


time_sec = int(time_sec)


# In[12]:


#final_time = min(final_times, key = lambda x: abs(x - time_sec))


# In[13]:


select_times = []
for i in range(len(cgm_data)):
    if((cgm_data.loc[i,'Date']) == final_date and (final_times[i] > time_sec)):
        select_times.append((cgm_data.loc[i,'Time']))


# In[14]:


new_select_times = []
for i in range(len(select_times)):
    h_int, m_int, s_int = select_times[i].split(':')
    new_select_times.append(int(h_int+m_int+s_int))


# In[15]:


final_time = min(new_select_times, key = lambda x: abs(x - time_sec))


# # segmentation

# In[16]:


total_days = len(cgm_data.groupby([cgm_data['Date']]).mean())


# In[17]:


j = 0
day = [[]]*total_days
one_day = []
while(j < len(cgm_data)):
    base_date = cgm_data['Date'][j]
    one_day = []
    while(j < len(cgm_data) and cgm_data['Date'][j] == base_date):
        one_day.append([cgm_data['Index'][j], cgm_data['Date'][j], cgm_data['Time'][j], cgm_data['Sensor Glucose (mg/dL)'][j]])
        j += 1
    day.append(one_day)


# In[18]:


final_days = [[]]
for i in range(len(day)):
    if(len(day[i]) != 0):
        final_days.append(day[i])
final_days.remove(final_days[0])
        


# In[19]:


full_days = []
for i in range(len(final_days)):
    for j in range(len(final_days[i])):
        if(not(np.isnan(final_days[i][j][3]))):
            full_days.append(final_days[i][j])


# In[20]:


df = pd.DataFrame(full_days, columns = ['Index', 'Date', 'Time', 'Sensor Glucose (mg/dL)'])


# In[21]:


j = 0
full_final_days = [[]]*total_days
one_day = []
while(j < len(df)):
    base_date = df['Date'][j]
    one_day = []
    while(j < len(df) and df['Date'][j] == base_date):
        one_day.append([df['Index'][j], df['Date'][j], df['Time'][j], df['Sensor Glucose (mg/dL)'][j]])
        j += 1
    full_final_days.append(one_day)


# In[22]:


complete_final_days = []
for i in range(len(full_final_days)):
    if(len(full_final_days[i]) != 0):
        complete_final_days.append(full_final_days[i])
complete_final_days.remove(complete_final_days[0])
        


# In[23]:


try:
    for i in range(len(complete_final_days)):
        if(len(complete_final_days[i]) < 230 or len(final_days[i]) > 288):
            complete_final_days.remove(complete_final_days[i])
except IndexError:
    pass
        


# In[24]:


complete_days = len(complete_final_days)


# In[25]:


i = 0
j = 0
auto_mode_data = [[]] * len(complete_final_days)
while(j < len(complete_final_days) and (complete_final_days[i][j][1] != final_date) and (complete_final_days[i][j][2] != final_time)):
    one_day = []
    base_date = complete_final_days[i][j][1]
    while(j < len(complete_final_days[i]) and (complete_final_days[i][j][1] == base_date) and (complete_final_days[i][j][1] != final_date) and (complete_final_days[i][j][2] != final_time)):
        one_day = [complete_final_days[i][j][0], complete_final_days[i][j][1], complete_final_days[i][j][2], complete_final_days[i][j][3]]
        auto_mode_data.append(one_day)
        j += 1
    i += 1


# In[26]:


for i in range(len(complete_final_days)):
    for j in range(len(complete_final_days[i])):
        h, m, s = complete_final_days[i][j][2].split(':')
        complete_final_days[i][j][2] = h+m+s
        


# In[27]:


for i in range(len(complete_final_days)):
    for j in range(len(complete_final_days[i])):
        complete_final_days[i][j][2] = int(complete_final_days[i][j][2])


# In[28]:


for i in range(len(complete_final_days)):
    for j in range(len(complete_final_days[i])):
        if(complete_final_days[i][j][1] == final_date and complete_final_days[i][j][2] == final_time):
            sep_index = complete_final_days[i][j][0]


# In[29]:


auto_mode_data = []
manual_mode_data = []
for i in range(len(complete_final_days)):
    for j in range(len(complete_final_days[i])):
        if(complete_final_days[i][j][0] <= sep_index):
            auto_mode_data.append(complete_final_days[i][j])
        else:
            manual_mode_data.append(complete_final_days[i][j])


# In[30]:


j = 0
auto_complete = [[]]*len(auto_mode_data)
one_day = []
while(j < len(auto_mode_data)):
    base_date = auto_mode_data[j][1]
    one_day = []
    while(j < len(auto_mode_data) and auto_mode_data[j][1] == base_date):
        one_day.append([auto_mode_data[j][0], auto_mode_data[j][1], auto_mode_data[j][2], auto_mode_data[j][3]])
        j += 1
    auto_complete.append(one_day)
    i += 1


# In[31]:


final_auto_complete = [[]]
for i in range(len(auto_complete)):
    if(len(auto_complete[i]) != 0):
        final_auto_complete.append(auto_complete[i])
final_auto_complete.remove(auto_complete[0])


# In[32]:


j = 0
manual_complete = [[]]*len(manual_mode_data)
one_day = []
while(j < len(manual_mode_data)):
    base_date = manual_mode_data[j][1]
    one_day = []
    while(j < len(manual_mode_data) and manual_mode_data[j][1] == base_date):
        one_day.append([manual_mode_data[j][0], manual_mode_data[j][1], manual_mode_data[j][2], manual_mode_data[j][3]])
        j += 1
    manual_complete.append(one_day)
    i += 1


# In[33]:


final_manual_complete = [[]]
for i in range(len(manual_complete)):
    if(len(manual_complete[i]) != 0):
        final_manual_complete.append(manual_complete[i])
final_manual_complete.remove(manual_complete[0])


# In[34]:


auto_list = []
manual_list = []


# a) Percentage time in hyperglycemia (CGM > 180 mg/dL), b) percentage of time in hyperglycemia critical (CGM > 250 mg/dL), c) percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL), d) percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL), e) percentage time in hypoglycemia level 1 (CGM < 70 mg/dL), and f) percentage time in hypoglycemia level 2 (CGM < 54 mg/dL).

# # Percentage time in hyperglycemia (CGM > 180 mg/dL) wday_auto

# In[35]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 180):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_180 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_180)


# # percentage of time in hyperglycemia (CGM > 180 mg/dL) wday_manual

# In[36]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 180):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_180 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_180)


# # Percentage time in hyperglycemia (CGM > 180 mg/dL) dt_auto

# In[37]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 180 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_180 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_180)


# # Percentage time in hyperglycemia (CGM > 180 mg/dL) dt_manual

# In[38]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 180 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_180 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_180)


# # Percentage time in hyperglycemia (CGM > 180 mg/dL) on_auto

# In[39]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 180 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_180 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_180)


# # Percentage time in hyperglycemia (CGM > 180 mg/dL) on_manual

# In[40]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 180 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_180 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_180)


# # percentage of time in hyperglycemia critical (CGM > 250 mg/dL) wday_auto

# In[41]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 250):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_250 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_250)


# # percentage of time in hyperglycemia critical (CGM > 250 mg/dL) wday_manual

# In[42]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 250):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_250 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_250)


# # Percentage time in hyperglycemia critical(CGM > 250 mg/dL) dt_auto

# In[43]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 250 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_250 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_250)


# # Percentage time in hyperglycemia critical(CGM > 250 mg/dL) dt_manual

# In[44]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 250 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_250 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_250)


# # Percentage time in hyperglycemia critical (CGM > 250 mg/dL) on_auto

# In[45]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] > 250 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_250 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_250)


# # Percentage time in hyperglycemia critical (CGM > 250 mg/dL) on_manual

# In[46]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] > 250 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_250 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_250)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) wday_auto

# In[47]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 180):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_70180 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_70180)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) wday_manual

# In[48]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 180):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_70180 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_70180)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) dt_auto

# In[49]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 180 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_70180 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_70180)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) dt_manual

# In[50]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 180 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_70180 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_70180)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) on_auto

# In[51]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 180 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_70180 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_70180)


# # percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL) on_manual

# In[52]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 180 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_70180 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_70180)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) wday_auto

# In[53]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 150):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_70150 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_70150)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) wday_manual

# In[54]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 150):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_70150 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_70150)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) dt_auto

# In[55]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 150 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_70150 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_70150)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) dt_manual

# In[56]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 150 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_70150 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_70150)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) on_auto

# In[57]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] >= 70 and final_auto_complete[i][j][3] <= 150 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_70150 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_70150)


# # percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL) on_manual

# In[58]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] >= 70 and final_manual_complete[i][j][3] <= 150 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_70150 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_70150)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) wday_auto

# In[59]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 70):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_70 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_70)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) wday_manual

# In[60]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 70):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_70 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_70)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) dt_auto

# In[61]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 70 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_70 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_70)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) dt_manual

# In[62]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 70 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_70 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_70)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) on_auto

# In[63]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 70 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_70 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_70)


# # percentage time in hypoglycemia level 1 (CGM < 70 mg/dL) on_manual

# In[64]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 70 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_70 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_70)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) wday_auto

# In[65]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 54):
            ind_mean += final_auto_complete[i][j][3]/288
count_wday_sum_auto_54 = ind_mean/len(complete_final_days)
auto_list.append(count_wday_sum_auto_54)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) wday_manual

# In[66]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 54):
            ind_mean += final_manual_complete[i][j][3]/288
count_wday_sum_manual_54 = ind_mean/len(complete_final_days)
manual_list.append(count_wday_sum_manual_54)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) dt_auto

# In[67]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 54 and final_auto_complete[i][j][2] <= 240000 and final_auto_complete[i][j][2] >= 60000):
            ind_mean += final_auto_complete[i][j][3]/288
count_dt_sum_auto_54 = ind_mean/len(complete_final_days)
auto_list.append(count_dt_sum_auto_54)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) dt_manual

# In[68]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 54 and final_manual_complete[i][j][2] <= 240000 and final_manual_complete[i][j][2] >= 60000):
            ind_mean += final_manual_complete[i][j][3]/288
count_dt_sum_manual_54 = ind_mean/len(complete_final_days)
manual_list.append(count_dt_sum_manual_54)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) on_auto

# In[69]:


ind_mean = 0
for i in range(len(final_auto_complete)):
    for j in range(len(final_auto_complete[i])):
        if(final_auto_complete[i][j][3] < 54 and final_auto_complete[i][j][2] <= 60000 and final_auto_complete[i][j][2] >= 0):
            ind_mean += final_auto_complete[i][j][3]/288
count_on_sum_auto_54 = ind_mean/len(complete_final_days)
auto_list.append(count_on_sum_auto_54)


# # percentage time in hypoglycemia level 2 (CGM < 54 mg/dL) on_manual

# In[70]:


ind_mean = 0
for i in range(len(final_manual_complete)):
    for j in range(len(final_manual_complete[i])):
        if(final_manual_complete[i][j][3] < 54 and final_manual_complete[i][j][2] <= 60000 and final_manual_complete[i][j][2] >= 0):
            ind_mean += final_manual_complete[i][j][3]/288
count_on_sum_manual_54 = ind_mean/len(complete_final_days)
manual_list.append(count_on_sum_manual_54)


# In[71]:


final_df = pd.DataFrame([auto_list, manual_list], index = ['auto_mode', 'manual_mode'], columns = ['whole_day_gt_180', 'daytime_gt_180', 'overnight_gt_180', 'whole_day_gt_250', 'daytime_gt_250', 'overnight_gt_250', 'whole_day_gte_70_lte_180', 'daytime_gte_70_lte_180', 'overnight_gte_70_lte_180', 'whole_day_gte_70_lte_150', 'whole_day_gte_70_lte_150', 'whole_day_gte_70_lte_150', 'whole_day_lt_70', 'daytime_lt_70', 'overnight_lt_70', 'whole_day_lt_54', 'daytime_lt_54', 'overnight_lt_54'])


# In[72]:


final_df.to_csv(r'.\results.csv')

