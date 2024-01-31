"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "fgshsafadfhd"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
with app.app_context():
    db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/homepage.html', posts=posts)


@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    # return render_template('users.html', users=users)
    return render_template('users/index.html', users=users)



@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Shows list of all users in db"""
    return render_template('users/new.html')


@app.route('/users/new', methods=["POST"])
def users_new():
    new_user = User(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = request.form["image_url"] or None)
        
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



##################################################################################################################



@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
        content=request.form['content'],
        user=user, tags=tags) 
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}") 


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    # user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


###################################################################################################################################


@app.route('/tags')
def list_tags():
    """Shows list of all tags in db"""
    tags = Tag.query.all()
    # return render_template('tags.html', tags=tags)
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Shows list of all tags in db"""
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def tags_new():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)
        
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/show.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def tag_edit_form(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tags/edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tags_edit(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")