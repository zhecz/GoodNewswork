from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, FieldList, FormField
from wtforms.validators import InputRequired,DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import employee, building,work,maintenance,apartmentrehab,landscaping,pestcontrol
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime,timedelta

class BuildingForm(FlaskForm):
    buildingName = SelectField('Select Building',coerce=int,validators=[DataRequired()])
    submit = SubmitField('Select')
    
class ForgetPasswordForm (FlaskForm):
    email = StringField('Your email:',  validators= [DataRequired(),Email()])
    submit = SubmitField('Verify')    
    
    def validate_email(self, email):
        user = employee.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email not found in database')
            
            
            
            
class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old Password',validators= [DataRequired()])
    newpassword = PasswordField('New Password',validators= [DataRequired()])
    confirmpassword = PasswordField('Confirm Password',validators= [DataRequired(), EqualTo('newpassword')])
    submit = SubmitField('Change Password')
    
    def validate_newpassword(self, newpassword):
        if len(newpassword.data) < 5:
            raise ValidationError('Password must be at least 5 characters.')

class ChangeEmailForm(FlaskForm):
    oldemail = StringField('Old Email',validators= [DataRequired()])
    newemail = StringField('New Email',validators= [DataRequired()])
    confirmemail = StringField('Confirm Email',validators= [DataRequired(), EqualTo('newemail')])
    submit = SubmitField('Change Email')
    
    def validate_newemail(self, newemail):
        user = employee.query.filter_by(email=newemail.data).first()
        if user:
            raise ValidationError('Email is taken, please use other email')
            
class ChangePhoneForm(FlaskForm):
    oldphone = StringField('Old Phone',validators= [DataRequired()])
    newphone = StringField('New Phone',validators= [DataRequired()])
    confirmphone = StringField('Confirm Phone',validators= [DataRequired(), EqualTo('newphone')])
    submit = SubmitField('Change Phone')
    
    def validate_newPhone(self, newphone):
        user = employee.query.filter_by(phoneNumber=newphone.data).first()
        if user:
            raise ValidationError('Phone number is taken, please use other phone number')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    firstName = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number',validators=[DataRequired(),Length(min=10, max=11)])
    email = StringField('Email address', validators= [DataRequired(),Email()])
    position = SelectField('Position',choices=[('Maintenance','Maintenance'),('Front Desk','Front Desk')], validators=[DataRequired()],default=None)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken.')
            
    def validate_email(self, email):
        user = employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')
    
    def validate_password(self, password):
        if len(password.data) < 5:
            raise ValidationError('Password must be at least 5 characters.')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    def validate_username(self, username):
        user = employee.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username not found')
  
            


#building = [('Jonquil Hotel','Jonquil Hotel'),('Lloyd','Lloyd'),('New Life','New Life'),('Ministry Center','Ministry Center'),('JCP','JCP'),('No Bos Condo','No Bos Condo'),('Fargo','Fargo'),('Esperanza','Esperanza'),('Phoenix 1','Phoenix 1'),('Phoenix 2','Phoenix 2')]

class StartForm(FlaskForm):
    unitName = SelectField('Select Unit',coerce=int,validators=[DataRequired()],default=None)
    startTime =  DateTimeLocalField('Start Time',validators=[InputRequired()],format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Start")
    
    def validate_startTime(self, startTime):
        limit = timedelta(days = 1, hours = 0,minutes = 0, seconds = 0)
        if (startTime.data > datetime.now()):
            raise ValidationError("Start Date is in the future, invalid")
        elif ((datetime.now()-startTime.data)>limit):
            raise ValidationError("Start Date exceeds 24hours from the current time, invalid")

            
#class StartNonUnitForm(FlaskForm):
#    startTime =  DateTimeLocalField('Start Time',validators=[InputRequired()],format='%Y-%m-%dT%H:%M')
#    submit = SubmitField("Start")
#    
#    def validate_startTime(self, startTime):
#        if (startTime.data > datetime.now()):
#            raise ValidationError("Start Date is in the future, invalid")


class MaintenanceForm(FlaskForm):
    endTime = DateTimeLocalField('End Time',format='%Y-%m-%dT%H:%M',validators=[InputRequired()] )
    maintchoice = [('Electrical-Kitchen', 'Electrical-Kitchen'),('Electrical-Bathroom', 'Electrical-Bathroom'),
                   ('Electrical-Building', 'Electrical-Building'),('Plumbing-Kitchen', 'Plumbing-Kitchen'),('Plumbing-Bathroom', 'Plumbing-Bathroom'),
                   ('Plumbing-Building', 'Plumbing-Building'), ('Gas-Kitchen','Gas-Kitchen'),('Gas-Building','Gas-Building')]
    maintenanceType = SelectField('Maintenance Type', choices=maintchoice,validators=[DataRequired()])
    time = [('Yearly Maintenance', 'Yearly Maintenance'),('Work Order Maintenance', 'Work Order Maintenance')]
    yearOrworkOrder =SelectField('Yearly/Usual Maintenance', choices=time,validators=[DataRequired()])
    description =  StringField('Description',validators=[DataRequired()])
    picture =  picture = FileField('Detailed Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
   
    def validate_endTime(self,endTime):
        if (endTime.data > datetime.now()):
            raise ValidationError("End Date is in the future, invalid")
             
             
             
class ApartmentRehabForm(FlaskForm):
    endTime = DateTimeLocalField('End Time',format='%Y-%m-%dT%H:%M',validators=[InputRequired()] )
    apartreh = [('Bathroom','Bathroom'),('Painting','Painting'),('Plumbing','Plumbing'),('Sanding','Sanding'),('Gas','Gas'),('Remove Garbage','Remove Garbage'),('Electrical','Electrical'),('Others','Others')]
    rehabType = SelectField('Rehabilitation Type', choices=apartreh,validators=[DataRequired()])
    others = StringField('If Others,please state:')
    description =  StringField('Description',validators=[DataRequired()])
    picture =  picture = FileField('Detailed Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

    def validate_endTime(self,endTime):
        if (endTime.data > datetime.now()):
            raise ValidationError("End Date is in the future, invalid")



class LandscapingForm(FlaskForm):
    endTime = DateTimeLocalField('End Time',format='%Y-%m-%dT%H:%M',validators=[InputRequired()] )
    landscapingType = StringField('Landscaping type',validators=[DataRequired()])
    description =  StringField('Description',validators=[DataRequired()])
    picture =  picture = FileField('Detailed Picture', validators=[FileAllowed(['jpg', 'png','jfif'])])
    submit = SubmitField('Submit')
   
    def validate_endTime(self,endTime):
        if (endTime.data > datetime.now()):
            raise ValidationError("End Date is in the future, invalid")




class PestControlForm(FlaskForm):
    endTime = DateTimeLocalField('End Time',format='%Y-%m-%dT%H:%M',validators=[InputRequired()] )
    description =  StringField('Description',validators=[DataRequired()])
    picture =  picture = FileField('Detailed Picture', validators=[FileAllowed(['jpg', 'png','jfif'])])
    submit = SubmitField('Submit')

    def validate_endTime(self,endTime):
        if (endTime.data > datetime.now()):
            raise ValidationError("End Date is in the future, invalid")



class OtherForm(FlaskForm):
    endTime = DateTimeLocalField('End Time',format='%Y-%m-%dT%H:%M',validators=[InputRequired()] )
    otherchoice = [('Pick Up Groceries','Pick Up Groceries'),('Go to Store','Go to Store'),('others','others')]
    othersType = SelectField("Other Categories",choices = otherchoice,validators=[DataRequired()])
    other = StringField('if others please state:')
    description =  StringField('Description',validators=[DataRequired()])
    picture =  picture = FileField('Detailed Picture', validators=[FileAllowed(['jpg', 'png','jfif'])])
    submit = SubmitField('Submit')
      
    def validate_endTime(self,endTime):
        if (endTime.data > datetime.now()):
            raise ValidationError("End Date is in the future, invalid")
              


