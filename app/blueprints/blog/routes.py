from flask import request, render_template, redirect, url_for
from app import db
from .import bp as app
from .models import Post
from flask_login import current_user

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        p = Post(
            body=request.form.get('post_body'),
            user_id=1 # going to have to make the user id's dynamic
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('blog.home'))
    context = {
        'posts': Post.query.order_by(Post.date_created.desc()).all()
    }
    return render_template('home.html', **context)
    # return render_template('home.html', user=user, post=post)ren

@app.route('/<id>')
def blog_single(id):
    # for p in Post.query.all():
    #     if p['id'] == int(id):
    #         post = p
    #         break
    post = Post.query.get(id)
    context = {
        'post': post
    }
    return render_template('blog/single.html', **context)