from flask import Flask, request,send_file,json
from main import leads_rep
from main import DateFormat
from main import BadDate
from main import BadOption
from main import NoData
from werkzeug.exceptions import HTTPException
import os,time

app = Flask(__name__)

#errorjsontrial
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

#recieving input parameters
@app.route('/')
def welcome():
    return "<h1 style='font-family:fantasy;font-size:500%'><center>CUSP APP - API END</h1><hr width=80%><br><h3 style='font-family:fantasy;font-size:250%'><center>Enter Parameters By URL</h3></center><h4 style='font-family:fantasy;font-size:100%'><center> In the format :/search?start=yyyy-mm-dd&end=yyyy-mm-dd&tf=d/w/m&cid=(0-10)</h4>"
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

    #format of date
    #start date < end date
    #string values D W M Y
    try:
        if(start==-1 and end==-1 and tf==-1):
            return "Enter parameters for start ,end and tf"
        

        elif(cid!=0):
            leads_rep(start,end,tf,cid)

        else:
            leads_rep(start,end,tf,cid)
    except DateFormat:
        error_df=json.dumps({"code": 555, "description": "Please enter date in valid format YYYY-MM-DD or YYYY-M-D. If you entered the URL manually please check your spelling and try again.", "name": "DateFormat"})
        response = app.response_class(
        response=error_df,
        status=200,
        mimetype='application/json'
    )
        return response

    except BadDate:
        error_bd=json.dumps({"code": 555, "description": "Please enter start date smaller than the end date . If you entered the URL manually please check your spelling and try again.", "name": "BadDate"})
        response = app.response_class(
        response=error_bd,
        status=200,
        mimetype='application/json'
    )
        return response

    except BadOption:
        error_bo=json.dumps({"code": 555, "description": "Please enter the timeframe as 0/d/w/m. If you entered the URL manually please check your spelling and try again.", "name": "BadOption"})
        response = app.response_class(
        response=error_bo,
        status=200,
        mimetype='application/json'
    )
        return response

    except NoData:
        error_nd=json.dumps({"code": 555, "description": "There are no records to be entered for the given information. Please enter different attributes and try again.", "name": "NoData"})
        response = app.response_class(
        response=error_nd,
        status=200,
        mimetype='application/json'
    )
        return response



    while(os.path.exists('temp.csv')):
        return send_file('temp.csv') 
    else:
        time.sleep(1)
        print("processing")  
        
        
    #return "Hello {0},{1},{2},{3}!!!".format(start,end,cid,tf)
    

app.run(host='0.0.0.0', port=50100, debug=True)