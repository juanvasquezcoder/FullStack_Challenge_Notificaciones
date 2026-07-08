

async function deleteNotification(id) {
  await fetch(`${API}/notifications/${id}`, {
    method: "DELETE",
    headers: { "Authorization": `Bearer ${token}` }
  });
  loadNotifications();
}
