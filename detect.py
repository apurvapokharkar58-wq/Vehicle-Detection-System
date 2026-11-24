
import cv2
import csv
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

video_path = "videos/traffic.mp4"

vehicle_names = {
    2: "Car",
    3: "Bike",
    5: "Bus",
    7: "Truck"
}

tracked_vehicles = {}

vehicle_counts = {
    "Car": 0,
    "Bike": 0,
    "Bus": 0,
    "Truck": 0
}

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

        if result.boxes.id is not None:
            ids = result.boxes.id.int().cpu().tolist()
            classes = result.boxes.cls.int().cpu().tolist()

            for track_id, class_id in zip(ids, classes):

                if track_id not in tracked_vehicles:
                    name = vehicle_names.get(class_id)

                    if name:
                        tracked_vehicles[track_id] = name
                        vehicle_counts[name] += 1

        # Display counts
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

        # Save tracking video
        if writer is None:
            height, width = frame.shape[:2]

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

    # Generate CSV report
    with open("vehicle_report.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)

        csv_writer.writerow(["Vehicle Type", "Unique Count"])

        for name, count in vehicle_counts.items():
            csv_writer.writerow([name, count])

        csv_writer.writerow(["Total", sum(vehicle_counts.values())])

    print("\nUnique Vehicle Summary:")

    for name, count in vehicle_counts.items():
        print(f"{name}: {count}")

    print("Total:", sum(vehicle_counts.values()))
    print("CSV report generated: vehicle_report.csv")
    print("Tracking completed!")
