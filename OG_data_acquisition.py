import requests
import pandas
import json
from flatten_json import flatten
from pandas import json_normalize
from datetime import datetime

token = "15HsL4eXPBtlCfeUdw9hAwvdOWCmnTNKVlI5pJ3OLyo="

last_update_date = input('Enter the date of last update (format 2024-04-28):')
last_update_date_2 = last_update_date.replace('-','')
last_update_num = int(last_update_date_2)

update_date = datetime.strptime(last_update_date, '%Y-%m-%d')
update_date_api = update_date.strftime("%d-%m-%Y")


current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print("Current date & time : ", current_datetime)
str_current_datetime = str(current_datetime)

current_date_api = datetime.now().strftime("%d-%m-%Y")

#This section of the code extracts the OG Field Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGFieldsData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

error_string = 'Message'
error_count = 0

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)


df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["Fields"])
num_pages = df['NoOfPages'].values[0]

print(num_pages)

df_participants = pandas.json_normalize(json_dict['Fields'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'FieldName', 'FieldStatus',	
                                                                          'Terrain', 'AlternativeFieldName1', 'AlternativeFieldName2', 'AlternativeFieldName3', 
                                                                          'FieldLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'ResourceType'], record_prefix='Participants.', errors='ignore')

test = len(df2['Contractors'].value_counts())

if test < 1:
    print("List is empty")
    df_contractors = []
    pass

else:
    df_contractors = pandas.json_normalize(json_dict['Fields'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'FieldName', 'FieldStatus',	
                                                                          'Terrain', 'AlternativeFieldName1', 'AlternativeFieldName2', 'AlternativeFieldName3', 
                                                                          'FieldLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'ResourceType'], record_prefix='Contractors.', errors='ignore')


for page in range (2,num_pages):
    params['PageNumber'] = page 
    print(page)
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    
    
    if error_string in json_dict:
        print('error')
        error_count = error_count+1
        pass
    else:
        
        temp = pandas.DataFrame.from_dict(json_dict["Fields"])
    
        df_participants_temp = pandas.json_normalize(json_dict['Fields'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'FieldName', 'FieldStatus',	
                                                                          'Terrain', 'AlternativeFieldName1', 'AlternativeFieldName2', 'AlternativeFieldName3', 
                                                                          'FieldLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'ResourceType'], record_prefix='Participants.', errors='ignore')

        
    test = len(temp['Contractors'].value_counts())
        
    if test < 1:
        print("List is empty")
        df_contractors_temp = []
        pass
        
    else:

        df_contractors_temp = pandas.json_normalize(json_dict['Fields'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'FieldName', 'FieldStatus',	
                                                                          'Terrain', 'AlternativeFieldName1', 'AlternativeFieldName2', 'AlternativeFieldName3', 
                                                                          'FieldLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'ResourceType'], record_prefix='Contractors.', errors='ignore')

    df_participants = df_participants.append(df_participants_temp)
    df_contractors = df_contractors.append(df_contractors_temp)
    df2 = df2.append(temp)
    
print(df2)

contractors_list = df_contractors['AssetID'].unique().tolist()
participants_list = df_participants['AssetID'].unique().tolist()

ooc_list = contractors_list + participants_list

missing_companies = df2.query("AssetID not in @ooc_list")
missing_companies = missing_companies.drop('ParticipantsData',axis=1)
missing_companies = missing_companies.drop('ContractorData',axis=1)

final_contractors = df_contractors.sort_values(by=['AssetID','FieldName','AlternativeFieldName1','AlternativeFieldName2'])
final_participants = df_participants.sort_values(by=['AssetID','FieldName','AlternativeFieldName1','AlternativeFieldName2'])

temp1 = pandas.concat([final_contractors,final_participants])
temp2 = pandas.concat([temp1, missing_companies])

final_df = temp2.sort_values(by=['AssetID','FieldName','AlternativeFieldName1','AlternativeFieldName2'])


export_df = pandas.DataFrame()

export_df['Data Last Modified Date'] = final_df['ModifiedDate']
export_df['Data Delivery TimeStamp'] = final_df['ExtractedDate']
export_df['AssetID'] = final_df['AssetID']
export_df['Field Name'] = final_df['FieldName']
export_df['Field Status'] = final_df['FieldStatus']
export_df['Terrain'] = final_df['Terrain']
export_df['Alternate Field Name 1'] = final_df['AlternativeFieldName1']
export_df['Alternate Field Name 2'] = final_df['AlternativeFieldName2']
export_df['Alternate Field Name 3'] = final_df['AlternativeFieldName3']
export_df['Field Local Name (Local Language and Alphabet)'] = final_df['FieldLocalName_LocalLanguageAndAlphabet']
export_df['Country'] = final_df['Country']
export_df['Country ISO 2'] = final_df['CountryISO2']
export_df['Country ISO 3'] = final_df['CountryISO3']
export_df['Constituent Entity'] = final_df['ConstituentEntity']
export_df['Constituent Entities ID'] = final_df['ConstituentEntitiesID']
export_df['Participants'] = final_df['Participants.Participants']
export_df['Participant Stake'] = final_df['Participants.ParticipantStake']
export_df['Participants ID'] = final_df['Participants.ParticipantsID']
export_df['Operator'] = final_df['Operator']
export_df['Operator ID'] = final_df['OperatorID']

test = df_contractors.shape[0]
 
if test < 1:
        print("List is empty")
        export_df['Contractor'] = ""
        export_df['Contractor ID'] = ""

else:

    export_df['Contractor'] = final_df['Contractors.Contractor']
    export_df['Contractor ID'] = final_df['Contractors.ContractorID']

export_df['Latitude'] = final_df['Latitude']
export_df['Longitude'] = final_df['Longitude']
export_df['Resource Type'] = final_df['ResourceType']


file_name = "GD04_"+str_current_datetime+"GD_OG_Fields_Data.xlsx"

export_df.to_excel(file_name)


del export_df


#This section of the code extracts the OG Refinery Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGRefineryData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)


df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["Refinery"])
num_pages = df['NoOfPages'].values[0]

df_participants = pandas.json_normalize(json_dict['Refinery'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'RefineryName',	'Terrain',
                                                                          'ProjectStage', 'AlternativeRefineryName1', 'AlternativeRefineryName2', 'AlternativeRefineryName3', 
                                                                          'RefineryLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'RefineryType'], record_prefix='Participants.', errors='ignore')

test = len(df2['Contractors'].value_counts())

if test < 1:
    print("List is empty")
    df_contractors = []
    pass

else:

    df_contractors = pandas.json_normalize(json_dict['Refinery'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'RefineryName',	'Terrain',
                                                                          'ProjectStage', 'AlternativeRefineryName1', 'AlternativeRefineryName2', 'AlternativeRefineryName3', 
                                                                          'RefineryLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'RefineryType'], record_prefix='Contractors.', errors='ignore')



for page in range (2,num_pages):
    params['PageNumber'] = page 
    print(page)
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    if error_string in json_dict:
        print('error')
        error_count = error_count+1
    
    else:
        temp = pandas.DataFrame.from_dict(json_dict["Refinery"])
    
        df_participants_temp = pandas.json_normalize(json_dict['Refinery'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'RefineryName',	'Terrain',
                                                                          'ProjectStage', 'AlternativeRefineryName1', 'AlternativeRefineryName2', 'AlternativeRefineryName3', 
                                                                          'RefineryLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'RefineryType'], record_prefix='Participants.', errors='ignore')
    test = len(temp['Contractors'].value_counts())
        
    if test < 1:
        print("List is empty")
        df_contractors_temp = []
        pass
        
    else:

        df_contractors_temp = pandas.json_normalize(json_dict['Refinery'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'RefineryName',	'Terrain',
                                                                          'ProjectStage', 'AlternativeRefineryName1', 'AlternativeRefineryName2', 'AlternativeRefineryName3', 
                                                                          'RefineryLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'RefineryType'], record_prefix='Contractors.', errors='ignore')

    df_participants = df_participants.append(df_participants_temp)
    df_contractors = df_contractors.append(df_contractors_temp)
    df2 = df2.append(temp)
    
print(df2)

contractors_list = df_contractors['AssetID'].unique().tolist()
participants_list = df_participants['AssetID'].unique().tolist()

ooc_list = contractors_list + participants_list

missing_companies = df2.query("AssetID not in @ooc_list")
missing_companies = missing_companies.drop('ParticipantsData',axis=1)
missing_companies = missing_companies.drop('ContractorData',axis=1)

final_contractors = df_contractors.sort_values(by=['AssetID','RefineryName','AlternativeRefineryName1','AlternativeRefineryName2'])
final_participants = df_participants.sort_values(by=['AssetID','RefineryName','AlternativeRefineryName1','AlternativeRefineryName2'])

temp1 = pandas.concat([final_contractors,final_participants])
temp2 = pandas.concat([temp1, missing_companies])

final_df = temp2.sort_values(by=['AssetID','RefineryName','AlternativeRefineryName1','AlternativeRefineryName2'])

export_df = pandas.DataFrame()

export_df['Data Last Modified Date'] = final_df['ModifiedDate']
export_df['TimeStamp'] = final_df['ExtractedDate']
export_df['AssetID'] = final_df['AssetID']
export_df['Refinery Name'] = final_df['RefineryName']
export_df['Terrain'] = final_df['Terrain']
export_df['Project Stage'] = final_df['ProjectStage']
export_df['Alternate Refinery Name 1'] = final_df['AlternativeRefineryName1']
export_df['Alternate Refinery Name 2'] = final_df['AlternativeRefineryName2']
export_df['Alternate Refinery Name 3'] = final_df['AlternativeRefineryName3']
export_df['Refinery Local Name (Local Language and Alphabet)'] = final_df['RefineryLocalName_LocalLanguageAndAlphabet']
export_df['Country'] = final_df['Country']
export_df['Country ISO 2'] = final_df['CountryISO2']
export_df['Country ISO 3'] = final_df['CountryISO3']
export_df['Constituent Entity'] = final_df['ConstituentEntity']
export_df['Constituent Entities ID'] = final_df['ConstituentEntitiesID']
export_df['Participants'] = final_df['Participants.Participants']
export_df['Participant Stake'] = final_df['Participants.ParticipantStake']
export_df['Participants ID'] = final_df['Participants.ParticipantsID']
export_df['Operator'] = final_df['Operator']
export_df['Operator ID'] = final_df['OperatorID']

if test < 1:
        print("List is empty")
        export_df['Contractor'] = ""
        export_df['Contractor ID'] = ""

else:

    export_df['Contractor'] = final_df['Contractors.Contractor']
    export_df['Contractor ID'] = final_df['Contractors.ContractorID']


export_df['Latitude'] = final_df['Latitude']
export_df['Longitude'] = final_df['Longitude']
export_df['Refinery Type'] = final_df['RefineryType']


file_name = "GD05_"+str_current_datetime+"GD_Refinery_Project_Data.xlsx"

export_df.to_excel(file_name)

del export_df

#This section of the code extracts the OG Liquid Storage Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGLiquidStorageData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)


df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["LiquidStorage"])
num_pages = df['NoOfPages'].values[0]

df_participants = pandas.json_normalize(json_dict['LiquidStorage'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'LiquidStorageName','LiquidStorageStatus',
                                                                          'Terrain', 'AlternativeLiquidStorageName1', 'AlternativeLiquidStorageName2', 'AlternativeLiquidStorageName3', 
                                                                          'LiquidStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'Commodity'], record_prefix='Participants.', errors='ignore')

test = len(df2['Contractors'].value_counts())

if test < 1:
    print("List is empty")
    df_contractors = []
    pass

else:
    df_contractors = pandas.json_normalize(json_dict['LiquidStorage'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'LiquidStorageName','LiquidStorageStatus',
                                                                          'Terrain', 'AlternativeLiquidStorageName1', 'AlternativeLiquidStorageName2', 'AlternativeLiquidStorageName3', 
                                                                          'LiquidStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'Commodity'], record_prefix='Contractors.', errors='ignore')


for page in range (2,num_pages):
    params['PageNumber'] = page 
    print(page)
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    if error_string in json_dict:
        print('error')
        error_count = error_count+1
    else:
        temp = pandas.DataFrame.from_dict(json_dict["LiquidStorage"])
    
        df_participants_temp = pandas.json_normalize(json_dict['LiquidStorage'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'LiquidStorageName','LiquidStorageStatus',
                                                                          'Terrain', 'AlternativeLiquidStorageName1', 'AlternativeLiquidStorageName2', 'AlternativeLiquidStorageName3', 
                                                                          'LiquidStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'Commodity'], record_prefix='Participants.', errors='ignore')
    test = len(temp['Contractors'].value_counts())
        
    if test < 1:
        print("List is empty")
        df_contractors_temp = []
        pass
        
    else:

        df_contractors_temp = pandas.json_normalize(json_dict['LiquidStorage'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'LiquidStorageName','LiquidStorageStatus',
                                                                          'Terrain', 'AlternativeLiquidStorageName1', 'AlternativeLiquidStorageName2', 'AlternativeLiquidStorageName3', 
                                                                          'LiquidStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'Commodity'], record_prefix='Contractors.', errors='ignore')

    df_participants = df_participants.append(df_participants_temp)
    df_contractors = df_contractors.append(df_contractors_temp)
    df2 = df2.append(temp)
    
print(df2)

contractors_list = df_contractors['AssetID'].unique().tolist()
participants_list = df_participants['AssetID'].unique().tolist()

ooc_list = contractors_list + participants_list

missing_companies = df2.query("AssetID not in @ooc_list")
missing_companies = missing_companies.drop('ParticipantsData',axis=1)
missing_companies = missing_companies.drop('ContractorData',axis=1)

final_contractors = df_contractors.sort_values(by=['AssetID','LiquidStorageName','AlternativeLiquidStorageName1','AlternativeLiquidStorageName2'])
final_participants = df_participants.sort_values(by=['AssetID','LiquidStorageName','AlternativeLiquidStorageName1','AlternativeLiquidStorageName2'])

temp1 = pandas.concat([final_contractors,final_participants])
temp2 = pandas.concat([temp1, missing_companies])

final_df = temp2.sort_values(by=['AssetID','LiquidStorageName','AlternativeLiquidStorageName1','AlternativeLiquidStorageName2'])

export_df = pandas.DataFrame()

export_df['Data Last Modified Date'] = final_df['ModifiedDate']
export_df['Data Delivery TimeStamp'] = final_df['ExtractedDate']
export_df['AssetID'] = final_df['AssetID']
export_df['Liquid Storage Name'] = final_df['LiquidStorageName']
export_df['Status'] = final_df['LiquidStorageStatus']
export_df['Terrain'] = final_df['Terrain']
export_df['Alternate Liquid Storage Name 1'] = final_df['AlternativeLiquidStorageName1']
export_df['Alternate Liquid Storage Name 2'] = final_df['AlternativeLiquidStorageName2']
export_df['Alternate Liquid Storage Name 3'] = final_df['AlternativeLiquidStorageName3']
export_df['Liquid Storage Local Name (Local Language and Alphabet)'] = final_df['LiquidStorageLocalName_LocalLanguageAndAlphabet']
export_df['Country'] = final_df['Country']
export_df['Country ISO 2'] = final_df['CountryISO2']
export_df['Country ISO 3'] = final_df['CountryISO3']
export_df['Constituent Entity'] = final_df['ConstituentEntity']
export_df['Constituent Entities ID'] = final_df['ConstituentEntitiesID']
export_df['Participants'] = final_df['Participants.Participants']
export_df['Participant Stake'] = final_df['Participants.ParticipantStake']
export_df['Participants ID'] = final_df['Participants.ParticipantsID']
export_df['Operator'] = final_df['Operator']
export_df['Operator ID'] = final_df['OperatorID']

if test < 1:
        print("List is empty")
        export_df['Contractor'] = ""
        export_df['Contractor ID'] = ""

else:

    export_df['Contractor'] = final_df['Contractors.Contractor']
    export_df['Contractor ID'] = final_df['Contractors.ContractorID']


export_df['Latitude'] = final_df['Latitude']
export_df['Longitude'] = final_df['Longitude']
export_df['Commodity'] = final_df['Commodity']

file_name = "GD06_"+str_current_datetime+"GD_Liquid_Storage_Project_Data.xlsx"

export_df.to_excel(file_name)


del export_df

#This section of the code extracts the OG Gas Storage Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGGasStorageData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)


df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["GasStorage"])
num_pages = df['NoOfPages'].values[0]

df_participants = pandas.json_normalize(json_dict['GasStorage'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'GasStorageName','GasStorageStatus',
                                                                          'Terrain', 'AlternativeGasStorageName1', 'AlternativeGasStorageName2', 'AlternativeGasStorageName3', 
                                                                          'GasStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'GasStorageType'], record_prefix='Participants.', errors='ignore')

test = len(df2['Contractors'].value_counts())

if test < 1:
    print("List is empty")
    df_contractors = []
    pass

else:
    df_contractors = pandas.json_normalize(json_dict['GasStorage'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'GasStorageName','GasStorageStatus',
                                                                          'Terrain', 'AlternativeGasStorageName1', 'AlternativeGasStorageName2', 'AlternativeGasStorageName3', 
                                                                          'GasStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'GasStorageType'], record_prefix='Contractors.', errors='ignore')



for page in range (2,num_pages):
    params['PageNumber'] = page 
    print(page)
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    
    if error_string in json_dict:
        print('error')
        error_count = error_count+1

    else:
    
        temp = pandas.DataFrame.from_dict(json_dict["GasStorage"])
    
        df_participants_temp = pandas.json_normalize(json_dict['GasStorage'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'GasStorageName','GasStorageStatus',
                                                                          'Terrain', 'AlternativeGasStorageName1', 'AlternativeGasStorageName2', 'AlternativeGasStorageName3', 
                                                                          'GasStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'GasStorageType'], record_prefix='Participants.', errors='ignore')

    test = len(temp['Contractors'].value_counts())

    if test < 1:
        print("List is empty")
        df_contractors_temp = []
        pass
        
    else:
        
        df_contractors_temp = pandas.json_normalize(json_dict['GasStorage'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'GasStorageName','GasStorageStatus',
                                                                          'Terrain', 'AlternativeGasStorageName1', 'AlternativeGasStorageName2', 'AlternativeGasStorageName3', 
                                                                          'GasStorageLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'Latitude', 
                                                                          'Longitude', 'GasStorageType'], record_prefix='Contractors.', errors='ignore')

    df_participants = df_participants.append(df_participants_temp)
    df_contractors = df_contractors.append(df_contractors_temp)
    df2 = df2.append(temp)
    
print(df2)

contractors_list = df_contractors['AssetID'].unique().tolist()
participants_list = df_participants['AssetID'].unique().tolist()

ooc_list = contractors_list + participants_list

missing_companies = df2.query("AssetID not in @ooc_list")
missing_companies = missing_companies.drop('ParticipantsData',axis=1)
missing_companies = missing_companies.drop('ContractorData',axis=1)

final_contractors = df_contractors.sort_values(by=['AssetID','GasStorageName','AlternativeGasStorageName1','AlternativeGasStorageName2'])
final_participants = df_participants.sort_values(by=['AssetID','GasStorageName','AlternativeGasStorageName1','AlternativeGasStorageName2'])

temp1 = pandas.concat([final_contractors,final_participants])
temp2 = pandas.concat([temp1, missing_companies])

final_df = temp2.sort_values(by=['AssetID','GasStorageName','AlternativeGasStorageName1','AlternativeGasStorageName2'])

export_df = pandas.DataFrame()

export_df['Data Last Modified Date'] = final_df['ModifiedDate']
export_df['Data Delivery TimeStamp'] = final_df['ExtractedDate']
export_df['AssetID'] = final_df['AssetID']
export_df['Gas Storage Name'] = final_df['GasStorageName']
export_df['Status'] = final_df['GasStorageStatus']
export_df['Terrain'] = final_df['Terrain']
export_df['Alternate Gas Storage Name 1'] = final_df['AlternativeGasStorageName1']
export_df['Alternate Gas Storage Name 2'] = final_df['AlternativeGasStorageName2']
export_df['Alternate Gas Storage Name 3'] = final_df['AlternativeGasStorageName3']
export_df['Gas Storage Local Name (Local Language and Alphabet)'] = final_df['GasStorageLocalName_LocalLanguageAndAlphabet']
export_df['Country'] = final_df['Country']
export_df['Country ISO 2'] = final_df['CountryISO2']
export_df['Country ISO 3'] = final_df['CountryISO3']
export_df['Constituent Entity'] = final_df['ConstituentEntity']
export_df['Constituent Entities ID'] = final_df['ConstituentEntitiesID']
export_df['Participants'] = final_df['Participants.Participants']
export_df['Participant Stake'] = final_df['Participants.ParticipantStake']
export_df['Participants ID'] = final_df['Participants.ParticipantsID']
export_df['Operator'] = final_df['Operator']
export_df['Operator ID'] = final_df['OperatorID']

if test < 1:
        print("List is empty")
        export_df['Contractor'] = ""
        export_df['Contractor ID'] = ""

else:

    export_df['Contractor'] = final_df['Contractors.Contractor']
    export_df['Contractor ID'] = final_df['Contractors.ContractorID']


export_df['Latitude'] = final_df['Latitude']
export_df['Longitude'] = final_df['Longitude']
export_df['Gas Storage Type'] = final_df['GasStorageType']


file_name = "GD07_"+str_current_datetime+"GD_Gas_Storage_Project_Data.xlsx"

export_df.to_excel(file_name)


del export_df


#This section of the code extracts the OG Pipeline Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGPipelineData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)


df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["Pipeline"])
num_pages = df['NoOfPages'].values[0]

df_participants = pandas.json_normalize(json_dict['Pipeline'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'PipelineName','PipelineStatus',
                                                                          'Terrain', 'AlternativePipelineName1', 'AlternativePipelineName2', 'AlternativePipelineName3', 
                                                                          'PipelineLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'StartPointLatitude', 
                                                                          'StartPointLongitude', 'EndpointLatitude', 'EndpointLongitude','PipelineType',
                                                                          'Route1Latitude', 'Route1Longitude', 'Route2Latitude', 'Route2Longitude',
                                                                          'Route3Latitude', 'Route3Longitude', 'Route4Latitude', 'Route4Longitude',
                                                                          'Route5Latitude', 'Route5Longitude', 'Route6Latitude', 'Route6Longitude',
                                                                          'Route7Latitude', 'Route7Longitude', 'Route8Latitude', 'Route8Longitude',
                                                                          'Route9Latitude', 'Route9Longitude', 'Route10Latitude', 'Route10Longitude'], record_prefix='Participants.', errors='ignore')

test = len(df2['Contractors'].value_counts())

if test < 1:
    print("List is empty")
    df_contractors = []
    pass

else:
    df_contractors = pandas.json_normalize(json_dict['Pipeline'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'PipelineName','PipelineStatus',
                                                                          'Terrain', 'AlternativePipelineName1', 'AlternativePipelineName2', 'AlternativePipelineName3', 
                                                                          'PipelineLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'StartPointLatitude', 
                                                                          'StartPointLongitude', 'EndpointLatitude', 'EndpointLongitude','PipelineType',
                                                                          'Route1Latitude', 'Route1Longitude', 'Route2Latitude', 'Route2Longitude',
                                                                          'Route3Latitude', 'Route3Longitude', 'Route4Latitude', 'Route4Longitude',
                                                                          'Route5Latitude', 'Route5Longitude', 'Route6Latitude', 'Route6Longitude',
                                                                          'Route7Latitude', 'Route7Longitude', 'Route8Latitude', 'Route8Longitude',
                                                                          'Route9Latitude', 'Route9Longitude', 'Route10Latitude', 'Route10Longitude'], record_prefix='Contractors.', errors='ignore')




for page in range (2,num_pages):
    params['PageNumber'] = page 
    print(page)
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    if error_string in json_dict:
        print('error')
        error_count = error_count+1

    else:
    
        temp = pandas.DataFrame.from_dict(json_dict["Pipeline"])
    
        df_participants_temp = pandas.json_normalize(json_dict['Pipeline'], record_path =['ParticipantsData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'PipelineName','PipelineStatus',
                                                                          'Terrain', 'AlternativePipelineName1', 'AlternativePipelineName2', 'AlternativePipelineName3', 
                                                                          'PipelineLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'StartPointLatitude', 
                                                                          'StartPointLongitude', 'EndpointLatitude', 'EndpointLongitude','PipelineType',
                                                                          'Route1Latitude', 'Route1Longitude', 'Route2Latitude', 'Route2Longitude',
                                                                          'Route3Latitude', 'Route3Longitude', 'Route4Latitude', 'Route4Longitude',
                                                                          'Route5Latitude', 'Route5Longitude', 'Route6Latitude', 'Route6Longitude',
                                                                          'Route7Latitude', 'Route7Longitude', 'Route8Latitude', 'Route8Longitude',
                                                                          'Route9Latitude', 'Route9Longitude', 'Route10Latitude', 'Route10Longitude'], record_prefix='Participants.', errors='ignore')

    test = len(temp['Contractors'].value_counts())
        
    if test < 1:
        print("List is empty")
        df_contractors_temp = []
        pass
        
    else:
        
        
        df_contractors_temp = pandas.json_normalize(json_dict['Pipeline'], record_path =['ContractorData'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'AssetID', 'PipelineName','PipelineStatus',
                                                                          'Terrain', 'AlternativePipelineName1', 'AlternativePipelineName2', 'AlternativePipelineName3', 
                                                                          'PipelineLocalName_LocalLanguageAndAlphabet', 'Country', 'CountryISO2', 'CountryISO3', 'ConstituentEntitiesID', 
                                                                          'ConstituentEntity', 'OperatorID', 'Operator', 'StartPointLatitude', 
                                                                          'StartPointLongitude', 'EndpointLatitude', 'EndpointLongitude','PipelineType',
                                                                          'Route1Latitude', 'Route1Longitude', 'Route2Latitude', 'Route2Longitude',
                                                                          'Route3Latitude', 'Route3Longitude', 'Route4Latitude', 'Route4Longitude',
                                                                          'Route5Latitude', 'Route5Longitude', 'Route6Latitude', 'Route6Longitude',
                                                                          'Route7Latitude', 'Route7Longitude', 'Route8Latitude', 'Route8Longitude',
                                                                          'Route9Latitude', 'Route9Longitude', 'Route10Latitude', 'Route10Longitude'], record_prefix='Contractors.', errors='ignore')

    df_participants = df_participants.append(df_participants_temp)
    df_contractors = df_contractors.append(df_contractors_temp)
    df2 = df2.append(temp)
    
print(df2)

contractors_list = df_contractors['AssetID'].unique().tolist()
participants_list = df_participants['AssetID'].unique().tolist()

ooc_list = contractors_list + participants_list

missing_companies = df2.query("AssetID not in @ooc_list")
missing_companies = missing_companies.drop('ParticipantsData',axis=1)
missing_companies = missing_companies.drop('ContractorData',axis=1)

final_contractors = df_contractors.sort_values(by=['AssetID','PipelineName','AlternativePipelineName1','AlternativePipelineName2'])
final_participants = df_participants.sort_values(by=['AssetID','PipelineName','AlternativePipelineName1','AlternativePipelineName2'])

temp1 = pandas.concat([final_contractors,final_participants])
temp2 = pandas.concat([temp1, missing_companies])

final_df = temp2.sort_values(by=['AssetID','PipelineName','AlternativePipelineName1','AlternativePipelineName2'])

export_df = pandas.DataFrame()

export_df['Data Last Modified Date'] = final_df['ModifiedDate']
export_df['Data Delivery TimeStamp'] = final_df['ExtractedDate']
export_df['AssetID'] = final_df['AssetID']
export_df['Pipeline Name'] = final_df['PipelineName']
export_df['Status'] = final_df['PipelineStatus']
export_df['Terrain'] = final_df['Terrain']
export_df['Alternate Pipeline Storage Name 1'] = final_df['AlternativePipelineName1']
export_df['Alternate Pipeline Storage Name 2'] = final_df['AlternativePipelineName2']
export_df['Alternate Pipeline Storage Name 3'] = final_df['AlternativePipelineName3']
export_df['Pipeline Local Name (Local Language and Alphabet)'] = final_df['PipelineLocalName_LocalLanguageAndAlphabet']
export_df['Country'] = final_df['Country']
export_df['Country ISO 2'] = final_df['CountryISO2']
export_df['Country ISO 3'] = final_df['CountryISO3']
export_df['Constituent Entity'] = final_df['ConstituentEntity']
export_df['Constituent Entities ID'] = final_df['ConstituentEntitiesID']
export_df['Participants'] = final_df['Participants.Participants']
export_df['Participant Stake'] = final_df['Participants.ParticipantStake']
export_df['Participants ID'] = final_df['Participants.ParticipantsID']
export_df['Operator'] = final_df['Operator']
export_df['Operator ID'] = final_df['OperatorID']

if test < 1:
        print("List is empty")
        export_df['Contractor'] = ""
        export_df['Contractor ID'] = ""

else:

    export_df['Contractor'] = final_df['Contractors.Contractor']
    export_df['Contractor ID'] = final_df['Contractors.ContractorID']

export_df['Latitude'] = final_df['StartPointLatitude']
export_df['Longitude'] = final_df['StartPointLongitude']
export_df['Endpoint Latitude'] = final_df['EndpointLatitude']
export_df['Endpoint Longitude'] = final_df['EndpointLongitude']
export_df['Route1Latitude'] = final_df['Route1Latitude']
export_df['Route1Longitude'] = final_df['Route1Longitude']
export_df['Route2Latitude'] = final_df['Route2Latitude']
export_df['Route2Longitude'] = final_df['Route2Longitude']
export_df['Route3Latitude'] = final_df['Route3Latitude']
export_df['Route3Longitude'] = final_df['Route3Longitude']
export_df['Route4Latitude'] = final_df['Route4Latitude']
export_df['Route4Longitude'] = final_df['Route4Longitude']
export_df['Route5Latitude'] = final_df['Route5Latitude']
export_df['Route5Longitude'] = final_df['Route5Longitude']
export_df['Route6Latitude'] = final_df['Route6Latitude']
export_df['Route6Longitude'] = final_df['Route6Longitude']
export_df['Route7Latitude'] = final_df['Route7Latitude']
export_df['Route7Longitude'] = final_df['Route7Longitude']
export_df['Route8Latitude'] = final_df['Route8Latitude']
export_df['Route8Longitude'] = final_df['Route8Longitude']
export_df['Route9Latitude'] = final_df['Route9Latitude']
export_df['Route9Longitude'] = final_df['Route9Longitude']
export_df['Route10Latitude'] = final_df['Route10Latitude']
export_df['Route10Longitude'] = final_df['Route10Longitude']
export_df['Pipeline Type'] = final_df['PipelineType']

file_name = "GD03_"+str_current_datetime+"GD_Pipeline_Project_Data.xlsx"

export_df.to_excel(file_name)

print(error_count)


#This section of the code extracts the relevant OG Company Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/OG/GetOGCompaniesData"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)

df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict['Companies'])
num_pages = df['NoOfPages'].values[0]

print(num_pages)

for page in range (2,num_pages):
    print(page)
    params['PageNumber'] = page 
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    df = pandas.DataFrame.from_dict(json_dict['Companies'])
    df2 = df2.append(df)



export_df = pandas.DataFrame()

export_df['CDMS ID/Company ID'] = df2['CompanyID']
export_df['Company Name/Title'] = df2['CompanyName']
export_df['Company Name (in Local Language and Alphabet)'] = ""
export_df['City'] = df2['City']
export_df['State'] = df2['State']
export_df['HQ Country'] = df2['CompanyHQCountry']
export_df['Company Website URL'] = df2['CompanyWebSiteUrl']
export_df['ISIN'] = df2['ISIN']




file_name = "GD01_"+str_current_datetime+"OG_Company_Data.xlsx"



export_df.to_excel(file_name)


