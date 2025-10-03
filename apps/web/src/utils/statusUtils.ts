// Utility functions for status and priority styling

export const getStatusColor = (status: string): string => {
  switch (status) {
    case 'complete':
    case 'confirmed':
      return 'bg-green-100 text-green-800'
    case 'in-progress':
      return 'bg-yellow-100 text-yellow-800'
    case 'pending':
      return 'bg-blue-100 text-blue-800'
    case 'behind':
      return 'bg-red-100 text-red-800'
    case 'seated':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export const getPriorityColor = (priority: string): string => {
  switch (priority) {
    case 'urgent':
      return 'border-red-500 bg-red-50'
    case 'high':
      return 'border-orange-500 bg-orange-50'
    case 'medium':
      return 'border-yellow-500 bg-yellow-50'
    case 'low':
      return 'border-green-500 bg-green-50'
    default:
      return 'border-gray-500 bg-gray-50'
  }
}

export const getStatusText = (status: string): string => {
  switch (status) {
    case 'confirmed':
      return 'Confirmed'
    case 'pending':
      return 'Pending'
    case 'seated':
      return 'Seated'
    case 'complete':
      return 'Complete'
    case 'in-progress':
      return 'In Progress'
    case 'behind':
      return 'Behind'
    default:
      return status.charAt(0).toUpperCase() + status.slice(1).replace('-', ' ')
  }
}

export const getBorderColor = (status: string): string => {
  switch (status) {
    case 'confirmed':
    case 'complete':
      return 'border-green-500'
    case 'pending':
    case 'in-progress':
      return 'border-yellow-500'
    case 'seated':
      return 'border-blue-500'
    case 'behind':
      return 'border-red-500'
    default:
      return 'border-gray-500'
  }
}

export const getBadgeColor = (status: string): string => {
  switch (status) {
    case 'confirmed':
    case 'complete':
      return 'bg-green-600'
    case 'pending':
    case 'in-progress':
      return 'bg-yellow-600'
    case 'seated':
      return 'bg-blue-600'
    case 'behind':
      return 'bg-red-600'
    default:
      return 'bg-gray-600'
  }
}

export const getPriorityBadgeColor = (priority: string): string => {
  switch (priority) {
    case 'urgent':
      return 'bg-red-600'
    case 'high':
      return 'bg-orange-600'
    case 'medium':
      return 'bg-yellow-600'
    case 'low':
      return 'bg-green-600'
    default:
      return 'bg-gray-600'
  }
}

export const formatTimeAgo = (timestamp: Date): string => {
  const now = Date.now()
  const diff = now - timestamp.getTime()
  const minutes = Math.floor(diff / 60000)

  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes} min ago`

  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`

  const days = Math.floor(hours / 24)
  return `${days} day${days > 1 ? 's' : ''} ago`
}
