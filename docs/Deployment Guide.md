# Deployment Guide

## Introduction

This guide provides detailed instructions for deploying the SLID application in various environments. SLID is a Django-based web application that can be deployed using different methods depending on your infrastructure requirements and scale needs.

## Deployment Options

SLID can be deployed using the following methods:

1. **Docker Deployment** (Recommended)
   - Simple local deployment with Docker Compose
   - Production deployment with Docker Swarm or Kubernetes

2. **Cloud-Based Deployment**
   - Google Cloud Platform (GCP) with Cloud Run
   - Amazon Web Services (AWS) with Elastic Beanstalk
   - Microsoft Azure with App Service

3. **Traditional Server Deployment**
   - Ubuntu/Debian server with Gunicorn and Nginx
   - CentOS/RHEL server with Gunicorn and Apache

## Pre-Deployment Checklist

Before deploying SLID, ensure you have completed the following steps:

- [ ] Set all environment variables in a `.env` file or your deployment platform's environment settings
- [ ] Configure your database settings
- [ ] Set up social media API credentials
- [ ] Generate and configure a secure Django `SECRET_KEY`
- [ ] Configure static and media file storage
- [ ] Ensure `DEBUG=False` for production deployments
- [ ] Run `python manage.py check --deploy` to verify deployment security

## Docker Deployment

### Local Development with Docker Compose

The easiest way to get started with SLID is using Docker Compose for local development:

1. Ensure you have Docker and Docker Compose installed
2. Clone the SLID repository:
   ```bash
   git clone https://github.com/McMarian/SLID.git
   cd SLID
   ```

3. Create a `.env` file with your environment variables:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgres://postgres:postgres@db:5432/slid
   ALLOWED_HOSTS=localhost,127.0.0.1
   OPENAI_API_KEY=your_openai_key
   INSTAGRAM_CLIENT_ID=your_instagram_client_id
   INSTAGRAM_CLIENT_SECRET=your_instagram_client_secret
   FACEBOOK_CLIENT_ID=your_facebook_client_id
   FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
   ```

4. Run Docker Compose:
   ```bash
   docker-compose up
   ```

5. Access SLID at `http://localhost:8000`

### Production Deployment with Docker

For production, you'll need to modify the Docker configuration:

1. Update `docker-compose.yml` to use a production-ready configuration:
   ```yaml
   version: '3'

   services:
     web:
       build: .
       restart: always
       env_file: .env.prod
       volumes:
         - static_volume:/app/static
         - media_volume:/app/static/images
       depends_on:
         - db
         - redis
       networks:
         - slid-network

     db:
       image: postgres:14
       restart: always
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       env_file: .env.prod
       networks:
         - slid-network

     redis:
       image: redis:7
       restart: always
       networks:
         - slid-network

     nginx:
       image: nginx:1.23
       restart: always
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx/:/etc/nginx/conf.d/
         - static_volume:/usr/share/nginx/html/static
         - media_volume:/usr/share/nginx/html/media
         - ./certbot/conf:/etc/letsencrypt
         - ./certbot/www:/var/www/certbot
       depends_on:
         - web
       networks:
         - slid-network

     certbot:
       image: certbot/certbot
       volumes:
         - ./certbot/conf:/etc/letsencrypt
         - ./certbot/www:/var/www/certbot

   volumes:
     postgres_data:
     static_volume:
     media_volume:

   networks:
     slid-network:
   ```

2. Create an Nginx configuration file at `nginx/default.conf`:
   ```
   upstream slid {
       server web:8000;
   }

   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location /.well-known/acme-challenge/ {
           root /var/www/certbot;
       }

       location / {
           return 301 https://$host$request_uri;
       }
   }

   server {
       listen 443 ssl;
       server_name your-domain.com www.your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

       location /static/ {
           alias /usr/share/nginx/html/static/;
       }

       location /media/ {
           alias /usr/share/nginx/html/media/;
       }

       location / {
           proxy_pass http://slid;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Host $host;
           proxy_redirect off;
           client_max_body_size 20M;
       }
   }
   ```

3. Create a production environment file `.env.prod`:
   ```
   DEBUG=False
   SECRET_KEY=your_production_secret_key
   DATABASE_URL=postgres://postgres:secure_password@db:5432/slid
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   OPENAI_API_KEY=your_openai_key
   INSTAGRAM_CLIENT_ID=your_instagram_client_id
   INSTAGRAM_CLIENT_SECRET=your_instagram_client_secret
   FACEBOOK_CLIENT_ID=your_facebook_client_id
   FACEBOOK_CLIENT_SECRET=your_facebook_client_secret
   
   # Database settings
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=secure_password
   POSTGRES_DB=slid
   ```

4. Set up SSL certificates with Certbot:
   ```bash
   docker-compose run --rm certbot certonly --webroot -w /var/www/certbot -d your-domain.com -d www.your-domain.com
   ```

5. Start the production services:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

## Cloud-Based Deployment

### Google Cloud Platform (GCP) Deployment

SLID can be deployed to GCP using Cloud Run for the application and Cloud SQL for the database:

1. **Set up a GCP project**:
   - Create a new project in the GCP Console
   - Enable the required APIs (Cloud Run, Cloud SQL, Cloud Storage)

2. **Configure Cloud SQL**:
   - Create a PostgreSQL instance in Cloud SQL
   - Create a database named `slid`
   - Configure a user with appropriate permissions

3. **Set up Cloud Storage**:
   - Create buckets for static and media files
   - Configure appropriate permissions

4. **Modify SLID for GCP**:
   - Update settings.py to use GCP storage backends
   - Configure database connection to use Cloud SQL

5. **Deploy to Cloud Run**:
   - Build your container image
   - Push to Container Registry:
     ```bash
     gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/slid
     ```
   - Deploy to Cloud Run:
     ```bash
     gcloud run deploy slid --image gcr.io/YOUR_PROJECT_ID/slid --platform managed
     ```
   - Set environment variables in the Cloud Run console

For a complete GCP deployment guide with detailed architecture information, refer to [docs/Cloud Architecture.md](Cloud%20Architecture.md).

### AWS Elastic Beanstalk Deployment

To deploy SLID on AWS Elastic Beanstalk:

1. **Set up AWS account**:
   - Create an AWS account if you don't have one
   - Install the AWS CLI and EB CLI

2. **Configure AWS services**:
   - Create an RDS PostgreSQL database
   - Set up S3 buckets for static and media files
   - Configure IAM roles with appropriate permissions

3. **Initialize Elastic Beanstalk**:
   ```bash
   eb init -p python-3.9 slid
   ```

4. **Create a `.ebextensions` configuration folder** with the following files:
   - `01_packages.config` for system packages
   - `02_django.config` for Django-specific settings
   - `03_environment.config` for environment variables

5. **Create a Procfile**:
   ```
   web: gunicorn SLID.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Deploy to Elastic Beanstalk**:
   ```bash
   eb create slid-production
   ```

7. **Configure HTTPS**:
   - Request an SSL certificate through AWS Certificate Manager
   - Configure HTTPS in the Elastic Beanstalk environment

## Traditional Server Deployment

### Ubuntu Server with Gunicorn and Nginx

1. **Provision an Ubuntu server** (20.04 LTS or newer)

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
   ```

3. **Create a PostgreSQL database**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE slid;
   CREATE USER sliduser WITH PASSWORD 'password';
   ALTER ROLE sliduser SET client_encoding TO 'utf8';
   ALTER ROLE sliduser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE sliduser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE slid TO sliduser;
   \q
   ```

4. **Create a virtual environment**:
   ```bash
   sudo pip3 install virtualenv
   mkdir /var/www/slid
   cd /var/www/slid
   virtualenv venv
   source venv/bin/activate
   ```

5. **Clone the SLID repository**:
   ```bash
   git clone https://github.com/McMarian/SLID.git
   cd SLID
   pip install -r requirements.txt
   ```

6. **Configure environment variables**:
   Create a `.env` file in the project root with necessary environment variables.

7. **Initialize the application**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

8. **Set up Gunicorn**:
   Create `/etc/systemd/system/gunicorn.service`:
   ```
   [Unit]
   Description=gunicorn daemon for SLID
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/var/www/slid/SLID
   EnvironmentFile=/var/www/slid/SLID/.env
   ExecStart=/var/www/slid/venv/bin/gunicorn --workers 3 --bind unix:/var/www/slid/slid.sock SLID.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

9. **Configure Nginx**:
   Create `/etc/nginx/sites-available/slid`:
   ```
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /var/www/slid/SLID;
       }
       
       location /media/ {
           root /var/www/slid/SLID/static;
       }
       
       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/slid/slid.sock;
           proxy_read_timeout 90;
           client_max_body_size 20M;
       }
   }
   ```

10. **Enable the site**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/slid /etc/nginx/sites-enabled
    ```

11. **Start services**:
    ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl restart nginx
    ```

12. **Set up SSL with Let's Encrypt**:
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com -d www.your-domain.com
    ```

## Scaling Considerations

As your SLID instance grows, consider these scaling strategies:

### Database Scaling

- **Read Replicas**: Set up PostgreSQL read replicas to distribute read queries
- **Connection Pooling**: Use PgBouncer for efficient database connection management
- **Sharding**: For very large deployments, consider database sharding

### Application Scaling

- **Horizontal Scaling**: Deploy multiple application instances behind a load balancer
- **Caching**: Implement Redis for caching frequently accessed data
- **Asynchronous Processing**: Use Celery for background task processing

### Media Storage

- **Content Delivery Network (CDN)**: Configure a CDN for static and media files
- **Object Storage**: Use S3-compatible storage for scalable media handling

## Monitoring and Maintenance

### Setting Up Monitoring

1. **Application Monitoring**:
   - Implement Django application monitoring with Sentry
   - Add in your settings.py:
     ```python
     import sentry_sdk
     from sentry_sdk.integrations.django import DjangoIntegration

     sentry_sdk.init(
         dsn="your-sentry-dsn",
         integrations=[DjangoIntegration()],
         traces_sample_rate=0.5,
         send_default_pii=True
     )
     ```

2. **Server Monitoring**:
   - Set up Prometheus and Grafana for server metrics
   - Configure alerts for system resources (CPU, memory, disk space)

3. **Log Management**:
   - Centralize logs with ELK Stack (Elasticsearch, Logstash, Kibana) or a managed service like Datadog

### Backup Strategy

1. **Database Backups**:
   - Daily automated PostgreSQL backups
   - Regular testing of database restoration
   - Off-site storage of backup files

2. **Application Backups**:
   - Regular backups of application code and configuration
   - Version control for all custom code

3. **Media Backups**:
   - Regular backups of user-uploaded media files
   - Consider versioning for S3 or Cloud Storage buckets

### Maintenance Procedures

1. **Database Maintenance**:
   - Schedule regular VACUUM and ANALYZE operations
   - Monitor and optimize slow queries

2. **Software Updates**:
   - Establish a process for safely applying Django and dependency updates
   - Test updates in a staging environment before production deployment

3. **Security Updates**:
   - Subscribe to security mailing lists for all components
   - Apply security patches promptly

## Troubleshooting

### Common Deployment Issues

1. **Database Connection Issues**:
   - Check database credentials in environment variables
   - Ensure database server is accessible from application
   - Verify firewall rules allow database connections

2. **Static/Media Files Not Displaying**:
   - Verify STATIC_URL and MEDIA_URL configurations
   - Check file permissions on storage locations
   - Ensure collectstatic has been run successfully

3. **Application Errors**:
   - Check application logs for specific error messages
   - Verify all environment variables are correctly set
   - Ensure the database schema is up to date

### Log Locations

- **Django Application Logs**: Check your configured log paths in settings.py
- **Gunicorn Logs**: `/var/log/gunicorn/error.log`
- **Nginx Logs**: `/var/log/nginx/error.log`
- **Docker Logs**: Retrieve with `docker-compose logs`

## Conclusion

This deployment guide covers the most common deployment scenarios for SLID. The recommended approach is using Docker for both development and production environments, which provides consistency and simplifies the deployment process.

For large-scale deployments, consider a cloud-based approach with managed services for databases and storage, which will reduce operational overhead and improve scalability.

Remember to keep your deployment configurations in version control, and always test changes in a staging environment before applying them to production.

For additional assistance, consult the [Developer Guide](Developer%20Guide.md) or contact the SLID development team. 