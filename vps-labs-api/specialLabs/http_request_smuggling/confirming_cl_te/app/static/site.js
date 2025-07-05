document.addEventListener("DOMContentLoaded", function () {
  const messages = window.__flash_messages || [];
  const container = document.getElementById('toast-container');
  if (!container) return;

  messages.forEach((msg, i) => {
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.innerHTML = msg;
    toast.style.animationDelay = `${i * 0.2}s`;
    container.appendChild(toast);

    // Удалять по клику
    toast.addEventListener('click', () => toast.remove());

    // Автоматическое удаление через 10 сек
    setTimeout(() => toast.remove(), 10000);
  });
});

