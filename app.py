from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy storage for user information (replace this with your database)
user_info = {}

# Function to handle end of conversation and display user information
def end_conversation():
    # Retrieve user information from storage
    first_name = user_info.get('first_name', '')
    last_name = user_info.get('last_name', '')
    email = user_info.get('email', '')

    # Compose message with user information
    message = f"Thank you {first_name} {last_name} for chatting with us. We have your email address as {email}."

    return message

# Webhook endpoint for Dialogflow fulfillment
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)

    # Retrieve action from Dialogflow request
    action = req.get('queryResult').get('action')

    # Handle different actions
    if action == 'end_conversation':
        # Store user information from parameters
        parameters = req.get('queryResult').get('parameters')
        user_info['first_name'] = parameters.get('first_name', '')
        user_info['last_name'] = parameters.get('last_name', '')
        user_info['email'] = parameters.get('email', '')

        # Generate response for ending conversation
        fulfillment_text = end_conversation()

        # Send response back to Dialogflow
        return jsonify({'fulfillmentText': fulfillment_text})

    # Handle other actions if needed

if __name__ == '__main__':
    app.run(debug=True)
