import { fetchEventSource } from '@microsoft/fetch-event-source'

import type { StreamEvent } from './sse'
import { handleSseMessage } from './sse'
import { API_BASE_URL, MAX_UPLOAD_BYTES } from './config'

export const conversationUuid = crypto.randomUUID()

function formatErrorDetail(detail: unknown): string | null {
  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (item && typeof item === 'object' && 'msg' in item) {
          return typeof item.msg === 'string' ? item.msg : null
        }
        return null
      })
      .filter((message): message is string => message !== null)

    return messages.length > 0 ? messages.join(' ') : null
  }

  return null
}

async function getApiErrorMessage(
  response: Response,
  fallback: string,
): Promise<string> {
  const contentType = response.headers.get('content-type') ?? ''
  if (contentType.includes('application/json')) {
    const body = (await response.json().catch(() => null)) as {
      detail?: unknown
    } | null
    const detail = formatErrorDetail(body?.detail)
    if (detail) return detail
  }

  return fallback
}

export function streamResearch(
  question: string,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  return fetchEventSource(`${API_BASE_URL}/api/v1/questions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, uuid: conversationUuid }),
    signal,
    openWhenHidden: true,
    async onopen(response) {
      if (!response.ok) {
        throw new Error(
          await getApiErrorMessage(response, 'Research request failed.'),
        )
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

export async function uploadSources(
  files: File[],
  conversationUuid: string,
): Promise<void> {
  for (const file of files) {
    if (file.size > MAX_UPLOAD_BYTES) {
      throw new Error(`Maximum file size is ${MAX_UPLOAD_BYTES} bytes`)
    }
  }

  const formData = new FormData()
  formData.append('conversation_uuid', conversationUuid)
  for (const file of files) {
    formData.append('files', file)
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/documents`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error(await getApiErrorMessage(response, 'Source upload failed.'))
  }
}
