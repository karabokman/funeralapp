
from django.db import models
from django.utils import timezone

# Create your models here.
class Member(models.Model):
    policy_no = models.CharField(max_length=20)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)
    gender = models.CharField(max_length=15)
    contacts = models.CharField(max_length=15)
    email = models.CharField(max_length=150)
    marital_status = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.surname+" "+self.full_name


class Spouse(models.Model):
    partner = models.ForeignKey(Member, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)
    contacts = models.CharField(max_length=15)

    def __str__(self):
        return self.surname


class Kid(models.Model):
    parent = models.ForeignKey(Member, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)

    def __str__(self):
        return self.surname


class Beneficiary(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)
    contacts = models.CharField(max_length=15)
    relation = models.TextField()

    def __str__(self):
        return self.surname


class Dependant(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    identity_no = models.CharField(max_length=13)

    def __str__(self):
        return self.surname

def tenDays():
    return timezone.now()+timezone.timedelta(days=10)

class Transaction(models.Model):
    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=100, default='UNPAID')
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(default=tenDays)
    paid = models.DateTimeField(null=True)
    amount = models.DecimalField(max_digits=150,decimal_places=2,default=0.00)
    processed_by = models.CharField(max_length=100)

    def __str__(self):
        return self.member


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=150,decimal_places=2)

    def __str__(self):
        return self.name
def six_month():
    return timezone.now().date()+timezone.timedelta(days=183)

class MemberProduct(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inception = models.DateField(auto_now_add=True)
    Covered = models.DateField(default=six_month)

    def __str__(self):
        return self.product

class Quote(models.Model):
    full_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    contacts = models.CharField(max_length=15)
    email = models.CharField(max_length=150)
    company = models.CharField(max_length=255,null=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    Zip_code = models.CharField(max_length=10)
    status = models.CharField(max_length=100, default='UNPAID')
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(default=tenDays)
    paid = models.DateTimeField(null=True)
    amount = models.DecimalField(max_digits=150,decimal_places=2,default=0.00)
    processed_by = models.CharField(max_length=100)

    def __str__(self):
        return self.surname

class QuoteDetail(models.Model):
    quote_no = models.ForeignKey(Quote, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=150,decimal_places=2)

    def __str__(self):
        return self.description

class InvoiceDetail(models.Model):
    invoice_no = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=150,decimal_places=2)

    def __str__(self):
        return self.description

class Address(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return str(self.member)
