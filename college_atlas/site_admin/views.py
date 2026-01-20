from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import College, Degree, State, District, Country
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json


def admin_login(request):
    """
    Login view for site admin
    """
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', 'admin_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'site_admin/login.html')


def admin_logout(request):
    """
    Logout view for site admin
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    """
    Custom admin dashboard view with college listing
    """
    search_query = request.GET.get('search', '')
    college_type_filter = request.GET.get('college_type', '')
    district_filter = request.GET.get('district', '')
    
    colleges = College.objects.select_related('district__state').prefetch_related('degrees')
    
    if search_query:
        colleges = colleges.filter(
            Q(name__icontains=search_query) | 
            Q(district__name__icontains=search_query)
        )
    
    if college_type_filter:
        colleges = colleges.filter(college_type=college_type_filter)
    
    if district_filter:
        colleges = colleges.filter(district_id=district_filter)
    
    colleges = colleges.order_by('name')
    
    paginator = Paginator(colleges, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    districts = District.objects.select_related('state').order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'college_type_filter': college_type_filter,
        'district_filter': district_filter,
        'districts': districts,
        'college_types': College.COLLEGE_TYPES,
        'total_colleges': College.objects.count(),
    }
    
    return render(request, 'site_admin/dashboard.html', context)


@login_required(login_url='admin_login')
def create_college(request):
    """
    View to create a new college
    """
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            university = request.POST.get('university')
            college_type = request.POST.get('college_type')
            district_id = request.POST.get('district')
            address_line = request.POST.get('address_line')
            pincode = request.POST.get('pincode')
            website = request.POST.get('website')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            image = request.FILES.get('image')
            degree_ids = request.POST.getlist('degrees')
            
            college = College.objects.create(
                name=name,
                university=university or None,
                college_type=college_type,
                district_id=district_id,
                address_line=address_line,
                pincode=pincode,
                website=website or None,
                email=email or None,
                phone_number=phone_number or None,
                latitude=latitude or None,
                longitude=longitude or None,
                image=image
            )
            
            if degree_ids:
                college.degrees.set(degree_ids)
            
            messages.success(request, f'College "{name}" created successfully!')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating college: {str(e)}')
    
    districts = District.objects.select_related('state').order_by('state__name', 'name')
    degrees = Degree.objects.order_by('name')
    
    context = {
        'districts': districts,
        'degrees': degrees,
        'college_types': College.COLLEGE_TYPES,
        'is_edit': False,
    }
    
    return render(request, 'site_admin/create_college.html', context)


@login_required(login_url='admin_login')
def edit_college(request, pk):
    """
    View to edit an existing college
    """
    college = get_object_or_404(College, pk=pk)
    
    if request.method == 'POST':
        try:
            college.name = request.POST.get('name')
            college.university = request.POST.get('university') or None
            college.college_type = request.POST.get('college_type')
            college.district_id = request.POST.get('district')
            college.address_line = request.POST.get('address_line')
            college.pincode = request.POST.get('pincode')
            college.website = request.POST.get('website') or None
            college.email = request.POST.get('email') or None
            college.phone_number = request.POST.get('phone_number') or None
            college.latitude = request.POST.get('latitude') or None
            college.longitude = request.POST.get('longitude') or None
            
            if 'image' in request.FILES:
                college.image = request.FILES['image']
            
            college.save()
            
            degree_ids = request.POST.getlist('degrees')
            college.degrees.set(degree_ids)
            
            messages.success(request, f'College "{college.name}" updated successfully!')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error updating college: {str(e)}')
    
    districts = District.objects.select_related('state').order_by('state__name', 'name')
    degrees = Degree.objects.order_by('name')
    
    context = {
        'college': college,
        'districts': districts,
        'degrees': degrees,
        'college_types': College.COLLEGE_TYPES,
        'is_edit': True,
    }
    
    return render(request, 'site_admin/create_college.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def delete_college(request, pk):
    """
    View to delete a college
    """
    college = get_object_or_404(College, pk=pk)
    college_name = college.name
    
    try:
        college.delete()
        messages.success(request, f'College "{college_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting college: {str(e)}')
    
    return redirect('admin_dashboard')


@login_required(login_url='admin_login')
def degree_list(request):
    """List all degrees with search and pagination"""
    search_query = request.GET.get('search', '')
    
    degrees = Degree.objects.all()
    
    if search_query:
        degrees = degrees.filter(name__icontains=search_query)
    
    degrees = degrees.order_by('name')
    
    paginator = Paginator(degrees, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_degrees': Degree.objects.count(),
    }
    
    return render(request, 'site_admin/degree_list.html', context)


@login_required(login_url='admin_login')
def create_degree(request):
    """Create a new degree"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            duration_years = request.POST.get('duration_years', 4)
            
            Degree.objects.create(
                name=name,
                duration_years=duration_years
            )
            
            messages.success(request, f'Degree "{name}" created successfully!')
            return redirect('degree_list')
            
        except Exception as e:
            messages.error(request, f'Error creating degree: {str(e)}')
    
    context = {'is_edit': False}
    return render(request, 'site_admin/degree_form.html', context)


@login_required(login_url='admin_login')
def edit_degree(request, pk):
    """Edit an existing degree"""
    degree = get_object_or_404(Degree, pk=pk)
    
    if request.method == 'POST':
        try:
            degree.name = request.POST.get('name')
            degree.duration_years = request.POST.get('duration_years', 4)
            degree.save()
            
            messages.success(request, f'Degree "{degree.name}" updated successfully!')
            return redirect('degree_list')
            
        except Exception as e:
            messages.error(request, f'Error updating degree: {str(e)}')
    
    context = {
        'degree': degree,
        'is_edit': True,
    }
    return render(request, 'site_admin/degree_form.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def delete_degree(request, pk):
    """Delete a degree"""
    degree = get_object_or_404(Degree, pk=pk)
    degree_name = degree.name
    
    try:
        degree.delete()
        messages.success(request, f'Degree "{degree_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting degree: {str(e)}')
    
    return redirect('degree_list')


@login_required(login_url='admin_login')
def country_list(request):
    """List all countries with search and pagination"""
    search_query = request.GET.get('search', '')
    
    countries = Country.objects.annotate(
        state_count=Count('states')
    )
    
    if search_query:
        countries = countries.filter(name__icontains=search_query)
    
    countries = countries.order_by('name')
    
    paginator = Paginator(countries, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_countries': Country.objects.count(),
    }
    
    return render(request, 'site_admin/country_list.html', context)


@login_required(login_url='admin_login')
def create_country(request):
    """Create a new country"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            
            Country.objects.create(name=name)
            
            messages.success(request, f'Country "{name}" created successfully!')
            return redirect('country_list')
            
        except Exception as e:
            messages.error(request, f'Error creating country: {str(e)}')
    
    context = {'is_edit': False}
    return render(request, 'site_admin/country_form.html', context)


@login_required(login_url='admin_login')
def edit_country(request, pk):
    """Edit an existing country"""
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        try:
            country.name = request.POST.get('name')
            country.save()
            
            messages.success(request, f'Country "{country.name}" updated successfully!')
            return redirect('country_list')
            
        except Exception as e:
            messages.error(request, f'Error updating country: {str(e)}')
    
    context = {
        'country': country,
        'is_edit': True,
    }
    return render(request, 'site_admin/country_form.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def delete_country(request, pk):
    """Delete a country"""
    country = get_object_or_404(Country, pk=pk)
    country_name = country.name
    
    try:
        country.delete()
        messages.success(request, f'Country "{country_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting country: {str(e)}')
    
    return redirect('country_list')


@login_required(login_url='admin_login')
def state_list(request):
    """List all states with search and pagination"""
    search_query = request.GET.get('search', '')
    country_filter = request.GET.get('country', '')
    
    states = State.objects.select_related('country').annotate(
        district_count=Count('districts')
    )
    
    if search_query:
        states = states.filter(
            Q(name__icontains=search_query) | 
            Q(country__name__icontains=search_query)
        )
    
    if country_filter:
        states = states.filter(country_id=country_filter)
    
    states = states.order_by('name')
    
    paginator = Paginator(states, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    countries = Country.objects.order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'country_filter': country_filter,
        'countries': countries,
        'total_states': State.objects.count(),
    }
    
    return render(request, 'site_admin/state_list.html', context)


@login_required(login_url='admin_login')
def create_state(request):
    """Create a new state"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            country_id = request.POST.get('country')
            
            State.objects.create(
                name=name,
                country_id=country_id
            )
            
            messages.success(request, f'State "{name}" created successfully!')
            return redirect('state_list')
            
        except Exception as e:
            messages.error(request, f'Error creating state: {str(e)}')
    
    countries = Country.objects.order_by('name')
    context = {
        'countries': countries,
        'is_edit': False,
    }
    return render(request, 'site_admin/state_form.html', context)


@login_required(login_url='admin_login')
def edit_state(request, pk):
    """Edit an existing state"""
    state = get_object_or_404(State, pk=pk)
    
    if request.method == 'POST':
        try:
            state.name = request.POST.get('name')
            state.country_id = request.POST.get('country')
            state.save()
            
            messages.success(request, f'State "{state.name}" updated successfully!')
            return redirect('state_list')
            
        except Exception as e:
            messages.error(request, f'Error updating state: {str(e)}')
    
    countries = Country.objects.order_by('name')
    context = {
        'state': state,
        'countries': countries,
        'is_edit': True,
    }
    return render(request, 'site_admin/state_form.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def delete_state(request, pk):
    """Delete a state"""
    state = get_object_or_404(State, pk=pk)
    state_name = state.name
    
    try:
        state.delete()
        messages.success(request, f'State "{state_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting state: {str(e)}')
    
    return redirect('state_list')


@login_required(login_url='admin_login')
def district_list(request):
    """List all districts with search and pagination"""
    search_query = request.GET.get('search', '')
    state_filter = request.GET.get('state', '')
    
    districts = District.objects.select_related('state__country').annotate(
        college_count=Count('colleges')
    )
    
    if search_query:
        districts = districts.filter(
            Q(name__icontains=search_query) | 
            Q(state__name__icontains=search_query)
        )
    
    if state_filter:
        districts = districts.filter(state_id=state_filter)
    
    districts = districts.order_by('name')
    
    paginator = Paginator(districts, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    states = State.objects.select_related('country').order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'state_filter': state_filter,
        'states': states,
        'total_districts': District.objects.count(),
    }
    
    return render(request, 'site_admin/district_list.html', context)


@login_required(login_url='admin_login')
def create_district(request):
    """Create a new district"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            state_id = request.POST.get('state')
            
            District.objects.create(
                name=name,
                state_id=state_id
            )
            
            messages.success(request, f'District "{name}" created successfully!')
            return redirect('district_list')
            
        except Exception as e:
            messages.error(request, f'Error creating district: {str(e)}')
    
    states = State.objects.select_related('country').order_by('country__name', 'name')
    context = {
        'states': states,
        'is_edit': False,
    }
    return render(request, 'site_admin/district_form.html', context)


@login_required(login_url='admin_login')
def edit_district(request, pk):
    """Edit an existing district"""
    district = get_object_or_404(District, pk=pk)
    
    if request.method == 'POST':
        try:
            district.name = request.POST.get('name')
            district.state_id = request.POST.get('state')
            district.save()
            
            messages.success(request, f'District "{district.name}" updated successfully!')
            return redirect('district_list')
            
        except Exception as e:
            messages.error(request, f'Error updating district: {str(e)}')
    
    states = State.objects.select_related('country').order_by('country__name', 'name')
    context = {
        'district': district,
        'states': states,
        'is_edit': True,
    }
    return render(request, 'site_admin/district_form.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def delete_district(request, pk):
    """Delete a district"""
    district = get_object_or_404(District, pk=pk)
    district_name = district.name
    
    try:
        district.delete()
        messages.success(request, f'District "{district_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting district: {str(e)}')
    
    return redirect('district_list')
