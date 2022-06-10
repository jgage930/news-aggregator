from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from parsers import CnnParser, NprParser

# flask set up
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

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
	source = db.Column(db.String(50))
	published_date = db.Column(db.String(100))
	image_url = db.Column(db.Text)

# gets the article data from feeds and adds to database
# plan to run this on a cron or some sort of regular basis
def getArticles():
	cnn = CnnParser()
	npr = NprParser()

	cnn_data = cnn.parse()
	for dict in cnn_data:
		article = Article(**dict)
		db.session.add(article)
	
	# TODO must debug npr_parser not motivated at the moment
	# npr_data = npr.parse()
	# for dict in npr_data:
	# 	article = Article(**dict)
	# 	db.session.add(article)

	db.session.commit()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/article/<int:article_id>')
def article_view(article_id):	
	article = Article.query.filter_by(id=article_id).one()

	return render_template('article_view.html', article=article)

if __name__ == '__main__':
	app.run(debug=True)