from django.urls import path
from .views import HomepageView,MembersView,AddMemberView,MemberProfileView,AddSpouseView,AddKidView,AddDependantView,AddBeneficiaryView,DeleteKidView,DeleteDependantView,DeleteMemberView,MemberTransactionView,AddTransactionView,DeleteItemView,CreateTransactionView,DeleteTransactionView,MarkTransactionView,ProductsView,DeletePlanView,EditPlanView,MembersExcelView,InvoicePDFView
urlpatterns = [
    path('', HomepageView.as_view(), name="homepage"),
    path('view-members/', MembersView.as_view(), name="view-members"),
    path('add-member/', AddMemberView.as_view(), name="add-member"),
    path('member-profile/?P<id>[0-9]+)\\Z', MemberProfileView.as_view(), name="member-profile"),
    path('add-spouse/?P<id>[0-9]+)\\Z', AddSpouseView.as_view(), name="add-spouse"),
    path('add-kid/?P<id>[0-9]+)\\Z', AddKidView.as_view(), name="add-kid"),
    path('add-dependant/?P<id>[0-9]+)\\Z', AddDependantView.as_view(), name="add-dependant"),
    path('add-beneficiary/?P<id>[0-9]+)\\Z', AddBeneficiaryView.as_view(), name="add-beneficiary"),
    path('delete-kid/?P<id>[0-9]+)\\Z', DeleteKidView.as_view(), name="delete-kid"),
    path('delete-dependant/?P<id>[0-9]+)\\Z', DeleteDependantView.as_view(), name="delete-dependant"),
    path('delete-member/?P<id>[0-9]+)\\Z', DeleteMemberView.as_view(), name="delete-member"),
    path('member-transactions/?P<id>[0-9]+)\\Z', MemberTransactionView.as_view(), name="member-transactions"),
    path('create-transaction/?P<id>[0-9]+)\\Z', CreateTransactionView.as_view(), name="create-transaction"),
    path('add-transaction/?P<id>[0-9]+)\\Z', AddTransactionView.as_view(), name="add-transaction"),
    path('delete-item/?P<id>[0-9]+)\\Z', DeleteItemView.as_view(), name="delete-item"),
    path('delete-transaction/?P<id>[0-9]+)\\Z', DeleteTransactionView.as_view(), name="delete-transaction"),
    path('mark-transaction/?P<id>[0-9]+)\\Z', MarkTransactionView.as_view(), name="mark-transaction"),
    path('view-plans/', ProductsView.as_view(), name="view-plans"),
    path('delete-plan/?P<id>[0-9]+)\\Z', DeletePlanView.as_view(), name="delete-plan"),
    path('edit-plan/?P<id>[0-9]+)\\Z', EditPlanView.as_view(), name="edit-plan"),
    path('export-members-excel/', MembersExcelView.as_view(), name="export-members"),
    path('export-invoice-pdf/?P<id>[0-9]+)\\Z', InvoicePDFView.as_view(), name="export-invoice"),

]
