from flask import Flask
from flask import request,make_response,render_template
from main import get_csv
import traceback
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html",data={})

@app.route("/getData",methods=["POST"])
def getData():
    data = request.form
    print(data)
    try:
        start = data["begin"]
        end = data["end"]
        finData=get_csv(start,end)
        resp = make_response(finData)
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp


    except KeyError:
        traceback.print_exc()
        return ("INVALID DATA")




if __name__=="__main__":
    app.run(debug=True)