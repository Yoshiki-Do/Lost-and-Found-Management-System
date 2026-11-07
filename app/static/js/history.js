async function loadHistory() {
    try {
        const tableBody = document.getElementById("history-table-body");

        const lostNumber = document.getElementById("search-lost-number").value;
        const action = document.getElementById("search-action").value;
        const dateFrom = document.getElementById("search-date-from").value;
        const dateTo = document.getElementById("search-date-to").value;

        //Validate Lost Number
        if (lostNumber && (!Number.isInteger(Number(lostNumber)) || Number(lostNumber) < 1)) {
            alert("Lost Number must be a positive integer.");
            return;
        }

        //Validate date range
        if (dateFrom && dateTo && dateFrom > dateTo) {
            alert("History Date From must be earlier than or equal to History Date To.");
            return;
        }

        const response = await fetch("/history/");

        if (!response.ok) {
            throw new Error("Failed to load history");
        }

        const histories = await response.json();

        //Filter histories
        const filteredHistories = histories.filter(history => {
            const matchesLostNumber = !lostNumber || history.lost_number === Number(lostNumber);

            const matchesAction = !action || history.action === action;

            //Extract date part from created_at
            const historyDate = history.created_at.substring(0, 10);

            const matchesDateFrom = !dateFrom || historyDate >= dateFrom;

            const matchesDateTo = !dateTo || historyDate <= dateTo;
            
            return matchesLostNumber && matchesAction && matchesDateFrom && matchesDateTo;
        });

        tableBody.innerHTML = "";

        filteredHistories.forEach(history => {
            const row = document.createElement("tr");

            row.style.cursor = "pointer";

            row.addEventListener("click", () => {
                window.location.href = `/details/${history.lost_number}`;
            });

            const values = [
                history.lost_number,
                history.action,
                history.description,
                new Date(history.created_at).toLocaleDateString()
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");

                cell.textContent = value ?? "";
                
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("History error:", error);
        alert("Failed to load history.");
    }
}

//Search button
document.getElementById("search-button").addEventListener("click", loadHistory);

//Enter key support
document.querySelectorAll(
    "#search-lost-number, #search-action, #search-date-from, #search-date-to"
).forEach(input => {
    input.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            loadHistory();
        }
    });
});

//Reset button
document.getElementById("reset-button").addEventListener("click", () => {
    document.getElementById("search-lost-number").value = "";
    document.getElementById("search-action").value = "";
    document.getElementById("search-date-from").value = "";
    document.getElementById("search-date-to").value = "";

    loadHistory();
});

//Load all histories when page opens
document.addEventListener("DOMContentLoaded", loadHistory);