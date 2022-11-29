# importing the required libraries
import os
from flask import Flask, render_template, request, send_file

# initialising the flask app
app = Flask(__name__)

# displaying the HTML template at the home url
@app.route('/')
def index():
   return render_template('download.html')

# Sending the file to the user
@app.route('/download')
def download():
   return send_file('sample.pdf', as_attachment=True)

if __name__ == '__main__':
   app.run() # running the flask app