

async function markAsRead(id) {
  await fetch(`${API}/notifications/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ is_read: true })
  });
  loadNotifications();
}
