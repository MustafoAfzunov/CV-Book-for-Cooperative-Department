from django.urls import path
from .views import CVSubmitView, CVDetailView, CVListView, CVPDFView, CVEditView
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('submit/', views.CVSubmitView.as_view(), name='cv_submit'),
    path('cards/', views.cv_cards_view, name='cv_cards'),    
    path('list/', CVListView.as_view(), name='cv-list'),
    path('<int:cv_id>/', CVDetailView.as_view(), name='cv-detail'),
    path('<int:cv_id>/download/', CVPDFView.as_view(), name='cv-download'),
    path('<int:cv_id>/edit/', CVEditView.as_view(), name='cv-edit'),
    path('create/', TemplateView.as_view(template_name='cv/cv-form.html'), name='cv-create'),
    path('detail/<int:cv_id>/', views.cv_detail_view, name='cv_detail'),  # New detail view URL
]