from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from members.models import Transaction,Quote,QuoteDetail
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from authentication.models import Employee
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
import xlwt
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML,CSS
import tempfile

decoraters = [login_required(login_url='/auth/login'),user_passes_test(lambda u: u.groups.filter(name='Admin').exists())]
decoraters1 = [login_required(login_url='/auth/login')]

# Create your views here.
@method_decorator(decoraters,name='dispatch')
class AllTransactionsView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        if 'q' in request.GET:
            q = request.GET['q']
            multi_q = Q(Q(id__istartswith=q)|Q(status__iexact=q)|Q(created__istartswith=q)|Q(due__istartswith=q)|Q(paid__istartswith=q)|Q(amount__istartswith=q)|Q(processed_by__icontains=q))
            transactions = Transaction.objects.filter(multi_q).order_by('-id')
        else:
            transactions = Transaction.objects.all().order_by('-id')
        paginator = Paginator(transactions, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'transactions/transactions.html',context)


@method_decorator(decoraters1,name='dispatch')
class CreateQuoteView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)
        context = {
            'user': user,
        }
        return render(request, 'transactions/quote.html',context)

    def post(self,request):
        user = Employee.objects.get(user=request.user)
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        company = request.POST['company']
        contacts = request.POST['contacts']
        address = request.POST['address']
        city = request.POST['city']
        province = request.POST['province']
        zipcode = request.POST['zipcode']

        if len(zipcode) > 10:
            messages.error(request,"Postal code is too long")
            return redirect('create-quote')

        newQuote = Quote.objects.create(full_name=name,surname=surname,contacts=contacts,email=email,company=company,street=address,city=city,province=province,Zip_code=zipcode,processed_by=user.employee_no)
        newQuote.save()

        messages.success(request,"Quote ready")
        return redirect('edit-quote',newQuote.id)

@method_decorator(decoraters1,name='dispatch')
class EditQuoteView(View):
    def get(self, request,id):
        user = Employee.objects.get(user=request.user)
        quote = Quote.objects.get(pk=id)
        items = QuoteDetail.objects.filter(quote_no=quote)

        context = {
            'quote': quote,
            'items': items,
            'user': user,
        }

        return render(request, 'transactions/edit-quote.html',context)

    def post(self,request,id):
        quote = Quote.objects.get(pk=id)
        descrip = request.POST['description']
        amount = request.POST['amount']

        oldValue = str(quote.amount)
        newValue = float(oldValue)+float(amount)

        quote.amount = newValue
        quote.save()

        newitem = QuoteDetail.objects.create(quote_no=quote,description=descrip,amount=amount)
        newitem.save()

        messages.success(request,"Item added successfully")
        return redirect('edit-quote',quote.id)

@method_decorator(decoraters,name='dispatch')
class DeleteQuoteView(View):
    def get(self, request,id):
        quote = Quote.objects.get(pk=id)
        quote.delete()

        messages.success(request,"Quote deleted successfully")
        return redirect('all-quotes')

@method_decorator(decoraters,name='dispatch')
class DeleteQuoteItemView(View):
    def get(self, request,id):
        quote = QuoteDetail.objects.get(pk=id)
        quote.delete()

        transact = quote.quote_no

        oldValue = str(transact.amount)
        newValue = float(oldValue)-float(quote.amount)
        transact.amount = newValue
        transact.save()

        messages.success(request,"Items deleted successfully")
        return redirect('edit-quote',transact.id)

@method_decorator(decoraters1,name='dispatch')
class MarkQuoteView(View):
    def get(self, request,id):
        mark_item = Quote.objects.get(pk=id)
        if mark_item.status == 'UNPAID':
            mark_item.status = 'PAID'
            mark_item.paid = timezone.now()
            mark_item.save()
            messages.success(request, "Quote marked paid")
        elif mark_item.status == 'PAID':
            mark_item.status = 'UNPAID'
            mark_item.paid = None
            mark_item.save()
            messages.success(request, "Quote marked unpaid")
        else:
            messages.error(request,"Something went wrong")

        return redirect('edit-quote', mark_item.id)


@method_decorator(decoraters1,name='dispatch')
class AllQuotesView(View):
    def get(self, request):
        user = Employee.objects.get(user=request.user)

        if 'q' in request.GET:
            q = request.GET['q']
            multi_q = Q(Q(id__istartswith=q)|Q(status__iexact=q)|Q(created__istartswith=q)|Q(due__istartswith=q)|Q(paid__istartswith=q)|Q(amount__istartswith=q)|Q(processed_by__icontains=q))
            transactions = Quote.objects.filter(multi_q).order_by('-id')
        else:
            transactions = Quote.objects.all().order_by('-id')
        paginator = Paginator(transactions, 8)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'transactions/allquotes.html',context)


@method_decorator(decoraters,name='dispatch')
class TransactionsExcelView(View):
    def get(self,request):
        response = HttpResponse(content_type='application/ms-excel')
        response['content-Disposition'] = 'attachment; filename=Transactions - ' + str(timezone.now().date())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Transactions')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Invoice Number', 'Member', 'Status', 'Created', 'Due', 'Paid', 'Amount','Processed by']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = Transaction.objects.all().order_by('-id').values_list(
            'id','member__policy_no','status','created','due','paid','amount','processed_by'
        )

        for row in rows:
            row_num+=1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response


@method_decorator(decoraters,name='dispatch')
class QuotesExcelView(View):
    def get(self,request):
        response = HttpResponse(content_type='application/ms-excel')
        response['content-Disposition'] = 'attachment; filename=Quotes - ' + str(timezone.now().date())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Quotes')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Quote Number', 'Full name','Surname', 'Status', 'Created', 'Due', 'Paid', 'Amount','Processed by']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        rows = Quote.objects.all().order_by('-id').values_list(
            'id','full_name','surname','status','created','due','paid','amount','processed_by'
        )

        for row in rows:
            row_num+=1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response


@method_decorator(decoraters1,name='dispatch')
class QuotePDFView(View):
    def get(self,request,id):
        invoice = Quote.objects.get(pk=id)
        invoiceitems = QuoteDetail.objects.filter(quote_no=invoice)

        context = {
            'invoice': invoice,
            'invoiceitems': invoiceitems,
        }

        response = HttpResponse(content_type='application/pdf')
        response['content-Disposition'] = 'inline; attachment; filename=Quote #' + str(invoice.id)+'.pdf'
        response['content-Transfer-Encoding'] = 'binary'

        html_string = render_to_string('quote.html',context)

        html = HTML(string=html_string)
        result = html.write_pdf(stylesheets=[CSS('funeraladmin/static/css/bootstrap.min.css',)])

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            #output = open(output.name, 'rb')
            response.write(output.read())

        return response


