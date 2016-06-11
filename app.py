import os
import requests
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import QB_YTD_STATS


@app.route('/index', methods=['GET', 'POST'])
def index():
		errors = []
		results = {}
		if request.method == "POST":
			  try:
			  	url = request.form['url']
			  	r = requests.get(url)
			  	soup = BeautifulSoup(r.text, 'html.parser')
			  except:
			  	errors.append(
			  		"Unable to get URL. Please make sure it's valid and try again."
			  		)
			  	return render_template('index.html', errors=errors)
			  if r:
						table = soup.find("table", { "class" : "data" })
						for row in table.findAll("tr"):
							for cell in row.findAll("td"):
								for data in cell:
									print(data)


		return render_template('index.html', errors=errors,results=results)
if __name__ == '__main__':
	app.run()