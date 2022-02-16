from flask_login import login_user, logout_user
from .import bp as app
from flask import render_template, redirect, url_for, request, flash
from app.blueprints.authentication.models import User

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

    
@app.route('/register')
def register():
    return render_template('authentication/register.html')

