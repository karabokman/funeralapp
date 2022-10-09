from django.urls import path

from .views import AllTransactionsView,CreateQuoteView,EditQuoteView,DeleteQuoteView,AllQuotesView,MarkQuoteView,DeleteQuoteItemView,TransactionsExcelView,QuotesExcelView,QuotePDFView

urlpatterns = [
    path('', AllTransactionsView.as_view(), name="all-transactions"),
    path('create-quote/', CreateQuoteView.as_view(), name="create-quote"),
    path('all-quotes/', AllQuotesView.as_view(), name="all-quotes"),
    path('edit-quote/?P<id>[0-9]+)\\Z', EditQuoteView.as_view(), name="edit-quote"),
    path('delete-quote/?P<id>[0-9]+)\\Z', DeleteQuoteView.as_view(), name="delete-quote"),
    path('delete-quote-item/?P<id>[0-9]+)\\Z', DeleteQuoteItemView.as_view(), name="delete-itemquote"),
    path('mark-quote/?P<id>[0-9]+)\\Z', MarkQuoteView.as_view(), name="mark-quote"),
    path('export-transactions-excel/', TransactionsExcelView.as_view(), name="export-transactions"),
    path('export-quotes-excel/', QuotesExcelView.as_view(), name="export-quotes"),
    path('export-quote-pdf/?P<id>[0-9]+)\\Z', QuotePDFView.as_view(), name="export-quote"),

]
