# Kitchen Command Center - React Display

This is the TV display interface for the Kitchen Command Center. It shows a beautiful, auto-refreshing dashboard that connects to your Django API.

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure API URL

Edit `src/App.js` and update the API URL if your Django server is running on a different port:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### 3. Start the Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

## Features

- **Auto-refresh**: Updates every 10 seconds automatically
- **Dashboard View**: Shows tasks, events, housekeeping, and orders
- **Camera View**: Placeholder for live camera feed integration
- **Whiteboard View**: Placeholder for drawing canvas

## Connecting to Django API

Make sure your Django API is running on `http://localhost:8000` and has CORS enabled for `http://localhost:3000`.

In your Django `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8501",
]
```

## Deployment

### For TV Display

1. Build the production version:
   ```bash
   npm run build
   ```

2. Serve the build folder on your TV device (Raspberry Pi, etc.)

### For Development

Just run `npm start` and open in browser

## API Endpoints Used

- `GET /api/tasks/` - Fetch all tasks
- `GET /api/events/` - Fetch all events/reservations

## Customization

- Update colors in `src/App.css`
- Modify polling interval in `src/App.js` (line with `setInterval`)
- Add new views by creating new components

## Troubleshooting

### Can't connect to API

1. Check Django is running: `http://localhost:8000/api/tasks/`
2. Check CORS is configured in Django settings
3. Check browser console for errors

### Data not updating

1. Check the API is returning data
2. Open browser DevTools (F12) and check Network tab
3. Look for errors in Console tab