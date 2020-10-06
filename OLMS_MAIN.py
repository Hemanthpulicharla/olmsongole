from flask import Flask,render_template,url_for,redirect,flash,request,jsonify,send_file
from sqlalchemy import create_engine,asc,and_,func,extract
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from OLMS import Base,Overview,Wardens,Superwarden,Security,Students,Pending
from flask import session as login_session
import string
import datetime
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory


from flask import make_response
import requests

engine = create_engine('sqlite:///OLMS.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'Images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def showLogin():
	return render_template('login.html')
@app.route('/Authorization',methods=['GET','POST'])
def Authorize():
	username=request.form['username']
	password=request.form['pass']
	if(session.query(Wardens).filter_by(email=username).first() is not None):
		user=session.query(Wardens).filter_by(email=username).first()
		if(user.verify_password(password)):
			flash('Welcome %s'%(user.name))
			return redirect(url_for('Wardenpage',warden_id=user.id))
		else:
			return "<script>function myFunction() {alert('You are not authorized to login...');}</script><body onload='myFunction()'>"
	if(session.query(Students).filter_by(email=username).first() is not None):
		user=session.query(Students).filter_by(email=username).first()
		if(user.verify_password(password)):
			flash('Welcome %s'%(user.name))
			return redirect(url_for('studentpage',student_id=user.id))
		else:
			return "<script>function myFunction() {window.location='/'} alert('You are not authorized to login...');setTimeout(myFunction(),10000);/script><body onload='myFunction()'>"
	if(session.query(Superwarden).filter_by(email=username).first() is not None):
		user=session.query(Superwarden).filter_by(email=username).first()
		if(user.verify_password(password)):
			flash('Welcome %s'%(user.name))
			return redirect(url_for('Superwardenpage',superwarden_id=user.id))
		else:
			return "<script>function myFunction() {window.location='/'} alert('You are not authorized to login...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"
	if(session.query(Security).filter_by(email=username).first() is not None):
		user=session.query(Security).filter_by(email=username).first()
		if(user.verify_password(password)):
			flash('Welcome %s'%(user.name))
			return redirect(url_for('Securitypage',security_id=user.id))
		else:
			return "<script>function myFunction() {window.location='/'} alert('You are not authorized to login...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"

	else:
		return "<script>function myFunction() {window.location='/'}alert('Dont Cheat me OKay!! Redirecting.....');setTimeout('myFunction()', 10000);</script><body onload='myFunction()'>"


@app.route('/wardens/<int:warden_id>',methods=['GET','POST'])
def Wardenpage(warden_id):
	if 'username' not in login_session:
        return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	session.no_autoflush
	login_session['username']=warden.name
	use_date=datetime.datetime.now()
	pending=session.query(Pending).filter_by(warden=warden.name).all()
	overview=session.query(Overview).filter_by(warden=warden.name).all()
	month=session.query(Overview).filter_by(month=use_date.month).count()
	year=session.query(Overview).filter_by(year=use_date.year).count()
	pendings=len(pending)
	outpercents=len(overview)
	incamp=100-(pendings+outpercents)
	incampperc=float(incamp/100)*100
	return render_template('index.html',warden=warden,pendingper=pendings,outpercent=outpercents,overview=overview,month=month,incamp=incamp,year=year,incampus=incampperc)

@app.route('/student/<int:student_id>',methods=['GET','POST'])
def studentpage(student_id):
	if 'username' not in login_session:
        return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	login_session['username']=student.name
	warden=session.query(Wardens).filter_by(id=student.warden_id).first()
	return render_template('student.html',warden=warden,student=student)

@app.route('/superwarden/<int:superwarden_id>',methods=['GET','POST'])
def Superwardenpage(superwarden_id):
	if 'username' not in login_session:
       return redirect('/login')
	student=session.query(Pending).count()
	warden=session.query(Wardens).all()
	approve=session.query(Overview).count()
	pending=session.query(Pending).count()
	incamp=100-(approve+pending)
	month=session.query(Overview).filter_by(month=datetime.datetime.utcnow().month).count()
	year=session.query(Overview).filter_by(year=datetime.datetime.utcnow().year).count()
	superwarden=session.query(Superwarden).filter_by(id=superwarden_id).first()
	login_session['username']=superwarden.name
	return render_template('superwarden.html',warden=warden,student=student,superwarden=superwarden,month=month,year=year,approve=approve,pending=pending,incamp=incamp)
@app.route('/security/<int:security_id>',methods=['GET','POST'])
def Securitypage(security_id):
 	if 'username' not in login_session:
        return redirect('/login')	
	security=session.query(Security).filter_by(id=security_id).first()
	login_session['username']=security.name
	student=session.query(Overview).all()
	warden=session.query(Wardens).all()
	superwarden=session.query(Superwarden).all()
	return render_template('security.html',student=student,warden=warden,superwarden=superwarden)

@app.route('/leave/applying/<int:student_id>',methods=['GET','POST'])
def applyleave(student_id):
	if 'username' not in login_session:
        return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	warden=session.query(Wardens).filter_by(id=student.warden_id).first()
	return render_template('leave_application.html',student=student,warden=warden)
@app.route('/leave/pending/<int:student_id>',methods=['GET','POST'])
def leavesubmit(student_id):
	if 'username' not in login_session:
        return redirect('/login')
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return "<script> alert('File not selected')</script"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            reason=request.form['reason']
            fromdate=request.form['fromdate']
            todate=request.form['todate']
            contact=request.form['contact']
            student=session.query(Students).filter_by(id=student_id).first()
            warden=session.query(Wardens).filter_by(id=student.warden_id).first()
            pending=Pending(name=student.name,id_num=student.id_num,email=student.email,branch=student.branch,warden=warden.name,contact=contact,reason=reason,fromdate=fromdate,todate=todate,file=filename)
            session.add(pending)
            session.commit()
            flash("Whoa!! Your request submitted")
            return	"<script>function myFunction() {window.location.href='/student/%s'} alert('Your submitted succesfully Redirecting...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%student_id
        else:
        	return	"<script>function myFunction() {window.location='/student/%s'} alert('Problem in submitting please try again...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%student_id


@app.route('/pending/<int:warden_id>/table',methods=['GET','POST'])
def pending(warden_id):
	if 'username' not in login_session:
        return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	pending=session.query(Pending).filter_by(warden=warden.name).all()
	return render_template('tablesnew.html',pending=pending,warden=warden)
@app.route('/leaveapprove/<student_id>/<int:warden_id>',methods=['GET','POST'])
def leaveapprove(warden_id,student_id):
	if 'username' not in login_session:
        return redirect('/login')
	student=session.query(Pending).filter_by(id_num=student_id).first()
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	leave=Overview(name=student.name,fromdate=student.fromdate,todate=student.todate,id_num=student.id_num,email=student.email,branch=student.branch,warden=warden.name,reason=student.reason,contact=student.contact)
	session.add(leave)
	session.commit()
	session.delete(student)
	session.commit()
	warden.leaves_granted+=1
	return "<script>function myFunction() {window.location='/pending/%s/table'} alert('Submittted succesfully...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
	#else:
	#	return "<script>function myFunction() {window.location='/pending/%s/table'} alert('Problem in submitting...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
@app.route('/leavereject/<student_id>/<int:warden_id>')
def leavereject(student_id,warden_id):
	if 'username' not in login_session:
        return redirect('/login')
	pendingdown=session.query(Pending).filter_by(id_num=student_id).first()
	session.delete(pendingdown)
	session.commit()
	return "<script>function myFunction() {window.location='/pending/%s/table'} alert('Rejected leave and Redirecting...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
@app.route('/approved/<int:warden_id>',methods=['POST','GET'])
def Approved(warden_id):
	if 'username' not in login_session:
        return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	approved=session.query(Overview).filter_by(warden=warden.name).all()
	return render_template('approvedleaves.html',approved=approved,warden=warden)
@app.route('/depreciate/<student_id>/<int:warden_id>')
def depreciate(warden_id,student_id):
	if 'username' not in login_session:
        return redirect('/login')
	warden=session.query(Wardens).filter_by(id=warden_id).one()
	student=session.query(Overview).filter_by(id_num=student_id).first()
	session.delete(student)
	session.commit()
	return "<script>function myFunction() {window.location='/approved/%i'} alert('Yess Finally...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
		#return "<script>function myFunction() {window.location='/approved/%i'} alert('Sorry Couldnt depreciate...');setTimeout(myFunction(),10000);</script><body onload='myFunction()'>"%warden_id
@app.route('/superwarden/<int:sup_id>/table')
def superview(sup_id):
	if 'username' not in login_session:
        return redirect('/login')
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	pending=session.query(Pending).all()
	requests=len(pending)
	return render_template('supertable.html',pending=pending,superwarden=superwarden,requests=requests)
@app.route('/superapprove/<int:sup_id>')
def superapprove(sup_id):
	if 'username' not in login_session:
        return redirect('/login')
	superwarden=session.query(Superwarden).filter_by(id=sup_id).first()
	approved=session.query(Overview).all()
	return render_template('superapprove.html',approved=approved,superwarden=superwarden)
@app.route('/complaint/<int:student_id>')
def messcomplain(student_id):
	if 'username' not in login_session:
        return redirect('/login')
	student=session.query(Students).filter_by(id=student_id).first()
	return render_template('complain_form.html',student=student)
@app.route('/download/<int:id>')
def downloadfile(id):
	if 'username' not in login_session:
        return redirect('/login')
	student=session.query(Pending).filter_by(id=id).first()
	return send_from_directory(app.config['UPLOAD_FOLDER'],
                               student.file,as_attachment=True)
@app.route('/logout')
def logout():
	del login_session['username']
	return redirect(url_for('showLogin'))
if __name__=='__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)





