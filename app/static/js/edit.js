const lostNumber = window.location.pathname.split("/").pop();
const params = new URLSearchParams(window.location.search);
const returnUrl = params.get("from");

const detailsUrl = returnUrl
    ? `/details/${lostNumber}?from=${encodeURIComponent(returnUrl)}`
    : `/details/${lostNumber}`;

//Load existing item data
async function loadItem() {
    try {
        const response = await fetch(`/items/${lostNumber}`);

        if (!response.ok) {
            throw new Error("Failed to load item");
        }

        const item = await response.json();

        if (item.status !== "REGISTERED") {
            alert("Only registered items can be edited.");
            window.location.href = `/details/${lostNumber}`;
            return;
        }

        document.getElementById("lost-number").value = item.lost_number;
        document.getElementById("item-name").value = item.item_name;
        document.getElementById("description").value = item.description ?? "";
        document.getElementById("found-location").value = item.found_location;
        document.getElementById("found-at").value = item.found_at;
        document.getElementById("storage-box").value = item.storage_box;

    } catch (error) {
        console.error("Load item error:", error);
        alert("Failed to load item.");
        window.location.href = "/items/";
    }
}

//Save edited item
document.getElementById("edit-item-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const itemData = {
        item_name: document.getElementById("item-name").value.trim(),
        description: document.getElementById("description").value.trim() || null,
        found_location: document.getElementById("found-location").value.trim(),
        found_at: document.getElementById("found-at").value,
        storage_box: document.getElementById("storage-box").value.trim(),
    };

    if (
        !itemData.item_name ||
        !itemData.found_location ||
        !itemData.found_at ||
        !itemData.storage_box
    ) {
        alert("Please fill in all required fields.");
        return;
    }

    try {
        const response = await fetch(`/items/${lostNumber}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to update item");
        }

        alert("Item updated successfully");
        window.location.replace(detailsUrl);

    } catch (error) {
        console.error("Update item error:", error);
        alert(error.message);
    }
});

//Cancel editing
document.getElementById("cancel-button").addEventListener("click", () => {
    window.location.replace(detailsUrl);
});

//Initial load
loadItem();