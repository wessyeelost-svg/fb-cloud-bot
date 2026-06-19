import re
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Dashboard Interface Design (Premium Look)
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB CLOUD BOT</title>
    <script src="https://tailwindcss.com"></script>
</head>
<body class="bg-slate-900 min-h-screen flex items-center justify-center p-4">
    <div class="bg-slate-800 p-6 rounded-xl shadow-xl w-full max-w-md border border-slate-700">
        <h2 class="text-2xl font-bold text-center text-blue-500 mb-6">FB Cloud Bot v1.0</h2>
        <div class="mb-4">
            <label class="block text-slate-300 font-medium mb-2">Enter FB Cookie:</label>
            <textarea id="cookie" placeholder="datr=...; c_user=...; xs=..." class="w-full p-3 bg-slate-900 border border-slate-700 rounded text-slate-200 h-28 focus:outline-none focus:border-blue-500"></textarea>
        </div>
        <button onclick="startBot()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200">LAUNCH BOT</button>
        <div id="status" class="mt-4 p-3 bg-slate-900 border border-slate-700 rounded text-center text-slate-400 font-medium">Status: Waiting...</div>
    </div>
    <script>
        async function startBot() {
            const cookie = document.getElementById('cookie').value.trim();
            const status = document.getElementById('status');
            if(!cookie) { status.innerText = "Error: Paste cookie first!"; return; }
            status.innerText = "Processing on Cloud Server...";
            try {
                const res = await fetch('/api/react', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cookie: cookie })
                });
                const data = await res.json();
                status.innerText = data.message;
            } catch(e) { status.innerText = "Server Error!"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI)

@app.route('/api/react', methods=['POST'])
def auto_react():
    data = request.json or {}
    user_cookie = data.get("cookie", "").strip()
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36',
        'Cookie': user_cookie
    })
    
    try:
        response = session.get("https://facebook.com", timeout=12)
        if "logout.php" not in response.text and "mbasic_logout_button" not in response.text:
            return jsonify({"status": "error", "message": "Expired or Invalid Cookie!"})
        
        reaction_match = re.search(r'href="(/reactions/picker/\?[^"]+)"', response.text)
        if not reaction_match:
            return jsonify({"status": "success", "message": "Logged In Securely! No posts found."})
            
        picker_url = "https://facebook.com" + reaction_match.group(1).replace("&amp;", "&")
        picker_response = session.get(picker_url, timeout=12)
        
        like_action = re.search(r'href="(/ufi/reaction/\?[^"]+type=1[^"]+)"', picker_response.text)
        if like_action:
            final_target = "https://facebook.com" + like_action.group(1).replace("&amp;", "&")
            session.get(final_target, timeout=12)
            return jsonify({"status": "success", "message": "Success: 1 Post Liked on Cloud!"})
        
        return jsonify({"status": "error", "message": "FB Layout Changed or Post Already Liked."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run()
  
