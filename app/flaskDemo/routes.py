import os
import secrets
import re
import json
import requests
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flaskDemo import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, Permission, RoleNeed, identity_loaded
from flaskDemo.models import role,employee, unit,building,work,maintenance,apartmentrehab,others,landscaping,pestcontrol
from flaskDemo.forms import ChangeEmailForm,ChangePhoneForm,ChangePasswordForm,ForgetForm,StartForm,BuildingForm,RegistrationForm,LoginForm,MaintenanceForm,ApartmentRehabForm,LandscapingForm,PestControlForm,OtherForm
from datetime import datetime, timedelta
from sqlalchemy import or_, update, and_

import yaml
import pandas as pd
from numpy.random import randint
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import flaskDemo.authorize as authorize


import httplib2
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = authorize.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)


#admin_permission = Permission(RoleNeed(2))

maintainence_permission = Permission(RoleNeed(1))
frontdesk_permission = Permission(RoleNeed(2))

#Configure db
#Methods created 
# ---------------------------------------------------------------------------------------------------
   
#Send email
def emailsend(subject,emailsender,text):
    gmail_user = "goodnewspartners1@gmail.com"
    gmail_password = "goodnews24"
  
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = gmail_user
    message["To"] = emailsender
    message.attach(MIMEText(text,"plain"))
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, emailsender, message.as_string())





#def limit():
#    code = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
#    if code:
#        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
#        if((datetime.now()-code.startTimeAuto)>limit) or ((datetime.now()-code.startTimeManual)>limit):
#            code.endTimeAuto = datetime(9999,1,1,1,1,1)
#            code.endTimeManual = datetime(9999,1,1,1,1,1)
#            db.session.commit()
#            flash("Start time exceeds 24 hours, please contact Ken/Brandon to adjust previous work","danger")

@app.route("/")



##database manipulation
# ---------------------------------------------------------------------------------------------------

#@app.route("/data", methods=['GET', 'POST'])
#def data():
#
#    Building = building(buildingName='Lloyd',buildingAddress='7625-29 N. Bosworth Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building1 = building(buildingName='New Life',buildingAddress='7632-34 N. Paulina Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building2 = building(buildingName='Ministry Center',buildingAddress='7630 N. Paulina Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building3 = building(buildingName='JCP',buildingAddress='1546 W. Jonquil Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building4 = building(buildingName='No Bos Condo',buildingAddress='7645-47 N. Bosworth Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building5 = building(buildingName='Fargo',buildingAddress='1449 W. Fargo Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building6 = building(buildingName='Esperanza',buildingAddress='1556-58 W. Jonquil Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building7 = building(buildingName='Phoenix 1',buildingAddress='7729-31 N. Hermitage Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building8 = building(buildingName='Phoenix 2',buildingAddress='7727 N. Hermitage Avenue',postalCode =60626 ,numberOfrooms= 200)
#    Building9 = building(buildingName='Jonquil',buildingAddress='1600 W. Jonquil Terrace 7700 N. Ashland',postalCode =60626 ,numberOfrooms= 200)
#    Role1 = role(roleName = "Maintenance")
#    Role2 = role(roleName = "Front Desk")
#    Role3 = role(roleName = "admin")
#    db.session.add(Building)
#    db.session.add(Building1)
#    db.session.add(Building2)
#    db.session.add(Building3)
#    db.session.add(Building4)
#    db.session.add(Building5)
#    db.session.add(Building6)
#    db.session.add(Building7)
#    db.session.add(Building8)
#    db.session.add(Building9)
#    db.session.add(Role1)
#    db.session.add(Role2)
#    db.session.add(Role3)
#    
#    
#    db.session.commit()
#    hashed_password = bcrypt.generate_password_hash("gnp7737644998").decode('utf-8')
#    adminuser = employee(firstName="Good News",lastName="Partners",username="goodnews24",password=hashed_password,phoneNumber = "7737644998",email = "Brandon@goodnewspartners.org",roleID = 3 )   
#    db.session.add(adminuser)
#    db.session.commit()
#    
#    df = pd.read_csv('Unit Survey1.csv')
#    for index, row in df.iterrows():
#        Building = building.query.filter(building.buildingName == row['propertyname']).first()
#        print(row['propertyname'])
#        Unit = unit(buildingID = Building.buildingID,unitName= row['unit'])
#        db.session.add(Unit)
#        db.session.commit()
#
#  
#    return redirect(url_for('home'))   

#


#Employee manipulation 
# ---------------------------------------------------------------------------------------------------


@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('front'))
    return render_template('home.html')



@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('home'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('choices'))
    form = LoginForm()
    if form.validate_on_submit():
        Employee = employee.query.filter_by(username=form.username.data).first()
        if Employee and bcrypt.check_password_hash(Employee.password, form.password.data):
            login_user(Employee, remember=form.remember.data)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(Employee.employeeID))
            
            return redirect(url_for('front'))
        else:
            flash('Login Unsuccessful. Please confirm password', 'danger')
    return render_template('signin.html', form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('choices'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        roleID = role.query.filter_by(roleName = form.position.data).first()
        Employee = employee(firstName=form.firstName.data,lastName=form.lastName.data,username=form.username.data,password=hashed_password,phoneNumber = form.phone.data,email = form.email.data,roleID = roleID.roleID)
        db.session.add(Employee)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route("/forgotpass", methods=['GET', 'POST'])
def forgotpass():
    form = ForgetForm()
    if form.validate_on_submit():
        num = randint(100000, 999999)
        hashed_password = bcrypt.generate_password_hash(str(num)).decode('utf-8')
        Employee = employee.query.filter_by(email=form.email.data).first()
        Employee.password = hashed_password
        print(num)
        db.session.commit()
        try:
            text = ("Hello there,\n Here is your temporary password: \n"+ str(num) +"\n"+
          "Please sign in using this temporary password, and modify your password in Manage Account")
            emailsend("Good News Partner - Temporary Password",form.email.data,text)
            flash("Temporary Password Sent! Please check your email","success")
            return redirect(url_for('login'))
        except:
            flash("Not Successful in sending link","danger")
    return render_template('forgot.html',form=form)


@app.route("/forgotusername", methods=['GET', 'POST'])
def forgotusername():
    form = ForgetForm()
    if form.validate_on_submit():
        Employee = employee.query.filter_by(email=form.email.data).first()
        try:
            text = ("Hello there,\n Here is your username: \n"+ Employee.username +"\n"+
          "Please sign in using this username")
            emailsend("Good News Partner - Username Retrieval",form.email.data,text)
            flash("Username Sent! Please check your email","success")
            return redirect(url_for('login'))
        except:
            flash("Not Successful in sending link","danger")
    return render_template('forgot.html',form=form)


#Manage Account
# ---------------------------------------------------------------------------------------------------
    
@app.route("/manageacc", methods=['GET', 'POST'])
@login_required
def manageacc():
    return render_template('manageacc.html')  



@app.route("/changepass", methods=['GET', 'POST'])
@login_required
def changepass():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            Employee = employee.query.filter_by(employeeID = current_user.employeeID).first()
            if Employee and bcrypt.check_password_hash(Employee.password, form.oldpassword.data):
                hashed_password = bcrypt.generate_password_hash(form.newpassword.data).decode('utf-8')
                Employee.password = hashed_password
                db.session.commit()
                flash("Password modified!","success") #why flash does not work?
                return redirect(url_for('manageacc'))
        except:
            flash("Password change not successful","danger")
    return render_template("changepass.html",form=form)
        

@app.route("/changeemail", methods=['GET', 'POST'])
@login_required
def changeemail():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        try:
            Employee = employee.query.filter_by(employeeID = current_user.employeeID).first()
            Employee.email = form.newemail.data
            db.session.commit()
            flash("Email modified!","success") #why flash does not work?
            return redirect(url_for('manageacc'))
        except:
            flash("Email change not successful","danger")
    return render_template("changeemail.html",form=form)


@app.route("/changephone", methods=['GET', 'POST'])
@login_required
def changephone():
    form = ChangePhoneForm()
    if form.validate_on_submit():
        try:
            Employee = employee.query.filter_by(employeeID = current_user.employeeID).first()
            Employee.phoneNumber = form.newphone.data
            db.session.commit()
            flash("Phone number modified!","success") 
            return redirect(url_for('manageacc'))
        except:
            flash("Email change not successful","danger")
    return render_template("changephone.html",form=form)

#frontpage form
# ---------------------------------------------------------------------------------------------------


@app.route("/front", methods=['GET', 'POST'])
@login_required
def front(): #render frontpage buttons
    Employee = employee.query.filter_by(employeeID = current_user.employeeID).first()
    if Employee.roleID == 1:
        return render_template('frontpage-maintainence.html')
    elif Employee.roleID == 2:
        return render_template('frontpage-frontdesk.html')


#frontdesk app form
# ---------------------------------------------------------------------------------------------------

@app.route("/startstop_F", methods=['GET', 'POST'])
@login_required #render start and stop buttons
@frontdesk_permission.require(http_exception=403)
def startstop_frontdesk():       
    return render_template('startstop_frontdesk.html')


@app.route("/start_F", methods=['GET', 'POST'])
@login_required #render start and stop buttons
@frontdesk_permission.require(http_exception=403)
def start_frontdesk():
    code = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
    if code:
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if((datetime.now()-code.startTimeAuto)>limit):
            code.endTimeAuto = datetime(9999,1,1,1,1,1)
            code.endTimeManual = datetime(9999,1,1,1,1,1)
            db.session.commit()
            flash("Start time exceeds 24 hours, please contact Ken/Brandon to adjust previous work","danger")
            return render_template('startstop_frontdesk.html')
        else:
            flash("You have started already, please press stop to finish current work","danger")
            return redirect(url_for('startstop_frontdesk'))
    
    Building = building.query.filter(building.buildingName =="Jonquil").first() 
    Unit = unit.query.filter(unit.buildingID ==Building.buildingID ,unit.unitName == "Others").first()
    numid = "FDESK10000"
    fdnum = work.query.filter(work.workType == "frontdesk").order_by(work.workOrdernumber.desc()).first()
    if fdnum != None:
        numfd = int( fdnum.workOrdernumber[5:] ) +1
        numid = "FDESK"+ str(numfd)
    Work = work(employeeID = current_user.employeeID,workType = "frontdesk",buildingID =Building.buildingID , unitID = Unit.unitID,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = datetime.now(), endTimeManual=None)
    db.session.add(Work)
    db.session.commit()
    flash("successfully started this shift!","success")
    return redirect(url_for('startstop_frontdesk'))
   
    
@app.route("/stop_F", methods=['GET', 'POST'])
@login_required #render start and stop buttons
@frontdesk_permission.require(http_exception=403)
def stop_frontdesk():
    Work = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
    if Work == None:
        flash("No work have been started, please start a new session","danger")
        return redirect(url_for('startstop_frontdesk'))
    code = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
    if code:
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if((datetime.now()-code.startTimeAuto)>limit) or ((datetime.now()-code.startTimeManual)>limit):
            code.endTimeAuto = datetime(9999,1,1,1,1,1)
            code.endTimeManual = datetime(9999,1,1,1,1,1)
            db.session.commit()
            flash("Start time exceeds 24 hours, please contact Ken/Brandon to adjust previous work","danger")
            return render_template('startstop_frontdesk.html')
    Work.endTimeManual=datetime.now()
    Work.endTimeAuto=datetime.now()
    db.session.commit()
    logout_user()
    identity_changed.send(current_app._get_current_object(),identity=AnonymousIdentity())
    flash("successfully stopped this shift!","success")
    
    return redirect(url_for('home'))
     
#maintenence app form
# ---------------------------------------------------------------------------------------------------

@app.route("/choices", methods=['GET', 'POST'])
@maintainence_permission.require(http_exception=403)
@login_required
def choices(): #render worktype buttons
    return render_template('choices.html')




@app.route("/startstop/<string:worktype>", methods=['GET', 'POST'])
@login_required #render start and stop buttons
@maintainence_permission.require(http_exception=403)
def startstop(worktype):       
    return render_template('startstop.html',worktype = worktype)


@app.route("/building/<string:worktype>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def buildingchoice(worktype):
    code = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
    if code:
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if((datetime.now()-code.startTimeAuto)>limit) or ((datetime.now()-code.startTimeManual)>limit):
            code.endTimeAuto = datetime(9999,1,1,1,1,1)
            code.endTimeManual = datetime(9999,1,1,1,1,1)
            db.session.commit()
            flash("Start time exceeds 24 hours, please contact Ken/Brandon to adjust previous work","danger")
            return render_template('choices.html')
        else:
            flash("There is still ongoing work, please stop your current work before proceeding","danger")
            return redirect(url_for('stop',worktype=code.workType))
    Building= building.query.order_by(building.buildingName.asc()).all()
    buildingList = [(b.buildingID,b.buildingName) for b in Building]
    form = BuildingForm()
    form.buildingName.choices = buildingList
    if form.validate_on_submit():
        return redirect(url_for('start',worktype=worktype,buildingname=form.buildingName.data))
    return render_template('buildingchoice.html',form=form)




@app.route("/start/<string:worktype>/<string:buildingname>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def start(worktype,buildingname):
    if worktype=="maintainence":
        Units = unit.query.filter(unit.buildingID == buildingname)
        unitList = [(u.unitID, u.unitName) for u in Units]  #which worktype needs unitid????
        form = StartForm()
        form.unitName.choices = unitList
        if form.validate_on_submit():
                numid = "MAINT10000"
                maintnum = work.query.filter(work.workType == "maintainence").order_by(work.workOrdernumber.desc()).first()
                #print(maintnum)
                if maintnum != None:
                    nummaint = int( maintnum.workOrdernumber[5:] ) +1
                    numid = "MAINT"+ str(nummaint)
                Work = work(employeeID = current_user.employeeID,workType = worktype,buildingID =buildingname , unitID = form.unitName.data,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = form.startTime.data, endTimeManual=None)
                db.session.add(Work)
                db.session.commit()
                flash("Your Work Order Number is "+str(numid),"success")
                return redirect(url_for('stop',worktype=worktype))
        return render_template('start.html',form=form)
    


    elif worktype=="apartmentrehab":
        Units = unit.query.filter(unit.buildingID == buildingname)
        unitList = [(u.unitID, u.unitName) for u in Units]  #which worktype needs unitid????
        form = StartForm()
        form.unitName.choices = unitList
        if form.validate_on_submit():
                numid = "REHAB10000"
                rehabnum = work.query.filter(work.workType == "apartmentrehab").order_by(work.workOrdernumber.desc()).first()
                #print(maintnum)
                if rehabnum != None:
                    nummaint = int( rehabnum.workOrdernumber[5:] ) +1
                    numid = "REHAB"+ str(nummaint)
                Work = work(employeeID = current_user.employeeID,workType = worktype,buildingID =buildingname , unitID = form.unitName.data,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = form.startTime.data, endTimeManual=None)
                db.session.add(Work)
                db.session.commit()
                flash("Your Work Order Number is "+str(numid),"success")
                return redirect(url_for('stop',worktype=worktype))
        return render_template('start.html',form=form)    
    
    
    
    elif worktype=="landscaping":
        Units = unit.query.filter(unit.buildingID == buildingname,unit.unitName =='other')
        unitList = [(u.unitID, u.unitName) for u in Units]  
        form = StartForm()
        form.unitName.choices = unitList
        if form.validate_on_submit():
                numid = "LAND10000"
                landnum = work.query.filter(work.workType == "landscaping").order_by(work.workOrdernumber.desc()).first()
                #print(maintnum)
                if landnum != None:
                    numland = int( landnum.workOrdernumber[4:] ) +1
                    numid = "LAND"+ str(numland)
                Work = work(employeeID = current_user.employeeID,workType = worktype,buildingID =buildingname , unitID = form.unitName.data,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = form.startTime.data, endTimeManual=None)
                db.session.add(Work)
                db.session.commit()
                flash("Your Work Order Number is "+str(numid),"success")
                return redirect(url_for('stop',worktype=worktype))
        return render_template('start.html',form=form)
    
    
    
    elif worktype=="pestcontrol":
        Units = unit.query.filter(unit.buildingID == buildingname)
        unitList = [(u.unitID, u.unitName) for u in Units]  #which worktype needs unitid????
        form = StartForm()
        form.unitName.choices = unitList
        if form.validate_on_submit():
                numid = "PEST10000"
                pestnum = work.query.filter(work.workType == "pestcontrol").order_by(work.workOrdernumber.desc()).first()
                if pestnum != None:
                    numpest = int( pestnum.workOrdernumber[4:] ) +1
                    numid = "PEST"+ str(numpest)
                Work = work(employeeID = current_user.employeeID,workType = worktype,buildingID =buildingname , unitID = form.unitName.data,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = form.startTime.data, endTimeManual=None)
                db.session.add(Work)
                db.session.commit()
                flash("Your Work Order Number is "+str(numid),"success")
                return redirect(url_for('stop',worktype=worktype))
        return render_template('start.html',form=form)    
    
    
    
    
    elif worktype=="others":
        Units = unit.query.filter(unit.buildingID == buildingname)
        unitList = [(u.unitID, u.unitName) for u in Units]  #which worktype needs unitid????
        form = StartForm()
        form.unitName.choices = unitList
        if form.validate_on_submit():
                numid = "OTHR10000"
                othnum = work.query.filter(work.workType == "others").order_by(work.workOrdernumber.desc()).first()
                if othnum != None:
                    numoth = int( othnum.workOrdernumber[4:] ) +1
                    numid = "OTHR"+ str(numoth)
                Work = work(employeeID = current_user.employeeID,workType = worktype,buildingID =buildingname , unitID = form.unitName.data,workOrdernumber=numid,startTimeAuto=datetime.now(),endTimeAuto = None,startTimeManual = form.startTime.data, endTimeManual=None)
                db.session.add(Work)
                db.session.commit()
                flash("Your Work Order Number is "+str(numid),"success")
                return redirect(url_for('stop',worktype=worktype))
        return render_template('start.html',form=form)
    
    




@app.route("/stop/<string:worktype>",methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def stop(worktype):
    code = work.query.filter(work.employeeID == current_user.employeeID,work.endTimeAuto == None, work.endTimeManual == None).first()
    if code:
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if((datetime.now()-code.startTimeAuto)>limit) or ((datetime.now()-code.startTimeManual)>limit):
            code.endTimeAuto = datetime(9999,1,1,1,1,1)
            code.endTimeManual = datetime(9999,1,1,1,1,1)
            db.session.commit()
            flash("Start time exceeds 24 hours from current time, please contact Ken/Brandon to adjust previous work","danger")
            return render_template('choices.html')
    if worktype=="maintainence":
        maintcode = work.query.filter_by(employeeID = current_user.employeeID,workType = "maintainence",endTimeAuto = None, endTimeManual = None)
        return render_template("mainttable.html",works = maintcode)
    
    elif worktype=="apartmentrehab":
        aptcode = work.query.filter_by(employeeID = current_user.employeeID,workType = "apartmentrehab",endTimeAuto = None, endTimeManual = None)
        return render_template("apttable.html",works = aptcode)
    
    elif worktype=="landscaping":
        landcode = work.query.filter_by(employeeID = current_user.employeeID,workType = "landscaping",endTimeAuto = None, endTimeManual = None)
        return render_template("landtable.html",works = landcode)
    
    elif worktype=="pestcontrol":
        pestcode = work.query.filter_by(employeeID = current_user.employeeID,workType = "pestcontrol",endTimeAuto = None, endTimeManual = None)
        return render_template("pesttable.html",works = pestcode)
    
    elif worktype=="others":
         othrcode = work.query.filter_by(employeeID = current_user.employeeID,workType = "others",endTimeAuto = None, endTimeManual = None)
         return render_template("othrtable.html",works = othrcode)

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def save_picture(form_picture,picturename):
    
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = picturename + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    uploadFile(picture_fn,'flaskDemo/static/profile_pics/'+picture_fn,'image/'+f_ext)
   

    return picture_fn

@app.route("/maintainence/<string:workorder>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def maintainence(workorder):
    form = MaintenanceForm()
    if form.validate_on_submit():
         limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
         Work = work.query.filter(work.workOrdernumber==workorder).first()
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('maintainence',workorder=workorder))
         elif((Work.startTimeManual - form.endTime.data)>limit):
             flash("Gap between Start Time and End Time exceeds 24 hours, invalid","danger")
             return redirect(url_for('maintainence',workorder=workorder))
         image_file = "None"
         if form.picture.data:
             picture_file = save_picture(form.picture.data,Work.workOrdernumber)
             image_file = url_for('static', filename='profile_pics/' + picture_file) 
             
        
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         maint = maintenance(workID = Work.workID,maintenanceType=form.maintenanceType.data,yearOrworkOrder=form.yearOrworkOrder.data,description = form.description.data,picture = image_file)
         db.session.add(maint)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))

            
    return render_template('maintainence.html', title='Maintainence', form=form)


@app.route("/apartmentrehabs/<string:workorder>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def apartmentrehabs(workorder):
    form = ApartmentRehabForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==workorder).first()
         limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('apartmentrehabs',workorder=workorder))
         elif((Work.startTimeManual - form.endTime.data)>limit):
             flash("Gap between Start Time and End Time exceeds 24 hours, invalid","danger")
             return redirect(url_for('apartmentrehabs',workorder=workorder))
         image_file = "None"
         if form.picture.data:
             picture_file = save_picture(form.picture.data,Work.workOrdernumber)
             image_file = url_for('static', filename='profile_pics/' + picture_file) 
             
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         rehab = apartmentrehab(workID = Work.workID,rehabType=form.rehabType.data,others = form.others.data,description = form.description.data,picture = image_file)
         db.session.add(rehab)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))  
    return render_template('apartmentrehab.html', title='Apartment Rehab', form=form)


 
@app.route("/other/<string:workorder>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def otherss(workorder):
    form = OtherForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==workorder).first()
         limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('otherss',workorder = workorder))
         elif((Work.startTimeManual - form.endTime.data)>limit):
             flash("Gap between Start Time and End Time exceeds 24 hours, invalid","danger")
             return redirect(url_for('otherss',workorder = workorder))
         image_file = "None"
         if form.picture.data:
             picture_file = save_picture(form.picture.data,Work.workOrdernumber)
             image_file = url_for('static', filename='profile_pics/' + picture_file) 
             
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         other = others(workID = Work.workID,othersType=form.othersType.data,others=form.other.data,description = form.description.data,picture = image_file)
         db.session.add(other)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))
    return render_template('others.html', title='Others', form=form)
 
@app.route("/land_scaping/<string:workorder>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def land_scaping(workorder):
    form = LandscapingForm()
    if form.validate_on_submit():
        Work = work.query.filter(work.workOrdernumber==workorder).first()
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('land_scaping',workorder=workorder))
        elif((Work.startTimeManual - form.endTime.data)>limit):
             flash("Gap between Start Time and End Time exceeds 24 hours, invalid","danger")
             return redirect(url_for('land_scaping',workorder=workorder))
        image_file = "None"
        if form.picture.data:
             picture_file = save_picture(form.picture.data,Work.workOrdernumber)
             image_file = url_for('static', filename='profile_pics/' + picture_file) 
             
        Work.endTimeManual=form.endTime.data
        Work.endTimeAuto=datetime.now()        
        landscape = landscaping(workID = Work.workID,landscapingType=form.landscapingType.data,description = form.description.data,picture = image_file)
        db.session.add(landscape)
        db.session.commit()
        flash('Form has been successfully submitted','success')
        return redirect(url_for('home'))
   
    return render_template('landscaping.html', title='Landscaping', form=form)
 
@app.route("/pest_control/<string:workorder>", methods=['GET', 'POST'])
@login_required
@maintainence_permission.require(http_exception=403)
def pest_control(workorder):
    form = PestControlForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==workorder).first()
         limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('pest_control'))
         elif((Work.startTimeManual - form.endTime.data)>limit):
             flash("Gap between Start Time and End Time exceeds 24 hours, invalid","danger")
             return redirect(url_for('pest_control'))
         image_file = "None"
         if form.picture.data:
             picture_file = save_picture(form.picture.data,Work.workOrdernumber)
             image_file = url_for('static', filename='profile_pics/' + picture_file) 
             
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()                 
         pest = pestcontrol(workID = Work.workID,description = form.description.data,picture = image_file)
         db.session.add(pest)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))
   
    return render_template('pestcontrol.html', title='Pest Control', form=form)
 



