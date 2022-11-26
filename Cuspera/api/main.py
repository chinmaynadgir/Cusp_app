from operator import index
from re import M
import mysql.connector
import pandas as pd
import re
import os
import warnings
import configparser
config = configparser.ConfigParser()

warnings.filterwarnings("ignore")
def get_csv(begin,end):
    print("Step 1: Attempting SQL Connection")
    config.read('config.ini')
    host_c=config.get('sql','host')
    user_c=config.get('sql','user')
    password_c=config.get('sql','password')
    database_c=config.get('sql','database')

    mydb = mysql.connector.connect(
    host=host_c,
    user=user_c,
    password=password_c,
    database=database_c
    )
    if(mydb):
        print("SQL Connection Succesfull")




    print("Step 2: Recieving date range ")
    # begin=input("Enter beggining date in the form of YYYY-MM-DD ").strip()
    begin+=' 00::00::00"'

    # end=input("Enter ending date in the form of YYYY-MM-DD ").strip()
    end+=' 00::00::00"'

    query="SELECT cf.date as DATE, su.first_name as NAME , su.company_name as COMPANY,sr.report_id as REPORT,ac.region as STATE,ac.country as COUNTRY ,sr.url as REFERENCE_URL,co.source as CAMPAIGN ,cf.gats  FROM shareable_users as su,contact_fact as cf,content_fact as co,shareable_reports as sr,account as ac where cf.lead_id=su.id and su.id=sr.shareable_user_id and su.company_name=ac.name and sr.url=co.page"

    print("Date values accepted are "+begin+' to '+end)

    query=query+' and cf.date between '+'"'+begin+' and '+'"' +end+';'



    print("Step 3: Processing initial Query")
    result_df=pd.read_sql(query,mydb)

    result_df["COMMUNITY_SIZE"]=""
    result_df["I1"]=""
    result_df["I2"]=""
    result_df["I3"]=""
    result_df["I4"]=""
    result_df["I_Count"]=""
    result_df["B1"]=""
    result_df["B2"]=""
    result_df["B3"]=""
    result_df["B4"]=""
    result_df["B5"]=""
    result_df["B6"]=""
    result_df["B7"]=""
    result_df["B8"]=""
    result_df["B9"]=""
    result_df["B10"]=""
    result_df["B_Count"]=""

    print("Done ...")

    print("Step 4: Processing GATS and Compiling Results")


    re_cs=re.compile(r"[\"]CS.*?[\"]",re.M|re.I)
    re_ind=re.compile(r"[\"]V_.*?[\"]",re.M|re.I)
    re_B=re.compile(r"[\"]G.*?[\"]",re.M|re.I)

    for x in result_df.index:
        cs=re.findall(re_cs,result_df["gats"][x])
        ind=re.findall(re_ind,result_df["gats"][x])
        B=re.findall(re_B,result_df["gats"][x])
        if len(cs):
            result_df["COMMUNITY_SIZE"][x]=cs[0].split('|')[1].rstrip('\"')
        if len(ind):
            for i in range(0,min(len(ind),4)):
                if i==0:
                    result_df["I1"][x]=ind[i].split('|')[1].rstrip('\"')
                    
                elif i==1:
                    result_df["I2"][x]=ind[i].split('|')[1].rstrip('\"')
                    
                elif i==2:
                    result_df["I3"][x]=ind[i].split('|')[1].rstrip('\"')
                    
                elif i==3:
                    result_df["I4"][x]=ind[i].split('|')[1].rstrip('\"')
                    
        result_df["I_Count"][x]=len(ind)
        if len(B):
            for i in range(0,min(len(B),10)):
                if i==0:
                    result_df["B1"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==1:
                    result_df["B2"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==2:
                    result_df["B3"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==3:
                    result_df["B4"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==4:
                    result_df["B5"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==5:
                    result_df["B6"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==6:
                    result_df["B7"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==7:
                    result_df["B8"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==8:
                    result_df["B9"][x]=B[i].split('|')[1].rstrip('\"')
                    
                elif i==9:
                    result_df["B10"][x]=B[i].split('|')[1].rstrip('\"')
                    
                
                
        result_df["B_Count"][x]=len(B)

    print("Done ...")
        
    result_df.drop(['gats'],axis=1,inplace=True)
    val = result_df.to_csv()
    return val
    # file_path=input("Enter name of your file without extensions ")
    # file_path+='.csv'

    # print("Step 5: Saving the report to CSV")

    # result_df.to_csv(file_path,index=0)

    # print("Succesfully saved at "+file_path)