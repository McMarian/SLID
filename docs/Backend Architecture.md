# Backend Architecture of SLID

The backend architecture of SLID follows Django's Model-View-Controller (MVC) pattern, commonly referred to in Django as the Model-View-Template (MVT) pattern. Each component has a distinct role in the overall application structure, ensuring separation of concerns and modularity. Each app within the project has a specific role, and files such as ``models.py``, ``views.py``, ``urls.py``, ``admin.py``, ``forms.py``, ``tests.py``, and ``apps.py`` are organized according to Django's best practices. The following breakdown provides a detailed overview of how the project is structured, the functionality of different files, and how they work together to implement SLID’s features.

## Project Structure Overview
The SLID django project is divided into multiple apps that each focus on specific functionality, such as authentication, profile management, and content creation. Here's a generalized directory structure:
```
SLID/
│
├── auth_app/             # Handles user authentication
│   ├── migrations/       # Database migration files
│   ├── models.py         # Database models for user authentication
│   ├── views.py          # Views that process requests and return responses for authentication
│   ├── urls.py           # URL routing for the authentication-related views
│   ├── forms.py          # Forms for user login, registration, etc.
│   ├── admin.py          # Admin interface configuration for managing user authentication
│   ├── tests.py          # Unit tests for authentication functionality
│   └── apps.py           # Django app configuration for authentication
│
├── profile_app/          # Manages user profiles and connections
│   ├── migrations/
│   ├── models.py         # Database models for user profiles
│   ├── views.py          # Profile-related views (complete profile, edit profile, etc.)
│   ├── urls.py           # URL routing for profile-related operations
│   ├── forms.py          # Forms related to profile completion and updates
│   ├── admin.py          # Admin interface for managing user profiles
│   ├── tests.py          # Unit tests for profile management
│   └── apps.py           # Django app configuration for profiles
│
├── post_app/             # Handles content creation and social media integration
│   ├── migrations/
│   ├── models.py         # Models for posts (text, images, video) and social media integration
│   ├── views.py          # Views to create, update, and delete posts, as well as share them on social media
│   ├── urls.py           # URL routing for post-related actions
│   ├── forms.py          # Forms for creating or editing posts
│   ├── admin.py          # Admin interface for managing posts
│   ├── tests.py          # Unit tests for post creation and social media integration
│   └── apps.py           # Django app configuration for posts
│
├── settings.py           # Global Django settings (database config, middleware, etc.)
├── urls.py               # Main project URL routing
├── wsgi.py               # WSGI configuration for deployment
└── manage.py             # Django's command-line utility for administrative tasks
```

## Django MVT Pattern
Django’s Model-View-Template (MVT) architecture follows a structured approach for organizing the backend logic and database management. Here's how each component works within SLID:

* Model (Database Layer): Models are responsible for defining the structure of the data, such as users, profiles, and posts. SLID uses Django’s ORM (Object-Relational Mapper) to define models as Python classes. Each class represents a table in the database. For example:
    * In ``auth_app/models.py``, a ``User`` model defines fields like ``username``, ``email``, and ``password``, along with the necessary authentication logic.
    * In ``profile_app/models.py``, a ``Profile`` model defines fields such as ``bio``, ``profile_picture``, and ``social_links``.
    * In ``post_app/models.py``, a ``Post`` model contains fields for post content (e.g., text, image, or video) and stores the necessary metadata for social media integration.

* View (Controller Logic): Views are responsible for processing HTTP requests and returning HTTP responses. In SLID, views interact with the models to retrieve data from the database and render it using templates. These views handle the core logic of the system, such as user authentication, profile management, and content creation.
    * In ``auth_app/views.py``, the ``signUp`` and ``signIn`` views handle user registration and login. They use forms to validate input, communicate with the ``User`` model, and redirect users upon successful authentication.
    * In ``profile_app/views.py``, the ``completeProfile`` view is responsible for letting users add extra information to their profiles after sign-up.
    * In ``post_app/views.py``, the ``createPost`` view processes requests from users creating new posts. Once the form is submitted, the view communicates with the ``Post`` model to store the data in the database and trigger social media API calls to share the post.

* Template (User Interface): Templates in Django are responsible for rendering the HTML that users see and interact with. Templates are tightly coupled with views. Each view passes context data (retrieved from models) to the template, which then displays the data.
    * For example, in ``profile_app``, the template file ``complete_profile.html`` renders the form where users can update their profile information.
    * In ``post_app``, the template file ``create_post.html`` allows users to input the content for a new post, such as text, images, or videos, and choose which social media platforms to share it on.

## App-specific Breakdown

### ``auth_app/`` (Authentication):

* ``models.py``: Defines the ``User`` model and any additional fields necessary for user authentication and OAuth token storage.
* ``views.py``: Handles user registration, login, and logout. Integrates with forms for authentication and session management.
* ``urls.py``: Maps URL paths for authentication endpoints (e.g., ``/login/``, ``/register/``).
* ``forms.py``: Contains forms like ``LoginForm`` and ``RegistrationForm`` for validating user credentials and input.
* ``admin.py``: Configures the Django admin interface for managing users. This includes enabling features like searching users, viewing profiles, and resetting passwords.
* ``tests.py``: Contains unit tests for authentication functionality. These tests ensure proper user creation, login validation, and session handling.
* ``apps.py``: Defines the app configuration for ``auth_app``. This is required to set default configurations and app-specific settings.

### ``profile_app/`` (Profile Management):

* ``models.py``: Defines the ``Profile`` model, which links to the ``User`` model and stores user-specific information such as bio, profile picture, and links to external social media accounts.
* ``views.py``: Handles profile viewing, editing, and completion. Communicates with forms to validate profile information.
* ``urls.py``: URL routing for profile-related pages, such as ``/profile/<username>/`` and ``/editProfile/``.
* ``forms.py``: Contains forms for updating profile information, such as ``ProfileForm`` for adding a bio, profile picture, and other data.
* ``admin.py``: Adds the ``Profile`` model to the Django admin interface, enabling admins to view and edit user profiles directly from the admin dashboard.
* ``tests.py``: Includes unit tests for profile-related functionality, such as verifying profile updates and ensuring profile completion processes work as expected.
* ``apps.py``: Defines the app configuration for ``profile_app``, including any custom configurations needed for profiles.

### ``post_app/`` (Content Creation & Social Media Sharing):

* ``models.py``: Defines the ``Post`` model for storing user-generated content (text, images, video). It also tracks metadata related to external social media platforms, such as post IDs and timestamps.
* ``views.py``: Manages content creation, editing, and deletion. This includes logic for sharing content across multiple social media platforms via API calls.
* ``urls.py``: Contains URL patterns for post creation, editing, and deletion (e.g., ``/createPost/``, ``/updatePost/``, ``/deletePost/``).
* ``forms.py``: Provides forms for users to input content when creating or editing posts.
* ``admin.py``: Configures the Django admin interface for managing posts. Admins can view and delete posts, as well as check post statuses across platforms.
* ``tests.py``: Unit tests for post creation, updating, deletion, and social media synchronization. These tests ensure that the content-sharing functionality works correctly.
* ``apps.py``: Defines the app configuration for ``post_app``, managing post-related settings and initialization code.