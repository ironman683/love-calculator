from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Love Calculator</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💖</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 450px;
            width: 100%;
        }
        
        h1 {
            color: #e91e63;
            margin-bottom: 10px;
            font-size: 42px;
        }
        
        .subtitle {
            color: #999;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        input {
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #e91e63;
            box-shadow: 0 0 8px rgba(233, 30, 99, 0.2);
        }
        
        input::placeholder {
            color: #ccc;
        }
        
        button {
            width: 100%;
            padding: 14px;
            margin-top: 10px;
            background: linear-gradient(135deg, #e91e63, #c2185b);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(233, 30, 99, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 40px;
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        
        .result.show {
            display: block;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result-text {
            font-size: 24px;
            color: #333;
            margin-bottom: 15px;
        }
        
        .love-percentage {
            font-size: 64px;
            color: #e91e63;
            font-weight: bold;
            margin: 20px 0;
            animation: grow 0.6s ease-out;
        }
        
        @keyframes grow {
            from {
                transform: scale(0);
            }
            to {
                transform: scale(1);
            }
        }
        
        .message {
            font-size: 28px;
            font-weight: bold;
            margin-top: 20px;
            color: #667eea;
        }
        
        .reset-button {
            background: #f0f0f0;
            color: #666;
            margin-top: 20px;
            font-size: 14px;
            padding: 10px;
        }
        
        .reset-button:hover {
            background: #e0e0e0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .heart {
            position: fixed;
            bottom: -10px;
            font-size: 20px;
            animation: floatUp 4s linear infinite;
        }

        @keyframes floatUp {
            0% {
                transform: translateY(0);
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Love Calculator 💖</h1>
        <p class="subtitle">Just a little something I made for you 💖</p>
        <p style="font-size:12px;color:#bbb;margin-bottom:20px;">
        Made specially for someone very important ❤️ 
        </p>
        
        <form id="loveForm">
            <div class="form-group">
                <input type="text" id="name1" placeholder="Your Name" required>
            </div>
            <div class="form-group">
                <input type="text" id="name2" placeholder="His Name" required>
            </div>
            <button type="submit">Calculate Love 💗</button>
        </form>
        
        <div class="result" id="result">
            <div class="result-text" id="resultText"></div>
            <div class="love-percentage" id="percentage"></div>
            <div class="message" id="message"></div>
            <button type="button" class="reset-button" onclick="resetForm()">Try Again</button>
        </div>
    </div>

    <script>
        // Handle form submission
        document.getElementById('loveForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name1 = document.getElementById('name1').value.trim();
            const name2 = document.getElementById('name2').value.trim();
            
            if (!name1 || !name2) {
                alert('Please enter both names!');
                return;
            }
            
            try {
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({name1: name1, name2: name2})
                });
                
                const data = await response.json();
                
                document.getElementById('resultText').textContent = data.result_text;
                document.getElementById('percentage').textContent = data.percentage + '%';
                document.getElementById('message').textContent = data.message;
                document.getElementById('result').classList.add('show');
                for(let i=0;i<20;i++){
                    createHeart();
                }
                
            } catch (error) {
                alert('Error calculating love percentage. Please try again!');
                console.error(error);
            }
        });
        
        // Reset form function
        function resetForm() {
            document.getElementById('loveForm').reset();
            document.getElementById('result').classList.remove('show');
            document.getElementById('name1').focus();
        }
        
        function createHeart() {
            const heart = document.createElement("div");
            heart.classList.add("heart");
            heart.innerHTML = "💖";
            heart.style.left = Math.random() * 100 + "vw";
            heart.style.animationDuration = (Math.random() * 2 + 3) + "s";
            document.body.appendChild(heart);
            setTimeout(() => {
                heart.remove();
            }, 4000);
        }
        setInterval(createHeart, 800);
    </script>
</body>
</html>
'''

# Route to display the main page
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route to calculate love percentage
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    name1 = data.get('name1', '').strip()
    name2 = data.get('name2', '').strip()
    
    # Generate random love percentage between 70 and 100
    love_percentage = 100
    
    # Create result text
    result_text = f"{name1} ❤️ {name2}"
    
    message = "This was never meant to be random... it's always 100% 😙💖"
    
    return jsonify({
        'result_text': result_text,
        'percentage': love_percentage,
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
