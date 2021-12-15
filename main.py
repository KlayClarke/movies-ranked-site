import os
import requests
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, IntegerField, FloatField
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


db.create_all()


# new_movie = Movie(
#     title='',
#     year=,
#     description=''
#     rating=0,
#     ranking=0,
#     review='',
#     img_url=''
# )
#
# db.session.add(new_movie)
# db.session.commit()


class EditForm(FlaskForm):
    movie_title = StringField(label='Title', validators=[DataRequired()])
    movie_year = IntegerField(label='Year', validators=[DataRequired()])
    movie_description = StringField(label='Description', validators=[DataRequired()])
    movie_rating = FloatField(label='Rating', validators=[DataRequired()])
    movie_ranking = IntegerField(label='Ranking', validators=[DataRequired()])
    movie_review = StringField(label='Review', validators=[DataRequired()])
    movie_img_url = StringField(label='img_url', validators=[DataRequired()])


@app.route("/")
def home():
    # retrieve all movies
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", all_movies=all_movies)


@app.route('/edit/<movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    form = EditForm()
    movie = Movie.query.get(movie_id)
    if request.method == 'GET':
        form.validate_on_submit()
        return render_template('edit.html', form=form, movie=movie)
    elif request.method == 'POST' and form.validate_on_submit():
        pass


if __name__ == '__main__':
    app.run(debug=True)
