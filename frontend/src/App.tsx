import { useRef, useState } from 'react'
import type { ChangeEvent, SubmitEvent } from 'react'
import './App.css'
import { streamResearch, uploadSources } from './api'

function App() {
  const [requestText, setRequestText] = useState<string>('')
  const [markdown, setMarkdown] = useState<string>('')
  const [isResearching, setIsResearching] = useState<boolean>(false)
  const [researchError, setResearchError] = useState<string | null>(null)
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null)
  const [uploadMessage, setUploadMessage] = useState<string | null>(null)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState<boolean>(false)

  const abortControllerRef = useRef<AbortController | null>(null)
  const userAbortRequestedRef = useRef(false)

  const selectedFileArray = Array.from({ length: selectedFiles?.length ?? 0 }, (_, index) =>
    selectedFiles?.item(index),
  ).filter((file): file is File => file !== null && file !== undefined)
  const trimmedRequest = requestText.trim()

  async function handleResearchSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!trimmedRequest || isResearching) {
      return
    }

    const abortController = new AbortController()
    abortControllerRef.current = abortController
    userAbortRequestedRef.current = false
    setMarkdown('')
    setResearchError(null)
    setIsResearching(true)

    try {
      await streamResearch(
        trimmedRequest,
        (chunk) => {
          setMarkdown((current) => current + chunk)
        },
        abortController.signal,
      )
    } catch (error) {
      if (error instanceof DOMException && error.name === 'AbortError') {
        if (userAbortRequestedRef.current) {
          setResearchError('Research request cancelled.')
        }
      } else if (error instanceof Error) {
        setResearchError(error.message)
      } else {
        setResearchError('Research request failed.')
      }
    } finally {
      setIsResearching(false)
      abortControllerRef.current = null
      userAbortRequestedRef.current = false
    }
  }

  function handleAbort() {
    if (!abortControllerRef.current) {
      return
    }

    userAbortRequestedRef.current = true
    abortControllerRef.current.abort()
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const files = event.currentTarget.files
    setSelectedFiles(files && files.length > 0 ? files : null)
    setUploadMessage(null)
    setUploadError(null)
  }

  async function handleUploadSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!selectedFiles || selectedFiles.length === 0 || isUploading) {
      return
    }

    setIsUploading(true)
    setUploadMessage(null)
    setUploadError(null)

    try {
      const result = await uploadSources(selectedFiles)
      const uploadedNames = result.uploaded.map((file) => file.name).join(', ')
      setUploadMessage(`Uploaded ${result.uploaded.length} source(s): ${uploadedNames}`)
    } catch (error) {
      if (error instanceof Error) {
        setUploadError(error.message)
      } else {
        setUploadError('Source upload failed.')
      }
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero" aria-labelledby="page-title">
        <h1 id="page-title">Research agent frontend</h1>
        <p>
          Submit a research request and upload any source files the backend should use. The
          response panel displays streamed markdown as plain source text.
        </p>
      </section>

      <section className="panel" aria-labelledby="sources-heading">
        <h2 id="sources-heading">Your sources</h2>
        <form className="form-stack" onSubmit={handleUploadSubmit}>
          <label htmlFor="source-files">Upload information sources</label>
          <input id="source-files" name="files" type="file" multiple onChange={handleFileChange} accept="text/*" />
          {selectedFileArray.length > 0 ? (
            <ul className="file-list" aria-label="Selected source files">
              {selectedFileArray.map((file) => (
                <li key={`${file.name}-${file.size}-${file.lastModified}`}>{file.name}</li>
              ))}
            </ul>
          ) : null}
          <div className="button-row">
            <button type="submit" disabled={isUploading || selectedFileArray.length === 0}>
              {isUploading ? 'Uploading...' : 'Upload sources'}
            </button>
          </div>
          {uploadMessage ? <p className="success">{uploadMessage}</p> : null}
          {uploadError ? <p className="error">{uploadError}</p> : null}
        </form>
      </section>

      <section className="panel" aria-labelledby="request-heading">
        <h2 id="request-heading">Research request</h2>
        <form className="form-stack" onSubmit={handleResearchSubmit}>
          <label htmlFor="research-request">What should the research agent investigate?</label>
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
              <button type="button" className="secondary" onClick={handleAbort}>
                Abort
              </button>
            ) : null}
          </div>
          {researchError ? <p className="error">{researchError}</p> : null}
        </form>
      </section>

      <section className="panel" aria-labelledby="response-heading">
        <h2 id="response-heading">Streaming response</h2>
        <pre className="markdown-output" aria-live="polite">
          {markdown || 'Submit a research request to see the markdown answer here.'}
        </pre>
      </section>
    </main>
  )
}

export default App
