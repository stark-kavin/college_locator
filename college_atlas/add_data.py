import os
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_atlas.settings')
django.setup()

from site_admin.models import Country, State, District, College
from django.db import transaction


def extract_pincode(address):
    """Extract pincode from address string"""
    import re
    # Look for 6-digit pincode pattern
    match = re.search(r'\b\d{6}\b', address)
    return match.group(0) if match else '000000'


def clean_phone(phone):
    """Clean phone number"""
    if phone:
        return phone.strip()
    return None


def clean_url(url):
    """Clean URL"""
    if url and url.strip():
        return url.strip()
    return None


def extract_college_name(college_field):
    """Extract college name from field (removing ID if present)"""
    if not college_field:
        return ''
    # Remove the (Id: C-XXXXX) part
    import re
    name = re.sub(r'\s*\(Id:\s*C-\d+\)\s*$', '', college_field)
    return name.strip()


def extract_university_name(university_field):
    """Extract university name from field (removing ID if present)"""
    if not university_field:
        return None
    # Remove the (Id: U-XXXX) part
    import re
    name = re.sub(r'\s*\(Id:\s*U-\d+\)\s*$', '', university_field)
    return name.strip() if name else None


def load_data_from_json():
    """Load college data from all JSON files in the data folder"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        return
    
    # Get all JSON files
    json_files = [f for f in os.listdir(data_dir) if f.endswith('_colleges_details.json')]
    
    if not json_files:
        print("No JSON files found in data directory")
        return
    
    print(f"Found {len(json_files)} JSON files to process")
    
    # Create India country if it doesn't exist
    country, created = Country.objects.get_or_create(name='India')
    if created:
        print("Created country: India")
    
    total_colleges = 0
    skipped_colleges = 0
    
    with transaction.atomic():
        for json_file in json_files:
            file_path = os.path.join(data_dir, json_file)
            print(f"\nProcessing: {json_file}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    colleges_data = json.load(f)
                
                for college_data in colleges_data:
                    try:
                        # Get or create state
                        state_name = college_data.get('state', '').strip()
                        if not state_name:
                            print(f"  Skipping college with no state: {college_data.get('college', 'Unknown')}")
                            skipped_colleges += 1
                            continue
                        
                        state, _ = State.objects.get_or_create(
                            name=state_name,
                            country=country
                        )
                        
                        # Get or create district
                        district_name = college_data.get('district', '').strip()
                        if not district_name:
                            district_name = 'Unknown'
                        
                        district, _ = District.objects.get_or_create(
                            name=district_name,
                            state=state
                        )
                        
                        # Extract college name
                        college_name = extract_college_name(college_data.get('college', ''))
                        if not college_name:
                            print(f"  Skipping college with no name in {state_name}")
                            skipped_colleges += 1
                            continue
                        
                        # Extract university name
                        university_name = extract_university_name(college_data.get('university'))
                        
                        # Extract address and pincode
                        address = college_data.get('address', '').strip()
                        pincode = extract_pincode(address)
                        
                        # Get coordinates
                        latitude = college_data.get('latitude')
                        longitude = college_data.get('longitude')
                        
                        # Convert to float/Decimal if present
                        if latitude:
                            try:
                                latitude = float(latitude)
                            except (ValueError, TypeError):
                                latitude = None
                        
                        if longitude:
                            try:
                                longitude = float(longitude)
                            except (ValueError, TypeError):
                                longitude = None
                        
                        # Create or update college
                        college, created = College.objects.update_or_create(
                            name=college_name,
                            district=district,
                            defaults={
                                'university': university_name,
                                'college_type': 'other',  # Default type, can be updated manually
                                'address_line': address if address else '',
                                'pincode': pincode,
                                'website': clean_url(college_data.get('website')),
                                'phone_number': clean_phone(college_data.get('phone')),
                                'latitude': latitude,
                                'longitude': longitude,
                                'image_url': clean_url(college_data.get('image_url')),
                            }
                        )
                        
                        if created:
                            total_colleges += 1
                        
                    except Exception as e:
                        print(f"  Error processing college {college_data.get('college', 'Unknown')}: {str(e)}")
                        skipped_colleges += 1
                        continue
                
                print(f"  ✓ Completed {json_file}")
                
            except json.JSONDecodeError as e:
                print(f"  Error reading {json_file}: {str(e)}")
                continue
            except Exception as e:
                print(f"  Unexpected error with {json_file}: {str(e)}")
                continue
    
    print(f"\n{'='*50}")
    print(f"Data import completed!")
    print(f"Total colleges added: {total_colleges}")
    print(f"Skipped colleges: {skipped_colleges}")
    print(f"Total states: {State.objects.count()}")
    print(f"Total districts: {District.objects.count()}")
    print(f"{'='*50}")


if __name__ == '__main__':
    print("Starting data import from JSON files...")
    print(f"{'='*50}\n")
    load_data_from_json()
