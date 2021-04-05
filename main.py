from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


posts = BlogPost.query.all()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    print(posts)
    return render_template("post.html", post=requested_post, ckeditor=ckeditor)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    form = CreatePostForm(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        img_url=requested_post.img_url,
        author=requested_post.author,
        body=requested_post.body
    )

    if form.validate_on_submit():
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        # requested_post.date = date.today().strftime('%B %d, %Y')
        requested_post.body = form.body.data
        requested_post.author = form.author.data
        requested_post.img_url = form.img_url.data

        db.session.commit()
        print(requested_post.id)
        return redirect(url_for('show_post', index=requested_post.id))
    return render_template("edit-post.html", form=form)


@app.route("/new-post", methods=["POST", "GET"])
def create_post():
    form = CreatePostForm(request.form)
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        image_url = form.img_url.data
        body = form.body.data

        new_post = BlogPost(
            title=title,
            subtitle=subtitle,
            date=date.today().strftime("%B %d, %Y"),
            body=body,
            author=author,
            img_url=image_url
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


@app.route("/delete/<int:index>")
def delete_blog(index):
    blog = BlogPost.query.get(index)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
