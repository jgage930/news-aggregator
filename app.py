from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# flask set up
app = Flask(__name__)
app.config['SQLALCHEM_DATABASE_URI'] = 'sqlite:///data.db'

# database
db = SQLAlchemy(app)

# Database Models
class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200))
	summary = db.Column(db.Text)
	archive_date = db.Column(db.DateTime)
	authors = db.Column(db.Text)
	orig_article_link = db.Column(db.Text)
	content = db.Column(db.Text)
	source = db.Column(db.String(15))

@app.route('/')
def index():
	pass

if __name__ == '__main__':
	app.run(debug=True)