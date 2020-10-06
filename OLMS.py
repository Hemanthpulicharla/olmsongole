# coding:utf-8
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base=declarative_base()

class Overview(Base):
	__tablename__='outstudents'

	id=Column(Integer,primary_key=True)
	name=Column(String(200))
	id_num=Column(String(200))
	email=Column(String(200))
	branch=Column(String(200))
	warden=Column(String(200))
	contact=Column(Integer)
	fromdate=Column(String(100))
	todate=Column(String(100))
	reason=Column(String(200))
	month=Column(String,default=datetime.datetime.utcnow().month)
	year=Column(String,default=datetime.datetime.utcnow().year)
	Timestamp= Column(DateTime, default=datetime.datetime.utcnow)

	@property
	def serialize(self):
		return {

			'name':self.name,
			'branch':self.branch,
			'warden':self.warden,
			'email':self.email,
			'contact':self.contact,
			'id':self.id_num,
			'reason':self.reason
			}
class Pending(Base):

	__tablename__='pending'
	
	id=Column(Integer,primary_key=True)
	name=Column(String(200))
	id_num=Column(String(200))
	email=Column(String(200))
	branch=Column(String(200))
	warden=Column(String(200))
	contact=Column(Integer)
	reason=Column(String(200))
	fromdate=Column(String(100))
	todate=Column(String(100))
	file=Column(String(100))
	Timestamp=Column(DateTime, default=datetime.datetime.utcnow)

	@property
	def serialize(self):
		return {

			'name':self.name,
			'branch':self.branch,
			'warden':self.warden,
			'email':self.email,
			'contact':self.contact,
			'id':self.id_num,
			'reason':self.reason
			}

class Wardens(Base):
	__tablename__='wardens'

	id=Column(Integer,primary_key=True)
	name=Column(String(200),index=True)
	email=Column(String(200),nullable=False)
	contact=Column(Integer)
	branch=Column(String(100))
	password_hash=Column(String(100))
	leaves_granted=Column(Integer)

	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password,self.password_hash)

class Students(Base):
	__tablename__='students'

	id=Column(Integer,index=True)
	id_num=Column(String(200),primary_key=True)
	name=Column(String(200),nullable=False)
	email=Column(String(200),nullable=False)
	picture=Column(String(200))
	branch=Column(String(200))
	leaves=Column(Integer)
	contact=Column(Integer)
	password_hash=Column(String(100))
	warden_id=Column(Integer,ForeignKey('wardens.id'))
	wardens=relationship(Wardens)


	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password,self.password_hash)

class Superwarden(Base):
	__tablename__='superwarden'

	id=Column(Integer,primary_key=True)
	name=Column(String(100),nullable=False)
	email=Column(String(100),nullable=False)
	branch=Column(String(20))
	contact=Column(String(100))
	password_hash=Column(String(100))

	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)
	def verify_password(self,password):
		return pwd_context.verify(password,self.password_hash)

class Security(Base):
	__tablename__='security'

	id=Column(Integer,primary_key=True)
	name=Column(String(200))
	email=Column(String(200),nullable=False)
	contact=Column(String(200))
	password_hash=Column(String(200))
	
	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)
	def verify_password(self,password):
		return pwd_context.verify(password,self.password_hash)

class Complaints(Base):

	__tablename__='complain'

	id=Column(Integer,primary_key=True)
	stud_name=Column(String(100),nullable=False)
	id_num=Column(String(100),nullable=False)
	branch=Column(String(100))
	email=Column(String(100))
	category=Column(String(100))
	description=Column(String(400))
	oneline=Column(String(100))
	Timestamp=Column(DateTime, default=datetime.datetime.utcnow)



engine=create_engine('sqlite:///OLMS.db')

Base.metadata.create_all(engine)

