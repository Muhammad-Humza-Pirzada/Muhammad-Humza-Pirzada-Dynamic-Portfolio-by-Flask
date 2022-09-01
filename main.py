from flask import Flask, render_template, request, current_app, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/admin_portpholio'
app.config['SQlALCHAMY_TRACK_NOTIFICATION'] = False
db = SQLAlchemy(app)
app.secret_key = 'login'

def save_images(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, 'static/assets/img', photo_name)
    photo.save(file_path)
    return photo_name

"""def about_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extention = os.path.splitext(photo.filename)
    about_photo = hash_photo + file_extention
    file_path = os.path.join(current_app.root_path, '../dynamic_portfolio/static/assets/images', about_photo)
    photo.save(file_path)
    return about_photo"""


class REGISTRATION(db.Model):
    u_id = db.Column(db.Integer(), primary_key=True)
    u_fname = db.Column(db.String(25))
    u_lname = db.Column(db.String(25))
    u_email = db.Column(db.String(25))
    u_pass = db.Column(db.String(25))
    u_image = db.Column(db.String(50))
    date = db.Column(db.String())



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        u_fname = request.form.get('f_name')
        u_lname = request.form.get('l_name')
        u_email = request.form.get('u_email')
        u_pass = request.form.get('u_pass')
        u_img = save_images(request.files.get('u_img'))

        add_registration = REGISTRATION(u_fname=u_fname, u_lname=u_lname, u_email=u_email, u_pass=u_pass, u_image=u_img, date=datetime.now())
        db.session.add(add_registration)
        db.session.commit()
    return render_template('registration.html')


@app.route('/', methods=['POST', 'GET'])
def login():
    form_data = ABOUT_ME.query.all()
    for data in form_data:
        email = data.email
        password = data.password
    if request.method == 'POST':
        l_email = request.form.get('l_email')
        l_pass = request.form.get('l_pass')

        if l_email == "" or l_pass == "":
            enter_field = "Please Enter All Field"
            return render_template('/admin/login.html', enter_field=enter_field,
                                                        image=data.a_image)
        
        elif l_email is not data.email and password is not data.password:
            valid_ep = "Please Enter Valid Email and Password"
            return render_template('/admin/login.html', valid_ep=valid_ep,
                                                        image=data.a_image)

        else:
            if l_email == email and l_pass == password:
                session['email'] = email
                session['full_name'] = data.full_name
                session['a_image'] = data.a_image
                flash("You are Logged In.....")

                return render_template('/admin/index.html', email=email,
                                                            full_name=data.full_name,
                                                            a_image=data.a_image)
            else:
                msg = 'invalid user email or password'
                return render_template('/admin/login.html', msg=msg, image=data.a_image)

    return render_template('/admin/login.html', image=data.a_image)

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash("You have Logged Out.....")
    return redirect(url_for('login'))



@app.route("/home")
def home():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
    else:
        return redirect(url_for('login'))
    return render_template('/admin/index.html', email=email,full_name=full_name, a_image=a_image)


"""About me start"""
class ABOUT_ME(db.Model):
    about_id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    phone = db.Column(db.String())
    country = db.Column(db.String())
    city = db.Column(db.String())
    c_code = db.Column(db.String())
    z_code = db.Column(db.String())
    gender = db.Column(db.String())
    a_image = db.Column(db.String())
    a_desc = db.Column(db.String())

@app.route('/about_me', methods=['POST', 'GET'])
def about_me():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        u_about_me = ABOUT_ME.query.filter_by().first()
        if request.method == 'POST':
            if request.files.get('about_img'):
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/assets/img', + u_about_me.a_image))
                    u_about_me.a_image = save_images(request.files.get('about_img'))
                except:
                    u_about_me.a_image = save_images(request.files.get('about_img'))
            u_about_me.full_name = request.form['f_name']
            u_about_me.email = request.form['email']
            u_about_me.password = request.form['pass']
            u_about_me.phone = request.form['p_number']
            u_about_me.country = request.form['country']
            u_about_me.city = request.form['city']
            u_about_me.c_code = request.form['c_code']
            u_about_me.z_code = request.form['z_code']
            u_about_me.gender = request.form['gender']
            u_about_me.a_desc = request.form['about_desc']
            db.session.add(u_about_me)
            db.session.commit()
            flash("You Have Successfully Updated")
            return redirect(url_for('about_me'))

    else:
        return redirect(url_for('login'))
    return render_template('/admin/about_me.html', about_me=u_about_me, full_name=full_name, email=email, a_image=a_image)
"""about me end"""


"""this is ssection add project it is started there """

class ADD_PROJECT(db.Model):
    s_no = db.Column(db.Integer(), primary_key = True)
    project_name = db.Column(db.String())
    project_title = db.Column(db.String())
    project_desc = db.Column(db.String())
    project_img = db.Column(db.String())
    project_date = db.Column(db.String())


@app.route("/add_project", methods=['POST', 'GET'])
def add_project():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        if request.method == 'POST':
            p_name = request.form.get('p_name')
            p_title = request.form.get('p_title')
            p_description = request.form.get('p_description')
            image = save_images(request.files.get('p_img'))
            if p_name == "" or p_title == "" or p_description == "" or image == "":
                flash("Plese Fill Feild...")
            else:
                add_post = ADD_PROJECT(project_name=p_name, project_title=p_title,
                                       project_desc=p_description, project_img=image)
                db.session.add(add_post)
                db.session.commit()
                flash("Your Project has been added...")
                return redirect(url_for('add_project'))
    else:
        return redirect(url_for('login'))

    return render_template('/admin/add_project.html', email=email,full_name=full_name, a_image=a_image)

"""this is ssection add project it is ended there"""

"""this is display project section start"""

@app.route("/my_project")
def my_project():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        my_items = ADD_PROJECT.query.all()
    else:
        return redirect(url_for('login'))
    return render_template('/admin/my_project.html', my_items=my_items, email=email,
                                                full_name=full_name, a_image=a_image)

"""this is display project section end"""


"""this is updated section"""
@app.route('/update_project/<int:s_no>', methods=['POST', 'GET'])
def update_project(s_no):
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        u_project = ADD_PROJECT.query.filter_by(s_no=s_no).first()
        if request.method == 'POST':
            if request.files.get('p_img'):
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/assets/img/', + u_project.project_img))
                    u_project.project_img =save_images(request.files.get('p_img'))
                except:
                    u_project.project_img = save_images(request.files.get('p_img'))

            u_project.project_name = request.form['p_name']
            u_project.project_title = request.form['p_title']
            u_project.project_desc = request.form['p_description']

            db.session.add(u_project)
            db.session.commit()
            flash("Your Project has been Updated....")
            return redirect(url_for('my_project'))
    else:
        return redirect(url_for('login'))

    return render_template('/admin/update_project.html', u_project=u_project, email=email,
                                                        full_name=full_name , a_image=a_image)

"""this is updated section end"""


class MY_TEAM(db.Model):
    team_id = db.Column(db.Integer(), primary_key=True)
    team_name = db.Column(db.String())
    team_lname = db.Column(db.String())
    team_email = db.Column(db.String())
    team_skills = db.Column(db.String())
    country = db.Column(db.String())
    gender = db.Column(db.String())
    team_image = db.Column(db.String())
    date = db.Column(db.String())
"""this is my team section"""

@app.route("/my_team", methods=['POST', 'GET'])
def my_team():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        my_teams = MY_TEAM.query.all()
        if request.method == "POST":
            t_name = request.form.get("team_name")
            t_lname = request.form.get("team_lname")
            t_email = request.form.get("team_email")
            t_skills = request.form.get("team_skills")
            t_country = request.form.get("country")
            t_gender = request.form.get("gender")

            if t_name == "" or t_lname == "" or t_email == "" or t_skills == "" or t_country == "" or t_gender == "":
                fill_field = "Please Fill All Field"
                return render_template('/admin/my_team.html', fill_f=fill_field, my_teams=my_teams, email=email, full_name=full_name, a_image=a_image)

            else:
                try:
                    image = save_images(request.files.get('team_image'))
                except:
                    image = save_images(request.files.get('team_image'))

                add_team_member = MY_TEAM(team_name=t_name, team_lname=t_lname, team_email=t_email,
                                          team_skills=t_skills, country=t_country, gender=t_gender,
                                          team_image=image, date=datetime.now())

                db.session.add(add_team_member)
                db.session.commit()
                flash("Your Team Member Has Been Added.....")
                return redirect(url_for('my_team'))
    else:
        return redirect(url_for('login'))

    return render_template('/admin/my_team.html', my_teams=my_teams, email=email, full_name=full_name, a_image=a_image)

"""this is my team section end"""

"""this is deleted section"""
@app.route('/delete_project/<int:s_no>')
def delete_project(s_no):
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        d_project = ADD_PROJECT.query.filter_by(s_no=s_no).first()
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/assets/img/', + d_project.project_img))
            db.session.delete(d_project)
        except:
            db.session.delete(d_project)
        db.session.commit()
    else:
        return redirect(url_for('login'))
    flash("Your Project has been deleted.....")
    return redirect(url_for('my_project'))

"""this is deleted section end"""

"""update team start"""
@app.route("/update_team/<int:team_id>", methods=["POST", "GET"])
def update_team(team_id):
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        u_team = MY_TEAM.query.filter_by(team_id=team_id).first()
        if request.method == 'POST':
            if request.files.get("team_image"):
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/assets/img', + u_team.team_image))
                    u_team.team_image = save_images(request.files.get('team_image'))
                except:
                    u_team.team_image = save_images(request.files.get('team_image'))

            u_team.team_name = request.form['team_name']
            u_team.team_lname = request.form['team_lname']
            u_team.team_email = request.form['team_email']
            u_team.team_skills = request.form['team_skills']
            u_team.country = request.form['country']
            u_team.gender = request.form['gender']

            db.session.add(u_team)
            db.session.commit()
            flash("Your Team Member Has Been Updated")
            return redirect(url_for('my_team'))
    else:
        return redirect(url_for('login'))

    return render_template('/admin/update_team.html', u_team=u_team, email=email, full_name=full_name, a_image=a_image)

"""update team end"""

"""delete team start"""
@app.route("/delete_team/<int:team_id>", methods=["POST", "GET"])
def delete_team(team_id):
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        d_team = MY_TEAM.query.filter_by(team_id=team_id).first()
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/assets/img', + d_team.team_image))
            db.session.delete(d_team)
        except:
            db.session.delete(d_team)
        db.session.commit()
    else:
        return redirect(url_for('login'))
    flash("Your Team Has been Deleted...")
    return redirect(url_for('my_team'))
"""delete team end"""

"""client start"""
class CLIENT(db.Model):
   client_id = db.Column(db.Integer(), primary_key=True)
   client_name = db.Column(db.String())
   client_email = db.Column(db.String())
   client_subject = db.Column(db.String())
   client_message = db.Column(db.String())
   date = db.Column(db.String())

@app.route("/client")
def client():
    if 'email' in session and 'full_name' in session and 'a_image' in session:
        email = session['email']
        full_name = session['full_name']
        a_image = session['a_image']
        my_client = CLIENT.query.all()
    else:
        return redirect(url_for('login'))

    return render_template('/admin/client.html', email=email, full_name=full_name, a_image=a_image, client=my_client)

"""client end"""

if __name__ == "__main__":
    app.run(debug=True)

    """f_name = request.form.get('f_name')
      email = request.form.get('email')
      phone = request.form.get('p_number')
      country = request.form.get('country')
      city = request.form.get('city')
      c_code = request.form.get('c_code')
      z_code = request.form.get('z_code')
      gender = request.form.get('gender')
      a_img = save_images(request.files.get('about_img'))
      a_desc = request.form.get('about_desc')"""