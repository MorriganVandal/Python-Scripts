import difflib
import pandas
import re
from fuzzywuzzy import process
import fuzzywuzzy
from rapidfuzz import fuzz
import numpy as np


gd_data = pandas.read_excel(r"C:\Users\ChloeNeil\2024-05-28 00-40-54GD_Power_Asset_Data.xlsx")
rr_data = pandas.read_excel(r"C:\Users\ChloeNeil\rr_projects.xlsx")

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
#This part also cleans up the gd dataset for matching, removing points with no location information
#This part also removes all duplicate datapoints for GDAssetID, since we want this value to be unique for matching


big_data.dropna(subset=['Latitude'], inplace=True)
big_data = big_data[big_data['Latitude'] != 0]
big_data = big_data[big_data['Longitude'] != 0]

not_relevant = ['Wind','Solar CPV','Solar PV','Solar Thermal']

big_data = big_data.query("Technology not in @not_relevant")

big_data.to_excel('GD_projects_matching_list.xlsx')

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

rr_data['split name'] = rr_data["clean name"].astype(str).apply(lambda x: ''.join(x.split()[:2]))

big_data['Split Power Plant Name'] = big_data["Clean Power Plant Name"].astype(str).apply(lambda x: ''.join(x.split()[:2]))

#here is where we find the closest name for each RR datapoint within a list of GD names that are located in the same country 

print(rr_data)
print(big_data)

matching_sample = rr_data

col_sec_rr = 'iso3'
col_sec_gd = 'ISO3Code' 
 
list_seccode = matching_sample[col_sec_rr].unique()
res = pandas.DataFrame()
for col_sec in list_seccode:
    tmp = matching_sample[matching_sample[col_sec_rr]==col_sec]
    tmp2 = tmp.copy()
    tmp2['Closest Match'] = tmp2['split name'].astype(str)
    tmp2["Closest Match"] = tmp2["Closest Match"].apply(lambda x: (difflib.get_close_matches(x, big_data[big_data[col_sec_gd]==col_sec]['Split Power Plant Name'].astype(str), cutoff = 0.95)[:1] or [None])[0])	
    res = pandas.concat([res, tmp2], axis=0)
    
df_95 = res.copy()


#Here we perform a secondary matching, dropping all matches whose power plant types dont also match

df_95.dropna(subset=['Closest Match'], inplace=True)

intersection95 = pandas.merge(df_95, big_data, left_on='Closest Match', right_on='Split Power Plant Name')

print(intersection95)

intersection95 = intersection95.query('projecttype == Technology')
intersection95 = intersection95.query('iso3 == ISO3Code')
intersection_temp = intersection95.drop_duplicates(subset='split name', keep=False)
intersection_temp2 = intersection95[intersection95.duplicated(subset=['split name'], keep=False)]
final_df = pandas.concat([matching_sample,intersection_temp]).drop_duplicates(subset='rr project id',keep='last')

print(intersection_temp)
print(intersection_temp2)

count = intersection_temp2['rr project id'].nunique()

print(count)

matching_sample = rr_data

col_sec_rr = 'iso3'
col_sec_gd = 'ISO3Code' 
 
list_seccode = matching_sample[col_sec_rr].unique()
res = pandas.DataFrame()
for col_sec in list_seccode:
    tmp = matching_sample[matching_sample[col_sec_rr]==col_sec]
    tmp2 = tmp.copy()
    tmp2['Closest Match'] = tmp2['clean name'].astype(str)
    tmp2["Closest Match"] = tmp2["Closest Match"].apply(lambda x: (difflib.get_close_matches(x, big_data[big_data[col_sec_gd]==col_sec]['Clean Power Plant Name'].astype(str), cutoff = 0.99)[:1] or [None])[0])	
    res = pandas.concat([res, tmp2], axis=0)
    
df_99 = res.copy()

df_99.dropna(subset=['Closest Match'], inplace=True)
intersection99 = pandas.merge(df_99, big_data, left_on='Closest Match', right_on='Clean Power Plant Name')
intersection99 = intersection99.query('projecttype == Technology')
intersection99 = intersection99.query('iso3 == ISO3Code')

print(intersection99)

project_list = intersection99['name'].unique()

multi_matched2 = intersection_temp2.query("name not in @project_list")

matched2 = pandas.concat([intersection_temp,intersection99]).drop_duplicates(subset='rr project id',keep='last')

matched_projects = pandas.DataFrame()
multi_matched_list = pandas.DataFrame()


matched_projects["GD ID"] = matched2["GlobalAssetId"].copy()
matched_projects["GD Name"] = matched2["ParentAssetName"].copy()
matched_projects["RR Project ID"] = matched2["rr project id"].copy()
matched_projects["RR Project Name"] = matched2["name"].copy()


multi_matched_list["RR Name"] = multi_matched2['name'].copy()
multi_matched_list["RR Project ID"] = multi_matched2['rr project id'].copy()
multi_matched_list["RR Project Type"] = multi_matched2['projecttype'].copy()
multi_matched_list["Description"] = multi_matched2['propject description'].copy()
multi_matched_list["GD Name"] = multi_matched2['ParentAssetName'].copy()
multi_matched_list["GD ID"] = multi_matched2['GlobalAssetId'].copy()
multi_matched_list["Type"] = multi_matched2['projecttype'].copy()
multi_matched_list["Country"] = multi_matched2['country name '].copy()
multi_matched_list["GD Alternative Name"] = multi_matched2['AlternativeName1'].copy()
multi_matched_list["GD Alternative Name 2"] = multi_matched2['AlternativeName2'].copy()
multi_matched_list["GD Alternative Name 3"] = multi_matched2['AlternativeName3'].copy()
multi_matched_list["GD Region"] = multi_matched2['Region'].copy()
multi_matched_list["GD Constituent Entity/State Or Province/Sea Or Water Body_x"] = multi_matched2['StateorProvince'].copy()
multi_matched_list["GD County"] = multi_matched2['County'].copy()
multi_matched_list["GD City or Town"] = multi_matched2['CityorTown'].copy()
multi_matched_list["GD Status"] = multi_matched2['Status'].copy()


multi_matched_projects = pandas.DataFrame()

temp_df = multi_matched2.drop_duplicates(subset='rr project id', keep='first').copy()

multi_matched_projects["GD ID"] = ""
multi_matched_projects["GD Name"] = ""
multi_matched_projects["RR Project ID"] = temp_df["rr project id"]
multi_matched_projects["RR Project Name"] = temp_df["name"]

multirr_gd = multi_matched_list[multi_matched_list.duplicated(subset=['GD ID'], keep=False)]
onerr_to_multigd = multi_matched_list.drop_duplicates(subset='GD ID', keep=False)


matched_projects.reset_index(drop=True)
multi_matched_list.reset_index(drop=True)
multi_matched_projects.reset_index(drop=True)
multirr_gd.reset_index(drop=True)
onerr_to_multigd.reset_index(drop=True)

matched_projects.to_excel("matched_projects.xlsx")
multirr_gd.to_excel("multi_rr_match_to_one_gd.xlsx")
onerr_to_multigd.to_excel("one_rr_match_to_multi_gd.xlsx")
multi_matched_projects.to_excel(("multi_matched_projects(to fill).xlsx"))


intersection_temp3 = pandas.concat([matching_sample,matched2,multi_matched2]).drop_duplicates(subset='rr project id',keep=False)
intersection_temp3.to_excel("unmatched.xlsx")


