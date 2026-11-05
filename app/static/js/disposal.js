async function loadDisposalItems() {
    try {
        const storageMonth = document.getElementById("storage-month").value;
        const tableBody = document.getElementById("disposal-table-body");
        const itemCount = document.getElementById("item-count");
        const disposeButton = document.getElementById("dispose-all-button");

        if (!storageMonth) {
            alert("Please select a storage month.");
            return;
        }

        const params = new URLSearchParams({
            storage_month: storageMonth,
            status: "REGISTERED"
        });

        const response = await fetch(`/items/?${params.toString()}`);

        if (!response.ok) {
            throw new Error("Failed to load disposal items");
        }

        const items = await response.json();

        tableBody.innerHTML = "";

        items.forEach(item => {
            const row = document.createElement("tr");

            const values = [
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

        itemCount.textContent = items.length;
        disposeButton.disabled = items.length === 0; 

    } catch (error) {
        console.error("Disposal error:", error);
        alert("Failed to load disposal items.");
    }
}

document.getElementById("search-button").addEventListener("click", loadDisposalItems);

document.getElementById("dispose-all-button").addEventListener("click", async () => {
    const storageMonth = document.getElementById("storage-month").value;
    const itemCount = document.getElementById("item-count").textContent;

    if (!storageMonth || Number(itemCount) === 0) {
        return;
    }

    const confirmed = confirm(
        `Are you sure you want to dispose ${itemCount} items for ${storageMonth}? This action cannot be undone.`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`/items/bulk-dispose/${storageMonth}`, {method: "PATCH"});

        if (!response.ok) {
            throw new Error("Failed to dispose items");
        }

        const disposedItems = await response.json();

        alert(`${disposedItems.length} items have been disposed.`);

        await loadDisposalItems();

    } catch (error) {
        console.error("Bulk disposal error:", error);
        alert("Failed to dispose items.");
    }
});

document.getElementById("storage-month").addEventListener("change", () => {
    document.getElementById("disposal-table-body").innerHTML = "";
    document.getElementById("item-count").textContent = "0";
    document.getElementById("dispose-all-button").disabled = true;
});