const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

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