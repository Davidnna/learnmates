const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');

/**
 * Shared HTTP helper for the future Flask JSON API.
 * The current Flask application primarily serves HTML forms, so feature API
 * methods should be wired only after the corresponding authenticated JSON
 * endpoints have been added and tested. Never put Groq/database secrets here.
 */
export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...(options.headers || {}),
    },
  });
  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json')
    ? await response.json()
    : await response.text();
  if (!response.ok) {
    const message = typeof payload === 'object' && payload?.error ? payload.error : `Request failed (${response.status})`;
    throw new Error(message);
  }
  return payload;
}

export const api = {
  health: () => apiRequest('/health'),
  // Add auth, tutor, documents, quiz and progress calls as Flask JSON routes land.
};
