import email
from urllib import request
# from xmlrpc.server import _DispatchArity1
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import TempUser, Donor
from request.models import Request, Status
import uuid
from django.db import transaction
from django.template import RequestContext
User = get_user_model()
"""
functions are defined in accending order
"""


def change_password(request, token=None):
    """
    this function gets the user form  given token and sets the password field of that user
    """
    try:
        with transaction.atomic():
            if request.method == 'POST':
                msg = 'password changed successfully'
                password = request.POST['password']
                try:
                    user = User.objects.get(token=uuid.uuid5(
                        uuid.NAMESPACE_X500, str(token)))
                    user.set_password(password)
                    user.token = uuid.uuid4()
                    user.save()
                except:
                    msg = "Invalid token"
                messages.info(request, msg)
                return redirect('/')
            else:
                return render(request, 'change_password.html', {'token': token})
    except:
        return redirect('/')  # redirecting if the token is inncorrect


def donor_edit(request):
    
    with transaction.atomic():
        msg = ''
        if request.method == 'POST':
            try:
                name= request.POST['name']
                blood = request.POST['blood']
                age = request.POST['age']
                phone=request.POST['phone']
                city = request.POST['city']
                district = request.POST['district']
                state = request.POST['state']
                country = request.POST['country']
                pincode = request.POST['pincode']
                if request.user.is_authenticated:
                    try:
                        obj = Donor.objects.get(email=request.user)
                        try:
                            obj.name=name
                            obj.blood = blood
                            obj.age = age
                            obj.pincode = pincode
                            obj.city = city
                            obj.district = district
                            obj.state = state
                            obj.country = country
                            obj.email = request.user
                            obj.save()
                            msg = 'successfully saved'
                        except:
                            msg = 'invalid values, please try again'
                    except:
                        msg = 'not registered as donor'
                else:
                    msg = 'you are not authenticated'
            except:
                msg = f'error occured, please try again '
        messages.info(request, msg)
        return redirect('/login')


def donor_register(request):
    """
    gets the details using post, checking authentication of request.user , check if the user  exist in donor table
    ,if not donor object is created
    """
    with transaction.atomic():
        msg = ''
        if request.method == 'POST':
            try:
                name= request.POST['name']
                blood = request.POST['blood']
                age = request.POST['age']
                phone=request.POST['phone']
                city = request.POST['city']
                district = request.POST['district']
                state = request.POST['state']
                country = request.POST['country']
                pincode = request.POST['pincode']
                # rollno = request.POST['rollno']
                # instituition = request.POST['instituition']
              
                if request.user.is_authenticated:
                 
                    if not Donor.objects.filter(email=request.user).exists():
                        
                        obj = Donor.objects.create(email=request.user, name=name,blood=blood, age=age,phone=phone, city=city, district=district,
                                                   state=state, country=country,pincode=pincode, 
                                                #    roll_no=rollno, instituition=instituition
                        )
                        obj.save()
                    else:
                        
                        msg = 'already registered as a donor'
                else:
                   
                    msg = 'you are not authenticated'
            except:
                
                msg = f'error occured, please try again '
        messages.info(request, msg)
        return redirect('/login')


def forget_password(request):
    """
    get he email using post, get the according user object, generating token using uuid4() , save this token in token field using uuid5,the link is sent  for changing password(token is appened at end) through email
    """
    with transaction.atomic():
        msg = ''
        if request.method == 'POST':
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                if user:
                    token = uuid.uuid4()
                    user.token = uuid.uuid5(uuid.NAMESPACE_X500, str(token))
                    user.save()
                    msg = f'A mail sent to {email}'
                    # instead of mailing
                    print(f'{settings.URL_OF_THE_WEBSITE}change_password/{token}')
            except:
                msg = 'Invalid Email'
            messages.info(request, msg)
        return render(request, 'get_email.html')


def home(request):
    return render(request, 'home.html')



def login_user(request):
    """
    #if the method is not post check if the request.user is authenticated , if yes set user to request.user 
    #if the method is post the details are recieved using post , then authenticate the user using its email and pwd
    #then login the user 
    #required details like donations , my requests(status table) are attached as dictionary in the render()
    #in status of table - it contains all status table rows of request tabel row    which match the user feild to the user's email    [donor_identified and request_id fields are additionally added]
    #in donations - take the rows in status table which matches donor id and get the row of request table rows using reqid , then added a another field called donated date (line 189)
    """
    with transaction.atomic():
        user = None
        if request.user.is_authenticated:
            try:
                user = User.objects.get(email = request.user)
            except:
                return render(request,'home.html')   
        elif request.method == 'POST':   
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
        else:
            return render(request,'home.html')    
        try:         
            if user is not None:
                login(request, user)
                
                is_donor = True
                user_requests = Request.objects.filter(user = user.email).order_by('reqid')
                status_of_requests = []
                rdetails=[]
                
                for req in user_requests:
                    rdetails1=Request.objects.get(reqid = req.reqid)
                    rdetails.append(rdetails1)
               
                for req in user_requests:
                    all_status = Status.objects.filter(reqid = req.reqid).order_by('id')
                    for single_status in all_status:
                        if single_status :
                            single_status.request_id = req.reqid
                            if not single_status.completed:
                                if single_status.currentstatus == settings.CURRENT_STATUS_DICT[2]:
                                    single_status.donor_identified = True
                                else :
                                    single_status.donor_identified = False
                               
                            status_of_requests.append(single_status)
                         
                donor_details= []
                donations_list = []
                try:
                    donor_details = Donor.objects.get(email = user.email)
                    donorid = donor_details.donorid
                    donations = Status.objects.filter(donorid = donorid)
                    donations_list = []
                    for donation in donations:
                        request_obj = donation.reqid
                        request_obj.donateddate = donation.donateddate
                        donations_list.append(request_obj)

                except:
                    is_donor = False  
                # request=Request.objects.get(email=user.email)
                # print(request)
                # zippedList=[]
                # zippedList = zip(rdetails,status_of_requests)
               
                global dict1
                dict1={'user': user, 'is_donor' : is_donor, 'donor_details' : donor_details,'donations' : donations_list, 'status' : status_of_requests,'rdetails':rdetails}
                return render(request, 'donor.html',dict1)
                
                
            else:

                if User.objects.filter(email = email).exists():
                    messages.info(request, 'password is incorrect')
                    messages.info(request, email)
                    messages.info(request, password)
                else:
                    messages.info(request, 'email is incorrect')
                    messages.info(request, email)
                    messages.info(request, password)
                return render(request,'home.html')   
        except:
            pass 
 
def logout_user(request):
    logout(request)
    return redirect('/')


def register(request, token):
    """
    get the token and match it in tempuser table to get the user details
    and create a new user in User table with this details
    """
    with transaction.atomic():
        try:
            user = TempUser.objects.get(token=token)
            if user:
                email = user.email
                password = user.password
                name = user.name
                phone = user.phone
                User.objects.create_user(
                    name=name, password=password, email=email, phone=phone, token=token)
                messages.info(request, 'account registered successfully')
                TempUser.objects.get(token=token).delete()
                return redirect('/')
        except Exception as e:
            pass


def signup_user(request):
  
    with transaction.atomic():
        print('Signup')
        if request.method == 'POST':
            email = request.POST['email']
            name = request.POST['name']
            password = request.POST['password']
            phone = request.POST['phone']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email unavailable')
                messages.info(request, name)
                messages.info(request, email)
                messages.info(request, password)

            else:
                token = uuid.uuid4()
                TempUser.objects.create(
                    name=name, password=password, email=email, phone=phone, token=token)
                messages.info(request, f'A mail sent to {email}')
                # instead of mailing
                print(f'{settings.URL_OF_THE_WEBSITE}register/{token}')
            return redirect('/')

        else:
            return redirect('/')


def user_edit(request):
    """
    check if the user is authenticated and set the fields of user
    """
    with transaction.atomic():
        msg = ''
        if request.method == 'POST':
            name = request.POST['name']
            phone = request.POST['phone']
            if request.user.is_authenticated:
                user = User.objects.get(email=request.user)
                user.name = name
                user.phone = phone
                user.save()
                messages.info(request, 'successfully saved')
                return redirect('/login')


def requestpage(request):
    return render(request, 'req-blood.html')


def loginpage(request):
    return render(request, 'login.html')


def signuppage(request):
    return render(request, 'signup.html')


def userreq(request):
    return render(request, 'userreq.html')


def yourdonationspage(request):
    return render(request, 'your_donations.html',dict1)


def yourrequestspage(request):
   
    return render(request, 'your_requests.html',dict1)


def donoreditpage(request):
    if dict1['is_donor'] == False:
        return render(request, 'donor.html',dict1)
    else:
        return render(request, 'donor-edit.html',dict1)

