from flask import Flask, jsonify, request

app = Flask(__name__)

ROOMS = [
    {"id": 1, "type": "Standard", "price": 2500},
    {"id": 2, "type": "Deluxe", "price": 4000},
    {"id": 3, "type": "Suite", "price": 6500},
]

# Demo only: bookings are stored in memory.
# They will disappear when the application restarts.
bookings = []


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/rooms")
def get_rooms():
    return jsonify({"rooms": ROOMS}), 200


@app.post("/bookings")
def create_booking():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400

    room_id = data.get("room_id")
    guest_name = data.get("guest_name")

    if (
        not isinstance(room_id, int)
        or isinstance(room_id, bool)
        or not isinstance(guest_name, str)
        or not guest_name.strip()
    ):
        return jsonify({
            "error": "Valid room_id and guest_name are required"
        }), 400

    room = next((r for r in ROOMS if r["id"] == room_id), None)

    if room is None:
        return jsonify({"error": "Room not found"}), 404

    booking = {
        "id": len(bookings) + 1,
        "room_id": room_id,
        "guest_name": guest_name.strip(),
        "status": "confirmed",
    }

    bookings.append(booking)

    return jsonify({"booking": booking}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)