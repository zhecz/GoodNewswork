from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@login_manager.user_loader
def load_user(user_id):
    return employee.query.get(int(user_id))

class employee(db.Model, UserMixin):
    __tablename__ = 'Employee'
    __table_args__ = {'extend_existing': False}
    employeeID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200),unique=True,nullable = False)
    password = db.Column(db.String(70), nullable=False)
    phoneNumber = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def get_id(self): 
        return (self.employeeID)


class building(db.Model, UserMixin):
    __tablename__ = 'Building'
    __table_args__ = {'extend_existing': False}
    buildingID = db.Column(db.Integer, primary_key=True)
    buildingName = db.Column(db.String(200), nullable=False)
    buildingAddress = db.Column(db.String(200), nullable=False)
    postalCode = db.Column(db.Integer, nullable=False)
    numberOfrooms = db.Column(db.Integer, nullable=False)

class unit(db.Model, UserMixin):
    __tablename__ = 'Unit'
    __table_args__ = {'extend_existing': False}
    buildingID = db.Column(db.Integer,db.ForeignKey('Building.buildingID'), nullable=False)
    unitID = db.Column(db.Integer,primary_key=True)
    unitName = db.Column(db.String(200), nullable=False)
   



class work(db.Model, UserMixin):
    __tablename__ = 'Work'
    __table_args__ = {'extend_existing': False}
    workID = db.Column(db.Integer, primary_key=True, nullable=False)
    employeeID = db.Column(db.Integer,db.ForeignKey('Employee.employeeID'), nullable=False)
    buildingID = db.Column(db.Integer,db.ForeignKey('Building.buildingID'),nullable = False)
    unitID = db.Column(db.Integer, db.ForeignKey('Unit.unitID'),nullable = False)
    workType = db.Column(db.String(100),nullable = False)
    workOrdernumber = db.Column(db.Integer,unique=True,nullable = False)
    startTimeAuto = db.Column(db.DateTime,nullable = False)
    endTimeAuto = db.Column(db.DateTime,nullable = True)
    startTimeManual = db.Column(db.DateTime,nullable = False)
    endTimeManual = db.Column(db.DateTime,nullable = True)
    
class maintenance(db.Model, UserMixin):
    __tablename__ = 'Maintenance'
    __table_args__ = {'extend_existing': False}
    mainID = db.Column(db.Integer, primary_key = True,nullable = False)
    workID = db.Column(db.Integer,db.ForeignKey('Work.workID'),nullable = False)
    maintenanceType = db.Column(db.String(200),nullable = False)
    yearOrworkOrder = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(200),nullable = False)
    picture = db.Column(db.String(200))

class apartmentrehab(db.Model, UserMixin):
    __tablename__ = 'ApartmentRehab'
    __table_args__ = {'extend_existing': False}
    rehID = db.Column(db.Integer, primary_key = True,nullable = False)
    workID = db.Column(db.Integer,db.ForeignKey('Work.workID'),nullable = False)
    rehabType = db.Column(db.String(200),nullable = False)
    others = db.Column(db.String(200),nullable = True)
    description = db.Column(db.String(200),nullable = False)
    picture = db.Column(db.String(200))

class others(db.Model, UserMixin):
    __tablename__ = 'Others'
    __table_args__ = {'extend_existing': False}
    othID = db.Column(db.Integer, primary_key = True,nullable = False)
    workID = db.Column(db.Integer,db.ForeignKey('Work.workID'),nullable = False)
    othersType = db.Column(db.String(200),nullable = False)
    others = db.Column(db.String(200),nullable = True)
    description = db.Column(db.String(200),nullable = False)
    picture = db.Column(db.String(200))

class landscaping(db.Model, UserMixin):
    __tablename__ = 'Landscaping'
    __table_args__ = {'extend_existing': False}
    lanscID = db.Column(db.Integer, primary_key = True,nullable = False)
    workID = db.Column(db.Integer,db.ForeignKey('Work.workID'),nullable = False)
    landscapingType = db.Column(db.String(200),nullable = False)
    description = db.Column(db.String(200),nullable = False)
    picture = db.Column(db.String(200))
    
class pestcontrol(db.Model, UserMixin):
    __tablename__ = 'PestControl'
    __table_args__ = {'extend_existing': False}
    pcID = db.Column(db.Integer, primary_key = True,nullable = False)
    workID = db.Column(db.Integer,db.ForeignKey('Work.workID'),nullable = False)
    description = db.Column(db.String(200),nullable = False)
    picture = db.Column(db.String(200))


