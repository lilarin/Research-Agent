import { useRef, useState } from 'react'

import { streamResearch } from '../api'

export function useResearch() {
  const [answer, setAnswer] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isResearching, setIsResearching] = useState(false)
  const abortControllerRef = useRef<AbortController | null>(null)
  const userAbortRequestedRef = useRef(false)

  async function submit(question: string) {
    if (isResearching) return

    const abortController = new AbortController()
    abortControllerRef.current = abortController
    userAbortRequestedRef.current = false
    setAnswer('')
    setError(null)
    setIsResearching(true)

    try {
      await streamResearch(
        question,
        (event) => {
          if (event.event === 'message') {
            setAnswer((current) => current + event.data.answer)
          }
        },
        abortController.signal,
      )
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') {
        if (userAbortRequestedRef.current) {
          setError('Research request cancelled.')
        }
      } else if (error instanceof Error) {
        setError(error.message)
      } else {
        setError('Research request failed.')
      }
    } finally {
      setIsResearching(false)
      abortControllerRef.current = null
      userAbortRequestedRef.current = false
    }
  }

  function abort() {
    if (!abortControllerRef.current) return

    userAbortRequestedRef.current = true
    abortControllerRef.current.abort()
  }

  return { answer, error, isResearching, submit, abort }
}
