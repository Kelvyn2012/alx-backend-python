from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import timedelta, date

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample data (hosts, listings, bookings, reviews)."

    def handle(self, *args, **kwargs):
        # Create demo hosts
        hosts = []
        for i in range(3):
            host, _ = User.objects.get_or_create(
                username=f"host{i+1}",
                defaults={"email": f"host{i+1}@example.com", "password": "demo1234"},
            )
            hosts.append(host)

        self.stdout.write(self.style.SUCCESS(f"Created {len(hosts)} hosts."))

        # Create demo guests
        guests = []
        for i in range(5):
            guest, _ = User.objects.get_or_create(
                username=f"guest{i+1}",
                defaults={"email": f"guest{i+1}@example.com", "password": "demo1234"},
            )
            guests.append(guest)

        self.stdout.write(self.style.SUCCESS(f"Created {len(guests)} guests."))

        # Create sample listings
        listings = []
        for i in range(5):
            listing, _ = Listing.objects.get_or_create(
                title=fake.sentence(nb_words=4),
                defaults={
                    "description": fake.paragraph(nb_sentences=3),
                    "location": fake.city(),
                    "price_per_night": round(random.uniform(30, 300), 2),
                    "host": random.choice(hosts),
                },
            )
            listings.append(listing)

        self.stdout.write(self.style.SUCCESS(f"Created {len(listings)} listings."))

        # Create sample bookings
        for _ in range(10):
            listing = random.choice(listings)
            guest = random.choice(guests)
            check_in = fake.date_between(start_date="-1y", end_date="today")
            check_out = check_in + timedelta(days=random.randint(1, 14))

            Booking.objects.get_or_create(
                listing=listing,
                user=guest,
                check_in=check_in,
                check_out=check_out,
                defaults={
                    "status": random.choice(["pending", "confirmed", "cancelled"])
                },
            )

        self.stdout.write(self.style.SUCCESS("Created sample bookings."))

        # Create sample reviews
        for listing in listings:
            for guest in random.sample(guests, k=random.randint(1, len(guests))):
                Review.objects.get_or_create(
                    listing=listing,
                    user=guest,
                    defaults={
                        "rating": random.randint(1, 5),
                        "comment": fake.sentence(nb_words=10),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Created sample reviews."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
