# Kitchen Command Center - React Frontend

This is the React frontend for the Kitchen Command Center, providing a modern, real-time dashboard for kitchen operations.

## Features

- **Real-time Dashboard**: Live updates every 10 seconds
- **Responsive Design**: Optimized for tablets and large displays
- **Multiple Views**: Dashboard, Camera Feed, and Whiteboard
- **API Integration**: Connects to Django backend for data
- **Touch-friendly**: Designed for kitchen tablet use

## Quick Start

### Development

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm start
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - React Frontend: http://localhost:3000
   - Django API: http://localhost:8000
   - Streamlit Admin: http://localhost:8501

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   Django API    │    │   PostgreSQL    │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Port 5432)   │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • REST API      │    │ • Data Storage  │
│ • Camera View   │    │ • Real-time     │    │ • Persistence   │
│ • Whiteboard    │    │ • WebSockets    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## API Endpoints

The React app connects to these Django API endpoints:

- `GET /api/tasks/` - Fetch tasks/prep items
- `GET /api/events/` - Fetch reservations/events
- `POST /api/tasks/` - Create new tasks
- `PUT /api/tasks/{id}/` - Update task status

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
```

### API Configuration

Update the `API_BASE_URL` in `src/App.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
```

## Development

### Adding New Views

1. Create a new view component in `src/App.js`
2. Add a navigation button in the `ViewButton` section
3. Add the view to the main content render logic

### Styling

The app uses custom CSS with Tailwind-like utilities. To add Tailwind CSS:

```bash
npm install -D tailwindcss
npx tailwindcss init
```

### Real-time Updates

The app polls the API every 10 seconds. To change this:

```javascript
// In useEffect
const interval = setInterval(() => {
  fetchAllData();
}, 10000); // Change this value (milliseconds)
```

## Production Deployment

### Build Process

1. **Create production build**:
   ```bash
   npm run build
   ```

2. **Serve with Nginx**:
   ```bash
   docker-compose up frontend
   ```

### Performance Optimization

- **Code Splitting**: Implement React.lazy() for large components
- **Caching**: Configure service worker for offline functionality
- **Compression**: Enable gzip compression in Nginx
- **CDN**: Use CDN for static assets in production

## Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Check Django API is running on port 8000
   - Verify CORS settings in Django
   - Check network connectivity

2. **Build Errors**:
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version (requires 18+)

3. **Docker Issues**:
   - Rebuild containers: `docker-compose down && docker-compose up --build`
   - Check Docker logs: `docker-compose logs frontend`

### Development Tools

- **React Developer Tools**: Browser extension for debugging
- **Network Tab**: Monitor API calls and responses
- **Console**: Check for JavaScript errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
