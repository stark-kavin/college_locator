# College Atlas - Deployment to Render.com

## Prerequisites
- A Render.com account
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Create a PostgreSQL Database on Render
1. Log in to your Render dashboard
2. Click "New +" and select "PostgreSQL"
3. Give it a name (e.g., `college-atlas-db`)
4. Choose a region close to your users
5. Select the free plan or your preferred plan
6. Click "Create Database"
7. Note: Render will automatically provide the `DATABASE_URL` to your web service

### 2. Create a Web Service on Render
1. Click "New +" and select "Web Service"
2. Connect your Git repository
3. Configure the service:
   - **Name**: college-atlas (or your preferred name)
   - **Region**: Same as your database
   - **Branch**: main (or your default branch)
   - **Root Directory**: `college_atlas`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn college_atlas.wsgi:application`

### 3. Set Environment Variables
In the Render dashboard for your web service, go to the "Environment" tab and add:

- **SECRET_KEY**: Generate a new Django secret key (you can use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- **DEBUG**: `False` (for production)
- **RENDER_EXTERNAL_HOSTNAME**: Your Render app URL (e.g., `college-atlas.onrender.com`)
- **DATABASE_URL**: This will be automatically set when you link the PostgreSQL database
- **PYTHON_VERSION**: `3.11.4` (or your Python version)

### 4. Link the Database
1. In your web service settings, scroll to "Environment Variables"
2. Click "Add from Database" and select your PostgreSQL database
3. This will automatically add the `DATABASE_URL` environment variable

### 5. Deploy
1. Click "Create Web Service" or "Deploy" if it's already created
2. Render will build and deploy your application
3. Monitor the logs for any errors
4. Once deployed, your app will be available at `https://your-app-name.onrender.com`

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and update with your local settings:
   ```bash
   cp .env.example .env
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Important Notes

- **Static Files**: Whitenoise is configured to serve static files in production
- **Database**: The app uses SQLite locally and PostgreSQL in production
- **Media Files**: For production, consider using cloud storage (AWS S3, Cloudinary, etc.) for user-uploaded files
- **Security**: Never commit your `.env` file with real credentials to version control
- **SSL**: Render provides free SSL certificates automatically

## Troubleshooting

- If migrations fail, check your `DATABASE_URL` is correctly set
- If static files don't load, ensure `STATIC_ROOT` is set and `collectstatic` ran successfully
- Check Render logs for detailed error messages
- Ensure all required environment variables are set in Render dashboard
