const API = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}

// Wrapper de fetch que agrega el token automáticamente
// y redirige a login si la sesión expiró (401)
async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = options.headers || {};
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, { ...options, headers });

  if (res.status === 401) {
    logout();
    throw new Error("Sesión expirada");
  }
  return res;
}

// Protege páginas que requieren estar logueado.
// Llamar al inicio de me.html y notifications.html
async function requireAuth() {
  if (!getToken()) {
    window.location.href = "/login";
    return null;
  }
  const res = await apiFetch("/auth/me");
  if (!res.ok) return null;
  return await res.json();
}