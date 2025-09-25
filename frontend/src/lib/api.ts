export interface UserContext {
  occasion?: string;
  style_preference?: string;
  body_type?: string;
  color_preference?: string;
  budget?: string;
}

const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export async function analyzeImage(imageBase64: string, userContext: UserContext) {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_base64: imageBase64, user_context: userContext })
  });
  if (!res.ok) throw new Error(`Analyze failed: ${res.status}`);
  return res.json();
}

export async function getRecommendations(userContext: UserContext, imageBase64?: string) {
  const res = await fetch(`${API_BASE}/api/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_context: userContext, image_base64: imageBase64 })
  });
  if (!res.ok) throw new Error(`Recommend failed: ${res.status}`);
  return res.json();
}

export async function chat(messages: { role: 'user' | 'assistant' | 'system'; content: string }[]) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages })
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return res.json();
}


