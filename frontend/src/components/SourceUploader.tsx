import type { ChangeEvent, FormEvent } from 'react'
import { useEffect, useRef, useState } from 'react'

import { conversationUuid, uploadSources } from '../api'
import { DOCUMENTS_ACCEPT, isSupportedDocument } from '../config'

function fileKey(file: File): string {
  return `${file.name}-${file.size}-${file.lastModified}`
}

export function SourceUploader() {
  const [files, setFiles] = useState<File[]>([])
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement | null>(null)

  useEffect(() => {
    if (!message && !error) return

    const timer = setTimeout(() => {
      setMessage(null)
      setError(null)
    }, 3000)

    return () => clearTimeout(timer)
  }, [message, error])

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const selected = Array.from(event.currentTarget.files ?? [])
    const supported = selected.filter(isSupportedDocument)
    const unsupported = selected.filter((file) => !isSupportedDocument(file))

    if (unsupported.length > 0) {
      setError(
        `Unsupported file format: ${unsupported
          .map((file) => file.name)
          .join(', ')}`,
      )
    }

    setFiles((current) => {
      const existing = new Set(current.map(fileKey))
      return [
        ...current,
        ...supported.filter((file) => !existing.has(fileKey(file))),
      ]
    })
    event.currentTarget.value = ''
    setMessage(null)
  }

  function removeFile(fileToRemove: File) {
    setFiles((current) => current.filter((file) => file !== fileToRemove))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (files.length === 0 || isUploading) return

    setIsUploading(true)
    setMessage(null)
    setError(null)

    try {
      await uploadSources(files, conversationUuid)
      setMessage(`Uploaded ${files.length} source(s).`)
      setFiles([])
      if (fileInputRef.current) fileInputRef.current.value = ''
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : 'Source upload failed.',
      )
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <section className="panel" aria-labelledby="sources-heading">
      <h2 id="sources-heading">Your sources</h2>
      <form className="form-stack" onSubmit={handleSubmit}>
        <label htmlFor="source-files">Upload information sources</label>
        <input
          id="source-files"
          name="files"
          type="file"
          multiple
          ref={fileInputRef}
          onChange={handleFileChange}
          accept={DOCUMENTS_ACCEPT}
        />
        {files.length > 0 ? (
          <ul className="file-list" aria-label="Selected source files">
            {files.map((file) => (
              <li key={fileKey(file)}>
                <span className="file-name">{file.name}</span>
                <button
                  type="button"
                  className="file-remove"
                  aria-label={`Remove ${file.name}`}
                  title="Remove"
                  onClick={() => removeFile(file)}
                  disabled={isUploading}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        ) : null}
        <div className="button-row">
          <button type="submit" disabled={isUploading || files.length === 0}>
            {isUploading ? 'Uploading...' : 'Upload sources'}
          </button>
        </div>
        {message ? <p className="success">{message}</p> : null}
        {error ? <p className="error">{error}</p> : null}
      </form>
    </section>
  )
}
