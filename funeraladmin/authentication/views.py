from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Employee,EmployeeAddress
from members.models import Transaction
from random import randrange
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
import rsaidnumber


decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='Admin').exists())]
decoraters1 = [login_required(login_url='/auth/login'),]
# Create your views here.
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have Successfully Logged Out')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user= auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)

                    messages.success(request,"Welcome "+ user.first_name + " " + user.last_name+ ". You are now logged in.")

                    return redirect('homepage')

                messages.success(request,"Account is not active. Please verify email.")
                return render(request, 'authentication/login.html')

            messages.success(request, "Invalid login credentials. Try again.")
            return render(request, 'authentication/login.html')

        messages.success(request, "Email and password fields cannot be empty.")
        return render(request, 'authentication/login.html')

@method_decorator(decoraters,name='dispatch')
class RegisterStaffView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        context = {
            'user': user,
        }
        return render(request, 'authentication/register.html',context)

    def post(self,request):
        name = request.POST['name']
        surname = request.POST['surname']
        idnum = request.POST['idnum']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']
        contacts = request.POST['contacts']
        email = request.POST['email']
        role = request.POST['role']
        passW = request.POST['password']
        confirmPassW = request.POST['password1']


        if passW == confirmPassW:

            if len(passW) < 6:
                messages.error(request, "Password too short")
                return render('add-staff')

            if len(idnum) > 13:
                messages.error(request, "Identity number is too long")
                return render('add-staff')

            idchecker = rsaidnumber.parse(idnum, False)

            if not idchecker.valid:
                messages.error(request, "Invalid Identity Number")
                return redirect('add-staff')

            exists = True
            while exists:

                digits = ""
                for i in range(0, 8):
                    value = randrange(0, 10)
                    digits = digits + str(value)

                employeeNo ="STA"+ digits
                if not Employee.objects.filter(employee_no=employeeNo).exists():
                    if not User.objects.filter(username=employeeNo).exists():
                        if not Transaction.objects.filter(processed_by=employeeNo).exists():
                            exists = False


                new_user = User.objects.create_user(username=employeeNo,email=email,first_name=name,last_name=surname)
                new_user.set_password(passW)
                new_user.save()

                user = User.objects.get(username=employeeNo)

                employee = Employee.objects.create(user=user,employee_no=employeeNo,full_name=name,surname=surname,identity_no=idnum,gender=gender,contacts=contacts,email=email,role=role)
                employee.save()

                employee_model = Employee.objects.get(employee_no=employeeNo)

                addr = EmployeeAddress.objects.create(employee=employee_model,street=address,city=city,province=province,zip=zipcode)
                addr.save()

                messages.success(request,"Employee added successfully")
                messages.success(request, "Employee Number: "+ str(employeeNo))
                return redirect('staff-members')

@method_decorator(decoraters,name='dispatch')
class StaffMembersView(View):
    def get(self, request):

        user = Employee.objects.get(user=request.user)

        if 'q' in request.GET:
            q = request.GET['q']
            multi_q = Q(Q(employee_no__icontains=q)|Q(full_name__icontains=q)|Q(surname__icontains=q)|Q(identity_no__icontains=q)|Q(gender__iexact=q)|Q(contacts__icontains=q)|Q(email__icontains=q)|Q(role__icontains=q))
            staff = Employee.objects.filter(multi_q).order_by('-id')
        else:
            staff = Employee.objects.all().order_by('-id')
        paginator = Paginator(staff, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)


        context = {
            'page_obj': page_obj,
            'user': user,
        }

        return render(request, 'authentication/staff.html',context)

@method_decorator(decoraters,name='dispatch')
class EmployeeProfile(View):
    def get(self, request,id):
        user = Employee.objects.get(user=request.user)
        employee = Employee.objects.get(pk=id)
        employeeStats = User.objects.get(username=employee.employee_no)
        addr = EmployeeAddress.objects.get(employee=employee)

        context = {
            'employee': employee,
            'address': addr,
            'stats': employeeStats,
            'user': user,
        }
        return render(request, 'authentication/employee.html', context)

    def post(self,request,id):
        employee = Employee.objects.get(pk=id)
        newaddress = EmployeeAddress.objects.get(employee=employee)

        name = request.POST['name']
        surname = request.POST['surname']
        idnum = request.POST['idnum']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']
        contacts = request.POST['contacts']
        email = request.POST['email']
        role = request.POST['role']


        if len(idnum) > 13:
            messages.error(request,"Identity Number is too long")
            return redirect('employee-profile',employee.id)

        idchecker = rsaidnumber.parse(idnum, False)

        if not idchecker.valid:
            messages.error(request, "Invalid Identity Number")
            return redirect('employee-profile',employee.id)

        employee.full_name = name
        employee.surname = surname
        employee.identity_no = idnum
        employee.gender = gender
        employee.contacts = contacts
        employee.email = email
        employee.role = role
        employee.save()

        newaddress.street = address
        newaddress.city = city
        newaddress.province = province
        newaddress.zip = zipcode
        newaddress.save()

        messages.success(request,"Staff details updated")
        return redirect('employee-profile',employee.id)


@method_decorator(decoraters,name='dispatch')
class DeleteEmployee(View):
    def get(self, request,id):
        employee = Employee.objects.get(pk=id)
        user = employee.user
        user.delete()

        messages.success(request,"Employee deleted successfully")
        return redirect('staff-members')










