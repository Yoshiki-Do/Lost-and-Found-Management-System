const backupButton=document.getElementById("backup-button");
const backupSelect=document.getElementById("backup-select");
const restoreButton=document.getElementById("restore-button");
const backupMessage=document.getElementById("backup-message");

async function loadBackups() {
    try {
        const response = await fetch("/backup/list");

        if (!response.ok) {
            throw new Error("Failed to load backup list.");
        }

        const data = await response.json();

        backupSelect.innerHTML = `
            <option value="">Select a backup file</option>
        `;

        data.backups.forEach(filename => {
            const option = document.createElement("option");
            option.value = filename;
            option.textContent = filename;
            backupSelect.appendChild(option);
        });

        restoreButton.disabled = true;

    } catch (error) {
        backupMessage.textContent = error.message;
    }
}

//Create and r\download a backup
backupButton.addEventListener("click", async () => {
    try {
        backupButton.disabled = true;
        backupMessage.textContent = "Creating backup...";

        const response = await fetch("/backup/", {method: "POST"});

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Backup failed.");
        }

        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);

        const disposition = response.headers.get("Content-Disposition");
        const filenameMatch = disposition?.match(/filename="?([^"]+)"?/);
        const filename = filenameMatch ? filenameMatch[1] : "lost_and_found_backup.db";

        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = filename;
        link.click();

        URL.revokeObjectURL(downloadUrl);

        backupMessage.textContent = "Backup created successfully.";

        await loadBackups();

    } catch (error) {
        backupMessage.textContent = error.message;

    } finally {
        backupButton.disabled = false;
    }
});

//Enable Restore button when a backup is selected
backupSelect.addEventListener("change", () => {
    restoreButton.disabled = !backupSelect.value;
});

//Restore selected backup
restoreButton.addEventListener("click", async () => {
    const filename = backupSelect.value;

    if (!filename) {
        return;
    }

    const confirmed = window.confirm(
        `Are you sure you want to restore this backup?\n\n${filename}\n\n` +
        "The current database will be replaced. " +
        "A backup of the current database will be created automatically."
    );

    if(!confirmed) {
        return;
    }

    try {
        restoreButton.disabled = true;
        backupMessage.textContent = "Restoring database...";

        const response = await fetch("/backup/restore", {
            method: "POST",
            headers: {
                "content-Type": "application/json"
            },
        body: JSON.stringify({
            filename: filename
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Restore failed.");
    }

    backupMessage.textContent = "Database restored successfully.";

    await loadBackups();

    } catch (error) {
        backupMessage.textContent = error.message;

    } finally {
        restoreButton.disabled = !backupSelect.value;
    }
});

//Load backup list when the page opens
loadBackups();