'use client'

import { useState, useEffect } from 'react'
import { kitchenSimulator, generateKitchenMetrics, generateStaffAssignments } from '@/utils/simulator'

export default function TestPage() {
  const [isSimulating, setIsSimulating] = useState(false)
  const [metrics, setMetrics] = useState(generateKitchenMetrics())
  const [staff, setStaff] = useState(generateStaffAssignments())
  const [updates, setUpdates] = useState<any[]>([])
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    // Update metrics every 30 seconds
    const metricsInterval = setInterval(() => {
      setMetrics(generateKitchenMetrics())
    }, 30000)

    // Update staff every 2 minutes
    const staffInterval = setInterval(() => {
      setStaff(generateStaffAssignments())
    }, 120000)

    return () => {
      clearInterval(metricsInterval)
      clearInterval(staffInterval)
    }
  }, [])

  const startSimulation = () => {
    if (isSimulating) return

    setIsSimulating(true)
    kitchenSimulator.start()

    const unsubscribe = kitchenSimulator.subscribe((update) => {
      setUpdates(prev => [update, ...prev.slice(0, 9)]) // Keep last 10 updates
      setLastUpdate(new Date())
    })

    // Store unsubscribe function for cleanup
    ;(window as any).simulatorUnsubscribe = unsubscribe
  }

  const stopSimulation = () => {
    if (!isSimulating) return

    setIsSimulating(false)
    kitchenSimulator.stop()

    if ((window as any).simulatorUnsubscribe) {
      ;(window as any).simulatorUnsubscribe()
    }
  }

  const resetData = () => {
    setUpdates([])
    setMetrics(generateKitchenMetrics())
    setStaff(generateStaffAssignments())
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Kitchen Command Center - Test Page</h1>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Simulation Controls</h2>
          <div className="flex items-center space-x-4">
            <button
              onClick={startSimulation}
              disabled={isSimulating}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                isSimulating
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-green-600 text-white hover:bg-green-700'
              }`}
            >
              {isSimulating ? 'Simulating...' : 'Start Simulation'}
            </button>

            <button
              onClick={stopSimulation}
              disabled={!isSimulating}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                !isSimulating
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-red-600 text-white hover:bg-red-700'
              }`}
            >
              Stop Simulation
            </button>

            <button
              onClick={resetData}
              className="px-4 py-2 rounded-lg font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              Reset Data
            </button>
          </div>

          <div className="mt-4 text-sm text-gray-600">
            <p><strong>Status:</strong> {isSimulating ? 'Active' : 'Stopped'}</p>
            <p><strong>Last Update:</strong> {lastUpdate.toLocaleString()}</p>
          </div>
        </div>

        {/* Kitchen Metrics */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Kitchen Metrics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{metrics.ordersInQueue}</div>
              <div className="text-sm text-gray-600">Orders in Queue</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">{metrics.prepCompletion}%</div>
              <div className="text-sm text-gray-600">Prep Complete</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{metrics.averageTicketTime}m</div>
              <div className="text-sm text-gray-600">Avg Ticket Time</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${metrics.kitchenStatus === 'Operational' ? 'text-green-600' : 'text-red-600'}`}>
                {metrics.kitchenStatus}
              </div>
              <div className="text-sm text-gray-600">Kitchen Status</div>
            </div>
          </div>
        </div>

        {/* Staff Assignments */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Staff Assignments</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {staff.map((member, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">{member.name}</h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    member.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {member.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{member.currentTask}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Live Updates */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Live Updates</h2>
          {updates.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No updates yet. Start the simulation to see live data.</p>
          ) : (
            <div className="space-y-3">
              {updates.map((update, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-gray-900 capitalize">
                      {update.type.replace('-', ' ')}
                    </span>
                    <span className="text-sm text-gray-500">
                      {new Date().toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600">
                    <pre className="whitespace-pre-wrap bg-gray-50 p-2 rounded">
                      {JSON.stringify(update.data, null, 2)}
                    </pre>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="mt-8 text-center">
          <div className="space-x-4">
            <a
              href="/display"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              View Display Page
            </a>
            <a
              href="/tablet"
              className="inline-block px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              View Tablet Page
            </a>
            <a
              href="/"
              className="inline-block px-6 py-3 bg-gray-600 text-white rounded-lg font-medium hover:bg-gray-700 transition-colors"
            >
              Home
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
