//Store the last searched conditions
let searchedParams = new URLSearchParams();

async function loadItems() {
    try {
        const lostNumber = document.getElementById("search-lost-number").value;
        const itemName = document.getElementById("search-item-name").value;
        const status = document.getElementById("search-status").value;
        const dateFrom = document.getElementById("search-date-from").value;
        const dateTo = document.getElementById("search-date-to").value;

        if (lostNumber && (!Number.isInteger(Number(lostNumber)) || Number(lostNumber) < 1)) {
            alert("Lost Number must be a positive integer.");
            return;
        }

        if (dateFrom && dateTo && dateFrom > dateTo) {
            alert("Found Date From must be earlier than or equal to Found Date To.");
            return;
        }

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

        if (dateFrom) {
            params.append("found_date_from", dateFrom);
        }

        if (dateTo) {
            params.append("found_date_to", dateTo);
        }

        searchedParams = new URLSearchParams(params);

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
                new Date(item.found_at + "T00:00:00").toLocaleDateString(),
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

//Search when pressing Enter
document.querySelectorAll(
    "#search-lost-number, #search-item-name, #search-status", "#search-date-from", "#search-date-to"
).forEach(input => {
    input.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            loadItems();
        }
    });
});

document.getElementById("reset-button").addEventListener("click", () => {
    document.getElementById("search-lost-number").value = "";
    document.getElementById("search-item-name").value = "";
    document.getElementById("search-status").value = "";
    document.getElementById("search-date-from").value = "";
    document.getElementById("search-date-to").value = "";
    
    loadItems();
});

//Get status from URL
const urlParams = new URLSearchParams(window.location.search);
const statusFromUrl = urlParams.get("status");

//Set status filter
if (statusFromUrl) {
    document.getElementById("search-status").value = statusFromUrl;
}

//Load items
loadItems();

//Export items as CSV
document.getElementById("export-csv-button").addEventListener("click", () => {
    window.location.href = `/items/export/csv?${searchedParams.toString()}`;
});