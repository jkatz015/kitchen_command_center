# Kitchen Command Center - Deployment Guide

## Quick Start Options

### Option 1: Docker Compose (Recommended for Full-Stack)

#### Prerequisites

- Docker and Docker Compose installed
- Domain name (optional, can use IP address)

#### Steps

1. **Set up environment variables:**

Create `apps/api/.env`:

```bash
# Django Production Settings
DJANGO_SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=false
ALLOWED_HOSTS=your-domain.com,api.your-domain.com

# Database Settings
POSTGRES_DB=kcc
POSTGRES_USER=kcc
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_HOST=db
POSTGRES_PORT=5432

# CORS Settings (add your frontend domain)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.streamlit.app
```

Create `apps/web/.env.local`:

```bash
# Frontend Environment Variables
NEXT_PUBLIC_APP_ENV=production
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

1. **Deploy with Docker Compose:**

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

1. **Access your application:**

- API: <http://your-server-ip:8000>
- Frontend: Deploy separately to Streamlit Cloud (see Option 2)

### Option 2: Separate Services (Recommended for Production)

#### Backend (Django API) - Deploy to Railway/Render

**Railway:**

1. Connect your GitHub repo to Railway
1. Set environment variables in Railway dashboard
1. Railway will auto-detect Django and deploy

**Render:**

1. Create new Web Service on Render
1. Connect GitHub repo
1. Build command: `cd apps/api && pip install -r requirements.txt`
1. Start command: `cd apps/api && gunicorn kcc.wsgi:application --bind 0.0.0.0:$PORT`

**Required Environment Variables:**

```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=your-api-domain.railway.app
POSTGRES_DB=kcc
POSTGRES_USER=kcc
POSTGRES_PASSWORD=secure-password
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend.streamlit.app
```

#### Frontend (Streamlit) - Deploy to Streamlit Cloud

**Streamlit Cloud (recommended):**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set environment variables in Streamlit Cloud dashboard:

   ```bash
   API_URL=https://your-api-domain.railway.app
   ```

#### Database - PostgreSQL

**Options:**

- Railway PostgreSQL (if using Railway for backend)
- Render PostgreSQL (if using Render)
- Supabase (free tier available)
- AWS RDS
- DigitalOcean Managed Database

### Option 3: All-in-One Platforms

#### Vercel (Frontend) + Railway (Backend + DB)

1. Deploy Next.js to Vercel
1. Deploy Django + PostgreSQL to Railway
1. Connect via environment variables

#### Streamlit Cloud (Frontend) + Railway (Backend + DB)

1. Deploy Streamlit to Streamlit Cloud
2. Deploy Django API to Railway
3. Set up PostgreSQL database
4. Update `API_URL` in Streamlit Cloud

## Environment Variables Reference

### Backend (Django)

```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=your-domain.com
POSTGRES_DB=kcc
POSTGRES_USER=kcc
POSTGRES_PASSWORD=secure-password
POSTGRES_HOST=db-host
POSTGRES_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend (Next.js)

```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_APP_ENV=production
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=false
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up proper database backups

## Monitoring & Maintenance

- Set up health checks for your API
- Monitor database performance
- Set up log aggregation
- Configure alerts for downtime
- Regular security updates

## Troubleshooting

### Common Issues

1. **CORS errors**: Check CORS_ALLOWED_ORIGINS
1. **Database connection**: Verify database credentials and network access
1. **Build failures**: Check Node.js version compatibility
1. **Static files**: Ensure proper static file serving in production

### Useful Commands

```bash
# Check Django health
curl https://your-api-domain.com/admin/

# Check API endpoints
curl https://your-api-domain.com/api/

# View build logs
# Check your hosting platform's logs section
```

## Cost Estimates

### Free Tier Options

- Streamlit Cloud: Free for frontend
- Railway: $5/month for backend + database
- Render: Free tier available
- Supabase: Free tier for database

### Production Recommendations

- Use managed databases for production
- Enable CDN for static assets
- Set up proper monitoring
- Consider load balancing for high traffic
