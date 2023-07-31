import requests
import pandas as pd
from datetime import datetime, date, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import dateformat, formats, timezone
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views import generic
from soilRegenApp.forms import AddFarmForm, DeleteFarmForm
from .models import Amendment, AmendmentCategory, AmendmentElement, AmendmentType, Analysis, AnalysisItem
from .models import Country, Element, Farm, Field, ReportItem, SoilReport, Source, SourceAmendment, UserProfile
from .services import ReportAnalysisService, RecommendationService, AmendmentRatioService


def index(request):
    return render(request, 'index.html')


class AmendmentController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def amendment_list(self, request):
        amendments = Amendment.objects.all() 
        context = {'amendments': amendments.order_by('product_name')}
        return render(request, 'amendment_list.html', context)

    def amendment_detail(self, request, amendment_id):
        try:
            amendment = Amendment.objects.get(amendment_id=amendment_id)
        except Amendment.DoesNotExist:
            messages.error(request, f"Amendment ID {amendment_id} does not exist")
            return redirect('amendment_list')
        context = {
            'amendment': amendment
        }
        return render(request, 'amendment_detail.html', context)


class AnalysisController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def analysis_list(self, request):
        print("Analysis: GET ALL")
        analyses = Analysis.objects.all() 
        context = {'analyses': sorted(analyses, key=lambda analysis: analysis.analysis_date)}
        return render(request, 'analysis_list.html', context)

    def analysis_detail(request, analysis_id):
        try:
            analysis = Analysis.objects.get(analysis_id=analysis_id)
        except Analysis.DoesNotExist:
            messages.error(request, f"Analysis ID {analysis_id} does not exist")
            return redirect('analysis_list')
        context = {
            'analysis': analysis,
        }
        return render(request, 'analysis_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_analysis(self, request):
        if request.method == 'POST':
            analysis_date = request.POST.get('analysis_date')
            description = request.POST.get('description')
            soil_report_id = request.POST.get('soil_report_id')
            new_analysis = Analysis.objects.create(
                analysis_date=analysis_date,
                description=description,
                soil_report_id=soil_report_id
            )
            new_analysis.save()
            return redirect('analysis_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_analysis(self, request, analysis_id):
        analysis = get_object_or_404(Analysis, analysis_id=analysis_id)
        if request.method == 'POST':
            analysis.analysis_date = request.POST.get('analysis_date')
            analysis.description = request.POST.get('description')
            analysis.soil_report_id = request.POST.get('soil_report_id')
            analysis.save()
            return redirect('analysis_detail', analysis_id=analysis.analysis_id)

    # Delete operation
    def delete_analysis(self, request, analysis_id):
        analysis = get_object_or_404(Analysis, analysis_id=analysis_id)
        analysis.delete()
        return redirect('analysis_list')

class AnalysisItemController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def analysis_item_list(self, request):
        print("Analysis Item: GET ALL")
        analysis_items = AnalysisItem.objects.all() 
        context = {'analysis_items': sorted(analysis_items, key=lambda item: item.description)}
        return render(request, 'analysis_item_list.html', context)

    def analysis_item_detail(request, item_id):
        try:
            analysis_item = AnalysisItem.objects.get(item_id=item_id)
        except AnalysisItem.DoesNotExist:
            messages.error(request, f"Analysis Item ID {item_id} does not exist")
            return redirect('analysis_item_list')
        context = {
            'analysis_item': analysis_item,
        }
        return render(request, 'analysis_item_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_analysis_item(self, request):
        if request.method == 'POST':
            description = request.POST.get('description')
            analysis_id = request.POST.get('analysis_id')
            report_item_id = request.POST.get('report_item_id')
            new_analysis_item = AnalysisItem.objects.create(
                description=description,
                analysis_id=analysis_id,
                report_item_id=report_item_id
            )
            new_analysis_item.save()
            return redirect('analysis_item_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_analysis_item(self, request, item_id):
        analysis_item = get_object_or_404(AnalysisItem, item_id=item_id)
        if request.method == 'POST':
            analysis_item.description = request.POST.get('description')
            analysis_item.analysis_id = request.POST.get('analysis_id')
            analysis_item.report_item_id = request.POST.get('report_item_id')
            analysis_item.save()
            return redirect('analysis_item_detail', item_id=analysis_item.item_id)

    # Delete operation
    def delete_analysis_item(self, request, item_id):
        analysis_item = get_object_or_404(AnalysisItem, item_id=item_id)
        analysis_item.delete()
        return redirect('analysis_item_list')


class ElementController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def element_list(self, request):
        print("Element: GET ALL")
        elements = Element.objects.all() 
        context = {'elements': sorted(elements, key=lambda element: element.element_name)}
        return render(request, 'element_list.html', context)

    def element_detail(request, element_id):
        try:
            element = Element.objects.get(element_id=element_id)  
        except Element.DoesNotExist:
            messages.error(request, f"Element ID {element_id} does not exist")
            return redirect('element_list')
        context = {
            'element': element,
        }
        return render(request, 'element_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_element(self, request):
        if request.method == 'POST':
            element_name = request.POST.get('element_name')
            common_name = request.POST.get('common_name')
            element_symbol = request.POST.get('element_symbol')
            description = request.POST.get('description')
            new_element = Element.objects.create(
                element_name=element_name,
                common_name=common_name,
                element_symbol=element_symbol,
                description=description
            )
            new_element.save()
            return redirect('element_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_element(self, request, element_id):
        element = get_object_or_404(Element, element_id=element_id)
        if request.method == 'POST':
            element.element_name = request.POST.get('element_name')
            element.common_name = request.POST.get('common_name')
            element.element_symbol = request.POST.get('element_symbol')
            element.description = request.POST.get('description')
            element.save()
            return redirect('element_detail', element_id=element.element_id)

    # Delete operation
    def delete_element(self, request, element_id):
        element = get_object_or_404(Element, element_id=element_id)
        element.delete()
        return redirect('element_list')


class FarmController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def farm_list(self, request):
        print("Farm: GET ALL")
        farms = Farm.objects.all()
        context = {'farms': sorted(farms, key=lambda farm: farm.farm_name)}
        return render(request, 'farm_list.html', context)

    def farm_detail(request, farm_id):
        try:
            farm = Farm.objects.get(farm_id=farm_id)
            farm_fields = farm.field_set.order_by('field_name')
        except Farm.DoesNotExist:
            messages.error(request, f"Farm ID {farm_id} does not exist")
            return redirect('farm_list')
        context = {
            'farm': farm,
            'farm_fields': farm_fields
        }
        return render(request, 'farm_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_farm(self, request):
        if request.method == 'POST':
            farm_name = request.POST.get('farm_name')
            description = request.POST.get('description')
            user_id = request.POST.get('user_id')
            new_farm = Farm.objects.create(
                farm_name=farm_name,
                description=description,
                user_id=user_id
            )
            new_farm.save()
            return redirect('farm_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_farm(self, request, farm_id):
        farm = get_object_or_404(Farm, farm_id=farm_id)
        if request.method == 'POST':
            farm.farm_name = request.POST.get('farm_name')
            farm.description = request.POST.get('description')
            farm.user_id = request.POST.get('user_id')
            farm.save()
            return redirect('farm_detail', farm_id=farm.farm_id)

    # Delete operation
    def delete_farm(self, request, farm_id):
        farm = get_object_or_404(Farm, farm_id=farm_id)
        farm.delete()
        return redirect('farm_list')


class FieldController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def field_list(self, request):
        print("Field: GET ALL")
        fields = Field.objects.all() 
        context = {'fields': sorted(fields, key=lambda field: field.field_name)}
        return render(request, 'field_list.html', context)

    def field_detail(request, field_id):
        try:
            field = Field.objects.get(field_id=field_id)
        except Field.DoesNotExist:
            messages.error(request, f"Field ID {field_id} does not exist")
            return redirect('field_list')
        context = {
            'field': field,
        }
        return render(request, 'field_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_field(self, request):
        if request.method == 'POST':
            field_name = request.POST.get('field_name')
            field_acres = request.POST.get('field_acres')
            soil_type = request.POST.get('soil_type')
            growing_zone = request.POST.get('growing_zone')
            description = request.POST.get('description')
            farm_id = request.POST.get('farm_id')
            new_field = Field.objects.create(
                field_name=field_name,
                field_acres=field_acres,
                soil_type=soil_type,
                growing_zone=growing_zone,
                description=description,
                farm_id=farm_id
            )
            new_field.save()
            return redirect('field_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_field(self, request, field_id):
        field = get_object_or_404(Field, field_id=field_id)
        if request.method == 'POST':
            field.field_name = request.POST.get('field_name')
            field.field_acres = request.POST.get('field_acres')
            field.soil_type = request.POST.get('soil_type')
            field.growing_zone = request.POST.get('growing_zone')
            field.description = request.POST.get('description')
            field.farm_id = request.POST.get('farm_id')
            field.save()
            return redirect('field_detail', field_id=field.field_id)

    # Delete operation
    def delete_field(self, request, field_id):
        field = get_object_or_404(Field, field_id=field_id)
        field.delete()
        return redirect('field_list')


class ReportItemController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def report_item_list(self, request):
        print("ReportItem: GET ALL")
        report_items = ReportItem.objects.all() 
        context = {'report_items': sorted(report_items, key=lambda item: item.tested_element)}
        return render(request, 'report_item_list.html', context)

    def report_item_detail(request, item_id):
        try:
            report_item = ReportItem.objects.get(item_id=item_id)
        except ReportItem.DoesNotExist:
            messages.error(request, f"ReportItem ID {item_id} does not exist")
            return redirect('report_item_list')
        context = {
            'report_item': report_item,
        }
        return render(request, 'report_item_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_report_item(self, request):
        if request.method == 'POST':
            tested_element = request.POST.get('tested_element')
            unit = request.POST.get('unit')
            results = request.POST.get('results')
            target_ratio = request.POST.get('target_ratio')
            target_level = request.POST.get('target_level')
            report_id = request.POST.get('report_id')
            new_report_item = ReportItem.objects.create(
                tested_element=tested_element,
                unit=unit,
                results=results,
                target_ratio=target_ratio,
                target_level=target_level,
                report_id=report_id
            )
            new_report_item.save()
            return redirect('report_item_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_report_item(self, request, item_id):
        report_item = get_object_or_404(ReportItem, item_id=item_id)
        if request.method == 'POST':
            report_item.tested_element = request.POST.get('tested_element')
            report_item.unit = request.POST.get('unit')
            report_item.results = request.POST.get('results')
            report_item.target_ratio = request.POST.get('target_ratio')
            report_item.target_level = request.POST.get('target_level')
            report_item.report_id = request.POST.get('report_id')
            report_item.save()
            return redirect('report_item_detail', item_id=report_item.item_id)

    # Delete operation
    def delete_report_item(self, request, item_id):
        report_item = get_object_or_404(ReportItem, item_id=item_id)
        report_item.delete()
        return redirect('report_item_list')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class SoilReportController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def report_list(self, request):
        print("Report: GET ALL")
        reports = Report.objects.all()
        context = {'reports': sorted(reports, key=lambda report: report.report_name)}
        return render(request, 'report_list.html', context)

    def report_detail(request, report_id):
        try:
            report = Report.objects.get(report_id=report_id)
            report_fields = report.field_set.order_by('report_date')  
        except Report.DoesNotExist:
            messages.error(request, f"Report ID {report_id} does not exist")
            return redirect('report_list')
        context = {
            'report': report,
            'report_fields': report_fields
        }
        return render(request, 'report_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_report(self, request):
        if request.method == 'POST':
            report_date = request.POST.get('report_date')
            lab_name = request.POST.get('lab_name')
            field_id = request.POST.get('field_id')
            new_report = Report.objects.create(
                report_date=report_date,
                lab_name=lab_name,
                field_id=field_id
            )
            new_report.save()
            return redirect('report_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_report(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        if request.method == 'POST':
            report.report_date = request.POST.get('report_date')
            report.lab_name = request.POST.get('lab_name')
            report.field_id = request.POST.get('field_id')
            report.save()
            return redirect('report_detail', report_id=report.report_id)

    # Delete operation
    def delete_report(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        report.delete()
        return redirect('report_list')


class SourceController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def source_list(self, request):
        sources = Source.objects.all() 
        context = {'sources': sources.order_by('name')}
        return render(request, 'source_list.html', context)

    def source_detail(self, request, source_id):
        try:
            source = Source.objects.get(source_id=source_id)
        except Source.DoesNotExist:
            messages.error(request, f"Source ID {source_id} does not exist")
            return redirect('source_list')
        context = {
            'source': source
        }
        return render(request, 'source_detail.html', context)


class UserProfileController(View):
    def __init__(self):
        self.api_key = settings.API_KEY

    @method_decorator(login_required(login_url='/accounts/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def profile_list(self, request):
        print("UserProfile: GET ALL")
        user_profiles = UserProfile.objects.all()
        context = {'user_profiles': sorted(user_profiles, key=lambda profile: profile.user.username)}
        return render(request, 'user_profile_list.html', context)

    def profile_detail(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            messages.error(request, f"User ID {user_id} does not exist")
            return redirect('profile_list')
        context = {
            'user_profile': user_profile
        }
        return render(request, 'user_profile_detail.html', context)

    # Create operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def create_profile(self, request):
        if request.method == 'POST':
            user = request.POST.get('user')
            street_address = request.POST.get('street_address')
            town = request.POST.get('town')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            phone = request.POST.get('phone')
            notes = request.POST.get('notes')

            new_profile = UserProfile.objects.create(
                user=user,
                street_address=street_address,
                town=town,
                state=state,
                zip=zip,
                phone=phone,
                notes=notes,
            )
            new_profile.save()
            return redirect('profile_list')

    # Update operation
    @csrf_exempt  # Using this decorator to allow POST requests
    def update_profile(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if request.method == 'POST':
            user_profile.street_address = request.POST.get('street_address')
            user_profile.town = request.POST.get('town')
            user_profile.state = request.POST.get('state')
            user_profile.zip = request.POST.get('zip')
            user_profile.phone = request.POST.get('phone')
            user_profile.notes = request.POST.get('notes')

            user_profile.save()
            return redirect('profile_detail', user_id=user_profile.user.id)

    # Delete operation
    def delete_profile(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        user_profile.delete()
        return redirect('profile_list')
