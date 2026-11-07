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

async function loadRecentItems() {
    try {
        const response = await fetch("/dashboard/recent-items");

        if (!response.ok) {
            throw new Error("Failed to load recent items");
        }

        const items = await response.json();

        const tableBody = document.getElementById("recent-items-table-body");

        tableBody.innerHTML = "";

        items.forEach(item => {
            const row = document.createElement("tr");

            row.style.cursor = "pointer";

            row.addEventListener("click", () => {
                window.location.href = `/details/${item.lost_number}`;
            });

            const values =[
                item.lost_number,
                item.item_name,
                item.found_location,
                new Date(item.found_at + "T00:00:00").toLocaleDateString(),
                item.storage_box,
                item.status
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "";
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Recent items error:", error);
    }
}

loadDashboard();
loadRecentItems();