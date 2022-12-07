# Cusp_app
<hr width =80%>
<center>
<img src='https://raw.githubusercontent.com/chinmaynadgir/Cusp_app/main/cusp.png' title="interface"> </img>
<hr width =80%>

# REQUIREMENTS<hr width=50%>

PANDAS<br>
MYSQL.CONNECTOR<br>
Python 3.9.7 (tags/v3.9.7:1016ef3)<br>
Flask app<br>



# STEPS TO RUN<hr width=50%>
TO RUN USE "PY api.py"<br>
use the url shown in the flask terminal<br>
For ex:<br>
http://192.168.0.119:50100/search?start=2022-05-03&end=2022-05-29&tf=1&cid=1<br>

# DESCRIPTION OF THE PARAMETERS<hr width=50%>
here the parameters are <br>
->start : start date<br>
->end : end date<br>
->tf is time frame : <br>
	  if tf is 0:leads report is generated<br>
	  if tf is d: aggregate by daily  data<br>
	  if tf is w aggregate by weekly data<br>
	  if tf is m aggregate by monthly data<br>

->if cid is the customer id from (0-12):<br>
	  if cid is 0: select all the customers.<br>
