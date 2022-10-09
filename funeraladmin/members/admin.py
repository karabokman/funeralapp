from django.contrib import admin
from .models import Member,Kid,Dependant,MemberProduct,QuoteDetail,Quote,Transaction,InvoiceDetail,Spouse,Address,Beneficiary,Product

# Register your models here.
admin.site.register(Member)
admin.site.register(Kid)
admin.site.register(Dependant)
admin.site.register(MemberProduct)
admin.site.register(QuoteDetail)
admin.site.register(Quote)
admin.site.register(Transaction)
admin.site.register(InvoiceDetail)
admin.site.register(Spouse)
admin.site.register(Address)
admin.site.register(Beneficiary)
admin.site.register(Product)