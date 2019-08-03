from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required


class PitchForm(FlaskForm):

    pitch = TextAreaField('Pitch:',validators = [Required()])
    category = SelectField('Type',choices=[('business','Business pitch'),('science','Science pitch'),('life','Life pitch')],validators=[Required()])
    submit = SubmitField('Submit')
    
    
class UpdateProfile(FlaskForm):
    post = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentsForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[Required()])
    submit = SubmitField('Submit')