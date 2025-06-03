document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("search-input");
  if (!input) return;

  const container = document.querySelector(".feed-container");
  const cards = container.querySelectorAll(".post-card");

  input.addEventListener("input", function () {
    const query = input.value.toLowerCase().trim();

    cards.forEach(card => {
      const title = card.querySelector(".post-card__title")?.innerText.toLowerCase() || "";
      const subtitle = card.querySelector(".post-card__subtitle")?.innerText.toLowerCase() || "";
      const author = card.querySelector(".post-card__author")?.innerText.toLowerCase() || "";

      const match = title.includes(query) || subtitle.includes(query) || author.includes(query);

      card.style.display = match ? "block" : "none";
    });
  });
});

