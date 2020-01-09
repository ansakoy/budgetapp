from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from budget_app.forms import RegistrationForm, LoginForm, UpdateAccountForm

from budget_app import app, bcrypt, db
from budget_app.models import User, Expense, Category

EXPENSES = [
    {
        'category': 'Food',
        'comment': '',
        'date': '2020-01-08',
        'price': 100.0
    },
    {
        'category': 'Internet',
        'comment': '2kom',
        'date': '2020-01-08',
        'price': 390.0
    },
    {
        'category': 'Other',
        'comment': 'палеонтологический музей',
        'date': '2020-01-08',
        'price': 600.0
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/expenses')
@login_required
def expenses():
    return render_template('expenses.html', expenses=EXPENSES, title='Expenses')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('expenses'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_pw,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('expenses'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('expenses'))
        else:
            flash('Login failed. Check email or password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Changes submitted', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=img_file,
                           form=form)