from django.shortcuts import render,redirect
from . models import Enquiry,Adminlogin,tbl_session,tbl_course,Student
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .import smssender
# Create your views here.
def index(req):
    return render(req, 'index.html')

def contact(req):
    if req.method=="POST":
        name=req.POST['name']
        gender=req.POST['gender']
        address=req.POST['address']
        contactno=req.POST['contactno']
        emailaddress=req.POST['emailaddress']
        enquirytext=req.POST['enquirytext']
        enquirydate=datetime.datetime.today()
        enq= Enquiry(name=name, gender=gender, address=address, contactno=contactno, emailaddress=emailaddress, enquirytext=enquirytext, enquirydate=enquirydate)
        enq.save()
        smssender.sendsms(contactno)
        msg="your Enquiry is submitted successfully"
        return render(req, 'contact.html', {'msg':msg})
    return render(req, 'contact.html') 
def login(req):
    return render(req, 'login.html')
def logcode(req):
    if req.method == 'POST':
        usertype = req.POST['usertype']
        userid = req.POST['userid']
        password = req.POST['password']
        if usertype == 'admin':
            try:
                user = Adminlogin.objects.get(userid=userid, password=password)
                if user is not None:
                    req.session['adminid'] = userid
                    return redirect('adminlayout')
            except ObjectDoesNotExist:
                return render(req,'login.html',{'msg':'Invalid User'}) 
        elif usertype == 'student':
            try:
                stu=Student.objects.get(emailaddress=userid,password=password)
                if stu is not None:
                    req.session['studentid']=userid
                    return redirect('studentdash')
            except ObjectDoesNotExist:
                return render(req,'login.html',{'meg':'Invalid User'}) 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)       
def adminlayout(req):
    try:
        if req.session['adminid']!=None:
            return render(req, 'adminlayout.html') 
    except  KeyError:
        return redirect('login')      
def showenq(req):
    sh=Enquiry.objects.all()
    return render(req, 'showenquiry.html',{'Show':sh})
def addsession(req):

    return render(req,'addsession.html')
def assave(req):
    Session=req.POST['session']
    created_date=timezone.now()
    ads=tbl_session(Session= Session,created_date=created_date)
    ads.save()
    return redirect('addsession')
def showsession(req):
    se=tbl_session.objects.all()
    return render(req,'showsession.html',{'session':se})
def addcourse(req):
    ch=tbl_session.objects.all()
    if req.method=="POST":
        course_session=req.POST['course_session']
        course_name=req.POST['course_name']
        course_duration=req.POST['course_duration']
        course_fees=req.POST['course_fees']
        created_date=timezone.now()
        cor=tbl_course(course_session=course_session,course_name=course_name,course_fees=course_fees,created_date=created_date,course_duration=course_duration)
        cor.save()
        return redirect('addcourse')
    return render(req,'addcourse.html',{'ch':ch})
def deltbl(req,id):
    de=tbl_session.objects.get(pk=id)
    de.delete()
    return redirect('showsession')
def showcourse(req):
    se=tbl_course.objects.all()
    return render (req,'showcourse.html',{'Se':se})
def coldel(req,id):
    yt=tbl_course.objects.get(pk=id)
    yt.delete() 
    return redirect('showcourse')
def editsession(req,id):
    qw=tbl_session.objects.get(pk=id)
    if req.method=='POST':
        Session=req.POST['Session']
        created_date=timezone.now()
        tbl_session.objects.filter(pk=id).update(Session=Session,created_date=created_date)        
        return redirect('showsession')
    return render(req,'editsession.html',{'show': qw})
def updatedata(req,id):
    pass
def addstudent(req):
    if req.method=='POST':
        name=req.POST['name']
        emailaddress=req.POST['emailaddress']
        contactno=req.POST['contactno']
        gender=req.POST['gender']
        stu=Student(name=name,emailaddress=emailaddress,contactno=contactno,gender=gender,password=12345,fees=0)
        stu.save()
        subject = 'Welcome to Biotech Park Lucknow – Your Online Admission Details'
        message = f'''
        Dear {name},
        Welcome to Biotech Park Lucknow!
        We are thrilled to have you join our community. Below are your login details to access the Nou Egyan portal for your online admission process:
        Portal Link: biotechpark.org.in
        Username: {emailaddress}
        Password:{12345}

        Important Instructions:

        1.Log In: Use the provided credentials to log into Biotech park.
     2.Complete Admission Form: Fill out the online admission form with accurate details.
     3.Submit Required Documents: Upload all necessary documents as specified on the portal.
     4.Check Status: Regularly check your portal for updates on your admission status.
     5.Should you encounter any issues or have any questions, please do not hesitate to reach out to our support team at [Insert Contact Information].

     We look forward to your successful admission and to welcoming you to Biotech Park Lucknow!

     Best regards,

     [Rohit Kumar]
     [CTO Softpro India]
     Biotech Park Lucknow
     [7080102008]
     [softproindia.in]


        

     Please keep this information secure and do not share it with anyone.
        '''
        from_email = 'arin9450434099@gmail.com'
        recipient_list = [emailaddress]

        # Send email
        send_mail(subject, message, from_email, recipient_list)

        # Add success message and redirect
        messages.success(req, 'Registration successful! Please check your email for confirmation.')

    return render(req,'addstudent.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def studentdash(req):
    if 'studentid' in req.session:
        studentid=req.session['studentid']
        stu=Student.objects.get(emailaddress=studentid)
        asign=""
        if stu.status=="A":
            asign="yes"
        return render(req,'studentdash.html',{'asign':asign,'stu':stu})
    else:
        return redirect('login')
def application(req):
    try:
        if req.session['studentid']!=None:
            stuid=req.session['studentid']
            stu=Student.objects.get(emailaddress=stuid)
            ses=tbl_session.objects.all()
            course=tbl_course.objects.all()
            return render (req,'application.html',{'stu':stu , 'ses':ses , 'course':course})
    except KeyError:
        return redirect('login')
    
def saveinfo(req):
    if req.method=="POST":
        name=req.POST['name']
        fname=req.POST['fname']
        mname=req.POST['mname']
        gender=req.POST['gender']
        emailaddress=req.POST['emailaddress']
        contactno=req.POST['contactno']
        dob=req.POST['dob']
        aadharno=req.POST['aadharno']
        address=req.POST['address']
        session=req.POST['session']
        course=req.POST['course']
        hs_percent=req.POST['hs_percent']
        inter_percent=req.POST['inter_percent']
        c=tbl_course.objects.get(course_name=course)
        fees=c.course_fees
        course_duration=c.course_duration
        Student.objects.filter(emailaddress=emailaddress).update(name=name,fname=fname,mname=mname,gender=gender,contactno=contactno,dob=dob,aadharno=aadharno,address=address,session=session,course=course,hs_percent=hs_percent,inter_percent=inter_percent,fees=fees,course_duration=course_duration)
        return redirect ('application')

def showstudent(req):
    uy=Student.objects.all()
    return render (req,'showstudent.html',{'ow':uy})
def uploaddoc(req):
    if req.method=='POST':
        stuid=req.session['studentid']
        stu=Student.objects.get(emailaddress=stuid)
        pic=req.FILES['pic']
        aadharpic=req.FILES['aadharpic']
        hs_marksheet=req.FILES['hs_marksheet']
        inter_marksheet=req.FILES['inter_marksheet']
        sign=req.FILES['sign']
        fs=FileSystemStorage()
        picfile=fs.save(pic.name,pic)
        aadharfile=fs.save(aadharpic.name,aadharpic)
        hsfile=fs.save(hs_marksheet.name,hs_marksheet)
        interfile=fs.save(inter_marksheet.name,inter_marksheet)
        signfile=fs.save(sign.name,sign)
        stu.pic=picfile
        stu.aadharpic=aadharfile
        stu.hs_marksheet=hsfile
        stu.inter_marksheet=interfile
        stu.sign=signfile
        stu.application_status="C"
        stu.save()
        return redirect('studentdash')

def verifydoc(req):
    students=Student.objects.filter(application_status="C")
    return render(req,'verifydoc.html',{'students':students})   

def admindash(req):
    return render(req,'admindash.html')   

def verifystu(req,id):
    Student.objects.filter(sid=id).update(application_status="V")
    return redirect('verifydoc')

def payfees(req):
    studentid=req.session['studentid']
    stu=Student.objects.get(emailaddress=studentid)
    vs=""
    if stu.application_status=="V":
        vs="yes"
    return render(req,'payfees.html',{'stu':stu,'vs':vs})

def finalsubmit(req):
    studentid=req.session['studentid']
    stu=Student.objects.get(emailaddress=studentid)
    if req.method=="POST":
        fees_ss=req.FILES['fees_ss']
        fs=FileSystemStorage()
        feesfile=fs.save(fees_ss.name,fees_ss)
        stu.fees_ss=feesfile
        stu.fees_status="P"
        stu.save()
        subject = '📢📢 Congratulations! Your Admission is Confirmed 📢📢'
        message = f'''
        Dear [{stu.name}],
        Here are the details of your admission
        Name: [{stu.name}]
        Course Enrolled: [{stu.course}]
        Session: [{stu.session}]
        We look forward to welcoming you to our campus and are excited to have you join our academic community. Please make sure to keep an eye on your email for any further instructions and important updates regarding the start of your course and orientation activities.

         If you have any questions or need further assistance, feel free to contact our support team at [Support Email] or [Support Phone Number].

        Once again, congratulations and best wishes for your upcoming academic journey!

        Warm regards,

     [Rohit Kumar]
     [CTO Softro india]
     [Softpro India Computer Technology Lucknow]
     [7080102008]
     
        '''
        from_email = 'arin9450434099@gmail.com'
        recipient_list = [stu.emailaddress]
   
        # Send email
        send_mail(subject, message, from_email, recipient_list)

        # Add success message and redirect
        messages.success(req, 'Registration successful! Please check your email for confirmation.')
        return redirect('studentdash')
    return render (req,'finalsubmit.html',{'stu':stu})

def finalverification(req):
    students=Student.objects.filter(fees_status="P",status="")
    return render(req,'finalverification.html',{'students':students})

def assign(req,id):
    stu=Student.objects.filter(sid=id).update(status="A")
    return redirect('finalstudents')

def finalstudents(req):
    students=Student.objects.filter(status="A")
    return render (req,'finalstudents.html',{'students':students})

def logout(req):
    req.session.flush()
    return redirect('login')

def changepass(req):
    return render(req,'changepass.html')

def changesave(req): 
    if 'studentid' in req.session:
        userid=req.session.get('studentid')
        user=Student.objects.filter(emailaddress=userid).first()
        password=req.POST['password']
        confpass=req.POST['confpass']
        if user:
            user.password=password
            user.save()
        return redirect('login')
    else:
        return redirect('login')