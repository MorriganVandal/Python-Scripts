import pandas
import collections
import itertools
import re

def hydro_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('hydro','Hydro')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('House','Plant')
    longstring = longstring.replace('Scheme','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Works','Plant')
    longstring = longstring.replace('Site','Plant')
    longstring = longstring.replace('Headworks','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('house','Plant')
    longstring = longstring.replace('scheme','Plant')
    longstring = longstring.replace('Headworks','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('works','Plant')
    longstring = longstring.replace('site','Plant')
    return longstring


def bio_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('bio','Bio')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Generator','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('generator','Plant')
    return longstring

def geo_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('geo','Geo')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Generator','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('generator','Plant')
    return longstring

def nuclear_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('nuclear','Nuclear')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Generator','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('generator','Plant')
    return longstring


def ocean_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('tidal','Tidal')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('Farm','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Generator','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('generator','Plant')
    return longstring

def thermal_standardization(longstring):
    longstring = longstring.replace('Power','')
    longstring = longstring.replace('plant','Plant')
    longstring = longstring.replace('oil','Oil')
    longstring = longstring.replace('coal','Coal')
    longstring = longstring.replace('diesel','Oil')
    longstring = longstring.replace('Diesel','Oil')
    longstring = longstring.replace('gas','Gas')
    longstring = longstring.replace('dual-fueled','Dual-Fuel')
    longstring = longstring.replace('dual fueled','Dual-Fuel')
    longstring = longstring.replace('Dual Fired','Dual-Fuel')
    longstring = longstring.replace('Dual Fueled','Dual-Fuel')
    longstring = longstring.replace('Dual-Fired','Dual-Fuel')
    longstring = longstring.replace('dual-fired','Dual-Fuel')
    longstring = longstring.replace('dual fired','Dual-Fuel')
    longstring = longstring.replace('Project','Plant')
    longstring = longstring.replace('Farm','Plant')
    longstring = longstring.replace('Station','Plant')
    longstring = longstring.replace('Facility','Plant')
    longstring = longstring.replace('Complex','Plant')
    longstring = longstring.replace('Generator','Plant')
    longstring = longstring.replace('project','Plant')
    longstring = longstring.replace('station','Plant')
    longstring = longstring.replace('facility','Plant')
    longstring = longstring.replace('complex','Plant')
    longstring = longstring.replace('generator','Plant')
    return longstring


def hydro_update(longstring):
    Hydro = 'Hydro'
    Plant = 'Plant'

    if Hydro in longstring and Plant in longstring:
        return longstring
        
    if Hydro in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Hydro not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Hydro+' '+Plant
        return new_name
    
    if Hydro not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Hydro+' '+Plant
        return new_name
    

def bio_update(longstring):
    Bio = 'Bio'
    Plant = 'Plant'

    if Bio in longstring and Plant in longstring:
        return longstring
        
    if Bio in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Bio not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Bio+' '+Plant
        return new_name
    
    if Bio not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Bio+' '+Plant
        return new_name

def geo_update(longstring):
    Geo = 'Geothermal'
    Plant = 'Plant'

    if Geo in longstring and Plant in longstring:
        return longstring
        
    if Geo in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Geo not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Geo+' '+Plant
        return new_name
    
    if Geo not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Geo+' '+Plant
        return new_name
    
def nuclear_update(longstring):
    Nuclear = 'Nuclear'
    Plant = 'Plant'

    if Nuclear in longstring and Plant in longstring:
        return longstring
        
    if Nuclear in longstring and Plant not in longstring:
        temp_name = longstring.replace('Nuclear','')
        new_name = temp_name+' '+Nuclear+' '+Plant
        return new_name
    
    if Plant in longstring and Nuclear not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Nuclear+' '+Plant
        return new_name
    
    if Nuclear not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Nuclear+' '+Plant
        return new_name

def tidal_update(longstring):
    Tidal = 'Tidal'
    Plant = 'Plant'

    if Tidal in longstring and Plant in longstring:
        return longstring
        
    if Tidal in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Tidal not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Tidal+' '+Plant
        return new_name
    
    if Tidal not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Tidal+' '+Plant
        return new_name

def ocean_update(longstring):
    Ocean = 'Ocean'
    Plant = 'Plant'

    if Ocean in longstring and Plant in longstring:
        return longstring
        
    if Ocean in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Ocean not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Ocean+' '+Plant
        return new_name
    
    if Ocean not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Ocean+' '+Plant
        return new_name
    
def wave_update(longstring):
    Wave = 'Wave'
    Plant = 'Plant'

    if Wave in longstring and Plant in longstring:
        return longstring
        
    if Wave in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Wave not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Wave+' '+Plant
        return new_name
    
    if Wave not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Wave+' '+Plant
        return new_name
    


def oil_update(longstring):
    Oil = 'Oil'
    Plant = 'Plant'

    if Oil in longstring and Plant in longstring:
        return longstring
        
    if Oil in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Oil not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Oil+' '+Plant
        return new_name
    
    if Oil not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Oil+' '+Plant
        return new_name

def coal_update(longstring):
    Coal = 'Coal'
    Plant = 'Plant'

    if Coal in longstring and Plant in longstring:
        return longstring
        
    if Coal in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Coal not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Coal+' '+Plant
        return new_name
    
    if Coal not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Coal+' '+Plant
        return new_name

def gas_update(longstring):
    Gas = 'Gas'
    Plant = 'Plant'

    if Gas in longstring and Plant in longstring:
        return longstring
        
    if Gas in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Gas not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Gas+' '+Plant
        return new_name
    
    if Gas not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Gas+' '+Plant
        return new_name

def dual_update(longstring):
    Dual = 'Dual-Fuel'
    Plant = 'Plant'

    if Dual in longstring and Plant in longstring:
        return longstring
        
    if Dual in longstring and Plant not in longstring:
        new_name = longstring+' '+Plant
        return new_name
    
    if Plant in longstring and Dual not in longstring:
        
        temp_name = longstring.replace('Plant','')
        new_name = temp_name+' '+Dual+' '+Plant
        return new_name
    
    if Dual not in longstring and Plant not in longstring:
        
        new_name = longstring+' '+Dual+' '+Plant
        return new_name

big_data = pandas.read_excel(r"C:\Users\ChloeNeil\GlobalData-Anne de Chastonay-RepRisk AG-List of Power Plants-Final Deliverable-Apr 1, 2024 (1).xlsx")

#This section of the code deals with the hydro projects

hydro_tech = ['Hydro']

name_changes = big_data.query('Technology in @hydro_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (hydro_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (hydro_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_hydro = output

final_data_hydro["New Power Plant Name"] = final_data_hydro["New Power Plant Name"].str.replace('(nan)','')
final_data_hydro["New Power Plant Name"] = final_data_hydro["New Power Plant Name"].str.replace('()','')


final_data_hydro.to_excel('New Hydro Project Names_Chloe_2.xlsx')

#This section of the code deals with the Bio plant data

bio_tech = ['Biopower']

name_changes = big_data.query('Technology in @bio_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (bio_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (bio_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_bio = output

final_data_bio["New Power Plant Name"] = final_data_bio["New Power Plant Name"].str.replace('(nan)','')
final_data_bio["New Power Plant Name"] = final_data_bio["New Power Plant Name"].str.replace('()','')


final_data_bio.to_excel('New Bio Project Names_Chloe_2.xlsx')

#This section of the code deals with the Geothermal plant data

geo_tech = ['Geothermal']

name_changes = big_data.query('Technology in @geo_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (geo_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (geo_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_geo = output

final_data_geo["New Power Plant Name"] = final_data_geo["New Power Plant Name"].str.replace('(nan)','')
final_data_geo["New Power Plant Name"] = final_data_geo["New Power Plant Name"].str.replace('()','')


final_data_geo.to_excel('New Geo Project Names_Chloe_2.xlsx')

#This section of the code deals with the Nuclear plant data

nuclear_tech = ['Nuclear']

name_changes = big_data.query('Technology in @nuclear_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (nuclear_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (nuclear_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_nuclear = output

final_data_nuclear["New Power Plant Name"] = final_data_nuclear["New Power Plant Name"].str.replace('(nan)','')
final_data_nuclear["New Power Plant Name"] = final_data_nuclear["New Power Plant Name"].str.replace('()','')


final_data_nuclear.to_excel('New Nuclear Project Names_Chloe_2.xlsx')

#This section of the code deals with the ocean plant data

tidal_tech = ['Tidal Technology']

name_changes = big_data.query('Type in @tidal_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (ocean_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (tidal_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_tidal = output

final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('(nan)','')
final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('()','')


final_data_tidal.to_excel('New Tidal Project Names_Chloe_2.xlsx')


#-------

ocean_tech = ['Ocean Thermal Technology']

name_changes = big_data.query('Type in @ocean_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (ocean_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (ocean_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_tidal = output

final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('(nan)','')
final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('()','')


final_data_tidal.to_excel('New Ocean Thermal Project Names_Chloe_2.xlsx')


#-------

wave_tech = ['Wave Technology']

name_changes = big_data.query('Type in @tidal_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (ocean_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (wave_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_tidal = output

final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('(nan)','')
final_data_tidal["New Power Plant Name"] = final_data_tidal["New Power Plant Name"].str.replace('()','')


final_data_tidal.to_excel('New Wave Project Names_Chloe_2.xlsx')


#This section of the code deals with the fossil plant data

oil_tech = ['Oil']
gas_tech = ['Gas']
coal_tech = ['Coal']
dual_tech = ['Dual-Fuel']


name_changes = big_data.query('Type in @oil_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (thermal_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (oil_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))

grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_oil = output

final_data_oil["New Power Plant Name"] = final_data_oil["New Power Plant Name"].str.replace('(nan)','')
final_data_oil["New Power Plant Name"] = final_data_oil["New Power Plant Name"].str.replace('()','')


final_data_oil.to_excel('New Oil Project Names_Chloe_2.xlsx')

#-------

name_changes = big_data.query('Type in @coal_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (thermal_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (coal_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))


grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_coal = output

final_data_coal["New Power Plant Name"] = final_data_coal["New Power Plant Name"].str.replace('(nan)','')
final_data_coal["New Power Plant Name"] = final_data_coal["New Power Plant Name"].str.replace('()','')


final_data_coal.to_excel('New Coal Project Names_Chloe_2.xlsx')

#-------

name_changes = big_data.query('Type in @gas_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (thermal_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (gas_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))


grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_gas = output

final_data_gas["New Power Plant Name"] = final_data_gas["New Power Plant Name"].str.replace('(nan)','')
final_data_gas["New Power Plant Name"] = final_data_gas["New Power Plant Name"].str.replace('()','')


final_data_gas.to_excel('New Gas Project Names_Chloe_2.xlsx')

#-------

name_changes = big_data.query('Type in @dual_tech')

name_changes["New Power Plant Name"] = name_changes["Power Plant Name"].apply(lambda x: (thermal_standardization(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (dual_update(x)))	

name_changes["New Power Plant Name"] = name_changes["New Power Plant Name"].apply(lambda x: (" ".join(x.split())))


grouped_data = name_changes.groupby('Asset ID')
dfs = []

value_counts = name_changes.value_counts(subset=['Asset ID'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
    
    
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len1 = temp.shape[0]
    owners = temp['Owner'].unique().tolist()
    len_owners = len(owners)
    others = ['Others']
    first_owner = str(owners[0])
    if len_owners == 1 and first_owner not in others:
            temp2 = temp
            temp2['New Power Plant Name'] = temp["New Power Plant Name"].apply(lambda x: (x+' '+'('+first_owner+')'))	
    else:
        temp2 = temp
    dfs2.append(temp2)
    
output = pandas.concat(dfs2)

final_data_dual = output

final_data_dual["New Power Plant Name"] = final_data_dual["New Power Plant Name"].str.replace('(nan)','')
final_data_dual["New Power Plant Name"] = final_data_dual["New Power Plant Name"].str.replace('()','')


final_data_dual.to_excel('New Dual-Fuel Project Names_Chloe_2.xlsx')


#-------

final_data = pandas.concat([final_data_hydro,final_data_bio,final_data_geo,final_data_nuclear,final_data_tidal,final_data_oil,final_data_coal,final_data_gas,final_data_dual])


final_data.to_excel('New Project Names_Chloe_2.xlsx')

