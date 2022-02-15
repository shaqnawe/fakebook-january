from crypt import methods
from app import app, db
from flask import render_template, request, redirect, url_for
from .models import User, Post

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        p = Post(
            body=request.form.get('post_body'),
            user_id=1 # going to have to make the user id's dynamic
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('home'))
    context = {
        'posts': Post.query.order_by(Post.date_created.desc()).all()
    }
    return render_template('home.html', **context)
    # return render_template('home.html', user=user, post=post)ren

@app.route('/blog/<id>')
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')