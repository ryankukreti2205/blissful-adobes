from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import uuid
from decimal import Decimal

app = Flask(__name__)
CORS(app) 

# Initialize AWS services
REGION = 'us-east-1'
dynamodb = boto3.resource('dynamodb', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

TABLE_NAME = 'HotelBookings'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:852215679230:BlissfulAbodes_Notifications'
table = dynamodb.Table(TABLE_NAME)

# --- 1. CREATE BOOKING (Guest Portal) ---
@app.route('/book', methods=['POST'])
def book_room():
    try:
        data = request.json
        booking_id = str(uuid.uuid4())
        
        # Extracting the new data from your upgraded React form
        guest_name = data.get('guest_name')
        room_type = data.get('room_type')
        check_in = data.get('check_in', 'N/A')
        check_out = data.get('check_out', 'N/A')
        
        # DynamoDB requires floats to be cast as Decimals
        total_cost = Decimal(str(data.get('total_cost', 0))) 

        table.put_item(
            Item={
                'booking_id': booking_id,
                'guest_name': guest_name,
                'room_type': room_type,
                'check_in': check_in,
                'check_out': check_out,
                'total_cost': total_cost,
                'status': 'Confirmed'
            }
        )

        # Publish the alert to SNS
        message = f"New booking!\nID: {booking_id}\nGuest: {guest_name}\nRoom: {room_type}\nDates: {check_in} to {check_out}"
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Blissful Abodes - New Reservation"
        )

        return jsonify({"message": "Booking successful!", "booking_id": booking_id}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


# --- 2. READ BOOKINGS (Staff Portal) ---
@app.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        # A simple 'scan' reads every item in the table. 
        # (For massive enterprise apps, you'd use 'query' instead to save compute costs).
        response = table.scan()
        items = response.get('Items', [])
        
        return jsonify(items), 200
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch bookings"}), 500


# --- 3. DELETE BOOKING (Admin Portal) ---
@app.route('/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        table.delete_item(
            Key={
                'booking_id': booking_id
            }
        )
        return jsonify({"message": f"Booking {booking_id} successfully cancelled."}), 200
    except Exception as e:
        print(f"Error deleting data: {e}")
        return jsonify({"error": "Failed to cancel booking"}), 500

if __name__ == '__main__':
    # Running on 5000 (Remember to use 5001 if your Mac's AirPlay receiver is still on!)
    app.run(host='0.0.0.0', port=5000)