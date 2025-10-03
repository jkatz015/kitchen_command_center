'use client'

import { useState } from 'react'
import { dummyPrepItems, dummyOrderAdds, dummyHousekeepingNotes, dummyWhiteboardNotes } from '@/data/dummyData'
import { PrepItem, OrderAdd, HousekeepingNote, WhiteboardNote } from '@/types'
import { getStatusColor, getPriorityColor, formatTimeAgo } from '@/utils/statusUtils'

export default function Tablet() {
  const [isSaving, setIsSaving] = useState(false)

  const handleSaveSnapshot = async () => {
    setIsSaving(true)
    // TODO: Implement backend integration
    console.log('Save snapshot clicked - backend integration pending')

    // Simulate save operation
    setTimeout(() => {
      setIsSaving(false)
      alert('Snapshot saved! (Placeholder - no backend yet)')
    }, 1000)
  }


  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top Bar */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-gray-900">Kitchen Command Center</h1>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Online</span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              {new Date().toLocaleString()}
            </div>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
              Settings
            </button>
          </div>
        </div>
      </header>

      {/* Main Control Panel - 4 Sections */}
      <main className="p-6">
        <div className="grid grid-cols-2 gap-6 h-[calc(100vh-120px)]">
          {/* Section 1: Whiteboard */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Whiteboard</h2>
                <div className="flex space-x-2">
                  <button
                    onClick={handleSaveSnapshot}
                    disabled={isSaving}
                    className="bg-green-600 text-white px-3 py-1 rounded text-sm font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {isSaving ? 'Saving...' : 'Save Snapshot'}
                  </button>
                  <button className="text-blue-600 text-sm font-medium hover:text-blue-700">
                    Clear All
                  </button>
                </div>
              </div>
              <div className="flex-1 bg-gray-50 rounded-lg p-4 overflow-y-auto">
                <div className="space-y-4">
                  {dummyWhiteboardNotes.map((note: WhiteboardNote) => (
                    <div key={note.id} className={`border-l-4 p-4 rounded-lg ${getPriorityColor(note.priority)}`}>
                      <p className="text-lg font-semibold text-gray-900 mb-1">{note.title}</p>
                      <p className="text-base text-gray-700">{note.content}</p>
                      <p className="text-sm text-gray-500 mt-2">
                        {note.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Prep */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Prep</h2>
                <button className="text-green-600 text-sm font-medium hover:text-green-700">
                  Mark Complete
                </button>
              </div>
              <div className="flex-1 overflow-y-auto">
                <div className="space-y-4">
                  {dummyPrepItems.map((item: PrepItem) => (
                    <div key={item.id} className={`border-l-4 p-4 rounded-lg ${getPriorityColor(item.priority)}`}>
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
                        <span className={`text-sm px-3 py-1 rounded-full ${getStatusColor(item.status)}`}>
                          {item.status.replace('-', ' ')}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="text-base text-gray-700">
                          {item.quantity} {item.unit}
                          {item.assignedTo && <span className="text-sm text-gray-500 ml-2">• {item.assignedTo}</span>}
                        </div>
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={item.status === 'complete'}
                            className="mr-2 w-4 h-4"
                            readOnly
                          />
                        </label>
                      </div>
                      {item.notes && (
                        <p className="text-sm text-gray-600 mt-2 italic">{item.notes}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: Order Adds */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Order Adds</h2>
                <button className="text-purple-600 text-sm font-medium hover:text-purple-700">
                  New Order
                </button>
              </div>
              <div className="flex-1 overflow-y-auto">
                <div className="space-y-4">
                  {dummyOrderAdds.map((order: OrderAdd) => (
                    <div key={order.id} className={`border-l-4 p-4 rounded-lg ${getPriorityColor(order.priority)}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-lg font-semibold text-gray-900">Table {order.tableNumber}</span>
                        <span className="text-sm text-gray-500">
                          {formatTimeAgo(order.timestamp)}
                        </span>
                      </div>
                      <div className="mb-3">
                        <p className="text-base text-gray-700 font-medium mb-1">{order.originalItem}</p>
                        <p className="text-base text-gray-600">{order.modification}</p>
                      </div>
                      <div className="flex space-x-3">
                        <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
                          Accept
                        </button>
                        <button className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-400 transition-colors">
                          Decline
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 4: Housekeeping */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Housekeeping</h2>
                <button className="text-orange-600 text-sm font-medium hover:text-orange-700">
                  Mark All Done
                </button>
              </div>
              <div className="flex-1 overflow-y-auto">
                <div className="space-y-4">
                  {dummyHousekeepingNotes.map((note: HousekeepingNote) => (
                    <div key={note.id} className={`border-l-4 p-4 rounded-lg ${getPriorityColor(note.priority)}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-lg font-semibold text-gray-900">
                          {note.tableNumber ? `Table ${note.tableNumber}` : note.title}
                        </span>
                        <span className={`text-sm px-3 py-1 rounded-full ${getStatusColor(note.status)}`}>
                          {note.priority}
                        </span>
                      </div>
                      <p className="text-base text-gray-700 mb-3">{note.description}</p>
                      <div className="flex items-center justify-between">
                        <div className="text-sm text-gray-500">
                          {note.assignedTo && <span>Assigned to: {note.assignedTo}</span>}
                          {note.estimatedDuration && (
                            <span className="ml-2">Est. {note.estimatedDuration} min</span>
                          )}
                        </div>
                        <button className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          note.priority === 'urgent' ? 'bg-red-600 hover:bg-red-700' :
                          note.priority === 'high' ? 'bg-orange-600 hover:bg-orange-700' :
                          note.priority === 'medium' ? 'bg-yellow-600 hover:bg-yellow-700' :
                          'bg-green-600 hover:bg-green-700'
                        } text-white`}>
                          Mark Complete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
