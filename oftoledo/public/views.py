# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request
from flask import url_for, abort, session, jsonify
from flask_login import login_required, login_user, current_user

from oftoledo.extensions import login_manager, bcrypt
from oftoledo.public.forms import LoginForm, ContactForm, ForgotPassword, ResetPassword
from oftoledo.user.forms import RegisterForm
from oftoledo.user.models import User
from oftoledo.utils import flash_errors

from oftoledo.database import db

# Validate email and reset password tokens
from oftoledo.token import confirm_token

# Send password, confirmation, and contact emails
from oftoledo.send_emails import send_confirm_email, send_contact_email, send_password_reset_email

blueprint = Blueprint('public', __name__, static_folder='../static')


""" Might be able to delete this...?"""
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page."""
    return render_template('public/index.html')

@blueprint.route('/about/')
def about():
    """Render the about page page."""
    return render_template('public/about.html')

@blueprint.route('/contact-us/', methods=['GET', 'POST'])
def contact():
    """Contact Us page."""
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('public/contact.html', form = form)
        else:
            name = form.name.data
            email = form.email.data
            message = form.message.data
            send_contact_email(name, email, message)
            flash('Contact form submited. We will be in touch with you as soon as possible', 'success')
            return render_template('public/contact.html', form = form)
    return render_template('public/contact.html', form = form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        
        """Create User if form is valid"""
        User.create(email=form.email.data,
            full_name=form.full_name.data,
            username=form.username.data,
            password=form.password.data, 
            active=True, confirmed=False)
        
        """Find user, login, send a confirm email, redirect to home with flashed message"""
        user = User.query.filter_by(email = form.email.data).first()
        login_user(user)
        send_confirm_email(user)
        flash('Thank you for registering. Please confirm your email.', 'success')
        return redirect(url_for('public.home'))

    else:
        """Send error message if form is not valid"""
        flash_errors(form)

    """Render html if not a POST request"""
    return render_template('public/register.html', form=form)

# Email confirmation
@blueprint.route('/confirm/<token>')
def confirmEmail(token):
    """ confirm users email """
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('You have confirmed your account. Thanks!', 'success')
        return redirect(url_for('public.home'))
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('public.home'))


@blueprint.route('/login/', methods=['GET', 'POST'])
def login_page():
    """Login page."""
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            return redirect(url_for('public.home'))
        else:
            flash("We didn't recognize that, please try again", 'danger')
            return render_template('public/login.html', form=form)
    else:
        return render_template('public/login.html', form=form)


@blueprint.route('/forgot-password/', methods=['GET', 'POST'])
def forgotPassword():
    """Password page, user requests a password reset email"""
    form = ForgotPassword()
    if request.method == 'POST':
        if form.validate() == True:

            user = User.query.filter_by(email = form.email.data).first()
            
            # Alert user that the email wasn't found
            if not user:
                flash("We didn't find an account associated with that email :(", 'danger')
                return render_template('public/forgotpassword.html', form = form)

            send_password_reset_email(user)

            flash('Password reset. Please check your email', 'success')
            return redirect(url_for('public.home'))

        # Alert the user that the form was invalid
        else:
            flash('There was something wrong with the form, please try again', 'danger')
            return render_template('public/forgotpassword.html', form = form)
    
    # Render template for GET request
    else:
        return render_template('public/forgotpassword.html', form = form)



@blueprint.route('/password-reset/<token>/', methods=['GET', 'POST'])
def resetPassword(token):
    """Reset Password page, user resets password with confirm email"""
    try:
        email = confirm_token(token)
    except:
        return abort(404)

    form = ResetPassword()
    if request.method == 'POST':
        if form.validate() == True:
            user = db.session.query(User).filter_by(email = email).first()
            
            # get password from form and encrypt
            password = form.password.data
            password = bcrypt.generate_password_hash(password)

            #set new encrypted password to user
            user.password = password

            db.session.add(user)
            db.session.commit()

            flash('Password Reset', 'success')
            return redirect(url_for('public.login_page'))
        else:
            flash('Error, please try again', 'danger')
            return render_template('public/resetpassword.html', form = form, token=token)
    
    return render_template('public/resetpassword.html', form = form, token=token)