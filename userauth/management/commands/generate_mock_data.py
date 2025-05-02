from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userauth.models import UserProfile, SocialMediaAccount, Connection, Post, TermsAndConditions
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate comprehensive mock data for SLID database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write('Starting mock data generation...')

        # Clear existing data (optional - uncomment if needed)
        # self.stdout.write('Clearing existing data...')
        # User.objects.all().delete()

        # Create users with all related data
        self.stdout.write('Creating users and related data...')
        users = []
        profile_pictures = ['default_pp1.png', 'default_pp2.png', 'default_pp3.png']
        
        # Create 50 users with complete profiles
        for i in range(50):
            # Create user
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_joined=fake.date_time_between(start_date='-2y'),
                is_active=True
            )
            users.append(user)

            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                fullName=f"{user.first_name} {user.last_name}",
                bio=fake.text(max_nb_chars=200),
                profilePicture=random.choice(profile_pictures),
                user_code=fake.lexify(text='????####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                verified=random.choices([True, False], weights=[0.2, 0.8])[0],
                created_at=user.date_joined,
                profile_score=random.randint(0, 100),
                is_deleted=False
            )

            # Create terms acceptance
            TermsAndConditions.objects.create(
                user=user,
                accepted=True,
                date_accepted=user.date_joined + timedelta(minutes=random.randint(1, 60))
            )

        # Create social media accounts
        self.stdout.write('Creating social media accounts...')
        platforms = ['facebook', 'instagram', 'youtube', 'linkedin', 'google', 'x', 'tiktok']
        for user in users:
            # Each user has 2-5 social media accounts
            for platform in random.sample(platforms, random.randint(2, 5)):
                followers = random.randint(100, 50000)
                SocialMediaAccount.objects.create(
                    user=user,
                    platform=platform,
                    token=fake.uuid4(),
                    token_type='bearer',
                    expires=timezone.now() + timedelta(days=60),
                    data={
                        'followers': followers,
                        'following': int(followers * random.uniform(0.1, 1.5)),
                        'posts': random.randint(10, 1000),
                        'engagement_rate': round(random.uniform(0.01, 0.15), 4),
                        'last_post_date': fake.date_time_between(start_date='-30d').isoformat()
                    },
                    last_sync=fake.date_time_between(start_date='-7d'),
                    is_linked=True
                )

        # Create connections between users
        self.stdout.write('Creating user connections...')
        for user in users:
            # Each user connects with 5-15 other users
            other_users = random.sample([u for u in users if u != user], 
                                     random.randint(5, min(15, len(users)-1)))
            for other_user in other_users:
                Connection.objects.create(
                    user=user,
                    connected_user=other_user,
                    created_at=fake.date_time_between(
                        start_date=max(user.date_joined, other_user.date_joined)
                    ),
                    is_deleted=random.choices([True, False], weights=[0.1, 0.9])[0]
                )

        # Create posts
        self.stdout.write('Creating posts...')
        content_types = ['text', 'image', 'video']
        for user in users:
            # Create 10-30 posts for each user
            for _ in range(random.randint(10, 30)):
                content_type = random.choice(content_types)
                media_file = None
                if content_type == 'image':
                    media_file = f'posts/media/image_{random.randint(1, 10)}.jpg'
                elif content_type == 'video':
                    media_file = f'posts/media/video_{random.randint(1, 5)}.mp4'

                Post.objects.create(
                    user=user,
                    content_type=content_type,
                    content=fake.text() if content_type == 'text' else fake.sentence(),
                    media_file=media_file,
                    created_at=fake.date_time_between(
                        start_date=user.date_joined
                    ),
                    metadata={
                        'likes': random.randint(0, 5000),
                        'shares': random.randint(0, 500),
                        'comments': random.randint(0, 200),
                        'views': random.randint(100, 50000) if content_type in ['video', 'image'] else None,
                        'engagement_rate': round(random.uniform(0.01, 0.25), 4),
                        'platforms_shared': random.sample(platforms, random.randint(1, 3))
                    },
                    is_deleted=random.choices([True, False], weights=[0.05, 0.95])[0]
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated mock data for {len(users)} users'))
