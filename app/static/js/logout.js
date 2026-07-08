

function logout() {
  token = null;
  localStorage.removeItem("token");
  updateUI();
}