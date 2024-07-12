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

#This section of the code extracts the Power Asset data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/Power/GetPlantsData"

params = dict(
    TokenID = token,
    FromDate = current_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

error_string = 'Message'
error_count = 0

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)
df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["PowerPlants"])

df_owner = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Ownners'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Ownners.', errors='ignore')
    
df_operator = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Operators'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Operators.', errors='ignore')

test = len(df2['Contractors'].value_counts())
        
if test < 1:
    print("List is empty")
    df_contractor = []
    pass
        
else:


    df_contractor = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Contractors'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Contractors.', errors='ignore')


num_pages = df['NoOfPages'].values[0]

print(num_pages)


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

        df = pandas.DataFrame.from_dict(json_dict["PowerPlants"])
        df_owner_temp = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Ownners'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Ownners.', errors='ignore')
    
        df_operator_temp = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Operators'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Operators.', errors='ignore')

    test = len(df['Contractors'].value_counts())
        
    if test < 1:
        print("List is empty")
        df_contractor_temp = []

        pass
        
    else:


        df_contractor_temp = pandas.json_normalize(json_dict['PowerPlants'], record_path =['Contractors'], meta=['PublishedStatus', 'CreatedDate',	
                                                                          'ModifiedDate', 'ExtractedDate', 'RequestedFrom', 
                                                                          'RequestedTo', 'Technology', 'GlobalAssetId',	'GlobalRefId',	
                                                                          'ParentAssetName', 'AssetName', 'AlternativeName1', 'AlternativeName2', 
                                                                          'AlternativeName3', 'Region', 'Country', 'ISO2Code', 'ISO3Code', 
                                                                          'StateorProvince', 'StateTaxonomyID', 'County', 'CityorTown', 
                                                                          'SubTechnology', 'Status', 'Latitude', 'Longitude'], record_prefix='Contractors.', errors='ignore')

    df_owner = df_owner.append(df_owner_temp)
    df_operator = df_operator.append(df_operator_temp)
    df_contractor = df_contractor.append(df_contractor_temp)
    df2 = df2.append(df)



owner_list = df_owner['GlobalRefId'].unique().tolist()
operator_list = df_operator['GlobalRefId'].unique().tolist()
contractor_list = df_contractor['GlobalRefId'].unique().tolist()

ooc_list = owner_list + operator_list + contractor_list

missing_companies = df2.query("GlobalRefId not in @ooc_list")
missing_companies = missing_companies.drop('Ownners',axis=1)
missing_companies = missing_companies.drop('Operators',axis=1)
missing_companies = missing_companies.drop('Contractors',axis=1)


final_owners = df_owner.sort_values(by=['GlobalAssetId','GlobalRefId','ParentAssetName','AssetName'])
final_operators = df_operator.sort_values(by=['GlobalAssetId','GlobalRefId','ParentAssetName','AssetName'])
final_contractors = df_contractor.sort_values(by=['GlobalAssetId','GlobalRefId','ParentAssetName','AssetName'])

temp1 = pandas.concat([final_owners,final_operators])
temp2 = pandas.concat([temp1,final_contractors])
temp3 = pandas.concat([temp2, missing_companies])

final_df = temp3.sort_values(by=['GlobalAssetId','GlobalRefId','ParentAssetName','AssetName'])

output_df = pandas.DataFrame()

output_df['PublishedStatus'] = final_df['PublishedStatus']
output_df['ExtractedDate'] = final_df['ExtractedDate']
output_df['CreatedDate'] = final_df['CreatedDate']
output_df['ModifiedDate'] = final_df['ModifiedDate']
output_df['GlobalAssetId'] = final_df['GlobalAssetId']
output_df['GlobalRefId'] = final_df['GlobalRefId']
output_df['Technology'] = final_df['Technology']
output_df['ParentAssetName'] = final_df['ParentAssetName']
output_df['AssetName'] = final_df['AssetName']
output_df['AlternativeName1'] = final_df['AlternativeName1']
output_df['AlternativeName2'] = final_df['AlternativeName2']
output_df['AlternativeName3'] = final_df['AlternativeName3']
output_df['Region'] = final_df['Region']
output_df['Country'] = final_df['Country']
output_df['ISO2Code'] = final_df['ISO2Code']
output_df['ISO3Code'] = final_df['ISO3Code']
output_df['StateorProvince'] = final_df['StateorProvince']
output_df['StateTaxonomyID'] = final_df['StateTaxonomyID']
output_df['County'] = final_df['County']
output_df['CityorTown'] = final_df['CityorTown']
output_df['SubTechnology'] = final_df['SubTechnology']
output_df['Status'] = final_df['Status']
output_df['Owner'] = final_df['Ownners.OwnerName']
output_df['Owner Stake (%)'] = final_df['Ownners.Stake']
output_df['Owner ID'] = final_df['Ownners.OwnerID']
output_df['Operator'] = final_df['Operators.OperatorName']
output_df['Operator ID'] = final_df['Operators.OperatorID']

test = df_contractor.shape[0]
 
if test < 1:
        print("List is empty")
        output_df['Contractor'] = ""
        output_df['Contractor ID'] = ""

else:
    output_df['Contractor'] = final_df['Contractors.ContractorName']
    output_df['Contractor ID'] = final_df['Contractors.ContractorID']

output_df['Latitude'] = final_df['Latitude']
output_df['Longitude'] = final_df['Longitude']

file_name = "GD08_"+str_current_datetime+"GD_Power_Asset_Data.xlsx"

output_df.to_excel(file_name)


#This section of the code extracts the Power Company Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/Power/GetPowerCompaniesData"

params = dict(
    TokenID = token,
    FromDate = current_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)

df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict['PowerCompanies'])
num_pages = df['NoOfPages'].values[0]

print(num_pages)

for page in range (2,num_pages):
    print(page)
    params['PageNumber'] = page 
    response = requests.get(url=url, params=params)
    text_data = response.text
    json_dict=json.loads(text_data)
    df = pandas.DataFrame.from_dict(json_dict['PowerCompanies'])
    df2 = df2.append(df)

export_df = pandas.DataFrame()

export_df['CDMS ID/Company ID'] = df2['CompanyID']
export_df['Company Name/Title'] = df2['CompanyName']
export_df['Company Name (in Local Language and Alphabet)'] = ""
export_df['City'] = df2['City']
export_df['State'] = df2['State']
export_df['HQ Country'] = df2['CompanyHQCountry']
export_df['Company Website URL'] = df2['CompanyWebSiteURL']
export_df['ISIN'] = df2['ISIN']


file_name = "GD01_"+str_current_datetime+"Power_Company_Data.xlsx"

export_df.to_excel(file_name)


