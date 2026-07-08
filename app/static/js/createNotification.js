

async function createNotification() {
  const title = document.getElementById("title").value;
  const message = document.getElementById("message").value;
  const channel = document.getElementById("channel").value;

  const res = await fetch(`${API}/notifications/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ title, message, channel })
  });

  if (res.ok) {
    document.getElementById("title").value = "";
    document.getElementById("message").value = "";
    setTimeout(loadNotifications, 500); // pequeño delay para dar tiempo al background task
  } else if (res.status === 401) {
    logout();
  }
}
