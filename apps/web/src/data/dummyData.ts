import { Reservation, PrepItem, OrderAdd, HousekeepingNote, WhiteboardNote } from '@/types'

// Dummy data for development and testing
export const dummyReservations: Reservation[] = [
  {
    id: '1',
    partyName: 'Smith Party',
    time: '6:30 PM',
    tableNumber: 12,
    guestCount: 4,
    status: 'confirmed',
    specialRequests: ['Birthday celebration', 'High chair needed'],
    phoneNumber: '(555) 123-4567'
  },
  {
    id: '2',
    partyName: 'Johnson Family',
    time: '7:15 PM',
    tableNumber: 8,
    guestCount: 6,
    status: 'pending',
    specialRequests: ['Vegetarian options'],
    phoneNumber: '(555) 234-5678'
  },
  {
    id: '3',
    partyName: 'Williams',
    time: '8:00 PM',
    tableNumber: 5,
    guestCount: 2,
    status: 'seated',
    specialRequests: ['Anniversary dinner'],
    phoneNumber: '(555) 345-6789'
  },
  {
    id: '4',
    partyName: 'Brown Group',
    time: '8:45 PM',
    tableNumber: 15,
    guestCount: 8,
    status: 'confirmed',
    specialRequests: ['Business dinner', 'Quiet table preferred'],
    phoneNumber: '(555) 456-7890'
  }
]

export const dummyPrepItems: PrepItem[] = [
  {
    id: '1',
    name: 'Onions diced',
    category: 'mise-en-place',
    quantity: '2',
    unit: 'lbs',
    status: 'complete',
    priority: 'medium',
    assignedTo: 'Chef Mike'
  },
  {
    id: '2',
    name: 'Garlic minced',
    category: 'mise-en-place',
    quantity: '1',
    unit: 'cup',
    status: 'complete',
    priority: 'medium',
    assignedTo: 'Chef Mike'
  },
  {
    id: '3',
    name: 'Herbs chopped',
    category: 'mise-en-place',
    quantity: '1/2',
    unit: 'cup',
    status: 'complete',
    priority: 'low',
    assignedTo: 'Chef Mike'
  },
  {
    id: '4',
    name: 'Chicken breast trimmed',
    category: 'protein',
    quantity: '15',
    unit: 'pieces',
    status: 'complete',
    priority: 'high',
    assignedTo: 'Chef Sarah'
  },
  {
    id: '5',
    name: 'Salmon portioned',
    category: 'protein',
    quantity: '3',
    unit: 'lbs',
    status: 'in-progress',
    priority: 'high',
    assignedTo: 'Chef Sarah',
    notes: 'Need 12 portions'
  },
  {
    id: '6',
    name: 'Steaks seasoned',
    category: 'protein',
    quantity: '8',
    unit: 'pieces',
    status: 'pending',
    priority: 'high',
    assignedTo: 'Chef Sarah'
  },
  {
    id: '7',
    name: 'Béarnaise sauce',
    category: 'sauce',
    quantity: '1',
    unit: 'batch',
    status: 'behind',
    priority: 'urgent',
    assignedTo: 'Sauce Station',
    notes: 'Running low'
  },
  {
    id: '8',
    name: 'Hollandaise ready',
    category: 'sauce',
    quantity: '1',
    unit: 'batch',
    status: 'behind',
    priority: 'urgent',
    assignedTo: 'Sauce Station'
  },
  {
    id: '9',
    name: 'Marinara heated',
    category: 'sauce',
    quantity: '2',
    unit: 'quarts',
    status: 'complete',
    priority: 'medium',
    assignedTo: 'Sauce Station'
  }
]

export const dummyOrderAdds: OrderAdd[] = [
  {
    id: '1',
    tableNumber: 12,
    originalItem: 'Caesar Salad',
    modification: 'Extra side salad - No dressing',
    timestamp: new Date(Date.now() - 2 * 60 * 1000), // 2 minutes ago
    status: 'pending',
    priority: 'medium'
  },
  {
    id: '2',
    tableNumber: 8,
    originalItem: 'Burger Deluxe',
    modification: 'No onions - Extra pickles',
    timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
    status: 'pending',
    priority: 'high'
  },
  {
    id: '3',
    tableNumber: 5,
    originalItem: 'Fish and Chips',
    modification: 'Substitute fries for sweet potato fries',
    timestamp: new Date(Date.now() - 8 * 60 * 1000), // 8 minutes ago
    status: 'pending',
    priority: 'low'
  },
  {
    id: '4',
    tableNumber: 15,
    originalItem: 'Steak Dinner',
    modification: 'Medium-rare instead of medium',
    timestamp: new Date(Date.now() - 12 * 60 * 1000), // 12 minutes ago
    status: 'pending',
    priority: 'high'
  }
]

export const dummyHousekeepingNotes: HousekeepingNote[] = [
  {
    id: '1',
    type: 'table-maintenance',
    title: 'Table 7 - Spill cleanup needed',
    description: 'Large spill on table - needs immediate attention',
    tableNumber: 7,
    status: 'pending',
    priority: 'urgent',
    assignedTo: 'Housekeeping Team',
    timestamp: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
    estimatedDuration: 10
  },
  {
    id: '2',
    type: 'table-maintenance',
    title: 'Table 15 - Silverware missing',
    description: 'Need 4 complete sets of silverware',
    tableNumber: 15,
    status: 'pending',
    priority: 'high',
    assignedTo: 'Housekeeping Team',
    timestamp: new Date(Date.now() - 20 * 60 * 1000), // 20 minutes ago
    estimatedDuration: 5
  },
  {
    id: '3',
    type: 'cleaning',
    title: 'Kitchen Station 1 - Deep clean',
    description: 'Scheduled deep clean for 2 PM',
    status: 'pending',
    priority: 'medium',
    assignedTo: 'Cleaning Crew',
    timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
    estimatedDuration: 45
  },
  {
    id: '4',
    type: 'special-request',
    title: 'Table 10 - Birthday setup',
    description: 'Birthday celebration setup needed - candles, dessert plate',
    tableNumber: 10,
    status: 'pending',
    priority: 'medium',
    assignedTo: 'Server Team',
    timestamp: new Date(Date.now() - 45 * 60 * 1000), // 45 minutes ago
    estimatedDuration: 15
  }
]

export const dummyWhiteboardNotes: WhiteboardNote[] = [
  {
    id: '1',
    type: 'special',
    title: 'Special of the Day',
    content: 'Pan-seared salmon with lemon butter sauce',
    priority: 'high',
    timestamp: new Date(Date.now() - 60 * 60 * 1000), // 1 hour ago
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // Expires in 24 hours
  },
  {
    id: '2',
    type: '86-item',
    title: '86 Items',
    content: 'Lobster bisque, Caesar salad',
    priority: 'high',
    timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
  },
  {
    id: '3',
    type: 'staff-note',
    title: 'Staff Notes',
    content: 'Dishwasher maintenance at 3 PM',
    priority: 'medium',
    timestamp: new Date(Date.now() - 45 * 60 * 1000), // 45 minutes ago
  },
  {
    id: '4',
    type: 'goal',
    title: 'Today\'s Goals',
    content: 'Reduce ticket times by 15%',
    priority: 'medium',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
  }
]
