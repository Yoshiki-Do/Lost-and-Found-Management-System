async function loadItemDetails() {
    try {
        const pathParts = window.location.pathname.split("/").filter(Boolean);
        const lostNumber = pathParts[pathParts.length - 1];

        const response = await fetch(`/items/${lostNumber}`);

        if (!response.ok) {
            throw new Error("Item not found");
        }

        const item = await response.json();

        document.getElementById("lost-number").textContent = item.lost_number ?? "";
        document.getElementById("item-name").textContent = item.item_name ?? "";
        document.getElementById("description").textContent = item.description ?? "";
        document.getElementById("found-location").textContent = item.found_location ?? "";
        document.getElementById("found-at").textContent = item.found_at ?? "";
        document.getElementById("registered-at").textContent = item.registered_at ?? "";
        document.getElementById("storage-month").textContent = item.storage_month ?? "";
        document.getElementById("storage-box").textContent = item.storage_box ?? "";
        document.getElementById("status").textContent = item.status ?? "";
        document.getElementById("retention-start-at").textContent = item.retention_start_at ?? "";
        document.getElementById("returned-at").textContent = item.returned_at ?? "";
        document.getElementById("disposed-at").textContent = item.disposed_at ?? "";
    } catch (error) {
        console.error("Details error:", error);

        document.getElementById("error-message").textContent = `Unable to load item details.": ${error.message}`;
    }
}

loadItemDetails();