from django.urls import include, path
from django.views.generic import TemplateView
from .views import SignUpView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),

    path('add_farm/', views.FarmController().create_farm, name='create_farm'),
    path('farm_detail/<int:farm_id>/', views.FarmController.as_view(), name='farm_detail'),
    path('delete_farm/<int:farm_id>/', views.FarmController().delete_farm, name='delete_farm'),
    path('update_farm/<int:farm_id>/', views.FarmController().update_farm, name='update_farm'),

    path('create_report/', views.SoilReportController().create_report, name='create_report'),
    path('report_detail/<int:report_id>/', views.SoilReportController().report_detail, name='report_detail'),
    path('delete_report/<int:report_id>/', views.SoilReportController().delete_report, name='delete_report'),
    path('update_report/<int:report_id>/', views.SoilReportController().update_report, name='update_report'),

    path('create_analysis/', views.AnalysisController().create_analysis, name='create_analysis'),
    path('analysis_detail/<int:analysis_id>/', views.AnalysisController().analysis_detail, name='analysis_detail'),
    path('delete_analysis/<int:analysis_id>/', views.AnalysisController().delete_analysis, name='delete_analysis'),
    path('update_analysis/<int:analysis_id>/', views.AnalysisController().update_analysis, name='update_analysis'),

    path('create_field/', views.FieldController().create_field, name='create_field'),
    path('field_detail/<int:field_id>/', views.FieldController().field_detail, name='field_detail'),
    path('delete_field/<int:field_id>/', views.FieldController().delete_field, name='delete_field'),
    path('update_field/<int:field_id>/', views.FieldController().update_field, name='update_field'),

    path('report_list/', views.SoilReportController().report_list, name='report_list'),
    path('analysis_list/', views.AnalysisController().analysis_list, name='analysis_list'),
    path('farm_list/', views.FarmController().farm_list, name='farm_list'),
    path('field_list/', views.FieldController().field_list, name='field_list'),
]
