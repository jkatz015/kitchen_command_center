'use client'

import { useState, useEffect } from 'react'
import { dummyReservations, dummyPrepItems, dummyOrderAdds, dummyHousekeepingNotes } from '@/data/dummyData'
import { Reservation, PrepItem, OrderAdd, HousekeepingNote } from '@/types'
import { getBorderColor, getStatusText, getBadgeColor, getPriorityBadgeColor, formatTimeAgo } from '@/utils/statusUtils'
import { kitchenSimulator, generateKitchenMetrics } from '@/utils/simulator'

export default function Display() {
  const [reservations, setReservations] = useState<Reservation[]>(dummyReservations)
  const [prepItems, setPrepItems] = useState<PrepItem[]>(dummyPrepItems)
  const [orderAdds, setOrderAdds] = useState<OrderAdd[]>(dummyOrderAdds)
  const [housekeepingNotes, setHousekeepingNotes] = useState<HousekeepingNote[]>(dummyHousekeepingNotes)
  const [kitchenMetrics, setKitchenMetrics] = useState(generateKitchenMetrics())
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    // Start the simulator
    kitchenSimulator.start()

    // Subscribe to simulator updates
    const unsubscribe = kitchenSimulator.subscribe((update) => {
      switch (update.type) {
        case 'order-add':
          setOrderAdds((prev: OrderAdd[]) => [update.data, ...prev])
          break
        case 'prep-update':
          setPrepItems((prev: PrepItem[]) => prev.map((item: PrepItem) =>
            item.name === update.data.item
              ? { ...item, status: update.data.status }
              : item
          ))
          break
        case 'housekeeping-note':
          setHousekeepingNotes((prev: HousekeepingNote[]) => [update.data, ...prev])
          break
        case 'reservation-update':
          setReservations((prev: Reservation[]) => prev.map((res: Reservation) =>
            res.tableNumber === update.data.tableNumber
              ? { ...res, status: update.data.status }
              : res
          ))
          break
      }
      setLastUpdate(new Date())
    })

    // Update kitchen metrics every 30 seconds
    const metricsInterval = setInterval(() => {
      setKitchenMetrics(generateKitchenMetrics())
    }, 30000)

    return () => {
      kitchenSimulator.stop()
      unsubscribe()
      clearInterval(metricsInterval)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Kitchen Command Center</h1>
                 <div className="text-sm text-gray-300">
                   {lastUpdate.toLocaleString()} • Live Updates
                 </div>
        </div>
      </header>

      {/* Main Content - 3 Column Layout */}
      <main className="flex h-[calc(100vh-80px)]">
        {/* Column 1: Reservations */}
        <div className="flex-1 border-r border-gray-700 p-6">
          <div className="h-full flex flex-col">
            <h2 className="text-xl font-semibold mb-4 text-blue-400">Reservations</h2>
            <div className="flex-1 bg-gray-800 rounded-lg p-4 overflow-y-auto">
                     <div className="space-y-4">
                       {reservations.map((reservation: Reservation) => (
                  <div key={reservation.id} className={`bg-gray-700 p-4 rounded border-l-4 ${getBorderColor(reservation.status)}`}>
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        <p className="text-xl font-semibold text-white">{reservation.partyName}</p>
                        <p className="text-lg text-gray-300">{reservation.time}</p>
                      </div>
                      <span className={`px-3 py-1 rounded text-sm font-medium ${getBadgeColor(reservation.status)}`}>
                        {getStatusText(reservation.status)}
                      </span>
                    </div>
                    <div className="text-base text-gray-300">
                      Table {reservation.tableNumber} • {reservation.guestCount} guests
                    </div>
                    {reservation.specialRequests && reservation.specialRequests.length > 0 && (
                      <div className="mt-2">
                        <p className="text-sm text-gray-400">Special requests:</p>
                        <ul className="text-sm text-gray-300 list-disc list-inside">
                          {reservation.specialRequests.map((request: string, index: number) => (
                            <li key={index}>{request}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Column 2: Prep */}
        <div className="flex-1 border-r border-gray-700 p-6">
          <div className="h-full flex flex-col">
            <h2 className="text-xl font-semibold mb-4 text-orange-400">Prep</h2>
            <div className="flex-1 bg-gray-800 rounded-lg p-4 overflow-y-auto">
                     <div className="space-y-4">
                       {prepItems.map((item: PrepItem) => (
                  <div key={item.id} className={`bg-gray-700 p-4 rounded border-l-4 ${getBorderColor(item.status)}`}>
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="text-xl font-semibold text-white">{item.name}</h3>
                      <span className={`px-3 py-1 rounded text-sm font-medium ${getBadgeColor(item.status)}`}>
                        {getStatusText(item.status)}
                      </span>
                    </div>
                    <div className="text-base text-gray-300 mb-1">
                      {item.quantity} {item.unit}
                      {item.assignedTo && <span className="ml-2">• {item.assignedTo}</span>}
                    </div>
                    {item.notes && (
                      <p className="text-sm text-gray-400 italic">{item.notes}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Column 3: Housekeeping/Order Adds */}
        <div className="flex-1 p-6">
          <div className="h-full flex flex-col">
            <h2 className="text-xl font-semibold mb-4 text-purple-400">Housekeeping & Order Adds</h2>
            <div className="flex-1 bg-gray-800 rounded-lg p-4 overflow-y-auto">
              <div className="space-y-4">
                {/* Order Adds Section */}
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-purple-400 mb-3">Order Modifications</h3>
                         <div className="space-y-3">
                           {orderAdds.map((order: OrderAdd) => (
                      <div key={order.id} className="bg-gray-700 p-3 rounded border-l-4 border-purple-500">
                        <div className="flex justify-between items-start mb-1">
                          <span className="text-lg font-semibold text-white">Table {order.tableNumber}</span>
                          <span className="text-sm text-gray-400">
                            {formatTimeAgo(order.timestamp)}
                          </span>
                        </div>
                        <p className="text-base text-gray-300 font-medium">{order.originalItem}</p>
                        <p className="text-sm text-gray-400">{order.modification}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Housekeeping Section */}
                <div>
                  <h3 className="text-lg font-semibold text-purple-400 mb-3">Housekeeping</h3>
                         <div className="space-y-3">
                           {housekeepingNotes.map((note: HousekeepingNote) => (
                      <div key={note.id} className="bg-gray-700 p-3 rounded border-l-4 border-orange-500">
                        <div className="flex justify-between items-start mb-1">
                          <span className="text-lg font-semibold text-white">
                            {note.tableNumber ? `Table ${note.tableNumber}` : note.title}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getPriorityBadgeColor(note.priority)}`}>
                            {note.priority}
                          </span>
                        </div>
                        <p className="text-base text-gray-300">{note.description}</p>
                        {note.assignedTo && (
                          <p className="text-sm text-gray-400 mt-1">Assigned to: {note.assignedTo}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
             <footer className="bg-gray-800 border-t border-gray-700 px-6 py-3">
               <div className="flex items-center justify-between text-sm text-gray-300">
                 <div className="flex items-center space-x-6">
                   <span>Kitchen Status: <span className={`font-medium ${kitchenMetrics.kitchenStatus === 'Operational' ? 'text-green-400' : 'text-red-400'}`}>{kitchenMetrics.kitchenStatus}</span></span>
                   <span>Orders in Queue: <span className="text-yellow-400 font-medium">{kitchenMetrics.ordersInQueue}</span></span>
                   <span>Prep Status: <span className="text-orange-400 font-medium">{kitchenMetrics.prepCompletion}% Complete</span></span>
                   <span>Avg Ticket Time: <span className="text-blue-400 font-medium">{kitchenMetrics.averageTicketTime} min</span></span>
                 </div>
                 <div className="flex items-center space-x-4">
                   <span>Last Updated: {lastUpdate.toLocaleTimeString()}</span>
                   <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                 </div>
               </div>
             </footer>
    </div>
  )
}
