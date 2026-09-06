import type { SubmitEvent } from 'react'
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

import './App.css'
import { SourceUploader } from './components/SourceUploader'
import { useResearch } from './hooks/useResearch'

function App() {
  const [requestText, setRequestText] = useState('')
  const { answer, error, isResearching, submit, abort } = useResearch()

  const trimmedRequest = requestText.trim()

  function handleResearchSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!trimmedRequest) return
    void submit(trimmedRequest)
  }

  return (
    <main className="app-shell">
      <section className="hero" aria-labelledby="page-title">
        <h1 id="page-title">Research agent frontend</h1>
        <p>
          Submit a research request and upload any source files the backend
          should use. The response panel renders the streamed markdown answer.
        </p>
      </section>

      <SourceUploader />

      <section className="panel" aria-labelledby="request-heading">
        <h2 id="request-heading">Research request</h2>
        <form className="form-stack" onSubmit={handleResearchSubmit}>
          <label htmlFor="research-request">
            What should the research agent investigate?
          </label>
          <textarea
            id="research-request"
            name="research-request"
            rows={6}
            value={requestText}
            onChange={(event) => setRequestText(event.currentTarget.value)}
            placeholder="Type here..."
          />
          <div className="button-row">
            <button type="submit" disabled={isResearching || !trimmedRequest}>
              {isResearching ? 'Researching...' : 'Start research'}
            </button>
            {isResearching ? (
              <button type="button" className="secondary" onClick={abort}>
                Abort
              </button>
            ) : null}
          </div>
          {error ? <p className="error">{error}</p> : null}
        </form>
      </section>

      <section className="panel" aria-labelledby="response-heading">
        <h2 id="response-heading">Streaming response</h2>
        <div className="markdown-output" aria-live="polite">
          {answer ? (
            <ReactMarkdown>{answer}</ReactMarkdown>
          ) : (
            'Submit a research request to see the markdown answer here.'
          )}
        </div>
      </section>
    </main>
  )
}

export default App
