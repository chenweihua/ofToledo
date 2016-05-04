from oftoledo.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Portfolio(SurrogatePK, Model):
    """A portfolio for a user."""

    __tablename__ = 'portfolios'
    title = Column(db.String(80), nullable=True)
    description = Column(db.String(), nullable=True)
    cover_image = Column(db.String(80), nullable=True)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='portfolios')

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

class Art(SurrogatePK, Model):
    """Art in a users portfolio."""

    __tablename__ = 'arts'
    title = Column(db.String(80), nullable=True)
    description = Column(db.String(), nullable=True)
    image = Column(db.String(), nullable=False)
    portfolio_id = reference_col('portfolios', nullable=True)
    portfolio = relationship('Portfolio', backref='arts')

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)