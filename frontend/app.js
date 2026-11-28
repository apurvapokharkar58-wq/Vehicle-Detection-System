
async function loadDashboard() {
    try {
        // Get vehicle summary
        const summaryResponse = await fetch("/api/summary");
        const summary = await summaryResponse.json();

        document.getElementById("totalVehicles").textContent =
            summary.total_vehicles;

        document.getElementById("totalCrossings").textContent =
            summary.total_crossings;

        document.getElementById("totalCars").textContent =
            summary.vehicles.Car?.detected || 0;

        document.getElementById("totalBikes").textContent =
            summary.vehicles.Bike?.detected || 0;

        // Display vehicle chart
        displayChart("vehicleChart", summary.vehicles, "detected");

        // Get color information from PostgreSQL
        const colorResponse = await fetch("/api/colors");
        const colors = await colorResponse.json();

        displayChart("colorChart", colors);

        // Get recent database events
        const eventsResponse = await fetch("/api/events");
        const events = await eventsResponse.json();

        const table = document.getElementById("eventsTable");
        table.innerHTML = "";

        events.forEach(event => {
            table.innerHTML += `
                <tr>
                    <td>${event.vehicle_id}</td>
                    <td>${event.vehicle_type}</td>
                    <td>${event.color || "Unknown"}</td>
                    <td>${event.direction}</td>
                    <td>${event.timestamp}</td>
                </tr>
            `;
        });

        if (events.length === 0) {
            table.innerHTML =
                '<tr><td colspan="5">No vehicle events found.</td></tr>';
        }

    } catch (error) {
        console.error("Dashboard loading error:", error);
    }
}

function displayChart(elementId, data, field = null) {
    const container = document.getElementById(elementId);
    container.innerHTML = "";

    const entries = Object.entries(data);
    const maxValue = Math.max(...entries.map(([key, value]) =>
        field ? value[field] : value
    ), 1);

    entries.forEach(([name, value]) => {
        const count = field ? value[field] : value;
        const percentage = (count / maxValue) * 100;

        container.innerHTML += `
            <div class="chart-item">
                <div class="chart-label">
                    <span>${name}</span>
                    <strong>${count}</strong>
                </div>
                <div class="chart-bar">
                    <div class="chart-fill"
                         style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    });
}

loadDashboard();

// Refresh dashboard data every 5 seconds
setInterval(loadDashboard, 5000);
