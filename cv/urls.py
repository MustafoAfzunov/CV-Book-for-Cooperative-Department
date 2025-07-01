from django.urls import path
from .views import CVRequestView, CVSubmitView, CVDetailView, CVListView, CVPDFView, CVEditView

urlpatterns = [
    path('request/', CVRequestView.as_view(), name='cv-request'),
    path('submit/', CVSubmitView.as_view(), name='cv-submit'),
    path('list/', CVListView.as_view(), name='cv-list'),
    path('<int:cv_id>/', CVDetailView.as_view(), name='cv-detail'),
    path('<int:cv_id>/download/', CVPDFView.as_view(), name='cv-download'),
    path('<int:cv_id>/edit/', CVEditView.as_view(), name='cv-edit'),
]