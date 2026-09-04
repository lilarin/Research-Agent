export type StreamEventData = {
  workflow_started: {event_ts_ms: number}
  node_started: {event_ts_ms: number; node: string}
  message: {event_ts_ms: number; answer: string}
  node_finished: {event_ts_ms: number; node: string; duration_ms: number}
  workflow_finished: {
    status: string
    event_ts_ms: number
    first_token_latency_ms: number | null
    generation_duration_ms: number | null
  }
  error: {event_ts_ms: number; message: string}
}

export type StreamEvent = {
  [Event in keyof StreamEventData]: {
    event: Event
    data: StreamEventData[Event]
  }
}[keyof StreamEventData]

type SseMessage = {
  event: string
  data: string
}

export function handleSseMessage(
  message: SseMessage,
  onEvent: (event: StreamEvent) => void,
): void {
  if (!message.event) return

  const payload = JSON.parse(message.data)
  if (message.event === 'error') {
    throw new Error((payload as StreamEventData['error']).message)
  }

  onEvent({event: message.event, data: payload} as StreamEvent)
}
