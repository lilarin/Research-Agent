export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8787'
export const MAX_UPLOAD_BYTES = Number(
  import.meta.env.VITE_DOCUMENTS_MAX_UPLOAD_BYTES,
)

const DOCUMENTS_FORMATS = JSON.parse(
  import.meta.env.VITE_DOCUMENTS_FORMATS,
) as string[]

export const DOCUMENTS_ACCEPT = DOCUMENTS_FORMATS.map((format) =>
  format === 'image' ? 'image/*' : `.${format}`,
).join(',')

export function isSupportedDocument(file: File): boolean {
  const extension = file.name.split('.').pop()?.toLowerCase()
  return (
    (extension !== undefined && DOCUMENTS_FORMATS.includes(extension)) ||
    (DOCUMENTS_FORMATS.includes('image') && file.type.startsWith('image/'))
  )
}
