function isEligibleForDisposal(storageMonth) {
    const [year, month] = storageMonth.split("-").map(Number);

    const now = new Date();

    const targetMonthIndex = year * 12 + month;
    const currentMonthIndex = now.getFullYear() * 12 + (now.getMonth() + 1);

    //Current month and previous two months are not eligible
    return targetMonthIndex < currentMonthIndex - 2;
}

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

                cell.textContent = value ?? "";

                row.appendChild(cell);
            });

            row.addEventListener("click", () => {
                const returnUrl = `bulk-disposal?storage_month=${encodeURIComponent(storageMonth)}`;

                window.location.href = `details/${item.lost_number}?from=${encodeURIComponent(returnUrl)}`;
            });

            row.style.cursor = "pointer";

            tableBody.appendChild(row);
        });

        itemCount.textContent = items.length;

        const eligible = isEligibleForDisposal(storageMonth);

        disposeButton.disabled = items.length === 0 || !eligible;

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
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to dispose items");
        }

        const disposedItems = await response.json();

        alert(`${disposedItems.length} items have been disposed.`);

        await loadDisposalItems();

    } catch (error) {
        console.error("Bulk disposal error:", error);
        alert(error.message);
    }
});

document.getElementById("storage-month").addEventListener("change", () => {
    const storageMonth = document.getElementById("storage-month").value;

    document.getElementById("disposal-table-body").innerHTML = "";
    document.getElementById("item-count").textContent = "0";

    const disposeButton = document.getElementById("dispose-all-button");
    disposeButton.disabled = true;
});