import os
import secrets
import re
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from flaskDemo import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, Permission, RoleNeed
from flaskDemo.models import role,employee, unit,building,work,maintenance,apartmentrehab,others,landscaping,pestcontrol
from flaskDemo.forms import ChangeEmailForm,ChangePhoneForm,ChangePasswordForm,ForgetPasswordForm,StartForm,BuildingForm,RegistrationForm,LoginForm,MaintenanceForm,ApartmentRehabForm,LandscapingForm,PestControlForm,OtherForm
from datetime import datetime
from sqlalchemy import or_, update, and_
import yaml
import pandas as pd
from numpy.random import randint
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


admin_permission = Permission(RoleNeed('admin'))

#Configure db

@app.route("/")

#database manipulation
#@app.route("/data", methods=['GET', 'POST'])
#def data():

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
#    Role1 = role(roleName = "user")
#    Role2 = role(roleName = "admin")
#    hashed_password = bcrypt.generate_password_hash("gnp7737644998").decode('utf-8')
#    adminuser = employee(firstName="Good News",lastName="Partners",username="goodnews24",password=hashed_password,phoneNumber = "7737644998",email = "Brandon@goodnewspartners.org",roleID = 1 )
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
#  
#    
#    
#    db.session.commit()
#    
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
#    return redirect(url_for('home'))   
    
#Employee manipulation 
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
        Employee = employee(firstName=form.firstName.data,lastName=form.lastName.data,username=form.username.data,password=hashed_password,phoneNumber = form.phone.data,email = form.email.data,roleID = 1)
        db.session.add(Employee)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/forgotpass", methods=['GET', 'POST'])
def forgotpass():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        num = randint(100000, 999999)
        
        hashed_password = bcrypt.generate_password_hash(str(num)).decode('utf-8')
        Employee = employee.query.filter_by(email=form.email.data).first()
        Employee.password = hashed_password
        print(num)
        db.session.commit()
        try:
            gmail_user = "goodnewspartners1@gmail.com"
            gmail_password = "goodnews24"
          
            
            message = MIMEMultipart("alternative")
            message["Subject"] = "Good News Partner - Temporary Password"
            message["From"] = gmail_user
            message["To"] = form.email.data
            text=("Hello there,\n Here is your temporary password: \n"+ str(num) +"\n"+
                  "Please sign in using this temporary password, and modify your password in Manage Account")
            message.attach(MIMEText(text,"plain"))
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, form.email.data, message.as_string())
            flash("Temporary Password Sent! Please check your email","success")
            return redirect(url_for('login'))
        except:
            flash("Not Successful in sending link","danger")
        
         
    return render_template('forgotpassword.html',form=form)


    
    



@app.route("/changepass", methods=['GET', 'POST'])
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


#main app form
@app.route("/choices", methods=['GET', 'POST'])
@login_required
def choices(): #render worktype buttons
    return render_template('choices.html')

@app.route("/front", methods=['GET', 'POST'])
@login_required
def front(): #render frontpage buttons
    return render_template('frontpage.html')

@app.route("/manageacc", methods=['GET', 'POST'])
@login_required
def manageacc():
    return render_template('manageacc.html')



@app.route("/startstop/<string:worktype>", methods=['GET', 'POST'])
@login_required #render start and stop buttons
def startstop(worktype):       
    return render_template('startstop.html',worktype = worktype)


@app.route("/building/<string:worktype>", methods=['GET', 'POST'])
@login_required
def buildingchoice(worktype):
    Building= building.query.all()
    buildingList = [(b.buildingID,b.buildingName) for b in Building]
    form = BuildingForm()
    form.buildingName.choices = buildingList
    if form.validate_on_submit():
        return redirect(url_for('start',worktype=worktype,buildingname=form.buildingName.data))
    return render_template('buildingchoice.html',form=form)




@app.route("/start/<string:worktype>/<string:buildingname>", methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('apartmentrehabs'))
    elif worktype=="landscaping":
        return redirect(url_for('landscaping'))
    elif worktype=="pestcontrol":
        return redirect(url_for('pestcontrol'))
    elif worktype=="others":
        return redirect(url_for('others'))
    
    




@app.route("/stop/<string:worktype>",methods=['GET', 'POST'])
@login_required
def stop(worktype):
    if worktype=="maintainence":
        return redirect(url_for('maintainence'))
    elif worktype=="apartmentrehab":
        return redirect(url_for('apartmentrehabs'))
    elif worktype=="landscaping":
        return redirect(url_for('landscaping'))
    elif worktype=="pestcontrol":
        return redirect(url_for('pestcontrol'))
    elif worktype=="others":
        return redirect(url_for('others'))


@app.route("/maintainence", methods=['GET', 'POST'])
@login_required
def maintainence():
    form = MaintenanceForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==form.workOrdernumber.data).first()
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('maintainence'))
         elif(Work.workType != "maintainence"):
             flash("Work Type for this work order number is not maintainence,wrong work order number",'danger')
             return redirect(url_for('maintainence'))
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         maint = maintenance(workID = Work.workID,maintenanceType=form.maintenanceType.data,yearOrworkOrder=form.yearOrworkOrder.data,description = form.description.data,picture = form.picture.data)
         db.session.add(maint)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))

            
    return render_template('maintainence.html', title='Maintainence', form=form)


@app.route("/apartmentrehabs", methods=['GET', 'POST'])
@login_required
def apartmentrehabs():
    form = ApartmentRehabForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==form.workOrdernumber.data).first()
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('apartmentrehabs'))
         elif(Work.workType != "apartmentrehab"):
             flash("Work Type for this work order number is not apartment rehab,wrong work order number",'danger')
             return redirect(url_for('apartmentrehabs'))
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         rehab = apartmentrehab(workID = Work.workID,rehabType=form.rehabType.data,others = form.others.data,description = form.description.data,picture = form.picture.data)
         db.session.add(rehab)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))  
    return render_template('apartmentrehab.html', title='Apartment Rehab', form=form)


 
@app.route("/other", methods=['GET', 'POST'])
@login_required
def others():
    form = OtherForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==form.workOrdernumber.data).first()
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('others'))
         elif(Work.workType != "others"):
             flash("Work Type for this work order number is not others, wrong work order number",'danger')
             return redirect(url_for('others'))
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()
         other = others(workID = Work.workID,othersType=form.othersType.data,others=form.other.data,description = form.description.data,picture = form.picture.data)
         db.session.add(other)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))
    return render_template('others.html', title='Others', form=form)
 
@app.route("/land_scaping", methods=['GET', 'POST'])
@login_required
def landscaping():
    form = LandscapingForm()
    if form.validate_on_submit():
        Work = work.query.filter(work.workOrdernumber==form.workOrdernumber.data).first()
        if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('landscaping'))
        elif(Work.workType != "landscaping"):
             flash("Work Type for this work order number is not landscaping, wrong work order number",'danger')
             return redirect(url_for('landscaping'))
        Work.endTimeManual=form.endTime.data
        Work.endTimeAuto=datetime.now()        
        landscape = landscaping(workID = Work.workID,landscapingType=form.landscapingType.data,description = form.description.data,picture = form.picture.data)
        db.session.add(landscape)
        db.session.commit()
        flash('Form has been successfully submitted','success')
        return redirect(url_for('home'))
   
    return render_template('landscaping.html', title='Landscaping', form=form)
 
@app.route("/pest_control", methods=['GET', 'POST'])
@login_required
def pestcontrol():
    form = PestControlForm()
    if form.validate_on_submit():
         Work = work.query.filter(work.workOrdernumber==form.workOrdernumber.data).first()
         if(form.endTime.data < Work.startTimeManual):
             flash("End Date is earlier than Start Date, invalid","danger")
             return redirect(url_for('pestcontrol'))
         elif(Work.workType != "pestcontrol"):
             flash("Work Type for this work order number is not pest control, wrong work order number",'danger')
             return redirect(url_for('pestcontrol'))
         Work.endTimeManual=form.endTime.data
         Work.endTimeAuto=datetime.now()                 
         pest = pestcontrol(workID = Work.workID,description = form.description.data,picture = form.picture.data)
         db.session.add(pest)
         db.session.commit()
         flash('Form has been successfully submitted','success')
         return redirect(url_for('home'))
   
    return render_template('pestcontrol.html', title='Pest Control', form=form)
 



