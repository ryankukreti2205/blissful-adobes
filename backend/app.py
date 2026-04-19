from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import uuid

app = Flask(__name__)

# This is the crucial line for your React frontend! 
# It allows cross-origin requests from your browser UI to this backend server.
CORS(app) 

# Initialize AWS services specific to your region
REGION = 'us-east-1'
dynamodb = boto3.resource('dynamodb', region_name=REGION)
sns = boto3.client('sns', region_name=REGION)

TABLE_NAME = 'HotelBookings'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:852215679230:BlissfulAbodes_Notifications' 

@app.route('/book', methods=['POST'])
def book_room():
    try:
        # 1. Parse incoming JSON payload from the React frontend
        data = request.json
        booking_id = str(uuid.uuid4()) # Generate a unique, random string ID
        guest_name = data.get('guest_name')
        room_type = data.get('room_type')

        # 2. Save the booking to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'booking_id': booking_id,
                'guest_name': guest_name,
                'room_type': room_type,
                'status': 'Confirmed'
            }
        )

        # 3. Publish the alert to SNS
        message = f"New booking confirmed!\nID: {booking_id}\nGuest: {guest_name}\nRoom: {room_type}"
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Blissful Abodes - New Booking"
        )

        # 4. Send a success response back to React
        return jsonify({
            "message": "Booking successful!", 
            "booking_id": booking_id
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)