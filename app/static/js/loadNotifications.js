

async function loadNotifications() {
  const res = await fetch(`${API}/notifications/`, {
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (res.status === 401) { logout(); return; }

  const notifications = await res.json();
  const container = document.getElementById("notificationsList");
  container.innerHTML = "";

  if (notifications.length === 0) {
    container.innerHTML = "<p>No tienes notificaciones aún.</p>";
    return;
  }

  notifications.forEach(n => {
    const div = document.createElement("div");
    div.className = "notif" + (n.is_read ? " leida" : "");
    div.innerHTML = `
      <strong>${n.title}</strong>
      <span class="status ${n.status}">${n.status}</span>
      <p>${n.message}</p>
      <small>Canal: ${n.channel} | ${new Date(n.created_at).toLocaleString()}</small><br>
      ${!n.is_read ? `<button onclick="markAsRead(${n.id})" style="width:auto; display:inline-block; margin-top:6px;">Marcar leída</button>` : ""}
      <button onclick="deleteNotification(${n.id})" style="width:auto; display:inline-block; margin-top:6px; background:#ef4444;">Eliminar</button>
    `;
    container.appendChild(div);
  });
}
