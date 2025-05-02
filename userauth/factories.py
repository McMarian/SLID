import factory
from django.contrib.auth.models import User
from userauth.models import UserProfile, SocialMediaAccount, Post, Connection
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    fullName = factory.Faker('name')
    bio = factory.Faker('text')
    verified = factory.Faker('boolean')

class SocialMediaAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialMediaAccount

    user = factory.SubFactory(UserFactory)
    platform = factory.Iterator(['instagram', 'facebook', 'youtube', 'linkedin'])
    token = factory.Faker('uuid4')
    is_linked = True 