

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form
  });
  const data = await res.json();
  if (!res.ok) {
    document.getElementById("authError").innerText = data.detail || "Error al iniciar sesión";
    return;
  }
  token = data.access_token;
  localStorage.setItem("token", token);
  updateUI();
}