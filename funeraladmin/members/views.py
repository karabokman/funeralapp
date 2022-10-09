from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Member,Transaction,Quote,Product,Spouse,Address,Kid,Dependant,Beneficiary,MemberProduct,InvoiceDetail,QuoteDetail
from authentication.models import Employee
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from random import randrange
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
import xlwt
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML,CSS
import tempfile
import rsaidnumber


decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='Admin').exists())]
decoraters1 = [login_required(login_url='/auth/login'),]

# Create your views here.
@method_decorator(decoraters1,name='dispatch')
class HomepageView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        members = Member.objects.all().order_by('-id')[:5]
        membersNo = len(Member.objects.all())
        overdue = len(Transaction.objects.filter(status='UNPAID'))
        staff = len(Employee.objects.all())
        quotes = len(Quote.objects.filter(status='UNPAID'))

        context = {
            'members': members,
            'membersNo': membersNo,
            'overdue': overdue,
            'staff': staff,
            'quotes': quotes,
            'user': user,
        }
        return render(request, 'members/index.html',context)

@method_decorator(decoraters1,name='dispatch')
class MembersView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        if 'q' in request.GET:
            q = request.GET['q']
            multi_q = Q(Q(policy_no__icontains=q)|Q(full_name__icontains=q)|Q(surname__icontains=q)|Q(identity_no__icontains=q)|Q(identity_no__icontains=q)|Q(gender__icontains=q)|Q(email__icontains=q)|Q(contacts__icontains=q)|Q(marital_status__icontains=q))
            members = Member.objects.filter(multi_q)
        else:
            if not user.role == 'STAFF':
                members = Member.objects.all().order_by('-id')
            else:
                members = Member.objects.none()

        paginator = Paginator(members, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'members/view-members.html',context)

@method_decorator(decoraters1,name='dispatch')
class AddMemberView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        options = Product.objects.all().order_by('id')

        context = {
            'options': options,
            'user': user,
        }
        return render(request, 'members/addmember.html',context)

    def post(self,request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        idnum = request.POST['idnum']
        contacts = request.POST['contacts']
        gender = request.POST['gender']
        marital = request.POST['marital']
        birthday = request.POST['birthday']
        address = request.POST['address']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']
        plan = request.POST['plan']

        idchecker = rsaidnumber.parse(idnum,False)

        if not idchecker.valid:
            messages.error(request, "Invalid Identity Number")
            return redirect('add-member')


        exists = True
        while exists:

            digits = ""
            for i in range(0, 8):
                value = randrange(0, 10)
                digits = digits + str(value)

            policyNo = digits
            if not Member.objects.filter(policy_no=policyNo).exists():
                exists = False

        if gender == 'GENDER':
            messages.error(request,"Choose gender")
            return redirect('add-member')
        if marital == 'MARITAL STATUS':
            messages.error(request, "Choose marital status")
            return redirect('add-member')




        addMember = Member.objects.create(policy_no=policyNo,full_name=name,surname=surname,identity_no=idnum,gender=gender,contacts=contacts,email=email,marital_status=marital,date_of_birth=birthday)
        addMember.save()

        memb = Member.objects.get(policy_no=policyNo)

        memaddr = Address.objects.create(member=memb,street=address,city=city,province=province,zip=zipcode)
        memaddr.save()

        product = Product.objects.get(name=plan)
        memplan = MemberProduct.objects.create(member=memb,product=product)
        memplan.save()

        if marital == 'MARRIED':
            mspouse = Spouse.objects.create(partner=memb)
            mspouse.save()

        messages.success(request,"Member added successfully")
        return redirect('member-profile',memb.id)

@method_decorator(decoraters1,name='dispatch')
class MemberProfileView(View):
    def get(self, request, id):
        user = Employee.objects.get(user=request.user)

        member = Member.objects.get(pk=id)
        if member.marital_status == 'MARRIED':
            if Spouse.objects.filter(partner=member).exists():
                spouse = Spouse.objects.get(partner=member)
        else:
            spouse = None
        kids = Kid.objects.filter(parent=member)
        depends = Dependant.objects.filter(member=member)
        if Beneficiary.objects.filter(member=member).exists():
            bene = Beneficiary.objects.get(member=member)
        else:
            bene = Beneficiary.objects.create(member=member)
            bene.save()
        if MemberProduct.objects.filter(member=member).exists():
            membCover = MemberProduct.objects.get(member=member)
        else:
            membCover = MemberProduct.objects.create(member=member)
            membCover.save()

        membAddress = Address.objects.get(member=member)

        options = Product.objects.all().order_by('id')

        context = {
            'member': member,
            'options': options,
            'spouse': spouse,
            'kids': kids,
            'depends': depends,
            'bene': bene,
            'membAddress': membAddress,
            'membCover': membCover,
            'user': user,
        }
        return render(request, 'members/member-profile.html',context)

    def post(self,request,id):
        member = Member.objects.get(pk=id)
        if MemberProduct.objects.filter(member=member).exists():
            membCover = MemberProduct.objects.get(member=member)
        else:
            membCover = MemberProduct.objects.create(member=member)
            membCover.save()
        membAddress = Address.objects.get(member=member)

        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        idnum = request.POST['idnum']
        contacts = request.POST['contacts']
        gender = request.POST['gender']
        marital = request.POST['marital']
        birthday = request.POST['birthday']
        address = request.POST['address']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']
        plan = request.POST['plan']
        inception = request.POST['inception']
        covered = request.POST['covered']

        if len(idnum) > 13:
            messages.error(request,"Identity number is too long")
            return redirect('member-profile', member.id)

        idchecker = rsaidnumber.parse(idnum, False)

        if not idchecker.valid:
            messages.error(request, "Invalid Identity Number")
            return redirect('member-profile', member.id)

        member.full_name = name
        member.surname = surname
        member.identity_no = idnum
        member.marital_status = marital
        member.contacts = contacts
        member.email = email
        member.gender = gender
        member.date_of_birth = birthday
        member.save()

        membAddress.street = address
        membAddress.city = city
        membAddress.province = province
        membAddress.zip = zipcode
        membAddress.save()

        memplan = Product.objects.get(name=plan)
        membCover.product = memplan
        membCover.inception = inception
        membCover.Covered = covered
        membCover.save()

        if marital == 'MARRIED':
            if not Spouse.objects.filter(partner=member).exists():
                spouse = Spouse.objects.create(partner=member)
                spouse.save()

        if marital == 'SINGLE':
            if Spouse.objects.filter(partner=member).exists():
                del_spouse = Spouse.objects.get(partner=member)
                del_spouse.delete()


        messages.success(request, "Member updated successfully")
        return redirect('member-profile', member.id)

@method_decorator(decoraters1,name='dispatch')
class AddSpouseView(View):
    def post(self, request, id):
        member = Member.objects.get(pk=id)
        spouse = Spouse.objects.get(partner=member)

        name = request.POST['spname']
        surname = request.POST['spsurname']
        idnum = request.POST['spidnum']
        contacts = request.POST['spcontacts']

        if len(idnum) > 13:
            messages.error(request,"Spouse Identity number too long")
            return redirect('member-profile', member.id)

        spouse.full_name = name
        spouse.surname = surname
        spouse.identity_no = idnum
        spouse.contacts = contacts
        spouse.save()

        messages.success(request,"Spouse updated successfully")
        return redirect('member-profile', member.id)

@method_decorator(decoraters1,name='dispatch')
class AddKidView(View):
    def post(self, request, id):
        member = Member.objects.get(pk=id)

        name = request.POST['kidnam']
        surname = request.POST['kidsurnam']
        idnum = request.POST['kididnum']

        if len(idnum) > 13:
            messages.error(request,"Identity number too long")
            return redirect('member-profile', member.id)

        new_kid = Kid.objects.create(parent=member,full_name=name,surname=surname,identity_no=idnum)
        new_kid.save()

        messages.success(request,"Child added successfully")
        return redirect('member-profile', member.id)

@method_decorator(decoraters1,name='dispatch')
class AddDependantView(View):
    def post(self, request, id):
        member = Member.objects.get(pk=id)

        name = request.POST['dpnam']
        surname = request.POST['dpsurnam']
        idnum = request.POST['dpidnum']

        if len(idnum) > 13:
            messages.error(request,"Identity number too long")
            return redirect('member-profile', member.id)

        new_depend = Dependant.objects.create(member=member,full_name=name,surname=surname,identity_no=idnum)
        new_depend.save()

        messages.success(request,"Dependant added successfully")
        return redirect('member-profile', member.id)

@method_decorator(decoraters1,name='dispatch')
class AddBeneficiaryView(View):
    def post(self, request, id):
        member = Member.objects.get(pk=id)
        bene = Beneficiary.objects.get(member=member)

        name = request.POST['bname']
        surname = request.POST['bsurname']
        idnum = request.POST['bidnum']
        contacts = request.POST['bcontacts']
        relation = request.POST['relation']

        if len(idnum) > 13:
            messages.error(request,"Beneficiary Identity number too long")
            return redirect('member-profile', member.id)

        bene.full_name = name
        bene.surname = surname
        bene.identity_no = idnum
        bene.contacts = contacts
        bene.relation = relation
        bene.save()

        messages.success(request,"Beneficiary updated successfully")
        return redirect('member-profile', member.id)

@method_decorator(decoraters,name='dispatch')
class DeleteKidView(View):
    def get(self, request, id):
        del_kid = Kid.objects.get(pk=id)
        del_kid.delete()

        messages.success(request,"Kid deleted successfully")
        return redirect('member-profile', del_kid.parent.id)

@method_decorator(decoraters,name='dispatch')
class DeleteDependantView(View):
    def get(self, request, id):
        del_depend = Dependant.objects.get(pk=id)
        del_depend.delete()

        messages.success(request, "Dependant deleted successfully")
        return redirect('member-profile', del_depend.member.id)

@method_decorator(decoraters,name='dispatch')
class DeleteMemberView(View):
    def get(self, request, id):
        del_member = Member.objects.get(pk=id)
        del_member.delete()

        messages.success(request, "Member deleted successfully")
        return redirect('view-members')

@method_decorator(decoraters1,name='dispatch')
class MemberTransactionView(View):
    def get(self, request,id):
        user = Employee.objects.get(user=request.user)

        member = Member.objects.get(pk=id)

        transactions = Transaction.objects.filter(member=member).order_by('-id')

        paginator = Paginator(transactions, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'member': member,
            'page_obj': page_obj,
            'user': user,

        }

        return render(request,'members/memberTransaction.html',context)


@method_decorator(decoraters1,name='dispatch')
class CreateTransactionView(View):
    def get(self, request,id):
        member = Member.objects.get(pk=id)
        user = Employee.objects.get(user=request.user)

        transaction = Transaction.objects.create(member=member,processed_by=user.employee_no)
        transaction.save()

        messages.success(request, "Transaction ready")
        return redirect('add-transaction', transaction.id)


@method_decorator(decoraters1,name='dispatch')
class AddTransactionView(View):
    def get(self, request,id):
        user = Employee.objects.get(user=request.user)

        transaction = Transaction.objects.get(pk=id)
        items = InvoiceDetail.objects.filter(invoice_no=transaction)

        context = {
            'transaction': transaction,
            'items': items,
            'user': user,
        }

        return render(request,'members/addTransaction.html',context)

    def post(self,request,id):
        transaction = Transaction.objects.get(pk=id)

        descrip = request.POST['description']
        amount = request.POST['amount']

        old_amount = str(transaction.amount)
        if transaction.amount == None:
            old_amount = 0
        new_amount = float(old_amount) + float(amount)

        new_item = InvoiceDetail.objects.create(invoice_no=transaction, description=descrip, amount=amount)
        new_item.save()

        transaction.amount = new_amount
        transaction.save()

        messages.success(request,"Item added successfully")
        return redirect('add-transaction', transaction.id)


@method_decorator(decoraters,name='dispatch')
class DeleteItemView(View):
    def get(self, request, id):
        del_item = InvoiceDetail.objects.get(pk=id)

        transact = del_item.invoice_no
        oldValue = str(transact.amount)
        newValue = float(oldValue) - float(str(del_item.amount))

        transact.amount = newValue
        transact.save()

        del_item.delete()

        messages.success(request, "Item deleted successfully")
        return redirect('add-transaction',transact.id)

@method_decorator(decoraters,name='dispatch')
class DeleteTransactionView(View):
    def get(self, request, id):
        del_item = Transaction.objects.get(pk=id)
        del_item.delete()

        messages.success(request, "Transaction deleted successfully")
        return redirect('member-transactions',del_item.member.id)

@method_decorator(decoraters1,name='dispatch')
class MarkTransactionView(View):
    def get(self, request, id):
        mark_item = Transaction.objects.get(pk=id)
        if mark_item.status == 'UNPAID':
            mark_item.status = 'PAID'
            mark_item.paid = timezone.now()
            mark_item.save()
            messages.success(request, "Transaction marked paid")
        elif mark_item.status == 'PAID':
            mark_item.status = 'UNPAID'
            mark_item.paid = None
            mark_item.save()
            messages.success(request, "Transaction marked unpaid")
        else:
            messages.error(request,"Something went wrong")

        return redirect('add-transaction', mark_item.id)

@method_decorator(decoraters,name='dispatch')
class ProductsView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        plans = Product.objects.all().order_by('id')

        context = {
            'plans': plans,
            'user': user,
        }

        return render(request,'members/products.html',context)

    def post(self,request):
        name = request.POST['name']
        amount = request.POST['amount']

        newProduct = Product.objects.create(name=name,price=amount)
        newProduct.save()

        messages.success(request,"Plan added successfully")
        return  redirect('view-plans')

@method_decorator(decoraters,name='dispatch')
class DeletePlanView(View):
    def get(self, request, id):
        del_item = Product.objects.get(pk=id)
        del_item.delete()

        messages.success(request, "Plan deleted successfully")
        return redirect('view-plans')

@method_decorator(decoraters,name='dispatch')
class EditPlanView(View):
    def get(self, request, id):
        user = Employee.objects.get(user=request.user)
        plan = Product.objects.get(pk=id)

        context = {
            'plan': plan,
            'user': user,
        }
        return render(request, 'members/editplan.html', context)

    def post(self,request, id):
        plan = Product.objects.get(pk=id)

        name = request.POST['name']
        amount = request.POST['amount']

        plan.name = name
        plan.price = amount
        plan.save()

        messages.success(request,"Plan updated successfully")
        return redirect('edit-plan',plan.id)

@method_decorator(decoraters,name='dispatch')
class MembersExcelView(View):
    def get(self,request):
        response = HttpResponse(content_type='application/ms-excel')
        response['content-Disposition'] = 'attachment; filename=Members - ' + str(timezone.now().date())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Members')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Policy Number', 'Full name', 'Surname', 'Identity Number', 'Gender','Contacts', 'Email', 'Marital Status', 'Date of birth']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = Member.objects.all().order_by('-id').values_list(
            'policy_no','full_name','surname','identity_no','gender','contacts','email','marital_status','date_of_birth'
        )

        for row in rows:
            row_num+=1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response

@method_decorator(decoraters1,name='dispatch')
class InvoicePDFView(View):
    def get(self,request,id):
        invoice = Transaction.objects.get(pk=id)
        invoiceitems = InvoiceDetail.objects.filter(invoice_no=invoice)

        context = {
            'invoice': invoice,
            'invoiceitems': invoiceitems,
        }

        response = HttpResponse(content_type='application/pdf')
        response['content-Disposition'] = 'inline; attachment; filename=Invoice #' + str(invoice.id)+'.pdf'
        response['content-Transfer-Encoding'] = 'binary'

        html_string = render_to_string('invoice.html',context)

        html = HTML(string=html_string)
        result = html.write_pdf(stylesheets=[CSS('funeraladmin/static/css/bootstrap.min.css',)])

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            #output = open(output.name, 'rb')
            response.write(output.read())

        return response




