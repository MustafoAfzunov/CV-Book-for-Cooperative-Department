from django.urls import path
from .views import CVSubmitView, CVDetailView, CVListView, CVPDFView, CVEditView
from django.views.generic import TemplateView

urlpatterns = [
    path('submit/', CVSubmitView.as_view(), name='cv-submit'),
    path('list/', CVListView.as_view(), name='cv-list'),
    path('<int:cv_id>/', CVDetailView.as_view(), name='cv-detail'),
    path('<int:cv_id>/download/', CVPDFView.as_view(), name='cv-download'),
    path('<int:cv_id>/edit/', CVEditView.as_view(), name='cv-edit'),
    path('create/', TemplateView.as_view(template_name='cv/cv-form.html'), name='cv-create'),
    path('cards/', TemplateView.as_view(template_name='cv/cv-cards.html'), name='cv-cards'),
]