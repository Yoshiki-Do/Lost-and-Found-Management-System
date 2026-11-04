async function loadItems() {
    try {
        const lostNumber = document.getElementById("search-lost-number").value;
        const itemName = document.getElementById("search-item-name").value;
        const status = document.getElementById("search-status").value;

        const params = new URLSearchParams();

        if (lostNumber) {
            params.append("lost_number", lostNumber);
        }

        if (itemName) {
            params.append("item_name", itemName);
        }

        if (status) {
            params.append("status", status);
        }

        const response = await fetch(`/items/?${params.toString()}`);

        if (!response.ok) {
            throw new Error("Failed to load items");
        }

        const items = await response.json();

        const tableBody = document.getElementById("items-table-body");

        tableBody.innerHTML = "";

        items.forEach(item => {
            const row = document.createElement("tr");

            const values =[
                item.lost_number,
                item.item_name,
                item.found_location,
                new Date(item.found_at).toLocaleDateString(),
                item.storage_box,
                item.status
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");

                if (index === 0) {
                    const link = document.createElement("a");
                    link.href = `/details/${item.lost_number}`;
                    link.textContent = value ?? "";

                    cell.appendChild(link);
                } else {
                    cell.textContent = value ?? "";
                }

                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Items error:", error);
    }
}

document.getElementById("search-button").addEventListener("click", loadItems);

document.getElementById("reset-button").addEventListener("click", () => {
    document.getElementById("search-lost-number").value = "";
    document.getElementById("search-item-name").value = "";
    document.getElementById("search-status").value = "";
    
    loadItems();
});