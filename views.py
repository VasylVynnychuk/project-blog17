from app import app, db
from flask import render_template, flash
from models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for, request
from forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse


@app.route('/')
def index():
    # posts = Post.query.filter(Post.user_id == User.id)
    # users = User.query.filter(User.id == Post.user_id)
    users = User.query.all()
    posts = Post.query.all()
    return render_template('index.html', posts=posts, users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    if username == 'admin':
        return render_template('user.html')

    user = User.query.filter_by(username=username).first_or_404()
    user_id = User.query.filter_by(id=user.id).first()
    if user_id == current_user:
        posts = Post.query.filter(Post.user_id == user.id).all()
        return render_template('user.html', user=user, posts=posts)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('posts.index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
