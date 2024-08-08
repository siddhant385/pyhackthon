def create_html_content(system_info):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Pyhackthon</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        .terminal {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #0a0a0a;
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        }}
        h1 {{
            color: #00ff00;
            text-align: center;
            text-shadow: 0 0 10px #00ff00;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .highlight {{
            color: #ff6347;
        }}
        .command-box, .system-info {{
            background-color: #101010;
            border: 1px solid #00ff00;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
        }}
        .command-box p {{
            color: #1e90ff;
        }}
        .system-info pre {{
            white-space: pre-wrap;
            word-break: break-all;
            margin: 0;
            color: #00ff00;
        }}
        .system-info p {{
            color: #ff8c00;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        .blink {{
            animation: blink 1s steps(1, end) infinite;
            color: #ff4500;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        .prompt::before {{
            content: "$ ";
            color: #00ff00;
        }}
        .service {{
            color: #adff2f;
        }}
        .footer {{
            color: #32cd32;
        }}
    </style>
</head>
<body>
    <div class="terminal">
        <h1>💻 Welcome to <span class="highlight">Pyhackthon</span> 🐍</h1>
        <p class="prompt service">Hello, <span class="highlight">Pyhackthon</span> is at your service!</p>
        <div class="command-box">
            <p><strong>🔒 Please send cmd commands:</strong></p>
            <p class="prompt"><span class="highlight">If you don't know a command, send me</span> <code>:help</code></p>
        </div>
        <div class="system-info">
            <p><strong>📊 System Information:</strong></p>
            <pre>{system_info}</pre>
        </div>
        <p class="blink">⚠️ Secure connection established</p>
        <hr style="border-color: #00ff00;">
        <p class="footer">Yours faithfully,<br>Pyhackthon Team 🤖</p>
    </div>
</body>
</html>
    """
    return html_content


def shell(display):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shell Terminal</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: white;
            margin: 0;
            padding: 20px;
        }}
        .terminal {{
            max-width: 800px;
            margin: 0 auto;
            background-color: #0a0a0a;
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            overflow: hidden;
        }}
        .prompt {{
            display: flex;
            align-items: center;
            font-size: 1.2em;
        }}
        .prompt::before {{
            content: "$root# ";
            color: #00ff00;
        }}
        .display {{
            background-color: #101010;
            border: 1px solid #00ff00;
            border-radius: 5px;
            padding: 15px;
            color: #1e90ff;
            white-space: pre-wrap;
            word-break: break-all;
            margin-top: 20px;
        }}
        .prompt {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <div class="terminal">
        <p class="prompt">$root#Shell Results: </p>
        <div class="display">
{display}
        </div>
    </div>
</body>
</html>
    """
    return html_content






