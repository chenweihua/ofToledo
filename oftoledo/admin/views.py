# -*- coding: utf-8 -*-
"""Admin views."""
from flask import Blueprint, render_template
from flask_login import login_required
from oftoledo.decorators import check_admin
from oftoledo.user.models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admin', static_folder='../static')

# =================================
# 			ADMIN ROUTES
# =================================

@blueprint.route('/')
@login_required
@check_admin
def adminhome():
	"""Admin Home"""
	return render_template('admins/home.html')

@blueprint.route('/user/<int:user_id>/')
@login_required
@check_admin
def viewCustomer(user_id):
	"""View a Users Account"""
	user = User.query.filter_by(id = user_id).first()
	return render_template('admins/user.html', user = user)