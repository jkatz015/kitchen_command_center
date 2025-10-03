// Simulated data generator for testing functionality
import { Reservation, PrepItem, OrderAdd, HousekeepingNote, WhiteboardNote } from '@/types'

// Simulate real-time updates by generating new data periodically
export class KitchenSimulator {
  private intervalId: NodeJS.Timeout | null = null
  private listeners: Array<(data: any) => void> = []

  start() {
    if (this.intervalId) return

    this.intervalId = setInterval(() => {
      this.generateRandomUpdate()
    }, 10000) // Update every 10 seconds
  }

  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
      this.intervalId = null
    }
  }

  subscribe(listener: (data: any) => void) {
    this.listeners.push(listener)
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  private generateRandomUpdate() {
    const updateType = Math.random()

    if (updateType < 0.3) {
      // Generate new order modification
      this.generateOrderModification()
    } else if (updateType < 0.5) {
      // Update prep status
      this.updatePrepStatus()
    } else if (updateType < 0.7) {
      // Generate housekeeping note
      this.generateHousekeepingNote()
    } else {
      // Update reservation status
      this.updateReservationStatus()
    }
  }

  private generateOrderModification() {
    const tables = [3, 5, 8, 12, 15, 20]
    const items = [
      'Caesar Salad', 'Burger Deluxe', 'Fish and Chips', 'Steak Dinner',
      'Chicken Parmesan', 'Pasta Carbonara', 'Salmon Fillet', 'Vegetarian Risotto'
    ]
    const modifications = [
      'Extra dressing on the side', 'No onions', 'Well done', 'Medium rare',
      'Add mushrooms', 'Extra cheese', 'No bacon', 'Substitute fries'
    ]

    const newOrder: OrderAdd = {
      id: `sim-${Date.now()}`,
      tableNumber: tables[Math.floor(Math.random() * tables.length)],
      originalItem: items[Math.floor(Math.random() * items.length)],
      modification: modifications[Math.floor(Math.random() * modifications.length)],
      timestamp: new Date(),
      status: 'pending',
      priority: Math.random() > 0.7 ? 'high' : 'medium'
    }

    this.notifyListeners({ type: 'order-add', data: newOrder })
  }

  private updatePrepStatus() {
    const statuses = ['complete', 'in-progress', 'pending', 'behind']
    const items = [
      'Onions diced', 'Garlic minced', 'Chicken breast trimmed', 'Salmon portioned',
      'Béarnaise sauce', 'Hollandaise ready', 'Carrots julienne', 'Mushrooms sautéed'
    ]

    const update = {
      item: items[Math.floor(Math.random() * items.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      timestamp: new Date()
    }

    this.notifyListeners({ type: 'prep-update', data: update })
  }

  private generateHousekeepingNote() {
    const types = ['table-maintenance', 'cleaning', 'supplies', 'special-request', 'equipment']
    const titles = [
      'Table cleanup needed', 'Silverware missing', 'Deep clean scheduled',
      'Birthday setup', 'Equipment repair', 'Supply restock'
    ]
    const descriptions = [
      'Spill cleanup required', 'Need complete silverware set', 'Scheduled maintenance',
      'Special celebration setup', 'Equipment malfunction', 'Running low on supplies'
    ]

    const newNote: HousekeepingNote = {
      id: `sim-${Date.now()}`,
      type: types[Math.floor(Math.random() * types.length)] as any,
      title: titles[Math.floor(Math.random() * titles.length)],
      description: descriptions[Math.floor(Math.random() * descriptions.length)],
      tableNumber: Math.random() > 0.5 ? Math.floor(Math.random() * 20) + 1 : undefined,
      status: 'pending',
      priority: Math.random() > 0.8 ? 'urgent' : Math.random() > 0.6 ? 'high' : 'medium',
      timestamp: new Date(),
      estimatedDuration: Math.floor(Math.random() * 30) + 5
    }

    this.notifyListeners({ type: 'housekeeping-note', data: newNote })
  }

  private updateReservationStatus() {
    const statuses = ['confirmed', 'pending', 'seated', 'completed']
    const tables = [3, 5, 8, 12, 15, 20]

    const update = {
      tableNumber: tables[Math.floor(Math.random() * tables.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      timestamp: new Date()
    }

    this.notifyListeners({ type: 'reservation-update', data: update })
  }

  private notifyListeners(data: any) {
    this.listeners.forEach(listener => listener(data))
  }
}

// Export singleton instance
export const kitchenSimulator = new KitchenSimulator()

// Utility function to generate random kitchen metrics
export function generateKitchenMetrics() {
  return {
    ordersInQueue: Math.floor(Math.random() * 20) + 5,
    prepCompletion: Math.floor(Math.random() * 30) + 70, // 70-100%
    averageTicketTime: Math.floor(Math.random() * 10) + 15, // 15-25 minutes
    kitchenStatus: Math.random() > 0.1 ? 'Operational' : 'Maintenance',
    lastUpdated: new Date()
  }
}

// Utility function to generate random staff assignments
export function generateStaffAssignments() {
  const staff = ['Chef Mike', 'Chef Sarah', 'Sauce Station', 'Prep Station', 'Garnish Station', 'Housekeeping Team']
  const assignments = staff.map(member => ({
    name: member,
    status: Math.random() > 0.2 ? 'active' : 'break',
    currentTask: Math.random() > 0.5 ? 'Working on orders' : 'On break'
  }))

  return assignments
}
