from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory store for transactions and balances
transactions = []
balances = {}


# Route to add points
@app.route('/add', methods=['POST'])
def add_points():
    # Get the data from the request
    data = request.get_json()
    payer = data['payer']
    points = data['points']
    timestamp = data['timestamp']

    # Convert the timestamp to a datetime object
    dt_object = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    
    # Add the transaction to the list of transactions
    transactions.append({
        'payer': payer,
        'points': points,
        'timestamp': dt_object
    })

    # Update the balance for the payer
    if payer in balances:
        balances[payer] += points
    else:
        balances[payer] = points

    return '', 200


# Route to spend points
@app.route('/spend', methods=['POST'])
def spend_points():
    data = request.get_json()
    points_to_spend = data['points']
    
    # Check if there are enough points
    total_points = sum(balances.values())
    if points_to_spend > total_points:
        return "User doesn't have enough points", 400
    
    # Sort transactions by timestamp (oldest first)
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])

    points_spent = {}

    # Go through each transaction and spend points
    for transaction in sorted_transactions:
        if points_to_spend <= 0:
            break

        payer = transaction['payer']
        
        # Either use up all the payer's points or the points to spend
        if transaction["points"] < 0:
            points_deducted = transaction["points"]
        else:
            points_deducted = min(transaction['points'], points_to_spend)

        # Update the points to spend and the balance
        points_to_spend -= points_deducted
        balances[payer] -= points_deducted

        # Update the points spent
        if payer not in points_spent:
            points_spent[payer] = 0
        
        points_spent[payer] -= points_deducted

    return jsonify(points_spent), 200


# Route to get the current balance
@app.route('/balance', methods=['GET'])
def get_balance():
    # returns a json of the current balances
    return jsonify(balances), 200


# Route to reset the state of the server
@app.route('/reset', methods=['POST'])
def reset():
    transactions.clear()
    balances.clear()

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
