
// Function to update 'mic_on' value in the JSON data
async function updateMicStatus(filePath, newStatus) {
    try {
        const data = await loadJSON(filePath);

        // Update the 'mic_on' value in the JSON object
        data.mic_on = newStatus;

        // Assuming you have an API endpoint to update the file on the server
        const response = await fetch(filePath, {
            method: 'PUT', // Use 'PATCH' if you want to partially update
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Failed to update ${filePath}: ${response.statusText}`);
        }

        console.log(`'mic_on' status updated to: ${newStatus}`);
        // Optionally, refresh the displayed JSON data
        displayJSON(filePath);
    } catch (error) {
        console.error("Error updating mic_on status:", error);
    }
}

