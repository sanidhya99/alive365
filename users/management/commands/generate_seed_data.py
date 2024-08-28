import random
from django.core.management.base import BaseCommand
from faker import Faker
from authentication.models import CustomUser
from doctors.models import DoctorCategory, Doctors
from users.models import Appointments, UserOffers

fake = Faker()

class Command(BaseCommand):
    help = 'Generate seed data for the project'

    def handle(self, *args, **kwargs):
        self.generate_users()
        self.generate_categories()
        self.generate_doctors()
        self.generate_appointments()
        self.generate_user_offers()

    def generate_users(self):
        for _ in range(10):
            user = CustomUser(
                name=fake.name(),
                phone=fake.phone_number()[:10],
                email=fake.email(),
                gender=fake.random_element(elements=('Male', 'Female')),
                dob=fake.date_of_birth(minimum_age=20, maximum_age=60),
                blood_group=fake.random_element(elements=('A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-')),
                marital_status=fake.boolean(),
                height=fake.random_number(digits=2, fix_len=True),
                weight=fake.random_number(digits=2, fix_len=True),
                emergency_contact=fake.phone_number()[:10],
                location=fake.city(),
                otp=fake.random_number(digits=4, fix_len=True),
                otp_verified=fake.boolean(),
                is_staff=False,
                is_superuser=False
            )
            user.set_password('password')
            user.save()

    def generate_categories(self):
        for _ in range(10):
            category = DoctorCategory(
                name=fake.word()
            )
            category.save()

    def generate_doctors(self):
        categories = DoctorCategory.objects.all()
        for _ in range(10):
            doctor = Doctors(
                name=fake.name(),
                phone=fake.phone_number()[:10],
                email=fake.email(),
                gender=fake.random_element(elements=('Male', 'Female')),
                dob=fake.date_of_birth(minimum_age=30, maximum_age=60),
                blood_group=fake.random_element(elements=('A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-')),
                marital_status=fake.boolean(),
                height=fake.random_number(digits=2, fix_len=True),
                weight=fake.random_number(digits=2, fix_len=True),
                emergency_contact=fake.phone_number()[:10],
                location=fake.city(),
                otp=fake.random_number(digits=4, fix_len=True),
                otp_verified=fake.boolean(),
                is_staff=False,
                is_superuser=False,
                category=random.choice(categories),
                experience=fake.random_int(min=1, max=30),
                qualification=fake.random_element(elements=('MBBS', 'MD', 'MS')),
                qualification_doc=fake.file_name(extension='pdf'),
                identity_doc=fake.file_name(extension='pdf'),
                price=fake.random_int(min=500, max=5000),
                rating=fake.random_int(min=1, max=5),
                rating_no=fake.random_int(min=0, max=100),
                time_slot=[['09:00', '12:00'], ['13:00', '17:00']]
            )
            doctor.set_password('password')
            doctor.save()

    def generate_appointments(self):
        users = CustomUser.objects.all()
        doctors = Doctors.objects.all()
        for _ in range(10):
            appointment = Appointments(
                doctor=random.choice(doctors),
                patient=random.choice(users),
                phone=fake.phone_number()[:10],
                age=fake.random_int(min=18, max=80),
                gender=fake.random_element(elements=('Male', 'Female')),
                address=fake.address(),
                date=fake.date_between(start_date='-1y', end_date='today'),
                time_slot=fake.time(),
            )
            appointment.save()

    def generate_user_offers(self):
        for _ in range(10):
            offer = UserOffers(
                image=fake.image_url(width=800, height=600)
            )
            offer.save()
