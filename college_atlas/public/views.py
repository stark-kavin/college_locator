from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from site_admin.models import College, State, District, Country

def home(request):
    """
    Renders the home page with necessary context for search dropdowns.
    """
    states = State.objects.all()
    countries = Country.objects.all()
    
    context = {
        'states': states,
        'countries': countries,
    }
    return render(request, 'public/home.html', context)

def college_detail(request, pk):
    """
    Renders the detail view for a specific college.
    """
    college = get_object_or_404(College, pk=pk)
    return render(request, 'public/college.html', {'college': college})

def filter_college(request):
    """
    Handles searching and filtering of colleges.
    """
    query = request.GET.get('q', '')
    country_id = request.GET.get('country')
    state_id = request.GET.get('state')
    district_id = request.GET.get('district')
    
    colleges = College.objects.select_related('district', 'district__state', 'district__state__country').all()
    
    if query:
        colleges = colleges.filter(
            Q(name__icontains=query) | 
            Q(district__name__icontains=query) | 
            Q(district__state__name__icontains=query)
        )
    
    if country_id:
        colleges = colleges.filter(district__state__country__id=country_id)
        
    if state_id:
        colleges = colleges.filter(district__state__id=state_id)
        
    if district_id:
        colleges = colleges.filter(district__id=district_id)

    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        colleges = colleges.order_by('name')
        
    paginator = Paginator(colleges, 12) # Show 12 colleges per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    countries = Country.objects.all()
    states = State.objects.filter(country_id=country_id) if country_id else []
    districts = District.objects.filter(state_id=state_id) if state_id else []

    context = {
        'colleges': page_obj,
        'countries': countries,
        'states': states,
        'districts': districts,
        'current_filters': {
            'q': query,
            'country': country_id,
            'state': state_id,
            'district': district_id,
        }
    }
    return render(request, 'public/filter_college.html', context)

def map_search(request):
    """
    Renders the map search view with college data for the map.
    """
    colleges = College.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    ).values('id', 'name', 'latitude', 'longitude', 'district__name', 'district__state__name')
    
    context = {
        'colleges_data': list(colleges) # Pass as list to be easily serialized to JSON in template
    }
    return render(request, 'public/map_search.html', context)

def get_states(request):
    """
    AJAX endpoint to get states for a selected country.
    """
    country_id = request.GET.get('country_id')
    if country_id:
        states = State.objects.filter(country_id=country_id).values('id', 'name')
        return JsonResponse({'states': list(states)})
    return JsonResponse({'states': []})

def get_districts(request):
    """
    AJAX endpoint to get districts for a selected state.
    """
    state_id = request.GET.get('state_id')
    if state_id:
        districts = District.objects.filter(state_id=state_id).values('id', 'name')
        return JsonResponse({'districts': list(districts)})
    return JsonResponse({'districts': []})
