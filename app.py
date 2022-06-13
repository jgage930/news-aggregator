from email import parser
from flask import Flask, jsonify, render_template
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

	next_article_id = article_id + 1

	return render_template('article_view.html', article=article, next_article_id=next_article_id)

@app.route('/cnn')
def cnn_landing_page():
	articles = Article.query.filter_by(source='CNN').limit(10).all()

	return render_template('cnn_landing_page.html', articles=articles)

@app.route('/debug/<int:article_id>')
def debug(article_id):
	parser = CnnParser()

	entry = parser.entries[article_id]
	print(parser.getContent(entry))
	return jsonify(entry)

if __name__ == '__main__':
	app.run(debug=True)