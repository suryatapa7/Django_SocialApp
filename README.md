# Django Social App - "til"

This is a social web application built with Django 5.2. The project includes multiple apps to provide social networking features such as user profiles, following other users, and posting content feeds.

## Features

- User authentication and registration using email with django-allauth
- User profiles with editable information and profile images
- Follow/unfollow functionality between users
- Content feed where users can create and view posts
- Media file handling for profile images and posts
- Responsive frontend with templates and static assets

## Project Structure

- `feed/` - Handles posts and content feed functionality
- `profiles/` - Manages user profiles and custom authentication forms
- `followers/` - Implements following relationships between users
- `til/` - Main project configuration including settings and URL routing
- `frontend/` - Contains frontend static files such as JavaScript
- `media/` - Directory for uploaded media files (profile images, post images)
- `static/` - Collected static files for deployment

## Installation

This project uses [pipenv](https://pipenv.pypa.io/en/latest/) for dependency management.

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

## Running the Development Server

Start the Django development server with:

```bash
python manage.py runserver
```

Then open your browser and navigate to `http://127.0.0.1:8000/`.

## Configuration

- Static files are served from the `frontend/` directory during development and collected into `static/` for deployment.
- Media files (uploads) are stored in the `media/` directory.
- Authentication is handled via django-allauth with email login and custom forms defined in the `profiles` app.

## Additional Notes

- The project uses SQLite as the default database.
- Templates are located in the `til/templates` directory and within each app's `templates` folder.
- The project includes support for thumbnailing images using `sorl.thumbnail`.

## License

This project is licensed under the MIT License.
