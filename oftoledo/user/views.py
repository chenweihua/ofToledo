# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user 
from oftoledo.database import db
from oftoledo.user.forms import UpdateInfo
from oftoledo.send_emails import send_confirm_email

# If you need a user confirmed before completing an action
# from oftoledo.decorators import check_confirmed

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

# =================================
# 			USER ROUTES
# =================================

@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))

@blueprint.route('/updateaccount', methods = ['POST'])
@login_required
def updateAccount():
	"""List members."""
	form = UpdateInfo()
	if request.method == 'POST':
	    if form.validate() == False:
	    	flash('Error. Pleae try again', 'danger')
	        return redirect(url_for('user.account'))
	    else:
	    	user = current_user
	    	user.full_name = form.full_name.data
	    	db.session.add(user)
	    	db.session.commit()
	        flash('Account Information Updated', 'success')
	        return redirect(url_for('user.account'))

@blueprint.route('/')
@login_required
def account():
	"""Show User Account Page."""
	form = UpdateInfo()
	return render_template('users/account.html', form = form)

@blueprint.route('/re-confirm/', methods = ['POST'])
@login_required
def reconfirmEmail():
    """Send user another confirm email if they didn't get the first"""
    user = current_user
    send_confirm_email(user)
    flash('Thank you, please check your email.', 'success')
    return redirect(url_for('public.home'))