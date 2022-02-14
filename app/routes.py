from app import app
from flask import render_template

derek = {
    'id': 1,
    'first_name': 'Derek',
    'last_name': 'Hawkins',
    'is_active': False
}
lucas = {
    'id': 2,
    'first_name': 'Lucas',
    'last_name': 'Lang',
    'is_active': True
}
posts = [
    {
        'id': 1,
        'body': 'This is the first post',
        'user': lucas
    },
    {
        'id': 2,
        'body': 'This is the second post',
        'user': lucas
    },
    {
        'id': 3,
        'body': 'This is the third post',
        'user': derek
    },
]

@app.route('/')
def home():
    context = {
        'posts': posts
    }
    return render_template('home.html', **context)
    # return render_template('home.html', user=user, post=post)ren

@app.route('/blog/<id>')
def blog_single(id):
    for p in posts:
        if p['id'] == int(id):
            post = p
            break
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