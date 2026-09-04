import {fetchEventSource} from '@microsoft/fetch-event-source'

import {handleSseMessage} from './sse'
import type {StreamEvent} from './sse'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8787'

export function streamResearch(
  question: string,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  return fetchEventSource(`${API_BASE_URL}/api/v1/questions`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question}),
    signal,
    async onopen(response) {
      if (!response.ok) {
        const text = await response.text()
        throw new Error(text || `Research request failed with ${response.status}`)
      }
    },
    onmessage(message) {
      handleSseMessage(message, onEvent)
    },
    onerror(error) {
      throw error
    },
  })
}

export type UploadResult = {
  uploaded: Array<{name: string; size: number; type: string}>
}

export async function uploadSources(files: FileList): Promise<UploadResult> {
  const formData = new FormData()
  for (let i = 0; i < files.length; i++) {
    const file = files.item(i)
    if (file) formData.append('files', file)
  }

  const response = await fetch(`${API_BASE_URL}/api/sources`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `Source upload failed with ${response.status}`)
  }

  return (await response.json()) as UploadResult
}
