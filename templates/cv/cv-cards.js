document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".filter-tab");
    const cards = document.querySelectorAll(".student-card");
    const searchInput = document.querySelector(".search-bar input");

    // Filter by Tab
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            // Remove 'active' from all, add to clicked tab
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const filter = tab.dataset.filter;
            cards.forEach(card => {
                if (filter === "all" || card.dataset.category === filter) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });

            // Clear search input when changing filter
            if (searchInput) searchInput.value = "";
        });
    });

    // Live Search
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase().trim();

            cards.forEach(card => {
                const name = card.querySelector(".student-name").textContent.toLowerCase();
                const major = card.querySelector(".student-major").textContent.toLowerCase();
                const matches = name.includes(query) || major.includes(query);

                // Match current filter too
                const activeFilter = document.querySelector(".filter-tab.active")?.dataset.filter;
                const matchesFilter = activeFilter === "all" || card.dataset.category === activeFilter;

                card.style.display = matches && matchesFilter ? "block" : "none";
            });
        });
    }
});
