// Kitchen Command Center TypeScript Interfaces

export interface Reservation {
  id: string
  partyName: string
  time: string
  tableNumber: number
  guestCount: number
  status: 'confirmed' | 'pending' | 'seated' | 'completed'
  specialRequests?: string[]
  phoneNumber?: string
}

export interface PrepItem {
  id: string
  name: string
  category: 'mise-en-place' | 'protein' | 'sauce' | 'vegetables' | 'garnish'
  quantity: string
  unit: string
  status: 'complete' | 'in-progress' | 'pending' | 'behind'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  notes?: string
  assignedTo?: string
}

export interface OrderAdd {
  id: string
  tableNumber: number
  originalItem: string
  modification: string
  timestamp: Date
  status: 'pending' | 'accepted' | 'declined' | 'completed'
  priority: 'low' | 'medium' | 'high'
  notes?: string
}

export interface HousekeepingNote {
  id: string
  type: 'table-maintenance' | 'cleaning' | 'supplies' | 'special-request' | 'equipment'
  title: string
  description: string
  tableNumber?: number
  status: 'pending' | 'in-progress' | 'completed'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  assignedTo?: string
  timestamp: Date
  estimatedDuration?: number // in minutes
}

export interface WhiteboardNote {
  id: string
  type: 'special' | '86-item' | 'staff-note' | 'goal' | 'announcement'
  title: string
  content: string
  priority: 'low' | 'medium' | 'high'
  timestamp: Date
  expiresAt?: Date
}
