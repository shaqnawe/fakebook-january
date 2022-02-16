from flask_login import current_user, login_user, logout_user
from .import bp as app
from flask import render_template, redirect, url_for, request, flash
from app.blueprints.authentication.models import User
from app import db

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email.lower()).first()
        if user is None or not user.check_password(password):
            flash('Either that was an invalid password or username. Try again. ', 'danger')
            return redirect(request.referrer)
        flash('User has successfully logged in', 'success')
        login_user(user)
        return redirect(url_for('blog.home'))
    return render_template('authentication/login.html')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data.get('email')).first()
        if user is not None:
            flash('That user already exists', 'warning')
            return redirect(request.referrer)
        if data.get('password') != data.get('password2'):
            flash("Your passwords don't match", 'warning')
            return redirect(request.referrer)
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully', 'success')
        # automatically log in user on successful registration
        login_user(new_user)
        flash('User logged in successfully', 'success')
        return redirect(url_for('blog.home'))

    return render_template('authentication/register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out successfully', 'primary')
    return redirect(url_for('authentication.login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # print(request.form)
        # print(current_user)
        data = request.form

        user = User.query.get(current_user.id)
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')

        if (data.get('password') and data.get('password2')) and (data.get('password') == data.get('password2')):
            user.generate_password(data.get('password'))
        elif (data.get('password') or data.get('password2')):
            flash("Your passwords don't match", 'warning')
            return redirect(request.referrer)
        db.session.commit()
        flash('Your information has been updated', 'info')
        return redirect(request.referrer)
    context = {
        'posts': current_user.posts.all()
    }
    return render_template('authentication/profile.html', **context)