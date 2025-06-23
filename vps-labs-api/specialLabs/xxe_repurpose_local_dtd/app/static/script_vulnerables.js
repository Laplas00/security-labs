// Этот скрипт подключается на каждой странице
// И работает только если в шаблоне передан window.vulnerabilities

document.addEventListener("DOMContentLoaded", () => {
  if (!window.vulnerabilities || !Array.isArray(window.vulnerabilities)) return;

  // Пример уязвимого поведения на DOM XSS
  if (window.vulnerabilities.includes("dom_xss_post_view")) {
    const comment = new URLSearchParams(window.location.search).get("comment");
    const box = document.getElementById("comment-display");
    if (box) box.innerHTML = comment;
  }

  // Тут будут добавляттся другие баги которые могут быть на фронте 
  // if (window.vulnerabilities.includes("something_else")) { ... }
});

