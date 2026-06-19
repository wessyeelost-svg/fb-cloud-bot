import re
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Part 1: Branded Dashboard UI Code
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB CLOUD BOT - Cx Munna</title>
    <script src="https://tailwindcss.com"></script>
</head>
<body class="bg-slate-950 min-h-screen flex items-center justify-center p-4 selection:bg-blue-500 selection:text-white">
    
    <div class="bg-slate-900 p-6 rounded-2xl shadow-2xl w-full max-w-md border border-slate-800 relative overflow-hidden">
        <!-- Neon Ambient Glow -->
        <div class="absolute -top-10 -right-10 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl"></div>

        <!-- Header Branding & Embedded SVG Vector Logo -->
        <div class="flex flex-col items-center mb-5 border-b border-slate-800/60 pb-4">
            <div class="w-14 h-14 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20 mb-3 transform hover:rotate-6 transition duration-300">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://w3.org">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 002-2H5a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                </svg>
            </div>
            
            <div class="flex items-center gap-2">
                <div id="live-indicator" class="w-2.5 h-2.5 bg-slate-500 rounded-full"></div>
                <h2 class="text-2xl font-black tracking-tight text-white">FB Cloud Controller</h2>
            </div>
            <p class="text-[10px] text-cyan-400 font-bold uppercase tracking-wider mt-1">Powered by Cx Munna</p>
        </div>
        
        <!-- Interactive Form Fields Inputs -->
        <div class="mb-3">
            <label class="block text-slate-400 text-xs font-semibold mb-1">Session Cookie Array:</label>
            <textarea id="cookie" placeholder="Paste target session profile cookies here..." class="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 h-16 text-xs focus:outline-none focus:border-blue-500 transition font-mono"></textarea>
        </div>

        <div class="mb-3">
            <label class="block text-slate-400 text-xs font-semibold mb-1">Select Reaction Type:</label>
            <select id="react-type" class="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-xs focus:outline-none focus:border-blue-500 transition">
                <option value="1">Like 👍</option>
                <option value="2">Love ❤️</option>
                <option value="16">Care 🥳</option>
                <option value="4">Haha 😂</option>
                <option value="8">Wow 😮</option>
                <option value="32">Sad 😢</option>
            </select>
        </div>

        <div class="mb-3">
            <label class="block text-slate-400 text-xs font-semibold mb-1">Custom Commentary Text:</label>
            <input id="comment-text" type="text" placeholder="e.g. Awesome click! 🔥 (Keep blank for reaction only)" class="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-xs focus:outline-none focus:border-blue-500 transition">
        </div>

        <div class="grid grid-cols-2 gap-2 mb-4">
            <div>
                <label class="block text-slate-400 text-xs font-semibold mb-1">Interval Window (Sec):</label>
                <input id="delay-input" type="number" value="25" min="10" class="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 text-xs focus:outline-none focus:border-blue-500 transition font-mono">
            </div>
            <div class="flex items-end">
                <button id="action-btn" onclick="toggleBot()" class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white font-bold py-2.5 rounded-xl text-xs transition shadow-md shadow-blue-500/10 active:scale-95">
                    LAUNCH ENGINE
                </button>
            </div>
        </div>

        <!-- Realtime Output Console Box -->
        <div class="text-xs text-slate-400 font-semibold mb-1">Live Pipeline Terminal:</div>
        <div id="log-box" class="h-28 bg-slate-950 border border-slate-800 rounded-xl p-3 text-[10px] font-mono overflow-y-auto text-green-400 space-y-1">
            <div class="text-slate-600">[system] Core micro-architecture initialized. Standby for authorization token.</div>
        </div>

        <!-- Footer Bottom Branding -->
        <div class="text-center text-[10px] text-slate-600 font-medium mt-4 pt-3 border-t border-slate-800/40">
            Engine Framework v3.5 &copy; 2026 | <span class="text-slate-500 font-bold">Cx Munna</span>
        </div>
    </div>

    <!-- Active Frontend Scripts Looping Control -->
    <script>
        let botInterval = null;
        let isRunning = false;

        function addLog(text, type="info") {
            const logBox = document.getElementById('log-box');
            const newLog = document.createElement('div');
            let color = "text-green-400";
            if (type === "error") color = "text-red-400";
            if (type === "system") color = "text-blue-400 font-bold";
            
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
                addLog("Execution Aborted: Missing required token metadata payload.", "error"); 
                return; 
            }

            let sec = parseInt(delayInput) || 25;
            if (sec < 10) sec = 10;

            if (isRunning) {
                clearInterval(botInterval);
                isRunning = false;
                btn.innerText = "LAUNCH ENGINE";
                btn.className = "w-full bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-bold py-2.5 rounded-xl text-xs transition";
                indicator.className = "w-2.5 h-2.5 bg-slate-500 rounded-full";
                addLog("Supervisor runtime thread terminated.", "system");
            } else {
                isRunning = true;
                btn.innerText = "HALT ENGINE";
                btn.className = "w-full bg-gradient-to-r from-red-600 to-rose-500 text-white font-bold py-2.5 rounded-xl text-xs transition";
                indicator.className = "w-2.5 h-2.5 bg-green-500 rounded-full animate-pulse shadow-md shadow-green-500/50";
                
                addLog(`Automation loop bound to target socket. Refresh sync: ${sec}s.`, "system");
                triggerCloudEngine(cookie, reactType, commentText);

                botInterval = setInterval(() => {
                    triggerCloudEngine(cookie, reactType, commentText);
                }, sec * 1000);
            }
        }

        async function triggerCloudEngine(cookie, reactType, commentText) {
            addLog("Parsing downstream matrix data layers...");
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
                addLog("Network pipeline timeout. Retrying packet connection...", "error"); 
            }
        }
    </script>
</body>
</html>
"""
# Part 2: Python Flask Multi-Reaction API Backend
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
        # Check active session token states safely
        response = session.get("https://facebook.com", timeout=12)
        if "logout.php" not in response.text and "mbasic_logout_button" not in response.text:
            return jsonify({"status": "error", "message": "Expired or Invalid Cookie Token Session!"})
        
        # Scrape available targets links inside timeline tree layout
        reaction_links = re.findall(r'href="(/reactions/picker/\?[^"]+)"', response.text)
        if not reaction_links:
            return jsonify({"status": "success", "message": "Timeline buffer parsed empty. No actions required."})
            
        picker_url = "https://facebook.com" + reaction_links[0].replace("&amp;", "&")
        picker_response = session.get(picker_url, timeout=12)
        
        # Extract targeted reaction node reference
        target_pattern = f'href="(/ufi/reaction/\\?[^"]+type={react_type}[^"]+)"'
        like_action = re.search(target_pattern, picker_response.text)
        
        action_msg = "Reaction deployed successfully!"

        if like_action:
            final_target = "https://facebook.com" + like_action.group(1).replace("&amp;", "&")
            session.get(final_target, timeout=12) # Fire reaction package update
        else:
            action_msg = "Post already had targeted reaction structure."

        # Commentary form routing handler
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
                session.post(comment_url, data=payload, timeout=12) # Fire commentary bundle post packet
                action_msg += " + Comment delivered securely."

        return jsonify({"status": "success", "message": f"Success: {action_msg}"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Pipeline exception fault: {str(e)}"})

if __name__ == '__main__':
    app.run()
        
