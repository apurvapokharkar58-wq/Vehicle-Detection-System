
from flask import Flask, jsonify, send_from_directory
from database import get_connection
import csv

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/api/summary")
def summary():

    vehicle_data = {}

    with open("vehicle_report.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["Vehicle Type"]

            if name == "Total":
                total_vehicles = int(row["Detected Count"])
                total_crossings = int(row["Line Crossing Count"])
            else:
                vehicle_data[name] = {
                    "detected": int(row["Detected Count"]),
                    "crossed": int(row["Line Crossing Count"])
                }

    return jsonify({
        "total_vehicles": total_vehicles,
        "total_crossings": total_crossings,
        "vehicles": vehicle_data
    })


@app.route("/api/events")
def events():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT vehicle_id, vehicle_type, color,
                   direction, event_timestamp
            FROM vehicle_events
            ORDER BY id DESC
            LIMIT 12
        """)

        records = cursor.fetchall()

        result = [
            {
                "vehicle_id": row[0],
                "vehicle_type": row[1],
                "color": row[2],
                "direction": row[3],
                "timestamp": row[4].strftime("%Y-%m-%d %H:%M:%S")
            }
            for row in records
        ]

        return jsonify(result)

    finally:
        connection.close()


@app.route("/api/colors")
def colors():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT color, COUNT(*)
            FROM (
                SELECT color
                FROM vehicle_events
                ORDER BY id DESC
                LIMIT 12
            ) AS recent_events
            GROUP BY color
            ORDER BY COUNT(*) DESC
        """)

        records = cursor.fetchall()

        return jsonify({
            row[0] or "Unknown": row[1]
            for row in records
        })

    finally:
        connection.close()

@app.route("/video")
def video():
    return send_from_directory(".", "tracking_output_web.mp4")
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
