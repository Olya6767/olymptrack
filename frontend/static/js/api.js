const API_BASE = "/api";
const USER_ID = 1; // TODO: replace with session-based user id

async function apiFetch(path, options = {}) {
    const res = await fetch(API_BASE + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!res.ok) throw new Error(`API error ${res.status}`);
    if (res.status === 204) return null;
    return res.json();
}
