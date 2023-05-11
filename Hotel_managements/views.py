from django.shortcuts import render,redirect
from Hotel_managements.models import Hotel
from Hotel_managements.reservation_model import Reservation
from Hotel_managements.forms import HotelForm
from Hotel_managements.Employee_form import EmployeeForm
from Hotel_managements.Employee_model import Employee_Member
from Hotel_managements.reservation_form import ReservationForm, BookingCheckout
from Hotel_managements.admin_model import Administration
from Hotel_managements.admin_form import AdminForm

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import django.core.exceptions



from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


import time
# Create your views here.



class LoginRegister():
    def Register(request):
        employee = Hotel.objects.all()
        if request.method == 'POST':
            form = HotelForm(request.POST)
            if form.is_valid():
                # Check if username already exists in the database
                if Hotel.objects.filter(username=form.cleaned_data['username']).exists():
                    # If username already exists, return an error message
                    messages.error(request, 'Username already exists')
                    return redirect('/register')
                else:
                    try:
                        form.save()
                        return redirect('/')        
                    except:
                        pass
        else:
            form = HotelForm()
        return render(request, 'register.html', {'form':form})

    @cache_control(no_cache=True, must_revalidate=True,no_store=True)   
    def Login(request):
        if 'username' in request.session:
            return redirect('/dashboard/')

        if request.method == 'POST':
            if 'username' in request.POST:
                # Handle customer login
                username = request.POST['username']
                password = request.POST['password']
                try:
                    user = Hotel.objects.get(username=username)
                    if user.check_password(password):
                        request.session['username'] = username
                        name = user.Employee_Name
                        return redirect('/dashboard/', {'names':name})
                    else:
                        return render(request, 'login.html', {'error_message': 'Invalid password'})
                except Hotel.DoesNotExist:
                    return render(request, 'login.html', {'error_message': 'Invalid username'})
        else:
            return render(request, 'login.html')


    def employee_login(request):

        if request.method == 'POST':
            if 'emp_username' in request.POST:
                # Handle customer login
                emp_username = request.POST['emp_username']
                emp_password = request.POST['emp_password']
                try:
                    user = Employee_Member.objects.get(emp_username=emp_username)
                    if user.check_password(emp_password):
                        request.session['emp_username'] = emp_username
                        name = user.Employees_Name
                        return redirect('/dashboard/', {'names':name})
                    else:
                        return render(request, 'login.html', {'error_message': 'Invalid password'})
                except Employee_Member.DoesNotExist:
                    return render(request, 'login.html', {'error_message': 'Invalid username'})
        else:
            return render(request, 'login.html')
        
        
class Dashboard():

    def __init__(self):
        pass
            
            
    
    def authorize(request):

    # rest of the code
    
        if 'username' in request.session:
                username = request.session['username']
                
                
                
                user = Hotel.objects.get(username=username)
                
                global name 
                global reservation
                
                
                name = user.Employee_Name
                global user_id
                user_id = user.id
                global reservations
                reservations = Reservation.objects.all().order_by('user_update')
                global form 
                form = ReservationForm()
                    
                reservation = Reservation.objects.get(user_id = user_id)
    
     
    def employe_authorize(request):
        emp_username = request.session['emp_username']
        
        employ = Employee_Member.objects.get(emp_username=emp_username)
        global name,jobs,level,email,salary,emp_id

        name = employ.Employees_Name 
        
        jobs = employ.type_job 
        print(jobs)
        salary = employ.salary
        emp_id = employ.emp_id
        level = employ.level 
 
        email = employ.emp_username
        
    @cache_control(no_cache=True, must_revalidate=True,no_store=True)           
    def user(request):
        
        
        global customer
        customer = request.session.get('username')
        global employee
        employee = request.session.get('emp_username')
        admin = request.session.get('admin_username')
        global acc
        if not customer and not employee:
            return redirect('/')
        
        if customer:
            
            Dashboard.authorize(request)
            
            
            room = reservation.room_type
            date = reservation.checkin_date
            
             # Count the number of reservations
            check_in_count = Reservation.objects.filter(user_update='checkin').count()
            print(check_in_count)


            single_room = Reservation.objects.filter(room_type = 'single',user_update='checkin').count()
            single_room_limit = 6

            double_room = Reservation.objects.filter(room_type = 'double',user_update='checkin').count()
            double_room_limit = 6

            triple_room = Reservation.objects.filter(room_type = 'triple',user_update='checkin').count()
            triple_room_limit = 8
            
            # Display message that check-in is full
            single_room_left = single_room_limit - single_room
            double_room_left = double_room_limit - double_room
            triple_room_left = triple_room_limit - triple_room
            
            
            single_rooms = Reservation.objects.filter(room_type = 'single').count()
            double_rooms = Reservation.objects.filter(room_type = 'double').count()
            triple_rooms = Reservation.objects.filter(room_type = 'triple',).count()
            acc = "customer"
            return render(request, 'dashboard.html',
                    { 'accounts':acc,'date':date,'room':room,'name': name, 'reservations': reservations,'id':user_id,'form': form, "check_in_left":check_in_count,
                        "single_room":single_room_left, "double_room":double_room_left,"triple_room":triple_room_left,
                        'Single':single_rooms, 'Double':double_rooms, 'Triple':triple_rooms
                    })
        elif employee:
            
            Dashboard.employe_authorize(request)
            
            acc = "employee"
            
            return render(request, 'dashboard.html',{ 'name':name, 'accounts':acc, 'type':jobs})
            

       

        
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def Logout(request):
        request.session.flush()
        return redirect('Login')
        
    def reservation(request):
        if 'username' not in request.session:
            return redirect('/')  # redirect to login page
        Dashboard.authorize(request)
            
            
        # Count the number of reservations
        check_in_count = Reservation.objects.filter(user_update='checkin').count()
        # Set the maximum limit of check-ins
        check_in_limit = 20

        single_room = Reservation.objects.filter(room_type = 'single').count()
        single_room_limit = 6

        double_room = Reservation.objects.filter(room_type = 'double').count()
        double_room_limit = 6

        triple_room = Reservation.objects.filter(room_type = 'triple').count()
        triple_room_limit = 8
        
        # Display message that check-in is full
        check_in_left = check_in_limit - check_in_count
        single_room_left = single_room_limit - single_room
        double_room_left = double_room_limit - double_room
        triple_room_left = triple_room_limit - triple_room
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                room_type = form.cleaned_data.get('room_type')
                if room_type == "double":
                    if double_room_left == 0:
                        messages.error(request, "Room Type Double is full")
                        return redirect('/dashboard/')
                    
                elif room_type == "single":
                    if single_room_left == 0:
                        messages.error(request, "Room Type Single is full")
                        return redirect('/dashboard/')
                
                elif room_type == "triple":
                    if triple_room_left == 0:
                        messages.error(request, "Room Type Triple is full")
                        return redirect('/dashboard/')
                
                # Check if the check-in limit has been reached
                try:
                    reservation = Reservation.objects.filter(user_id=user_id).first()
                    if reservation is not None:

                        reservation.user_id = user_id 
                        form = ReservationForm(request.POST, instance=reservation)
                        reservation.checkin_date = datetime.now()
                        reservation.checkin_time = datetime.now().time()
                        form.save()
                            
                        messages.success(request, 'Reservation updated successfully!')
                                
                    else:
                        raise Reservation.DoesNotExist

                except Reservation.DoesNotExist:
                    # Create a new reservation
                    reservation = form.save(commit=False)
                    reservation.user_id = user_id
                    reservation.checkin_date = datetime.now()
                    reservation.checkin_time = datetime.now().time()

                    reservation.save()
                    messages.success(request, 'New Reservation successfully!')
                    
            return redirect('/dashboard/')
            
        return render(request, 'dashboard.html')
        
    


    def User_update(request):
        if 'username' in request.session:
            username = request.session['username']
            try:
                user = Hotel.objects.get(username=username)
                user_id = user.id
                check_out_count = Reservation.objects.filter(user_update='checkout').count()
                check_out_limit = 20

                single_room = Reservation.objects.filter(room_type = 'single').count()
                single_room_limit = 6

                double_room = Reservation.objects.filter(room_type = 'double').count()
                double_room_limit = 6

                triple_room = Reservation.objects.filter(room_type = 'triple').count()
                triple_room_limit = 8
                
                if request.method == "POST":
                    form = ReservationForm(request.POST)
                    if form.is_valid():
                        # Check if the check-out limit has been reached
                        if check_out_count < check_out_limit:
                            try:
                                # Try to update the existing reservation
                                reservation = Reservation.objects.get(user_id=user_id)
                                form = ReservationForm(request.POST, instance=reservation)
                                form.save()
                            except Reservation.DoesNotExist:
                                # Create a new reservation
                                reservation = form.save(commit=False)
                                reservation.user_id = user_id
                                reservation.save()
                        else:
                            # Display message that check-out is full
                            check_out_left = check_out_limit - check_out_count
                            single_room_left = single_room_limit - single_room
                            double_room_left = double_room_limit - double_room
                            triple_room_left = triple_room_limit - triple_room
                            messages.error(request, f"Check-out is full. Only {check_out_left} check-out(s) left.")
                            messages.error(request, f"Single room is full. Only {single_room_left} Single room(s) left.")
                            messages.error(request, f"Double room is full. Only {double_room_left} Double room(s) left.")
                            messages.error(request, f"Triple room is full. Only {triple_room_left} Triple room(s) left.")
                            return redirect('/dashboard/')
                return render(request, 'dashboard.html')
            except Hotel.DoesNotExist:
                return render(request, 'dashboard.html',{'error_message': 'Invalid username'})

    
class Employee(Dashboard):
    @cache_control(no_cache=True, must_revalidate=True,no_store=True)
    def employee_view(request):
        if not request.session.get('emp_username'):
            return redirect('/')  # redirect to login page
        Dashboard.employe_authorize(request)
        Dashboard.user(request)
        employ = Employee_Member.objects.values('type_job').distinct()
        
        
        return render(request, 'employee.html', {'name':name,'accounts':acc,'type':jobs,'employ': employ})
    
    def get_employees(request,type_job):
        employees = []
        
        search = request.GET.get('search')
        employs = Employee_Member.objects.filter(type_job=type_job)
        employss = Employee_Member.objects.filter(type_job=type_job)
        job = type_job
        status = "active"
        Admin.admin_view(request)
        
        if search:
            employs = employs.filter(Q(Employees_Name__icontains = search))
            if employs.exists():
                message = None
                paginator = Paginator(employs,10) # Show 10 employees per page
                page = request.GET.get('page')
                employees = paginator.get_page(page)
                return render(request, 'view_employee.html', {'status':status,'employs': employss,'employ': employees,'name':name, 'accounts':acc,'job':job})  
            else:
                message = "No data found for the search query: {}".format(search)
        
        else:
            message = None
            paginator = Paginator(employs,6) # Show 10 employees per page
            page = request.GET.get('page')
            employees = paginator.get_page(page)
        return render(request, 'view_employee.html', {'status':status,'employs': employss,'employ': employees,'name':name, 'accounts':acc,'job':job})  
    

    
    
class Service(Dashboard):
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def service_view(request):
        
        
        
        customer = request.session.get('username')
        employee = request.session.get('emp_username')
        if not customer and not employee:
            return redirect('/')
        

        if customer:
            Dashboard.user(request)
            return render(request, 'service.html',{'name':name,'accounts':acc})
            
        
        if employee:
            Dashboard.employe_authorize(request)
            if jobs != "housekeeping manager":
                return redirect('/dashboard/')
            
           
            print("jobs", jobs)
            return render(request, 'service.html',{'name':name,'accounts':acc, 'type':jobs})
       

        


class Payroll(Dashboard):
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def payroll_view(request):
        if 'emp_username' not in request.session:
            return redirect('/')  # redirect to login page
        Dashboard.employe_authorize(request)
        Dashboard.user(request)
        
        
        
        return render(request, 'payroll.html', {'emp_id':emp_id,'name':name,'accounts':acc,'type':jobs, 'email':email, 'level':level,'salary':salary})

    def payment_method(request,emp_id):
              
        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            if payment_method in ('transfer', 'cheque'):
                # Get the specific Employee_Member instance
                employee = Employee_Member.objects.get(emp_id=emp_id)
               
                # Update the payment method for that instance
                employee.payment_method = payment_method.capitalize()
                # Save the instance to persist the changes in the database
                employee.save()
                
                return redirect('/payroll/')

class Admin(Dashboard):
    
    def create_admin(request):
        form = AdminForm()
        
        
        if request.method == "POST":
            form = AdminForm(request.POST)
            
            if form.is_valid():
                if Administration.objects.filter(admin_username=form.cleaned_data['admin_username']).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('/admin_create/')
                else:
                    try:
                        form.save()
                        return redirect('/admin_login/')
                    except:
                        pass
                    
        return render(request, 'admin_form.html', {'form':form})
    
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def login_admin(request):
        
        if request.method == 'POST':
            usernames = request.POST['admin_username']
            passwords = request.POST['password']
            
            try:
                admin_user = Administration.objects.get(admin_username=usernames)
                
                if admin_user.check_password(passwords):
                    request.session['admin_username'] = usernames
                    return redirect('/admin_panel/')
                else:
                    return render(request, 'admin_login.html', {'error_message': 'Invalid password'})
            
            except Administration.DoesNotExist:
                return render(request, 'admin_login.html', {'error_message': 'Invalid username'})
        else:
            return render(request, 'admin_login.html')

        
        #return render(request, 'admin_form.html', {'form':form})
    
        
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def admin_view(request):
        
        if not request.session.get('emp_username'):
            return redirect('/')
        if not request.session.get('admin_username'):
            return redirect('/admin_login/')
        
        Dashboard.employe_authorize(request)
        Dashboard.user(request)
        
        username = request.session['admin_username']
        form = EmployeeForm()
        admin_user = Administration.objects.get(admin_username=username)
        
        global name
        name = admin_user.Name
        global employ
        employ = Employee_Member.objects.values('type_job').distinct()
        
       
        return render(request, 'admin.html', {'form':form, 'name':name, 'accounts':acc,'employ': employ})
    
    
    def create_employees(request):
       
        if request.method == "POST":
            form = EmployeeForm(request.POST)
            if form.is_valid():
                # Check if username already exists in the database
                if Employee_Member.objects.filter(emp_username=form.cleaned_data['emp_username']).exists():
                    # If username already exists, return an error message
                    messages.error(request, 'Username already exists')
                    return redirect('/admin_panel/')
                else:
                    try:
                        form.save()
                        messages.success(request, "Employee Added Successfully")
                        return redirect('/admin_panel/')
                    except:
                        pass
        else:
            form= EmployeeForm()
        return render(request, 'admin.html')

        
    

    def get_employee(request,type_job):
        
       
        
        Admin.admin_view(request)
        form = EmployeeForm()
        
        employees = []
        
        search = request.GET.get('search')
        employs = Employee_Member.objects.filter(type_job=type_job)
        job = type_job
        status = "active"
        if search:
            employs = employs.filter(Q(Employees_Name__icontains = search))
            if employs.exists():
                message = None
                paginator = Paginator(employs,10) # Show 10 employees per page
                page = request.GET.get('page')
                employees = paginator.get_page(page)
                return render(request, 'job_details.html', {'status':status,'form':form,'employ': employees,'name':name, 'accounts':acc,'job':job})   
            else:
                message = "No data found for the search query: {}".format(search)
        else:
            message = None
            paginator = Paginator(employs,5) # Show 10 employees per page
            page = request.GET.get('page')
            employees = paginator.get_page(page)
        return render(request, 'job_details.html', {'status':status,'form':form,'employ': employees,'name':name, 'accounts':acc,'job':job})  
    
    
   
    
    def status(request,emp_id,type_job):
              
        if request.method == 'POST':
            status = request.POST.get('status')
            if status in ('Inactive', 'Active'):
                # Get the specific Employee_Member instance
                employee = Employee_Member.objects.get(emp_id=emp_id,type_job=type_job)
               
                # Update the payment method for that instance
                employee.status = status.capitalize()
                # Save the instance to persist the changes in the database
                employee.save()
                
                return redirect('/employee_detail/' + type_job + '/')



    def update_info(request, emp_id, type_job):
        try:
            employee = Employee_Member.objects.get(emp_id=emp_id, type_job=type_job)
        except Employee_Member.DoesNotExist:
            raise Employee_Member.DoesNotExist
        
        if employee is not None:
            if request.method == "POST":
                employee.Employees_Name = request.POST.get('Employees_Name')
                employee.emp_username = request.POST.get('emp_username')
                employee.emp_password = request.POST.get('emp_password')
                employee.salary = request.POST.get('salary')
                employee.type_job = request.POST.get('type_job')
                employee.gender = request.POST.get('gender')
                employee.level = request.POST.get('level')
                employee.payment_method = request.POST.get('payment_method')
                employee.save()
                return redirect('/employee_detail/' + type_job + '/')
            
            



        
class Booking(Admin):
    def __init__(self):
        pass
        
    @cache_control(no_cache=True, must_revalidate=True,no_store=True) 
    def date(request):
        
        if not request.session.get('emp_username'):
            return redirect('/')
        
        
        if not request.session.get('admin_username'):
            return redirect('/admin_login/')
        
        Admin.admin_view(request)
        
        Admin.employe_authorize(request)
        
        employees = []
        
        search = request.GET.get('search')
        reservations = Reservation.objects.all().order_by('user_update')
        
        if search:
            reservations = reservations.filter(Q(user__Employee_Name__icontains = search)) 
            
            if reservations.exists():
                message = None
                paginator = Paginator(reservations,10) # Show 10 employees per page
                page = request.GET.get('page')
                employees = paginator.get_page(page)
        
                form = BookingCheckout()
                
                
                return render(request, 'booking.html', {'reservation':employees, 'form':form,'message':message, 'name':name})
            
            else:
                message = "No data found for the search query: {}".format(search)
        else:
            form = BookingCheckout()
            message = None
            paginator = Paginator(reservations, 7) # Show 10 employees per page
            page = request.GET.get('page')
            employees = paginator.get_page(page)
        return render(request, 'booking.html', {'reservation':employees,'message':message,'name':name,'accounts':acc})
    
    def checkout(request,user_id):
        
        reservation = Reservation.objects.get(user_id=user_id)
        print(reservation, "reservation")
        
        reservations = Reservation.objects.all()
        if request.method == "POST":
            form = BookingCheckout(request.POST, instance = reservation)
            if form.is_valid():
                reservation.user_update = form.cleaned_data.get('user_update')
                reservation.Quantity = 0

                reservation.checkout_date = datetime.now()
                reservation.checkout_time = datetime.now().time()
                form.save()
                messages.success(request, 'Reservation checkout successfully!')
            
                return redirect('/booking/')
        
            else:
                form = BookingCheckout(instance=reservation)
        return render(request, 'booking.html', {'reservations':reservations,'form':form})
        
        
    
        
    def email():
        pass