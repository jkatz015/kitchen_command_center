import React, { useState, useEffect } from 'react';
import {
  MdCalendarToday,
  MdAssignment,
  MdPeople,
  MdVideocam,
  MdEdit,
  MdShoppingCart,
  MdChevronLeft,
  MdChevronRight,
  MdRefresh
} from 'react-icons/md';

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
  const reservations = [
    { time: '5:00 PM', name: 'Johnson', party: 4, notes: 'Birthday' },
    { time: '6:30 PM', name: 'Smith', party: 2, notes: 'Anniversary' },
    { time: '7:15 PM', name: 'Williams', party: 6, notes: 'Gluten-free' },
    { time: '8:00 PM', name: 'Brown', party: 3, notes: null },
  ];

  const prepTasks = [
    { id: 1, task: 'Dice 10 lbs onions', assigned: 'Mike', completed: true },
    { id: 2, task: 'Prep salad greens', assigned: 'Sarah', completed: true },
    { id: 3, task: 'Marinate chicken', assigned: 'Mike', completed: false },
    { id: 4, task: 'Chop herbs', assigned: 'Sarah', completed: false },
  ];

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
          ? 'bg-gray-300 text-gray-900 border-2 border-gray-900'
          : 'bg-transparent text-white hover:bg-gray-700'
      }`}
    >
      <Icon size={20} />
      <span className="font-medium">{label}</span>
    </button>
  );

  const DashboardView = () => {
    const completedPrepTasks = prepTasks.filter(task => task.completed).length;

    return (
      <div className="grid grid-cols-2 gap-6 h-full">
        {/* Today's Reservations */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <MdCalendarToday className="text-blue-400" size={28} />
            <h2 className="text-2xl font-bold">Today's Reservations</h2>
          </div>
          <div className="space-y-3">
            {reservations.map((reservation, idx) => (
              <div key={idx} className="bg-gray-700 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-xl font-semibold text-blue-300">{reservation.time}</div>
                    <div className="text-lg">{reservation.name} - Party of {reservation.party}</div>
                  </div>
                  {reservation.notes && (
                    <div className="text-yellow-400 text-sm bg-yellow-900 bg-opacity-30 px-2 py-1 rounded">
                      ⚠️ {reservation.notes}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Prep List */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <MdAssignment className="text-green-400" size={28} />
            <h2 className="text-2xl font-bold">Prep List</h2>
            <span className="ml-auto text-sm text-gray-400">
              {completedPrepTasks}/{prepTasks.length} completed
            </span>
          </div>
          <div className="space-y-3">
            {prepTasks.map((task) => (
              <div key={task.id} className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <div className={`w-6 h-6 rounded border-2 flex items-center justify-center ${
                    task.completed ? 'bg-blue-500 border-blue-500' : 'border-gray-400'
                  }`}>
                    {task.completed && <span className="text-white text-sm">✓</span>}
                  </div>
                  <div className="flex-1">
                    <div className={`text-lg ${task.completed ? 'line-through text-gray-400' : ''}`}>
                      {task.task}
                    </div>
                    <div className={`text-sm ${task.completed ? 'line-through text-gray-500' : 'text-gray-400'}`}>
                      Assigned: {task.assigned}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Housekeeping */}
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto">
          <div className="flex items-center gap-3 mb-4">
            <MdPeople className="text-purple-400" size={28} />
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
        <div className="bg-gray-800 rounded-xl p-6 overflow-auto flex flex-col">
          <div className="flex items-center gap-3 mb-4">
            <MdShoppingCart className="text-orange-400" size={28} />
            <h2 className="text-2xl font-bold">Order Guide</h2>
          </div>
          <div className="space-y-3 flex-1">
            {orderItems.map((item, idx) => (
              <div key={idx} className="bg-gray-700 rounded-lg p-4">
                <div className="text-lg">{item}</div>
              </div>
            ))}
          </div>
          <button className="mt-4 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            Add Item
          </button>
        </div>
      </div>
    );
  };

  const CameraView = () => (
    <div className="h-full flex flex-col">
      <div className="bg-gray-800 rounded-xl p-6 flex-1 flex flex-col">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
              <MdVideocam className="text-red-400" size={28} />
            <h2 className="text-2xl font-bold">Dining Room - Live Feed</h2>
            <span className="px-3 py-1 bg-red-500 text-white rounded-full text-sm font-semibold animate-pulse">
              LIVE
            </span>
          </div>
          <div className="flex gap-2">
            <button className="bg-gray-700 hover:bg-gray-600 p-3 rounded-lg transition-colors">
                <MdChevronLeft size={24} />
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 p-3 rounded-lg transition-colors">
              <MdChevronRight size={24} />
            </button>
          </div>
        </div>
        <div className="flex-1 bg-gray-900 rounded-lg flex items-center justify-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900"></div>
          <div className="relative z-10 text-center">
              <MdVideocam size={80} className="mx-auto mb-4 text-gray-600" />
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
              <MdEdit className="text-yellow-400" size={28} />
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
              <MdEdit size={60} className="mx-auto mb-3 opacity-30" />
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
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-4xl font-bold mb-2">Kitchen Command Center</h1>
          <p className="text-xl text-gray-300">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </p>
        </div>
        <div className="text-right">
          <p className="text-5xl font-bold mb-1">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
          <p className="text-lg text-gray-300">Service: Dinner</p>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex gap-3 mb-6">
          <ViewButton icon={MdCalendarToday} label="Dashboard" view="dashboard" />
          <ViewButton icon={MdVideocam} label="Dining Room" view="camera" />
          <ViewButton icon={MdEdit} label="Whiteboard" view="whiteboard" />
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
