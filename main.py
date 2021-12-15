import os
import requests
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, FloatField
from flask import Flask, render_template, redirect, url_for, request

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String(250))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250))


db.create_all()


class SearchForm(FlaskForm):
    movie_title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class EditForm(FlaskForm):
    movie_rating = FloatField(label='Your Rating Out Of 10 (e.g, 6.3)', validators=[DataRequired()])
    movie_review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    # retrieve all movies
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", all_movies=all_movies)


@app.route('/add/<movie_id>', methods=['GET', 'POST'])
def add(movie_id):
    form = EditForm()
    movie = Movie.query.get(movie_id)
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('edit.html', movie_id=movie_id, movie=movie, form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
        response = requests.get(url=tmdb_url)
        data = response.json()
        print(data)
        movie_title = data['original_title']
        movie_img_url = f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'
        movie_year = int(data['release_date'][0:4])
        movie_description = data['overview']
        new_movie = Movie(title=movie_title, year=movie_year, description=movie_description,
                          rating=form.movie_rating.data, review=form.movie_review.data, img_url=movie_img_url)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('add.html', form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        tmdb_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&' \
                   f'language=en-US&query={form.movie_title.data}&page=1&include_adult=false'

        response = requests.get(url=tmdb_url)
        data = response.json()['results']
        return render_template('select.html', movies=data)


@app.route('/edit/<movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    form = EditForm()
    movie = Movie.query.get(movie_id)
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('edit.html', form=form, movie=movie)
    elif request.method == 'POST' and form.validate_on_submit():
        movie.rating = form.movie_rating.data
        movie.review = form.movie_review.data
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete/<movie_id>')
def delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
