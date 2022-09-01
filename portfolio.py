from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/admin_portpholio'
app.config['SQlALCHAMY_TRACK_NOTIFICATION'] = False
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def home():
   my_self = ABOUT_ME.query.filter_by().first()
   return render_template('/portfolio/index.html', my_self=my_self)


class ABOUT_ME(db.Model):
   about_id = db.Column(db.Integer(), primary_key=True)
   full_name = db.Column(db.String())
   email = db.Column(db.String())
   phone = db.Column(db.String())
   country = db.Column(db.String())
   city = db.Column(db.String())
   c_code = db.Column(db.String())
   z_code = db.Column(db.String())
   gender = db.Column(db.String())
   a_image = db.Column(db.String())
   a_desc = db.Column(db.String())

@app.route('/about')
def about():
   my_self = ABOUT_ME.query.filter_by().first()
   return render_template('/portfolio/about.html', my_self=my_self)

@app.route('/skills')
def skills():
   my_self = ABOUT_ME.query.filter_by().first()
   return render_template('/portfolio/skills.html', my_self=my_self)

class MY_TEAM(db.Model):
   team_id = db.Column(db.String(), primary_key=True)
   team_name = db.Column(db.String())
   team_lname = db.Column(db.String())
   team_email = db.Column(db.String())
   team_skills = db.Column(db.String())
   country = db.Column(db.String())
   gender = db.Column(db.String())
   team_image = db.Column(db.String())
   date = db.Column(db.String())


@app.route('/services')
def services():
   my_self = ABOUT_ME.query.filter_by().first()
   my_team = MY_TEAM.query.all()

   return render_template('/portfolio/services.html', my_self=my_self, my_team=my_team)


class ADD_PROJECT(db.Model):
   s_no = db.Column(db.Integer(), primary_key=True)
   project_name = db.Column(db.String())
   project_title = db.Column(db.String())
   project_desc = db.Column(db.String())
   project_img = db.Column(db.String())
   project_date = db.Column(db.String())

@app.route('/project')
def project():
   my_self = ABOUT_ME.query.filter_by().first()
   project = ADD_PROJECT.query.all()
   return render_template('/portfolio/project.html', my_self=my_self, my_project=project)

@app.route('/blog')
def blog():
   my_self = ABOUT_ME.query.filter_by().first()
   return render_template('/portfolio/blog.html', my_self=my_self)


class CLIENT(db.Model):
   client_id = db.Column(db.Integer(), primary_key=True)
   client_name = db.Column(db.String())
   client_email = db.Column(db.String())
   client_subject = db.Column(db.String())
   client_message = db.Column(db.String())
   date = db.Column(db.String())

@app.route('/contact', methods=['POST', 'GET'])
def contact():
   if request.method == 'POST':
      c_name = request.form.get('client_name')
      c_email = request.form.get('client_email')
      c_subject = request.form.get('client_subject')
      c_message = request.form.get('client_message')

      add_contact = CLIENT(client_name=c_name, client_email=c_email,
                           client_subject=c_subject, client_message=c_message,
                           date=datetime.now())
      db.session.add(add_contact)
      db.session.commit()
   my_self = ABOUT_ME.query.filter_by().first()
   return render_template('/portfolio/contact.html', my_self=my_self)


if __name__ == '__main__':
   app.run(port=5001,
           debug=True)