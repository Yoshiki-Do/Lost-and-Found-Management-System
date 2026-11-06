const registerForm = document.getElementById("register-form");

//Automatically set Storage Month from Found Date
const foundAtInput = document.getElementById("found-at");
const storageMonthInput = document.getElementById("storage-month");

foundAtInput.addEventListener("change", () => {
    storageMonthInput.value = foundAtInput.value.substring(0, 7);
});

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const itemName = document.getElementById("item-name").value.trim();
    const foundLocation = document.getElementById("found-location").value.trim();
    const storageBox = document.getElementById("storage-box").value.trim();

    if (!itemName || !foundLocation || !storageBox) {
        alert("Please enter valid values for all required fields.")
        return;
    }

    const itemData = {
        item_name: document.getElementById("item-name").value,
        description: document.getElementById("description").value || null,
        found_location: document.getElementById("found-location").value,
        found_at: document.getElementById("found-at").value,
        storage_month: document.getElementById("found-at").value.substring(0, 7),
        storage_box: document.getElementById("storage-box").value
    };

    try {
        const response = await fetch("/items/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(JSON.stringify(error));
        }

        const result = await response.json();

        alert(`Item registered successfully! Lost Number: ${result.lost_number}`);

        registerForm.reset();

    } catch (error) {
        console.error("Registration error:", error);
        alert("Failed to register item. Please try again.");
    }
});