# lcdtradeins/decorators.py

from functools import wraps

from flask import current_app, request, session, flash, redirect, url_for, abort, jsonify
from flask.ext.login import current_user

from oftoledo.database import db


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('You must confirm your email first!', 'warning')
            return redirect(url_for('public.home'))
        return func(*args, **kwargs)

    return decorated_function

def check_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin is False:
            return abort(404)
        return func(*args, **kwargs)

    return decorated_function