#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, abort, Response
from flask_sqlalchemy import SQLAlchemy
from models import *
import logging
from logging import Formatter, FileHandler
from forms import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login',methods=['GET'])
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/login',methods=['POST'])
def login_POST():
    form = LoginForm(request.form)
    
    user=User.query.filter_by(name=form.name.data).first()
    if(user is None or (user.password!=form.password.data)):
        abort(403)  
        abort(Response('You are not allowed to access this resource'))
    else:
        return redirect(url_for('rdvs',userid=str(user.id)))
    
        
    
    
@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
# Error handlers.


@app.route('/register',methods=['GET'])
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/register',methods=['POST'])
def register_POST():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    if( password != confirm ):
        abort(403)
        return "password and confirmation don't match"
    else:
        try:
            user = User(name=name, email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('rdvs',userid=str(user.id)))
        except:
            
            abort(Response('cannot create user',409))


@app.route('/rdvs',methods=["GET"])
def rdvs():
    
    userid = request.args.get('userid')
    user=User.query.filter_by(id=userid).first()
    print(user.name)
    return render_template('layouts/rdv.html', user=user,form=RDVForm(request.form))

@app.route('/rdvs',methods=["POST"])
def rdvs_post():
    form = RDVForm(request.form)

    title = form.name.data
    time  = form.time.data
    nature = form.nature.data
    user_id = int(form.user.data)

    rdv = RDV(title=title,time=time,nature=nature,user_id=user_id)

    db.session.add(rdv)
    db.session.commit()

    user=User.query.filter_by(id=user_id).first()
    
    
    return render_template('layouts/rdv.html', user=user,form=form)




@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
