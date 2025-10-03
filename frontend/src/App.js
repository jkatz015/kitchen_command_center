import React, { useState, useEffect } from 'react';
import { Calendar, ClipboardList, Users, Camera, Edit3, ShoppingCart, ChevronLeft, ChevronRight, RefreshCw } from 'lucide-react';
import './App.css';

const KitchenDisplay = () => {
  const [activeView, setActiveView] = useState('dashboard');
  const [tasks, setTasks] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // API Configuration
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
      className={`flex items-center gap-2 px-4 py-3 rounded-lg transition-all ${
        activeView === view
          ? 'bg-blue-600 text-white'
          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
      }`}
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
      <div className="grid grid-cols-2 gap-6 h-full">
        {/* Reservations/Events */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <Calendar className="text-blue-400" size={28} />
            <h2 className="text-2xl font-bold">Today's Reservations</h2>
          </div>
          {loading ? (
            <div className="flex items-center justify-center h-48">
              <RefreshCw className="animate-spin text-blue-400" size={32} />
            </div>
          ) : todaysEvents.length > 0 ? (
            <div className="space-y-3">
              {todaysEvents.map((event) => {
                const startTime = new Date(event.start).toLocaleTimeString('en-US', {
                  hour: 'numeric',
                  minute: '2-digit',
                  hour12: true
                });
                return (
                  <div key={event.id} className="bg-gray-700 rounded-lg p-4 flex justify-between items-center">
                    <div>
                      <div className="text-xl font-semibold text-blue-300">{startTime}</div>
                      <div className="text-lg">{event.name}</div>
                      {event.location && <div className="text-sm text-gray-400">📍 {event.location}</div>}
                      {event.notes && <div className="text-sm text-yellow-400 mt-1">⚠️ {event.notes}</div>}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-8">
              No reservations scheduled for today
            </div>
          )}
        </div>

        {/* Tasks / Prep List */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <ClipboardList className="text-green-400" size={28} />
            <h2 className="text-2xl font-bold">Task List</h2>
            <span className="ml-auto text-sm text-gray-400">
              {completedTasks.length}/{tasks.length} completed
            </span>
          </div>
          {loading ? (
            <div className="flex items-center justify-center h-48">
              <RefreshCw className="animate-spin text-green-400" size={32} />
            </div>
          ) : tasks.length > 0 ? (
            <div className="space-y-3">
              {tasks.map((task) => (
                <div key={task.id} className={`bg-gray-700 rounded-lg p-4 ${task.completed ? 'opacity-50' : ''}`}>
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      className="w-6 h-6 rounded"
                      readOnly
                    />
                    <div className="flex-1">
                      <div className={`text-lg ${task.completed ? 'line-through' : ''}`}>{task.title}</div>
                      <div className="text-sm text-gray-400">
                        Created: {new Date(task.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-8">
              No tasks available
            </div>
          )}
        </div>

        {/* Housekeeping Notes */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <Users className="text-purple-400" size={28} />
            <h2 className="text-2xl font-bold">Housekeeping</h2>
          </div>
          <div className="space-y-3">
            {housekeepingNotes.map((note, idx) => (
              <div key={idx} className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="text-lg">{note.task}</div>
                    <div className="text-sm text-gray-400 mt-1">Due: {note.due}</div>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    note.priority === 'high' ? 'bg-red-500 text-white' :
                    note.priority === 'medium' ? 'bg-yellow-500 text-black' :
                    'bg-green-500 text-white'
                  }`}>
                    {note.priority.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Order Guide */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <ShoppingCart className="text-orange-400" size={28} />
            <h2 className="text-2xl font-bold">Order Guide</h2>
          </div>
          <div className="space-y-3">
            {orderItems.map((item, idx) => (
              <div key={idx} className="bg-gray-700 rounded-lg p-4">
                <div className="text-lg">{item}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const CameraView = () => (
    <div className="h-full flex flex-col">
      <div className="bg-gray-800 rounded-xl p-6 flex-1 flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Camera className="text-red-400" size={28} />
            <h2 className="text-2xl font-bold">Dining Room - Live Feed</h2>
            <span className="px-3 py-1 bg-red-500 text-white rounded-full text-sm font-semibold animate-pulse">
              LIVE
            </span>
          </div>
          <div className="flex gap-2">
            <button className="bg-gray-700 hover:bg-gray-600 p-3 rounded-lg transition-colors">
              <ChevronLeft size={24} />
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 p-3 rounded-lg transition-colors">
              <ChevronRight size={24} />
            </button>
          </div>
        </div>
        <div className="flex-1 bg-gray-900 rounded-lg flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900"></div>
          <div className="relative z-10 text-center">
            <Camera size={80} className="mx-auto mb-4 text-gray-600" />
            <p className="text-xl text-gray-500">Camera Feed Placeholder</p>
            <p className="text-sm text-gray-600 mt-2">Connect IP camera or webcam feed here</p>
          </div>
          <div className="absolute top-4 right-4 bg-black bg-opacity-70 px-4 py-2 rounded-lg">
            <div className="text-sm font-mono">{new Date().toLocaleTimeString()}</div>
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-400 flex items-center gap-2">
          <span className="w-3 h-3 bg-green-500 rounded-full"></span>
          Swipe left/right on tablet to move camera view
        </div>
      </div>
    </div>
  );

  const WhiteboardView = () => (
    <div className="h-full flex flex-col">
      <div className="bg-gray-800 rounded-xl p-6 flex-1 flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Edit3 className="text-yellow-400" size={28} />
            <h2 className="text-2xl font-bold">Whiteboard</h2>
          </div>
          <div className="flex gap-2">
            <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors">
              Clear
            </button>
            <button className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition-colors">
              Save
            </button>
          </div>
        </div>
        <div className="flex-1 bg-white rounded-lg flex items-center justify-center">
          <div className="text-center text-gray-400">
            <Edit3 size={60} className="mx-auto mb-3 opacity-30" />
            <p className="text-xl">Drawing Canvas</p>
            <p className="text-sm mt-2">Use tablet pen to draw notes and diagrams</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-screen bg-gray-900 text-white p-6 flex flex-col">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-2">Kitchen Command Center</h1>
            <p className="text-gray-400 text-lg">
              {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
            </p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-bold">
              {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
            <div className="text-gray-400 flex items-center justify-end gap-2">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              Updated: {lastUpdate.toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-3 mb-6">
        <ViewButton icon={Calendar} label="Dashboard" view="dashboard" />
        <ViewButton icon={Camera} label="Dining Room" view="camera" />
        <ViewButton icon={Edit3} label="Whiteboard" view="whiteboard" />
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {activeView === 'dashboard' && <DashboardView />}
        {activeView === 'camera' && <CameraView />}
        {activeView === 'whiteboard' && <WhiteboardView />}
      </div>
    </div>
  );
};

export default KitchenDisplay;
