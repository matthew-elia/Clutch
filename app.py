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


@app.route('/', methods=['GET', 'POST'])
def index():
		errors = []
		results = {}
		labels = []
		stats = []

		if request.method == "POST":
			  try:
			  	url = request.form['url']
			  	r = requests.get(url)
			  	soup = BeautifulSoup(r.content, 'html.parser')
			  except:
			  	errors.append(
			  		"Unable to get URL. Please make sure it's valid and try again."
			  		)
			  	return render_template('index.html', errors=errors)
			  if r:
						page_title = soup.find("tr", { "class" : "title" })
						for title in page_title.findAll("td"):
							print(title.get_text())

						categories = soup.find("tr", { "id" : "special"})
						for category in categories.findAll("td"):
							print(category.get_text())

						thead = soup.find("tr", { "class" : "label" })
						for label in thead.findAll("a"):
							print(label.get_text())
							labels.append(label.get_text())

						table = soup.find("table", { "class" : "data" })
						for row in table.findAll("tr", { "class" : "row1" or "row2" }):
							for data in row.findAll("td", { "class" : not "mybg4" }): 
									print(data.get_text())
									stats.append(data.get_text())

		return render_template('index.html', errors=errors, results=results)
if __name__ == '__main__':
	app.run()