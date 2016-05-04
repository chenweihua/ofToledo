# -*- coding: utf-8 -*-
"""Art forms."""
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .models import Portfolio, Art

class PortfolioForm(Form):
    """Portfolio form."""
    title = StringField('Portfolio Title', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField("Make new portfolio")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.portfolio = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(PortfolioForm, self).validate()
        if not initial_validation:
            return False

        return True
