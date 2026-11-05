async function loadDashboard() {
    try {
        const response = await fetch("/dashboard/summary");

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        document.getElementById("total-items").textContent = data.total_items;
        document.getElementById("registered-items").textContent = data.registered_items;
        document.getElementById("returned-items").textContent = data.returned_items;
        document.getElementById("disposed-items").textContent = data.disposed_items;
        
    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

const dashboardCards = document.querySelectorAll(".dashboard-card");

dashboardCards.forEach(card => {
    card.addEventListener("click", () => {
        const status = card.dataset.status;

        if (status) {
            window.location.href = `/items?status=${status}`;
        } else {
            window.location.href = "/items";
        }
    });
});

loadDashboard();