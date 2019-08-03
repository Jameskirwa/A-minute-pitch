from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User, Pitch, Comments
from flask_login import login_required, current_user
from .forms import PitchForm, UpdateProfile, CommentsForm
from .. import db,photos


@main.route('/')
def index():
    '''
    function to display pitches
    '''
    #Getting pitches from different categories
    business_pitches = Pitch.get_pitches('business')
    science_pitches = Pitch.get_pitches('science')
    life_pitches = Pitch.get_pitches('life')

    
   
    return render_template('index.html', business = business_pitches, science = science_pitches, life = life_pitches )
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.post = form.post.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))

@main.route('/pitch/new/', methods = ['GET','POST'])
@login_required
def add_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = form.pitch.data
        category = form.category.data
        new_pitch = Pitch(pitch_content = pitch,pitch_category = category,user = current_user, upvotes=0, downvotes=0)
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'One Minute pitch'
    return render_template('add_pitch.html',title = title, pitch_form=form)

@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    

    if request.args.get("upvote"):
        pitch.upvotes += 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id)) 

    elif request.args.get("downvote"):
        pitch.downvotes+=1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentsForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comments(comment = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()
    comments = Comments.get_comments(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments)












       






  
