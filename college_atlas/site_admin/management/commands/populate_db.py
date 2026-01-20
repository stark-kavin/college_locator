from django.core.management.base import BaseCommand
from site_admin.models import Country, State, District, College, Degree
from django.core.files.base import ContentFile
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        if College.objects.exists():
            self.stdout.write('Clearing existing data...')
            College.objects.all().delete()
            District.objects.all().delete()
            State.objects.all().delete()
            Country.objects.all().delete()
            Degree.objects.all().delete()

        usa = Country.objects.create(name='United States')
        india = Country.objects.create(name='India')

        ca = State.objects.create(name='California', country=usa)
        ny = State.objects.create(name='New York', country=usa)
        ma = State.objects.create(name='Massachusetts', country=usa)
        tn = State.objects.create(name='Tamil Nadu', country=india)

        stanford_dist = District.objects.create(name='Stanford', state=ca)
        berkeley_dist = District.objects.create(name='Berkeley', state=ca)
        cambridge_dist = District.objects.create(name='Cambridge', state=ma)
        ny_dist = District.objects.create(name='New York City', state=ny)
        chennai_dist = District.objects.create(name='Chennai', state=tn)

        bs_eng = Degree.objects.create(name='B.S. Engineering', duration_years=4)
        ms_cs = Degree.objects.create(name='M.S. Computer Science', duration_years=2)
        phd = Degree.objects.create(name='Ph.D.', duration_years=5)
        mba = Degree.objects.create(name='MBA', duration_years=2)
        md = Degree.objects.create(name='M.D. Medicine', duration_years=4)

        stanford = College.objects.create(
            name='Stanford University',
            college_type='eng',
            district=stanford_dist,
            address_line='450 Serra Mall',
            pincode='94305',
            website='https://www.stanford.edu',
            email='admission@stanford.edu',
            phone_number='+1 650-723-2300',
            latitude=37.4275,
            longitude=-122.1697
        )
        stanford.degrees.add(bs_eng, ms_cs, phd, mba, md)

        mit = College.objects.create(
            name='Massachusetts Institute of Technology',
            college_type='eng',
            district=cambridge_dist,
            address_line='77 Massachusetts Ave',
            pincode='02139',
            website='https://www.mit.edu',
            email='admissions@mit.edu',
            phone_number='+1 617-253-1000',
            latitude=42.3601,
            longitude=-71.0942
        )
        mit.degrees.add(bs_eng, ms_cs, phd)

        harvard = College.objects.create(
            name='Harvard University',
            college_type='arts',
            district=cambridge_dist,
            address_line='Massachusetts Hall',
            pincode='02138',
            website='https://www.harvard.edu',
            email='admissions@harvard.edu',
            phone_number='+1 617-495-1000',
            latitude=42.3736,
            longitude=-71.1097
        )
        harvard.degrees.add(phd, mba, md)

        columbia = College.objects.create(
            name='Columbia University',
            college_type='arts',
            district=ny_dist,
            address_line='116th St & Broadway',
            pincode='10027',
            website='https://www.columbia.edu',
            email='askc@columbia.edu',
            phone_number='+1 212-854-1754',
            latitude=40.8075,
            longitude=-73.9626
        )
        columbia.degrees.add(bs_eng, ms_cs, mba)
        
        iitm = College.objects.create(
            name='IIT Madras',
            college_type='eng',
            district=chennai_dist,
            address_line='IIT P.O., Chennai',
            pincode='600036',
            website='https://www.iitm.ac.in',
            email='registrar@iitm.ac.in',
            phone_number='+91 44 2257 8000',
            latitude=12.9915,
            longitude=80.2337
        )
        iitm.degrees.add(bs_eng, ms_cs, phd)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data'))
