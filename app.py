import re
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB CLOUD BOT ULTIMATE</title>
    <script src="https://tailwindcss.com"></script>
</head>
<body class="bg-slate-900 min-h-screen flex items-center justify-center p-4">
    <div class="bg-slate-800 p-6 rounded-xl shadow-xl w-full max-w-md border border-slate-700">
        
        <div class="flex items-center justify-center gap-2 mb-2">
            <div id="live-indicator" class="w-3 h-3 bg-gray-500 rounded-full"></div>
            <h2 class="text-2xl font-bold text-center text-blue-500">FB Cloud Controller v3.0</h2>
        </div>
        <p class="text-[10px] text-slate-400 text-center mb-5">Advanced Multi-Reaction & Custom Comment Framework</p>
        
        <div class="mb-3">
            <label class="block text-slate-300 text-xs font-medium mb-1">Session Cookie:</label>
            <textarea id="cookie" placeholder="Paste target profile cookies here..." class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-slate-200 h-16 text-xs focus:outline-none focus:border-blue-500 font-mono"></textarea>
        </div>

        <div class="mb-3">
            <label class="block text-slate-300 text-xs font-medium mb-1">Select Reaction Type:</label>
            <select id="react-type" class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-slate-200 text-xs focus:outline-none focus:border-blue-500">
                <option value="1">Like 👍</option>
                <option value="2">Love ❤️</option>
                <option value="16">Care 🥳</option>
                <option value="4">Haha 😂</option>
                <option value="8">Wow 😮</option>
                <option value="32">Sad 😢</option>
            </select>
        </div>

        <div class="mb-3">
            <label class="block text-slate-300 text-xs font-medium mb-1">Custom Comment Text:</label>
            <input id="comment-text" type="text" placeholder="e.g. Beautiful click! 🔥 (Keep empty for reaction only)" class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-slate-200 text-xs focus:outline-none focus:border-blue-500">
        </div>

        <div class="grid grid-cols-2 gap-2 mb-4">
            <div>
                <label class="block text-slate-300 text-xs font-medium mb-1">Interval Delay (Sec):</label>
                <input id="delay-input" type="number" value="25" min="10" class="w-full p-2 bg-slate-900 border border-slate-700 rounded text-slate-200 text-xs focus:outline-none focus:border-blue-500">
            </div>
            <div class="flex items-end">
                <button id="action-btn" onclick="toggleBot()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded text-xs transition duration-200">
                    LAUNCH ENGINE
                </button>
            </div>
        </div>

        <div class="text-xs text-slate-400 font-medium mb-1">Live Automation Logs:</div>
        <div id="log-box" class="h-28 bg-slate-900 border border-slate-700 rounded p-2 text-[10px] font-mono overflow-y-auto text-green-400 space-y-1">
            <div class="text-slate-500">[system] Cloud environment ready... awaiting launch authorization.</div>
        </div>
    </div>

    <script>
        let botInterval = null;
        let isRunning = false;

        function addLog(text, type="info") {
            const logBox = document.getElementById('log-box');
            const newLog = document.createElement('div');
            let color = "text-green-400";
            if (type === "error") color = "text-red-400";
            if (type === "system") color = "text-blue-400";
            
            newLog.className = color;
            newLog.innerText = `[${new Date().toLocaleTimeString()}] ${text}`;
            logBox.appendChild(newLog);
            logBox.scrollTop = logBox.scrollHeight;
        }

        function toggleBot() {
            const cookie = document.getElementById('cookie').value.trim();
            const reactType = document.getElementById('react-type').value;
            const commentText = document.getElementById('comment-text').value.trim();
            const delayInput = document.getElementById('delay-input').value.trim();
            const btn = document.getElementById('action-btn');
            const indicator = document.getElementById('live-indicator');

            if (!cookie) { 
                addLog("Execution Aborted: Missing profile cookie payload.", "error"); 
                return; 
            }

            let sec = parseInt(delayInput) || 25;
            if (sec < 10) sec = 10;

            if (isRunning) {
                clearInterval(botInterval);
                isRunning = false;
                btn.innerText = "LAUNCH ENGINE";
                btn.className = "w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded text-xs transition";
                indicator.className = "w-3 h-3 bg-gray-500 rounded-full";
                addLog("Automation supervisor loop halted.", "system");
            } else {
                isRunning = true;
                btn.innerText = "STOP ENGINE";
                btn.className = "w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 rounded text-xs transition";
                indicator.className = "w-3 h-3 bg-green-500 rounded-full animate-pulse";
                
                addLog(`Engine synchronized. Active loop target window: ${sec} seconds.`, "system");
                
                triggerCloudEngine(cookie, reactType, commentText);

                botInterval = setInterval(() => {
                    triggerCloudEngine(cookie, reactType, commentText);
                }, sec * 1000);
            }
        }

        async function triggerCloudEngine(cookie, reactType, commentText) {
            addLog("Scanning active target timeline elements...");
            try {
                const res = await fetch('/api/react', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cookie: cookie, react_type: reactType, comment: commentText })
                });
                const data = await res.json();
                
                if (data.status === "success") {
                    addLog(data.message, "info");
                } else {
                    addLog(data.message, "error");
                    if(data.message.includes("Expired")) toggleBot();
                }
            } catch(e) { 
                addLog("Network timeout. Retrying socket pipe line...", "error"); 
            }
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
    react_type = data.get("react_type", "1")
    comment_text = data.get("comment", "").strip()
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36',
        'Cookie': user_cookie
    })
    
    try:
        response = session.get("https://facebook.com", timeout=12)
        if "logout.php" not in response.text and "mbasic_logout_button" not in response.text:
            return jsonify({"status": "error", "message": "Expired or Invalid Cookie Token Session!"})
        
        reaction_links = re.findall(r'href="(/reactions/picker/\?[^"]+)"', response.text)
        if not reaction_links:
            return jsonify({"status": "success", "message": "Timeline buffer parsed empty. No actions required."})
            
        picker_url = "https://facebook.com" + reaction_links[0].replace("&amp;", "&")
        picker_response = session.get(picker_url, timeout=12)
        
        target_pattern = f'href="(/ufi/reaction/\\?[^"]+type={react_type}[^"]+)"'
        like_action = re.search(target_pattern, picker_response.text)
        
        action_msg = "Reaction deployed successfully!"

        if like_action:
            final_target = "https://facebook.com" + like_action.group(1).replace("&amp;", "&")
            session.get(final_target, timeout=12)
        else:
            action_msg = "Post already had targeted reaction."

        if comment_text:
            comment_form = re.search(r'action="(/a/comment\.php\?[^"]+)"', picker_response.text) or re.search(r'action="(/a/comment\.php\?[^"]+)"', response.text)
            fb_dtsg = re.search(r'name="fb_dtsg" value="([^"]+)"', response.text) or re.search(r'name="fb_dtsg" value="([^"]+)"', picker_response.text)
            jazoest = re.search(r'name="jazoest" value="([^"]+)"', response.text) or re.search(r'name="jazoest" value="([^"]+)"', picker_response.text)

            if comment_form and fb_dtsg and jazoest:
                comment_url = "https://facebook.com" + comment_form.group(1).replace("&amp;", "&")
                payload = {
                    'fb_dtsg': fb_dtsg.group(1),
                    'jazoest': jazoest.group(1),
                    'comment_text': comment_text
                }
                session.post(comment_url, data=payload, timeout=12)
                action_msg += " + Comment delivered securely."

        return jsonify({"status": "success", "message": f"Success: {action_msg}"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Pipeline exception fault: {str(e)}"})

if __name__ == '__main__':
    app.run()
                
