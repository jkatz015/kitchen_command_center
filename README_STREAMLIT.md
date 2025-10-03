# Kitchen Command Center - Streamlit Version

A comprehensive kitchen management system built with Streamlit for easy deployment and real-time updates.

## Features

### 🖥️ Display View
- **Reservations**: Real-time table status and guest information
- **Prep Items**: Kitchen prep tracking with priority levels
- **Order Modifications**: Live order changes and special requests
- **Housekeeping**: Maintenance and cleaning task management
- **Kitchen Metrics**: Performance indicators and status

### 📱 Tablet View
- **Touch-friendly Interface**: Optimized for tablet use
- **Whiteboard**: Staff notes and announcements
- **Quick Actions**: One-tap operations for common tasks
- **Tabbed Navigation**: Easy switching between sections

### 📊 Metrics Dashboard
- **Performance Charts**: Visual analytics with Plotly
- **Real-time Data**: Auto-refreshing metrics
- **Timeline Views**: Order and task progression

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the app**:
   Open your browser to `http://localhost:8501`

### Deployment Options

#### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

#### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Railway**: Direct Python deployment
- **DigitalOcean**: App Platform deployment
- **AWS/GCP**: Container deployment

## Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_HEADLESS`: Headless mode (default: true)

### Customization
- Edit `.streamlit/config.toml` for theme and server settings
- Modify `streamlit_app.py` for functionality changes
- Update `requirements.txt` for dependency management

## Architecture

### Data Structure
- **Reservations**: Table bookings and guest information
- **Prep Items**: Kitchen preparation tasks
- **Order Adds**: Menu modifications and special requests
- **Housekeeping**: Maintenance and cleaning tasks
- **Whiteboard**: Staff communication and announcements

### Real-time Updates
- Auto-refresh every 30 seconds
- Manual refresh button
- Live status indicators
- Color-coded priority system

### Responsive Design
- Mobile-friendly interface
- Tablet-optimized layouts
- Desktop display views
- Adaptive column layouts

## Development

### Adding New Features
1. Modify `streamlit_app.py` for new functionality
2. Update data structures in `get_sample_data()`
3. Add new display functions
4. Test with different view modes

### Styling
- Custom CSS in the main app
- Priority-based color coding
- Responsive design patterns
- Streamlit theme customization

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change port in config.toml
2. **Dependencies**: Ensure all packages in requirements.txt
3. **Performance**: Use `@st.cache_data` for expensive operations
4. **Memory**: Limit data size for large datasets

### Performance Tips
- Use `st.cache_data` for data loading
- Implement pagination for large lists
- Optimize auto-refresh intervals
- Use columns for better layout

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the Streamlit documentation
- Review the troubleshooting section

---

**Built with ❤️ using Streamlit**
