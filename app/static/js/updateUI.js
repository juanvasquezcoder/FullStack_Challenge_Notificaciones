

function updateUI() {
  const loggedIn = !!token;
  document.getElementById("authSection").style.display = loggedIn ? "none" : "block";
  document.getElementById("notifSection").style.display = loggedIn ? "block" : "none";
  document.getElementById("listSection").style.display = loggedIn ? "block" : "none";
  document.getElementById("userInfo").innerText = loggedIn ? "Sesión activa" : "";
  if (loggedIn) loadNotifications();
}