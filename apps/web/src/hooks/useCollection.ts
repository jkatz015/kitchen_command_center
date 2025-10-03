import { useState, useEffect } from 'react'
import {
  collection,
  onSnapshot,
  query,
  orderBy,
  where,
  DocumentData,
  Query,
  QueryConstraint
} from 'firebase/firestore'
import { db } from '@/lib/firebase'

interface UseCollectionOptions {
  orderByField?: string
  orderDirection?: 'asc' | 'desc'
  whereConditions?: QueryConstraint[]
}

interface UseCollectionReturn<T> {
  data: T[]
  loading: boolean
  error: string | null
}

/**
 * Custom hook for listening to Firestore collections
 * Returns an empty array as a stub for now
 *
 * @param collectionName - Name of the Firestore collection
 * @param options - Optional query options (orderBy, where conditions)
 * @returns Object with data array, loading state, and error state
 */
export function useCollection<T = DocumentData>(
  collectionName: string,
  options?: UseCollectionOptions
): UseCollectionReturn<T> {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Stub implementation - returns empty array
    // TODO: Implement actual Firestore collection listening
    console.log(`useCollection stub called for collection: ${collectionName}`, options)

    // Simulate loading state
    const timer = setTimeout(() => {
      setData([])
      setLoading(false)
      setError(null)
    }, 100)

    return () => clearTimeout(timer)

    /*
    // Future implementation when Firebase is properly configured:
    let q: Query<DocumentData>

    try {
      const collectionRef = collection(db, collectionName)

      if (options?.orderByField || options?.whereConditions) {
        const constraints: QueryConstraint[] = []

        // Add where conditions
        if (options.whereConditions) {
          constraints.push(...options.whereConditions)
        }

        // Add order by
        if (options.orderByField) {
          constraints.push(
            orderBy(
              options.orderByField,
              options.orderDirection || 'asc'
            )
          )
        }

        q = query(collectionRef, ...constraints)
      } else {
        q = collectionRef
      }

      const unsubscribe = onSnapshot(
        q,
        (snapshot) => {
          const docs = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
          })) as T[]

          setData(docs)
          setLoading(false)
          setError(null)
        },
        (err) => {
          console.error('Error listening to collection:', err)
          setError(err.message)
          setLoading(false)
        }
      )

      return unsubscribe
    } catch (err) {
      console.error('Error setting up collection listener:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
      setLoading(false)
    }
    */
  }, [collectionName, options?.orderByField, options?.orderDirection, options?.whereConditions])

  return { data, loading, error }
}

/**
 * Stub hook for listening to a single document
 * Returns null as a stub for now
 */
export function useDocument<T = DocumentData>(
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
