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


error_string = 'Message'
error_count = 0

#This section of the code extracts the Mining Asset Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/Mining/GetMineProjectDetails"

params = dict(
    TokenID = token,
    FromDate = update_date_api,
    ToDate = current_date_api,
    PageNumber = 1,
)

test = requests.get(url=url, params=params)

text_data = test.text
json_dict=json.loads(text_data)

print(json_dict)

df = pandas.DataFrame.from_dict(json_dict["TotalRecordsDetails"])
df2 = pandas.DataFrame.from_dict(json_dict["MineProjects"])

df_equities = pandas.json_normalize(json_dict['MineProjects'], record_path =['Equities'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='Equities.', errors='ignore')
    
df_operator = pandas.json_normalize(json_dict['MineProjects'], record_path =['Operators'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='Operators.', errors='ignore')
    


test = len(df2['CompaniesInvolved'].value_counts())

        
if test < 1:
    print("List is empty")
    df_involved = []
    pass
        
else:

    df_involved = pandas.json_normalize(json_dict['MineProjects'], record_path =['CompaniesInvolved'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='CompaniesInvolved.', errors='ignore')
    

num_pages = df['NoOfPages'].values[0]

print(df2)

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
        df = pandas.DataFrame.from_dict(json_dict["MineProjects"])
        df_equity_temp = pandas.json_normalize(json_dict['MineProjects'], record_path =['Equities'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='Equities.', errors='ignore')
    
        df_operator_temp = pandas.json_normalize(json_dict['MineProjects'], record_path =['Operators'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='Operators.', errors='ignore')
        
        test = len(df['CompaniesInvolved'].value_counts())
                
        if test < 1:
            print("List is empty")
            df_involved_temp = []
            pass
        
        else:
            df_involved_temp = pandas.json_normalize(json_dict['MineProjects'], record_path =['CompaniesInvolved'], meta=['MineId', 'MineName',	
                                                                          'AlternateMineName1', 'AlternateMineName2', 'AlternateMineName3', 
                                                                          'Region', 'Country', 'CountryISO2','CountryISO3',	
                                                                          'State', 'City', 'Latitude', 'Longitude', 
                                                                          'MineArea_Hectares', 'Stage', 'SubStage', 'Status', 'Commodities', 
                                                                          'PrimaryCommodities'], record_prefix='CompaniesInvolved.', errors='ignore')
    
        df_equities = df_equities.append(df_equity_temp)
        df_operator = df_operator.append(df_operator_temp)
        df_involved = df_involved.append(df_involved_temp)
        df2 = df2.append(df)

print(df2)

equity_list = df_equities['MineId'].unique().tolist()
operator_list = df_operator['MineId'].unique().tolist()
involved_list = df_involved['MineId'].unique().tolist()

ooc_list = equity_list + operator_list + involved_list

missing_companies = df2.query("MineId not in @ooc_list")
missing_companies = missing_companies.drop('Equities',axis=1)
missing_companies = missing_companies.drop('Operators',axis=1)
missing_companies = missing_companies.drop('CompaniesInvolved',axis=1)


final_equity = df_equities.sort_values(by=['MineId','MineName'])
final_operators = df_operator.sort_values(by=['MineId','MineName'])
final_involed = df_involved.sort_values(by=['MineId','MineName'])

temp1 = pandas.concat([final_equity,final_operators])
temp2 = pandas.concat([temp1,final_involed])
temp3 = pandas.concat([temp2, missing_companies])

final_df = temp3.sort_values(by=['MineId','MineName'])

output_df = pandas.DataFrame()

output_df['Data Delivery TimeStamp'] = current_datetime

final_df["Sl No."] = ""


grouped_data = final_df.groupby('MineId')
dfs = []

value_counts = final_df.value_counts(subset=['MineId'])

count = len(value_counts)-1

for key, group in grouped_data:
    dfs.append(group)
        
dfs2 = []   
    
for element in range (0,count):
    temp = dfs[element]
    len = temp.shape[0]
    temp["Sl No."] = element
    dfs2.append(temp)
    
output = pandas.concat(dfs2)

print(output)

output_df['Sl No.'] = output["Sl No."]
output_df['Mine ID'] = output['MineId']
output_df['Mine Name'] = output['MineName']
output_df['Alternate Mine Name1'] = output['AlternateMineName1']
output_df['Alternate Mine Name2'] = output['AlternateMineName2']
output_df['Alternate Mine Name3'] = output['AlternateMineName3']
output_df['Equity Partner'] = output['Equities.EquityPartner']
output_df['Equity Partner_CDMS ID'] = output['Equities.CompanyID']
output_df['Equity Partner Stake (%)'] = output['Equities.EquityPartnerStake_Percent']
output_df['Operator Company'] = output['Operators.CompanyName']
output_df['Operator Company_CDMS ID'] = output['Operators.CompanyID']
output_df['Region'] = output['Region']
output_df['Country'] = output['Country']
output_df['Country ISO 2'] = output['CountryISO2']
output_df['Country ISO 3'] = output['CountryISO3']
output_df['State'] = output['State']
output_df['City'] = output['City']
output_df['Latitude'] = output['Latitude']
output_df['Longitude'] = output['Longitude']
output_df['Mine Area (Hectares)'] = output['MineArea_Hectares']
output_df['Stage'] = output['Stage']
output_df['Sub Stage'] = output['SubStage']
output_df['Status'] = output['Status']
output_df['Commodities'] = output['Commodities']
output_df['Primary Commodities'] = output['PrimaryCommodities']

test = df_involved.shape[0]
 
if test < 1:
    print("List is empty")
    output_df['Involvement Type'] = ""
    output_df['Company Name'] = ""
    output_df['CDMS ID'] = ""
    output_df['Reported Year'] = ""
    output_df['Description'] = ""
    output_df['Contract Status'] = ""

else:
    output_df['Involvement Type'] = output['CompaniesInvolved.InvolvementType']
    output_df['Company Name'] = output['CompaniesInvolved.CompanyName']
    output_df['CDMS ID'] = output['CompaniesInvolved.CompanyID']
    output_df['Reported Year'] = output['CompaniesInvolved.ReportedYear']
    output_df['Description'] = output['CompaniesInvolved.Description']
    output_df['Contract Status'] = output['CompaniesInvolved.ContractStatus']

final_export_df = output_df

file_name = "GD02_"+str_current_datetime+"Mining_Data.xlsx"

final_export_df.to_excel(file_name)


#This section of the code extracts the Mining Company Data

url = "https://apidata.globaldata.com/GlobalDataRepRisk/api/Mining/GetCompanyDetails"

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


file_name = "GD01"+str_current_datetime+"Mining_Company_Data.xlsx"

export_df.to_excel(file_name)




