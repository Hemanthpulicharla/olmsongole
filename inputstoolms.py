from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from OLMS import Wardens,Students,Superwarden,Security,Base,Complaints


engine = create_engine('sqlite:///OLMS.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

warden1=Wardens(id=1,name="itsme",email="warden1@gmail.com",contact="23458975",branch="mech",leaves_granted=0)
warden1.hash_password('12uil')
session.add(warden1)
session.commit()

warden2=Wardens(id=2,name="itsyou",email="warden2@gmail.com",contact="123458975",branch="cse")
warden2.hash_password("12uil2")
session.add(warden2)
session.commit()

warden3=Wardens(id=3,name="itsus",email="warden3@gmail.com",contact="234589756",branch="Ece")
warden3.hash_password("12uil3")
session.add(warden3)
session.commit()

student1=Students(id=1,name="hemanth",id_num='o170078',email='o170078@rgukt.in',branch='mech',contact='1234567',warden_id=1,)
student1.hash_password("Hemanth")
session.add(student1)
session.commit()


student2=Students(id=2,name="hemantho",id_num='o170079',email='o170079@rgukt.in',branch='mech',contact='123456789',warden_id=1)
student2.hash_password("Hemanthoo")
session.add(student2)
session.commit()


student3=Students(id=3,name="hemanthot",id_num='o170080',email='o170080@rgukt.in',branch='mech',contact='123456247',warden_id=1)
student3.hash_password("Hemanthji")
session.add(student3)
session.commit()



superwarden1=Superwarden(id=1,name="bhushan",email="admin@rgukt.in",contact='2345678')
superwarden1.hash_password("admin")
session.add(superwarden1)
session.commit()



superwarden2=Superwarden(id=2,name="bhushanoo",email="admin2@rgukt.in",contact='2345678123')
superwarden2.hash_password("admin1")
session.add(superwarden2)
session.commit()



superwarden3=Superwarden(id=3,name="bhushan",email="admin3@rgukt.in",contact='2345673238')
superwarden3.hash_password("admin2")
session.add(superwarden3)
session.commit()

security1=Security(id=1,name="yellaya",email="pogaru@gmail.com",contact="123457299999")
security1.hash_password("Keyspet")
session.add(security1)
session.commit()

security2=Security(id=2,name="yelli",email="pogaruga@gmail.com",contact="1234572999")
security2.hash_password("Keyspett")
session.add(security2)
session.commit()

security3=Security(id=3,name="yellaiha",email="poragad@gmail.com",contact="1234599")
security3.hash_password("Biggboss")
session.add(security3)
session.commit()

print("yes!!! You got that")








