import { useState, useEffect } from 'react'

interface UseCollectionOptions {
  orderByField?: string
  orderDirection?: 'asc' | 'desc'
  whereConditions?: any[]
}

interface UseCollectionReturn<T> {
  data: T[]
  loading: boolean
  error: string | null
}

/**
 * Stub hook for collection data
 * Returns an empty array as a stub for now
 *
 * @param collectionName - Name of the collection
 * @param options - Optional query options (orderBy, where conditions)
 * @returns Object with data array, loading state, and error state
 */
export function useCollection<T = any>(
  collectionName: string,
  options?: UseCollectionOptions
): UseCollectionReturn<T> {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Stub implementation - returns empty array
    console.log(`useCollection stub called for collection: ${collectionName}`, options)

    // Simulate loading state
    const timer = setTimeout(() => {
      setData([])
      setLoading(false)
      setError(null)
    }, 100)

    return () => clearTimeout(timer)
  }, [collectionName, options?.orderByField, options?.orderDirection, options?.whereConditions])

  return { data, loading, error }
}

/**
 * Stub hook for listening to a single document
 * Returns null as a stub for now
 */
export function useDocument<T = any>(
  collectionName: string,
  documentId: string
): { data: T | null; loading: boolean; error: string | null } {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Stub implementation - returns null
    console.log(`useDocument stub called for: ${collectionName}/${documentId}`)

    const timer = setTimeout(() => {
      setData(null)
      setLoading(false)
      setError(null)
    }, 100)

    return () => clearTimeout(timer)
  }, [collectionName, documentId])

  return { data, loading, error }
}
