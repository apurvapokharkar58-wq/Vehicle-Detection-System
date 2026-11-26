import cv2
import csv
import subprocess
import imageio_ffmpeg
from ultralytics import YOLO
from datetime import datetime
from database import insert_vehicle_event
from color_classifier import classify_vehicle_color

# Load YOLO model
model = YOLO("yolo11n.pt")

video_path = "videos/Sample_Traffic.mp4"

vehicle_names = {
    2: "Car",
    3: "Bike",
    5: "Bus",
    7: "Truck"
}

tracked_vehicles = {}
previous_positions = {}
counted_ids = set()
crossing_events = []

line_crossing_counts = {
    "Car": 0,
    "Bike": 0,
    "Bus": 0,
    "Truck": 0
}

vehicle_counts = {
    "Car": 0,
    "Bike": 0,
    "Bus": 0,
    "Truck": 0
}

# Read video FPS
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.release()

if fps <= 0:
    fps = 30

writer = None

print("Starting vehicle tracking and CSV reporting...")

try:
    results = model.track(
        source=video_path,
        stream=True,
        tracker="bytetrack.yaml",
        persist=True,
        classes=[2, 3, 5, 7],
        conf=0.35,
        imgsz=416,
        device="cpu",
        verbose=False
    )

    for result in results:

        frame = result.plot()
        height, width = frame.shape[:2]

        # Counting line at the middle of the video
        current_line_y = height // 2

        cv2.line(
            frame,
            (0, current_line_y),
            (width, current_line_y),
            (0, 0, 255),
            2
        )

        if result.boxes.id is not None:

            ids = result.boxes.id.int().cpu().tolist()
            classes = result.boxes.cls.int().cpu().tolist()
            boxes = result.boxes.xyxy.int().cpu().tolist()

            for track_id, class_id, box in zip(ids, classes, boxes):

                name = vehicle_names.get(class_id)

                if not name:
                    continue

                x1, y1, x2, y2 = box
                center_y = (y1 + y2) // 2

                                # Extract vehicle image
                vehicle_image = frame[
                    max(0, y1):min(height, y2),
                    max(0, x1):min(width, x2)
                ]

                # Classify vehicle colour
                vehicle_color = classify_vehicle_color(vehicle_image)

                # Display vehicle type and colour
                cv2.putText(
                    frame,
                    f"{name} - {vehicle_color}",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

                # Count each tracked vehicle once
                if track_id not in tracked_vehicles:
                    tracked_vehicles[track_id] = name
                    vehicle_counts[name] += 1

                # Detect line crossing
                if track_id in previous_positions:

                    previous_y = previous_positions[track_id]

                    crossed_line = (
                        (previous_y < current_line_y <= center_y)
                        or
                        (previous_y > current_line_y >= center_y)
                    )

                    if crossed_line and track_id not in counted_ids:

                        line_crossing_counts[name] += 1
                        counted_ids.add(track_id)

                        direction = (
                            "Down" if center_y > previous_y else "Up"
                        )

                        event_timestamp = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        # Save event in memory for CSV
                        crossing_events.append({
                            "Vehicle ID": track_id,
                            "Vehicle Type": name,
                            "Color": vehicle_color,
                            "Timestamp": event_timestamp,
                            "Direction": direction
                        })

                        # Save event in PostgreSQL
                        insert_vehicle_event(
                            track_id,
                            name,
                            event_timestamp,
                            direction,
                            vehicle_color
                        )

                        print(
                            f"Database saved: {track_id} - "
                            f"{name} - {direction}"
                        )

                        print(
                            f"{name} crossed the line! ID: {track_id}"
                        )

                # Update previous vehicle position
                previous_positions[track_id] = center_y

        # Display detected vehicle counts
        y = 30

        for name, count in vehicle_counts.items():

            cv2.putText(
                frame,
                f"{name}: {count}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            y += 30

        # Display line crossing counts
        for name, count in line_crossing_counts.items():

            cv2.putText(
                frame,
                f"{name} Crossed: {count}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            y += 30

        # Save tracking video
        if writer is None:

            writer = cv2.VideoWriter(
                "tracking_output.mp4",
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (width, height)
            )

        writer.write(frame)

        cv2.imshow("Vehicle Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except Exception as error:
    print("Error:", error)

finally:

    if writer is not None:
        writer.release()

    cv2.destroyAllWindows()

    print("Converting tracking video for dashboard...")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i", "tracking_output.mp4",
            "-vcodec", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "tracking_output_web.mp4"
        ],
        check=True
    )

    print("Dashboard video updated successfully!")

    # Generate vehicle summary CSV
    with open("vehicle_report.csv", "w", newline="") as file:

        csv_writer = csv.writer(file)

        csv_writer.writerow([
            "Vehicle Type",
            "Detected Count",
            "Line Crossing Count"
        ])

        for name in vehicle_names.values():

            csv_writer.writerow([
                name,
                vehicle_counts[name],
                line_crossing_counts[name]
            ])

        csv_writer.writerow([
            "Total",
            sum(vehicle_counts.values()),
            sum(line_crossing_counts.values())
        ])

    # Generate line crossing events CSV
    with open("line_crossing_events.csv", "w", newline="") as file:

        fieldnames = [
            "Vehicle ID",
            "Vehicle Type",
            "Color",
            "Timestamp",
            "Direction"
]

        event_writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        event_writer.writeheader()
        event_writer.writerows(crossing_events)

    print("\nLine crossing events saved: line_crossing_events.csv")

    print("\nVehicle Summary:")

    for name in vehicle_names.values():

        print(
            f"{name}: Detected = {vehicle_counts[name]}, "
            f"Crossed = {line_crossing_counts[name]}"
        )

    print("Total detected:", sum(vehicle_counts.values()))
    print("Total crossings:", sum(line_crossing_counts.values()))

    print("CSV report generated: vehicle_report.csv")
    print("Tracking completed!")
