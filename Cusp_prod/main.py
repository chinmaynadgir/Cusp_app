#importing all the necessary libraries
from operator import index
from re import M
import mysql.connector
import pandas as pd
import re
import datetime
import warnings
import configparser

config = configparser.ConfigParser()
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class DateFormat(Error):
    """Raised when the input date is not in YYYY-MM-DD / YYYY-M-D Format"""
    pass


class BadDate(Error):
    """Raised when the start date is larger than the end date"""
    pass

class BadOption(Error):
    """Raised when the option is not D / W / M / Y"""
    pass

class NoData(Error):
    """Raised when the option is not D / W / M / Y"""
    pass
#ignore all warnings
warnings.filterwarnings("ignore")



#the main leads function which takes date range and choice,customer id 
def leads_rep(begin,end,choice,cust_id):
    #get all the parameters from the ini file
    def validate_date(x):
        re_date=re.compile(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$",re.M|re.I)
        if(re.match(re_date,x)):
            print("Date Accepted")
        else :
            raise DateFormat
    def GoodDate(s,e):
        format = '%Y-%m-%d'
        begin_obj = datetime.datetime.strptime(s, format)
        end_obj= datetime.datetime.strptime(e, format)
        if(end_obj<begin_obj):
            raise BadDate
    
    validate_date(begin)
    validate_date(end)
    GoodDate(begin,end)

    
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
    database=database_c)
    if(mydb):
        print("SQL Connection Succesfull")


    print("Step 2: Recieving date range and customerid")
    #begin=input("Enter beggining date in the form of YYYY-MM-DD ").strip()
    begin.strip()

    #end=input("Enter ending date in the form of YYYY-MM-DD ").strip()
    end.strip()

    #choice=input("Enter data to be aggregated:\t0.None\t1.Weekly\t2.Monthly : ").strip()
    choice.strip()
    if(choice not in ["0","d","m","w"]):
        print("wrong choice")
        raise BadOption
    #cust_id=input("Enter customer id : ").strip()
    #genereates the leads report
    if(choice=="0"):
        query="SELECT cf.date as DATE,mc.name as CUSTOMER, su.first_name as NAME , su.company_name as COMPANY,sr.report_id as REPORT,ac.region as STATE,ac.country as COUNTRY ,sr.url as REFERENCE_URL,co.source as CAMPAIGN ,cf.gats  FROM master_customers as mc,shareable_users as su,contact_fact as cf,content_fact as co,shareable_reports as sr,account as ac where cf.customer_id=mc.customer_id and cf.lead_id=su.id and su.id=sr.shareable_user_id and su.company_name=ac.name and sr.url=co.page"
        begin+=' 00::00::00"'
        end+=' 00::00::00"'
        print("Date values accepted are "+begin+' to '+end)

        query=query+' and cf.date between '+'"'+begin+' and '+'"' +end

        if(cust_id!=0):
            query=query+' and cf.customer_id ='+cust_id+';'



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
    #GROUP BY DAILY
    elif(choice=="d"):
        begin+=' 00::00::00'
        end+=' 00::00::00'
        query='SELECT customer_id,DATE(DATE_FORMAT(account_fact.date, "%Y-%m-01")) AS month_beginning,SUM(visitors) AS total_visitors,SUM(events) as total_events,SUM(impressions) as total_impressions,SUM(leads) as total_leads,SUM(time_spent) as total_time_spent FROM cuspera.account_fact where date between "'+begin+'" and "'+end+'"'
        if(cust_id!='0'):
            query=query+'and customer_id='+cust_id 
        query=query+' GROUP BY DATE(DATE_FORMAT(account_fact.date, "%Y-%m-%d")),customer_id order by date;'

    #GROUP BY WEEK
    elif(choice=="w"):
        begin+=' 00::00::00'
        end+=' 00::00::00'
        query='SELECT customer_id,FROM_DAYS(TO_DAYS(account_fact.date) -MOD(TO_DAYS(account_fact.date) -2, 7)) AS week_beginning,SUM(visitors) AS total_visitors,SUM(events) as total_events,SUM(impressions) as total_impressions,SUM(leads) as total_leads,SUM(time_spent) as total_time_spent FROM cuspera.account_fact WHERE date between "'+begin+'" and "'+end+'"'
        if(cust_id!='0'):
            query=query+ 'and customer_id='+cust_id 
        query=query+' GROUP BY FROM_DAYS(TO_DAYS(account_fact.date) -MOD(TO_DAYS(account_fact.date) -2, 7)),customer_id order by date;'
    #GROUP BY MONTH
    elif(choice=="m"):
        begin+=' 00::00::00'
        end+=' 00::00::00'
        query='SELECT customer_id,DATE(DATE_FORMAT(account_fact.date, "%Y-%m-01")) AS month_beginning,SUM(visitors) AS total_visitors,SUM(events) as total_events,SUM(impressions) as total_impressions,SUM(leads) as total_leads,SUM(time_spent) as total_time_spent FROM cuspera.account_fact where date between "'+begin+'" and "'+end+'"'
        if(cust_id!='0'):
            query=query+'and customer_id='+cust_id 
        query=query+' GROUP BY DATE(DATE_FORMAT(account_fact.date, "%Y-%m-01")),customer_id order by date;'
    print("Step 3: Processing initial Query")
    result_df=pd.read_sql(query,mydb)

    def time_string(row):
        secs=row['total_time_spent']
        return str(datetime.timedelta(seconds=secs))

    if(len(result_df)==0):
        raise NoData

    if(choice!="0"):
        result_df['total_time_spent']=result_df.apply(time_string,axis=1)


    
    #file_path=input("Enter name of your file without extensions ")
    file_path='temp'
    file_path+='.csv'
    print("Step 5: Saving the report to CSV")
    result_df.to_csv(file_path,index=0)
    print("Succesfully saved at "+file_path)

#leads_rep('2022-05-03','2022-05-29','1','1')

def leads_main(begin,end,choice,cust_id):
    try:
        leads_rep(begin,end,choice,cust_id)
        success_csv={"code":200,"description": "Successfully Sent CSV file", "name": "Success"}   
        return success_csv
    except DateFormat:
        error_df={"code": 555, "description": "Please enter date in valid format YYYY-MM-DD or YYYY-M-D. If you entered the URL manually please check your spelling and try again.", "name": "DateFormat"}
        return error_df
    except BadDate:
        error_bd={"code": 555, "description": "Please enter start date smaller than the end date . If you entered the URL manually please check your spelling and try again.", "name": "BadDate"}
        return error_bd

    except BadOption:
        error_bo={"code": 555, "description": "Please enter the timeframe as 0/d/w/m. If you entered the URL manually please check your spelling and try again.", "name": "BadOption"}
        return error_bo

    except NoData:
        error_nd={"code": 555, "description": "There are no records to be entered for the given information. Please enter different attributes and try again.", "name": "NoData"}
        return error_nd




 