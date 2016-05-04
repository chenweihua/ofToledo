# -*- coding: utf-8 -*-
"""Art views."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user, logout_user 
from oftoledo.database import db
from oftoledo.art.forms import PortfolioForm
from oftoledo.art.models import Portfolio
from oftoledo.user.models import User

# If you need a user confirmed before completing an action
# from oftoledo.decorators import check_confirmed

blueprint = Blueprint('art', __name__, static_folder='../static')


@blueprint.route('/<username>', methods = ['GET', 'POST'])
def viewUser(username):
	user = User.query.filter_by(username = username).first()
	"""Abort if user not found"""
	if not user:
		return abort(404)
	portfolios = Portfolio.query.filter_by(user_id = user.id).all()
	return render_template('art/user.html', user = user, portfolios = portfolios)


# =================================
# 			PORTFOLIO ROUTES
# =================================

@blueprint.route('/newportfolio', methods = ['GET', 'POST'])
@login_required
def newPortfolio():
	"""Make a new portfolio"""
	form = PortfolioForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('Error. Pleae try again', 'danger')
			return redirect(url_for('art.newPortfolio'))
		else:
			"""Create Portfolio if form is valid"""
			Portfolio.create(title=form.title.data,
				description=form.description.data,
				user_id = current_user.id)
			flash('New Portfolio Made', 'success')
			return redirect(url_for('art.viewUser'))
	return render_template('art/newportfolio.html', form = form)