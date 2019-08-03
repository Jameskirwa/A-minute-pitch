from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User (UserMixin,db.Model):
    __tablename__ = 'user'

    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user',lazy = 'dynamic')
    comments = db.relationship('Comments',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
        

    def __repr__(self):
        return f'User {self.username}'



class Pitch(db.Model):
     __tablename__ = 'pitches'

     id = db.Column(db.Integer,primary_key = True)
     pitch  = db.Column(db.String(255))
     pitch_content = db.Column(db.String())
     pitch_category =  db.Column(db.String(255))
     users_id = db.Column(db.Integer,db.ForeignKey("user.id"))
     upvotes = db.Column(db.Integer)
     downvotes = db.Column(db.Integer)
     comments = db.relationship('Comments',backref =  'pitch_id',lazy = "dynamic")
     
     
     
     
     def save_pitch(self):
         db.session.add(self)
         db.session.commit()

     @classmethod
     def get_pitch(cls,id):
        pitch = Pitch.query.filter_by(id=id).first()
        return pitch
     
     @classmethod
     def get_pitches(cls,pitch_category):
        pitches = Pitch.query.filter_by(pitch_category=pitch_category).all()
        return pitches
         

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String())
    pitch = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch):
        comments = Comments.query.filter_by(pitch_id=pitch).all()
        return comments  
     
    

        

     
     
     
         

    