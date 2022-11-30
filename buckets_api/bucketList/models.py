
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class ExtraMin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model , ExtraMin):
    """This class represents the users table."""
    __tablename__ = 'users'
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    

        

class Bucketitems(db.Model , ExtraMin):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlist'
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    

    

