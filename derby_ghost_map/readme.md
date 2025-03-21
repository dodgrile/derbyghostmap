# Derby Ghost Stories Map

An interactive web application that allows users to explore ghost stories around Derby. The app displays various points on a map, and each point leads to a specific flash fiction story with text, images, and audio narration.

Created for the Creative Project module of University of Derbys' humanities foundation year

## Features

- Interactive map of Derby with marked ghost story locations
- Detailed story pages with text, images, and audio narration
- Mobile-responsive design with atmospheric styling
- Admin interface for easy content management
- Navigation between stories at the same location

## Technology Stack

- **Backend**: Python with Django and Wagtail CMS
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Map Integration**: Leaflet.js (open-source JavaScript library)

## Local Development Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/derby-ghost-map.git
   cd derby-ghost-map
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser for the admin interface:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://localhost:8000 and the admin interface at http://localhost:8000/admin

## Content Management

### Adding Locations

1. Log in to the Wagtail admin
2. Navigate to Pages
3. Find the Ghost Map page and click "Add child page"
4. Select "Location Page"
5. Fill in details:
   - Title
   - Description
   - Coordinates (format: "latitude,longitude")
   - Featured image
   - History and other details

### Adding Stories

1. Navigate to a Location Page in the admin
2. Click "Add child page"
3. Select "Story Page"
4. Fill in details:
   - Title
   - Summary
   - Main image
   - Story content (using the StreamField blocks)
   - Audio narration (upload an MP3 file)
   - Year, author, sources, etc.

## Deployment

This application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure with:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn derby_ghost_map.wsgi:application`
4. Add environment variables:
   - `SECRET_KEY`: Your Django secret key
   - `DJANGO_SETTINGS_MODULE`: derby_ghost_map.settings.production
   - `DATABASE_URL`: Your PostgreSQL database URL

## Project Structure

```
derby_ghost_map/
├── derby_ghost_map/        # Project settings
├── ghost_stories/          # Main app
│   ├── models.py           # Wagtail page models
│   ├── blocks.py           # StreamField block definitions
│   ├── api.py              # API views for map data
│   ├── templates/          # HTML templates
│   └── static/             # Static files (CSS, JS, images)
├── static/                 # Global static files
├── media/                  # User-uploaded content
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- All the ghost story contributors
- Leaflet.js for the mapping functionality
- Wagtail CMS for the content management system
