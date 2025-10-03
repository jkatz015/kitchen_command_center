import React, { useState, useEffect } from 'react';
import { Calendar, ClipboardList, Users, Camera, Edit3, ShoppingCart, ChevronLeft, ChevronRight, RefreshCw } from 'lucide-react';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('dashboard');
  const [tasks, setTasks] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // API Configuration - CHANGE THIS TO YOUR DJANGO API URL
  const API_BASE_URL = 'http://localhost:8000/api';

  // Fetch tasks from Django API
  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`);
      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  // Fetch events from Django API
  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/events/`);
      if (response.ok) {
        const data = await response.json();
        setEvents(data);
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  // Fetch all data
  const fetchAllData = async () => {
    setLoading(true);
    await Promise.all([fetchTasks(), fetchEvents()]);
    setLoading(false);
    setLastUpdate(new Date());
  };

  // Initial fetch and set up polling
  useEffect(() => {
    fetchAllData();

    // Poll every 10 seconds for updates
    const interval = setInterval(() => {
      fetchAllData();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // Get today's events (reservations)
  const getTodaysEvents = () => {
    const today = new Date().toISOString().split('T')[0];
    return events.filter(event => {
      const eventDate = new Date(event.start).toISOString().split('T')[0];
      return eventDate === today;
    }).sort((a, b) => new Date(a.start) - new Date(b.start));
  };

  // Sample data for features not yet in API
  const housekeepingNotes = [
    { task: 'Deep clean walk-in cooler', priority: 'high', due: 'Today' },
    { task: 'Check fire suppression system', priority: 'medium', due: 'Tomorrow' },
    { task: 'Inventory dry storage', priority: 'low', due: 'This week' },
  ];

  const orderItems = [
    'Heavy cream - 2 cases',
    'Fresh basil - 5 bunches',
    'Chicken breast - 40 lbs',
    'Salmon fillets - 20 lbs',
  ];

  const ViewButton = ({ icon: Icon, label, view }) => (
    <button
      onClick={() => setActiveView(view)}
      className={`view-button ${activeView === view ? 'active' : ''}`}
    >
      <Icon size={20} />
      <span className="font-medium">{label}</span>
    </button>
  );

  const DashboardView = () => {
    const todaysEvents = getTodaysEvents();
    const incompleteTasks = tasks.filter(task => !task.completed);
    const completedTasks = tasks.filter(task => task.completed);

    return (
      <div className="dashboard-grid">
        {/* Reservations/Events */}
        <div className="dashboard-card">
          <div className="card-header">
            <Calendar className="icon-blue" size={28} />
            <h2>Today's Reservations</h2>
          </div>
          {loading ? (
            <div className="loading-container">
              <RefreshCw className="loading-spinner" size={32} />
            </div>
          ) : todaysEvents.length > 0 ? (
            <div className="card-content">
              {todaysEvents.map((event) => {
                const startTime = new Date(event.start).toLocaleTimeString('en-US', {
                  hour: 'numeric',
                  minute: '2-digit',
                  hour12: true
                });
                return (
                  <div key={event.id} className="event-item">
                    <div>
                      <div className="event-time">{startTime}</div>
                      <div className="event-name">{event.name}</div>
                      {event.location && <div className="event-location">📍 {event.location}</div>}
                      {event.notes && <div className="event-notes">⚠️ {event.notes}</div>}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="empty-state">
              No reservations scheduled for today
            </div>
          )}
        </div>

        {/* Tasks / Prep List */}
        <div className="dashboard-card">
          <div className="card-header">
            <ClipboardList className="icon-green" size={28} />
            <h2>Task List</h2>
            <span className="task-counter">
              {completedTasks.length}/{tasks.length} completed
            </span>
          </div>
          {loading ? (
            <div className="loading-container">
              <RefreshCw className="loading-spinner" size={32} />
            </div>
          ) : tasks.length > 0 ? (
            <div className="card-content">
              {tasks.map((task) => (
                <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                  <div className="task-content">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      className="task-checkbox"
                      readOnly
                    />
                    <div>
                      <div className={`task-title ${task.completed ? 'strikethrough' : ''}`}>
                        {task.title}
                      </div>
                      <div className="task-date">
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              No tasks available
            </div>
          )}
        </div>

        {/* Housekeeping Notes */}
        <div className="dashboard-card">
          <div className="card-header">
            <Users className="icon-purple" size={28} />
            <h2>Housekeeping</h2>
          </div>
          <div className="card-content">
            {housekeepingNotes.map((note, idx) => (
              <div key={idx} className="housekeeping-item">
                <div className="housekeeping-content">
                  <div className="housekeeping-task">{note.task}</div>
                  <div className="housekeeping-due">Due: {note.due}</div>
                </div>
                <span className={`priority-badge priority-${note.priority}`}>
                  {note.priority.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Order Guide */}
        <div className="dashboard-card">
          <div className="card-header">
            <ShoppingCart className="icon-orange" size={28} />
            <h2>Order Guide</h2>
          </div>
          <div className="card-content">
            {orderItems.map((item, idx) => (
              <div key={idx} className="order-item">
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const CameraView = () => (
    <div className="camera-container">
      <div className="dashboard-card camera-card">
        <div className="card-header">
          <div className="camera-header-left">
            <Camera className="icon-red" size={28} />
            <h2>Dining Room - Live Feed</h2>
            <span className="live-badge">LIVE</span>
          </div>
          <div className="camera-controls">
            <button className="camera-button">
              <ChevronLeft size={24} />
            </button>
            <button className="camera-button">
              <ChevronRight size={24} />
            </button>
          </div>
        </div>
        <div className="camera-feed">
          <div className="camera-placeholder">
            <Camera size={80} className="camera-icon" />
            <p className="camera-text">Camera Feed Placeholder</p>
            <p className="camera-subtext">Connect IP camera or webcam feed here</p>
          </div>
          <div className="camera-timestamp">
            {new Date().toLocaleTimeString()}
          </div>
        </div>
        <div className="camera-info">
          <span className="status-indicator"></span>
          Swipe left/right on tablet to move camera view
        </div>
      </div>
    </div>
  );

  const WhiteboardView = () => (
    <div className="whiteboard-container">
      <div className="dashboard-card whiteboard-card">
        <div className="card-header">
          <div className="whiteboard-header-left">
            <Edit3 className="icon-yellow" size={28} />
            <h2>Whiteboard</h2>
          </div>
          <div className="whiteboard-controls">
            <button className="whiteboard-button clear">Clear</button>
            <button className="whiteboard-button save">Save</button>
          </div>
        </div>
        <div className="whiteboard-canvas">
          <div className="whiteboard-placeholder">
            <Edit3 size={60} className="whiteboard-icon" />
            <p className="whiteboard-text">Drawing Canvas</p>
            <p className="whiteboard-subtext">Use tablet pen to draw notes and diagrams</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="app-container">
      {/* Header */}
      <div className="app-header">
        <div className="header-left">
          <h1 className="app-title">Kitchen Command Center</h1>
          <p className="app-date">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </p>
        </div>
        <div className="header-right">
          <div className="current-time">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
          <div className="update-info">
            <RefreshCw size={14} className={loading ? 'loading-spinner' : ''} />
            Updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="app-navigation">
        <ViewButton icon={Calendar} label="Dashboard" view="dashboard" />
        <ViewButton icon={Camera} label="Dining Room" view="camera" />
        <ViewButton icon={Edit3} label="Whiteboard" view="whiteboard" />
      </div>

      {/* Main Content */}
      <div className="app-content">
        {activeView === 'dashboard' && <DashboardView />}
        {activeView === 'camera' && <CameraView />}
        {activeView === 'whiteboard' && <WhiteboardView />}
      </div>
    </div>
  );
}

export default App;