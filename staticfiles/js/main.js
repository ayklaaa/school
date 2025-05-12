document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle
  const menuToggle = document.querySelector(".mobile-menu-toggle")
  const navMenu = document.querySelector(".nav-menu")

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("active")
      menuToggle.classList.toggle("active")
    })
  }

  // Event tabs
  const tabButtons = document.querySelectorAll(".tab-btn")
  const tabPanes = document.querySelectorAll(".tab-pane")

  if (tabButtons.length && tabPanes.length) {
    tabButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const tabId = this.getAttribute("data-tab")

        // Remove active class from all buttons and panes
        tabButtons.forEach((btn) => btn.classList.remove("active"))
        tabPanes.forEach((pane) => pane.classList.remove("active"))

        // Add active class to current button and pane
        this.classList.add("active")
        document.getElementById(tabId).classList.add("active")
      })
    })
  }

  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(".message")
  if (messages.length) {
    setTimeout(() => {
      messages.forEach((message) => {
        message.style.opacity = "0"
        setTimeout(() => {
          message.style.display = "none"
        }, 300)
      })
    }, 5000)
  }
})

document.addEventListener("DOMContentLoaded", function () {
    const newsCards = document.querySelectorAll(".news-card");

    const observer = new IntersectionObserver(entries => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add("show");
                }, index * 200); // Каждая следующая карточка задерживается на 200 мс
            }
        });
    }, { threshold: 0.2 });

    newsCards.forEach(card => observer.observe(card));
});


