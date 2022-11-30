from flask import Flask, request,send_file
from main import leads_rep
import os,time

app = Flask(__name__)

#recieving input parameters
@app.route('/search')
def search():
    if os.path.exists('temp.csv'):
        os.remove('temp.csv')

    # get the request query parameters as a python dict
    args = request.args.to_dict()

    # get the 'name' query parameter value with a default value as 'No Name'
    start = args.get("start",-1)    
    end = args.get("end",-1)
    cid=args.get("cid","-1")
    tf=args.get("tf",-1)

    if(start==-1 and end==-1 and tf==-1):
        return "Enter parameters for start ,end and tf"
    

    elif(cid!=0):
        leads_rep(start,end,tf,cid)

    else:
        leads_rep(start,end,tf,cid)

    while(os.path.exists('temp.csv')):
        return send_file('temp.csv') 
    else:
        time.sleep(1)
        print("processing")  
        
        
    #return "Hello {0},{1},{2},{3}!!!".format(start,end,cid,tf)
    

app.run(host='0.0.0.0', port=50100, debug=True)