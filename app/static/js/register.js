

async function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const full_name = document.getElementById("fullName").value;
  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name })
  });
  const data = await res.json();
  if (!res.ok) {
    document.getElementById("authError").innerText = data.detail || "Error al registrar";
    return;
  }
  document.getElementById("authError").innerText = "Registrado. Ahora inicia sesión.";
}