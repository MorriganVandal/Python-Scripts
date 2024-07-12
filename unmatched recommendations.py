import difflib
import pandas
import re
from fuzzywuzzy import process
import fuzzywuzzy
from rapidfuzz import fuzz
import numpy as np


gd_data = pandas.read_excel(r"C:\Users\ChloeNeil\2024-05-28 00-40-54GD_Power_Asset_Data.xlsx")
rr_data = pandas.read_excel(r"C:\Users\ChloeNeil\unmatched.xlsx")
matched = pandas.read_excel(r"C:\Users\ChloeNeil\matched_projects.xlsx")
multimatched = pandas.read_excel(r"C:\Users\ChloeNeil\Power Matching\multi_matched_projects(to fill).xlsx")
all_projects = pandas.read_excel(r"C:\Users\ChloeNeil\rr_projects.xlsx")


#This part fills out the missing location values for subprojects where location is inherited from parent level asset

gd_data.to_excel("temp.xlsx")
big_data_0 = pandas.read_excel("temp.xlsx")

big_data_0 = big_data_0.drop_duplicates(subset='GlobalRefId', keep='first')

grouped_data = big_data_0.groupby('GlobalAssetId')
dfs = []

value_counts = big_data_0.value_counts(subset=['GlobalAssetId'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len = temp.shape[0]
    if len > 1:
        temp2['Latitude'] = temp['Latitude'].replace(0.00000, np.nan).ffill()
        temp2['Longitude'] = temp['Longitude'].replace(0.00000, np.nan).ffill() 
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

big_data = output

#This part cleans up the reprisk data, picking only points with a single location, type and with a non empty name


big_data.dropna(subset=['Latitude'], inplace=True)
big_data = big_data[big_data['Latitude'] != 0]
big_data = big_data[big_data['Longitude'] != 0]

not_relevant = ['Wind','Solar CPV','Solar PV','Solar Thermal']

big_data = big_data.query("Technology not in @not_relevant")

big_data = big_data.drop_duplicates(subset='GlobalAssetId', keep='first')

print(big_data)

rr_data = rr_data.drop_duplicates(subset='rr project id', keep=False)
rr_data.dropna(subset=['name'], inplace=True)
rr_data['dupe test']= rr_data['name']
rr_data["dupe test"] = rr_data["dupe test"].str.replace('[','')
rr_data["dupe test"] = rr_data["dupe test"].str.replace('(','')
rr_data["dupe test"] = rr_data["dupe test"].str.replace(']','')
rr_data["dupe test"] = rr_data["dupe test"].str.replace(')','')
rr_data= rr_data[~rr_data['dupe test'].str.contains("Duplicate")]
rr_data= rr_data[~rr_data['dupe test'].str.contains("DUPLICATE")]
rr_data= rr_data[~rr_data['dupe test'].str.contains("duplicate")]
rr_data.drop(['dupe test'], axis=1, inplace=True)

#this cleans up the names of all datasets, to make for better matching

rr_data["clean name"] = rr_data["name"].str.lower()
big_data["Clean Power Plant Name"] = big_data["ParentAssetName"].str.lower()

#rr_data["bir name"] = rr_data["Matched GD Power Plant Name"].str.lower()

rr_data['clean name'] = rr_data['clean name'].astype(str)
rr_data["clean name"] = rr_data["clean name"].apply(lambda x: (re.sub('[\(\[].*?[\)\]]', '', x)))	
rr_data["clean name"] = rr_data["clean name"].str.replace('-','')
rr_data["clean name"] = rr_data["clean name"].str.replace('&','')
rr_data["clean name"] = rr_data["clean name"].str.replace(',','')
rr_data["clean name"] = rr_data["clean name"].str.replace("'",'')

big_data['Clean Power Plant Name'] =  big_data['Clean Power Plant Name'].astype(str)
big_data["Clean Power Plant Name"] =  big_data["Clean Power Plant Name"].apply(lambda x: (re.sub('[\(\[].*?[\)\]]', '', x)))	
big_data['Clean Power Plant Name'] =  big_data['Clean Power Plant Name'].str.replace('-','')
big_data['Clean Power Plant Name'] =  big_data['Clean Power Plant Name'].str.replace('&','')
big_data['Clean Power Plant Name'] =  big_data['Clean Power Plant Name'].str.replace(',','')
big_data['Clean Power Plant Name'] =  big_data['Clean Power Plant Name'].str.replace("'",'')


#this section takes the GlobalData dataset and separates it into smaller lists by power plant technology type

subtype_bio_gd = "Biopower"
subtype_geo_gd = 'Geothermal'
subtype_hydro_gd = "Hydro"
subtype_nuclear_gd = "Nuclear"
subtype_ocean_gd = "Ocean"
subtype_thermal_gd = "Thermal"

bio_data = big_data[big_data['Technology'].str.contains(subtype_bio_gd)].copy()
geo_data = big_data[big_data['Technology'].str.contains(subtype_geo_gd)].copy()
hydro_data = big_data[big_data['Technology'].str.contains(subtype_hydro_gd)].copy()
nuclear_data = big_data[big_data['Technology'].str.contains(subtype_nuclear_gd)].copy()
ocean_data = big_data[big_data['Technology'].str.contains(subtype_ocean_gd)].copy()
thermal_data = big_data[big_data['Technology'].str.contains(subtype_thermal_gd)].copy()



#this part is to replace the reprisk project tags with the globaldata technology types, so that they can be compared mathematically

rr_data['projecttype'] = rr_data['projecttype'].astype(str)
rr_data["projecttype"] = rr_data["projecttype"].apply(lambda x: (re.sub('[\(\[].*?[\)\]]', '', x)))	
big_data['Technology'] = big_data['Technology'].astype(str)


rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Biomass Power Plants','Biopower')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Geothermal Power Plants','Geothermal')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Hydropower Plants ','Hydro')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Nuclear Power Plants','Nuclear')
big_data['Technology'] = big_data['Technology'].str.replace('Solar CPV','Solar')
big_data['Technology'] = big_data['Technology'].str.replace('Solar Thermal','Solar')
big_data['Technology'] = big_data['Technology'].str.replace('Solar PV','Solar')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Solar Power Plants','Solar')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Fossil Fuel Power Plants','Thermal')
rr_data['projecttype'] =  rr_data['projecttype'].str.replace('Wind Power Plants','Wind')

#This portion of the code compares only the first two words of each name against each other

#rr_data['split name'] = rr_data["clean name"].astype(str).apply(lambda x: ''.join(x.split()[:2]))

#rr_data['bir split'] = rr_data["bir name"].astype(str).apply(lambda x: ''.join(x.split()[:2]))

#big_data['Split Power Plant Name'] = big_data["Clean Power Plant Name"].astype(str).apply(lambda x: ''.join(x.split()[:2]))

#This section of the code cleans up both name lists, removing words that are very common to the dataset

big_data['Dict Clean GD'] =  big_data['Clean Power Plant Name'].str.replace('power','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('plant','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('generator','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('station','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('generating','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('generation','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('project','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('park','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('biogas','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('waste water','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('landfill','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('gas','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('hydropower','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('hydroelectric','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('hydro','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('geo','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('geothermal','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('solar','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('diesel','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('coal','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('oil','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('fired','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('cogeneration','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('combined cycle','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('steam turbine','')
big_data['Dict Clean GD'] =  big_data['Dict Clean GD'].str.replace('wind','')


rr_data['Dict Clean RR'] =  rr_data['clean name'].str.replace('power','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('plant','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('generator','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('station','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('generating','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('generation','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('project','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('park','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('biogas','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('waste water','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('landfill','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('gas','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('hydropower','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('hydro','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('hydroelectric','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('geothermal','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('geo','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('solar','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('diesel','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('coal','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('oil','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('fired','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('cogeneration','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('combined cycle','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('steam turbine','')
rr_data['Dict Clean RR'] =  rr_data['Dict Clean RR'].str.replace('wind','')


#here is where we find the closest name for each RR datapoint within a list of GD names that are located in the same country 

print(rr_data)
print(big_data)

matching_sample = rr_data

col_sec_rr = 'iso3'
col_sec_gd = 'ISO3Code' 
 
#list_seccode = matching_sample[col_sec_rr].unique()
#res = pandas.DataFrame()
#for col_sec in list_seccode:
#    tmp = matching_sample[matching_sample[col_sec_rr]==col_sec]
#    tmp2 = tmp.copy()
#    tmp2['Close Matches Split'] = tmp2['split name'].astype(str)
#    tmp2["Close Matches Split"] = tmp2["Close Matches Split"].apply(lambda x: (process.extract(x, big_data[big_data[col_sec_gd]==col_sec]['Split Power Plant Name'].astype(str), limit=3)))	
#    res = pandas.concat([res, tmp2], axis=0)
    
#df_split = res.copy()

list_seccode = matching_sample[col_sec_rr].unique()
res = pandas.DataFrame()
for col_sec in list_seccode:
    tmp = matching_sample[matching_sample[col_sec_rr]==col_sec]
    tmp2 = tmp.copy()
    tmp2['Close Matches Dict'] = tmp2['Dict Clean RR'].astype(str)
    tmp2["Close Matches Dict"] = tmp2["Close Matches Dict"].apply(lambda x: (process.extract(x, big_data[big_data[col_sec_gd]==col_sec]['Dict Clean GD'].astype(str), limit=3) or [('None','None','None'),('None','None','None'),('None','None','None')]))	
    res = pandas.concat([res, tmp2], axis=0)
    
df_dict = res.copy()

#list_seccode = matching_sample[col_sec_rr].unique()
#res = pandas.DataFrame()
#for col_sec in list_seccode:
#    tmp = matching_sample[matching_sample[col_sec_rr]==col_sec]
#    tmp2 = tmp.copy()
#    tmp2['Close Matches Raw'] = tmp2['clean name'].astype(str)
#    tmp2["Close Matches Raw"] = tmp2["Close Matches Raw"].apply(lambda x: (process.extract(x, big_data[big_data[col_sec_gd]==col_sec]['Clean Power Plant Name'].astype(str), limit=3)))	
#    res = pandas.concat([res, tmp2], axis=0)
    
#df_raw = res.copy()


df_dict['Matches'] = pandas.Series(df_dict['Close Matches Dict']).astype(str).copy()
df_dict['Matches'] = df_dict['Matches'].str.replace('[','')
df_dict['Matches'] = df_dict['Matches'].str.replace('(','')
df_dict['Matches'] = df_dict['Matches'].str.replace("'",'')
df_dict['Matches'] = df_dict['Matches'].str.replace(')','')
df_dict['Matches'] = df_dict['Matches'].str.replace(']','')

df_dict['Match_1_ID'] = df_dict["Matches"].astype(str).apply(lambda x: (re.split(pattern=',', string=x)[2:3] or [None])[0])
df_dict['Match_2_ID'] = df_dict["Matches"].astype(str).apply(lambda x: (re.split(pattern=',', string=x)[5:6] or [None])[0])
df_dict['Match_3_ID'] = df_dict["Matches"].astype(str).apply(lambda x: (re.split(pattern=',', string=x)[8:9] or [None])[0])

dict_list = ["None","",' None',' None ','None ']

df_dict = df_dict.query('Match_1_ID not in @dict_list')
df_dict = df_dict.query('Match_2_ID not in @dict_list')
df_dict = df_dict.query('Match_3_ID not in @dict_list')

df_dict['Match_1_ID'] = df_dict['Match_1_ID'].str.strip()
df_dict['Match_2_ID'] = df_dict['Match_2_ID'].str.strip()
df_dict['Match_3_ID'] = df_dict['Match_3_ID'].str.strip()

df_dict['Match_1_ID'] = pandas.to_numeric(df_dict['Match_1_ID'])
df_dict['Match_2_ID'] = pandas.to_numeric(df_dict['Match_2_ID'])
df_dict['Match_3_ID'] = pandas.to_numeric(df_dict['Match_3_ID'])

print(df_dict)

temp_series = df_dict['Match_1_ID'] 
temp_series2 = df_dict['Match_2_ID'] 
temp_series3 = df_dict['Match_3_ID'] 

df_dict2 = pandas.merge(df_dict, big_data, left_on='Match_1_ID', right_index=True)
df_dict3 = pandas.merge(df_dict2, big_data, left_on='Match_2_ID', right_index=True)
df_dict4 = pandas.merge(df_dict3, big_data, left_on='Match_3_ID', right_index=True, suffixes=['_1','_2'])



unmatched_projects = pandas.DataFrame()

unmatched_projects["RR Project ID"] = df_dict4["rr project id"].copy()
unmatched_projects["RR Project Name"] = df_dict4["name"].copy()
unmatched_projects["RR Project Description"] = df_dict4["propject description"].copy()
unmatched_projects["RR Project Type"] = df_dict4["projecttype"].copy()
unmatched_projects["RR Project Country"] = df_dict4["country name "].copy()
unmatched_projects["RR Project ISO3"] = df_dict4["iso3"].copy()
unmatched_projects["GD ID"] = ""
unmatched_projects["GD Name"] = ""
unmatched_projects["GD Close Match 1"] = df_dict4["ParentAssetName_y"]
unmatched_projects["GD Close Match 2"] = df_dict4["ParentAssetName_1"]
unmatched_projects["GD Close Match 3"] = df_dict4["ParentAssetName_2"]

double_unmatched_projects = pandas.DataFrame()

double_unmatched_projects["RR Project ID"] = rr_data["rr project id"].copy()
double_unmatched_projects["RR Project Name"] = rr_data["name"].copy()
double_unmatched_projects["RR Project Description"] = rr_data["propject description"].copy()
double_unmatched_projects["RR Project Type"] = rr_data["projecttype"].copy()
double_unmatched_projects["RR Project Country"] = rr_data["country name "].copy()
double_unmatched_projects["RR Project ISO3"] = rr_data["iso3"].copy()
double_unmatched_projects["GD ID"] = ""
double_unmatched_projects["GD Name"] = ""
double_unmatched_projects["GD Close Match 1"] = ""
double_unmatched_projects["GD Close Match 2"] = ""
double_unmatched_projects["GD Close Match 3"] = ""

final_df = pandas.concat([double_unmatched_projects,unmatched_projects]).drop_duplicates(subset='RR Project ID',keep='last')


#The final step is to catch those projects that were first discarded from RR project list for reasons like: mulitple types, mulitple locations (these are usually very few).
#These projects will be added to the list of unmatched projects (unless they are known duplicates or have no name)       

unmatched = rr_data

unmatched_list = pandas.DataFrame()
multimatch_list = pandas.DataFrame()
matched_list = pandas.DataFrame()

unmatched_list['RR Project ID'] = unmatched['rr project id'].unique()
multimatch_list['RR Project ID'] = multimatched['RR Project ID'].unique()
matched_list['RR Project ID'] = matched['RR Project ID'].unique()

project_list_total = all_projects['rr project id'].unique()

temp1 = pandas.concat([unmatched_list, multimatch_list], axis=0)
temp2 = pandas.concat([temp1, matched_list], axis=0)

temp_list = temp2['RR Project ID']

df_missing = pandas.DataFrame()

all_projects['rrprojectid'] = all_projects['rr project id']

df_missing = all_projects.query("rrprojectid not in @temp_list")

df_missing.dropna(subset=['name'], inplace=True)
df_missing['dupe test']= df_missing['name'].astype(str)
df_missing["dupe test"] = df_missing["dupe test"].str.replace('[','')
df_missing["dupe test"] = df_missing["dupe test"].str.replace('(','')
df_missing["dupe test"] = df_missing["dupe test"].str.replace(']','')
df_missing["dupe test"] = df_missing["dupe test"].str.replace(')','')
df_missing= df_missing[~df_missing['dupe test'].str.contains("Duplicate")]
df_missing= df_missing[~df_missing['dupe test'].str.contains("DUPLICATE")]
df_missing= df_missing[~df_missing['dupe test'].str.contains("duplicate")]


missing = pandas.DataFrame()

missing["RR Project ID"] = df_missing["rr project id"].copy()
missing["RR Project Name"] = df_missing["name"].copy()
missing["RR Project Description"] = df_missing["propject description"].copy()
missing["RR Project Type"] = ""
missing["RR Project Country"] = ""
missing["RR Project ISO3"] = ""
missing["GD ID"] = ""
missing["GD Name"] = ""
missing["GD Close Match 1"] = ""
missing["GD Close Match 2"] = ""
missing["GD Close Match 3"] = ""

final_df_2 = pandas.concat([final_df,missing]).drop_duplicates(subset='RR Project ID',keep='first')

final_df_2.to_excel("unmatched_projects_with_close_matches.xlsx")

