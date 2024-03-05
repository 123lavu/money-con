from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# ExchangeRate-API API key
API_KEY = '643c55bfd6fc97bb8c82c81c'

# Home route
@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Currency Converter</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                .container {
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                
                h1 {
                    text-align: center;
                    color: #333;
                }
                
                form {
                    text-align: center;
                }
                
                label {
                    display: block;
                    margin-bottom: 10px;
                }
                
                input[type="text"],
                input[type="number"] {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                
                button:hover {
                    background-color: #45a049;
                }
                
                #result {
                    margin-top: 20px;
                    font-size: 18px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Currency Converter</h1>
                <form id="converter-form">
                    <label for="from_currency">From Currency:</label>
                    <input type="text" id="from_currency" name="from_currency"><br>
                    <label for="to_currency">To Currency:</label>
                    <input type="text" id="to_currency" name="to_currency"><br>
                    <label for="amount">Amount:</label>
                    <input type="number" id="amount" name="amount"><br>
                    <button type="submit">Convert</button>
                </form>
                <div id="result"></div>
            </div>

            <script>
                document.getElementById('converter-form').addEventListener('submit', function(event) {
                    event.preventDefault();
                    const formData = new FormData(this);
                    fetch('/convert', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('result').innerText = data;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            </script>
        </body>
        </html>
    ''')

# Currency conversion route
@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = float(request.form['amount'])

    try:
        # Make API request to ExchangeRate-API
        url = f"https://v6.exchangeratesapi.io/latest?base={from_currency}&symbols={to_currency}&apikey={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        data = response.json()

        # Perform currency conversion
        if 'rates' in data:
            exchange_rate = data['rates'][to_currency]
            converted_amount = amount * exchange_rate
            result = f"{amount} {from_currency} is equal to {converted_amount} {to_currency}"
        else:
            result = "Error fetching exchange rate"

    except requests.exceptions.RequestException as e:
        result = f"Error making API request: {e}"

    return result

if __name__ == '__main__':
    app.run(debug=True)
