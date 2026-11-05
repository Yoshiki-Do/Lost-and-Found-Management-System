async function loadHistory() {
    try {
        const tableBody = document.getElementById("history-table-body");

        const lostNumber = document.getElementById("search-lost-number").value;
        const action = document.getElementById("search-action").value;

        const response = await fetch("/history/");

        if (!response.ok) {
            throw new Error("Failed to load history");
        }

        const histories = await response.json();

        //Filter histories
        const filteredHistories = histories.filter(history => {
            const matchesLostNumber = !lostNumber || history.lost_number === Number(lostNumber);

            const matchesAction = !action || history.action === action;
            
            return matchesLostNumber && matchesAction; 
        });

        tableBody.innerHTML = "";

        filteredHistories.forEach(history => {
            const row = document.createElement("tr");

            const values = [
                history.lost_number,
                history.action,
                history.description,
                new Date(history.created_at).toLocaleDateString()
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");

                if (index === 0) {
                    const link =document.createElement("a");
                    link.href = `/details/${history.lost_number}`;
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
        console.error("History error:", error);
        alert("Failed to load history.");
    }
}

//Search button
document.getElementById("search-button").addEventListener("click", loadHistory);

//Reset button
document.getElementById("reset-button").addEventListener("click", () => {
    document.getElementById("search-lost-number").value = "";
    document.getElementById("search-action").value = "";

    loadHistory();
});

//Load all histories when page opens
document.addEventListener("DOMContentLoaded", loadHistory);