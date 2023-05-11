"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Hotel_managements.views import LoginRegister, Dashboard, Booking, Employee,Service,Admin,Payroll
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginRegister.Login, name="Login"),
    path('employee_login/', LoginRegister.employee_login, name="employee_login"),
    path('register/', LoginRegister.Register, name="Register"),
    path('dashboard/', Dashboard.user, name="dashboard"),
    path('dashboard/reservation/', Dashboard.reservation, name="reservation"),
    path('logout/', Dashboard.Logout, name="Logout"),
    path('booking/', Booking.date, name="booking"),
    path('booking/update/<int:user_id>/', Booking.checkout, name = "checkout"),
    path('employee/', Employee.employee_view, name="employee"),
    path('view_employee/<str:type_job>/', Employee.get_employees, name='view_employee'),
    path('service/', Service.service_view, name="service"),
    path('payroll/', Payroll.payroll_view, name="payroll"),
    path('admin_panel/', Admin.admin_view, name="admin"),
    path('admin_login/', Admin.login_admin, name="login_admin"),
    path('admin_create/', Admin.create_admin, name="new_admin"),
    path('add_emp/', Admin.create_employees, name="add_employee"),
    path('employee_detail/<str:type_job>/', Admin.get_employee, name='employee_detail'),
    path('payment_method/<int:emp_id>/', Payroll.payment_method, name='payment_method'),
    path('status/<str:type_job>/<int:emp_id>/', Admin.status, name='status'),
    path('update/<str:type_job>/<int:emp_id>/', Admin.update_info, name='update'),
    
]
