# guardian
Discord Security Moderation Bot
A powerful Discord moderation bot that provides comprehensive message logging and file security scanning to protect your server from malicious content.
🔒 Features
Message Logging

Logs all user messages with timestamps
Tracks message content, user information, and channels
Stores logs in a dedicated Discord channel

File Security Scanning

Automatic file downloads for analysis
File type detection using MIME type verification
Extension validation to detect disguised executables
SHA-256 hashing for file fingerprinting
Size limit enforcement (default 50MB)
Suspicious file alerts with @here notifications

Security Detection

Identifies potentially dangerous file extensions (.exe, .bat, .cmd, .scr, .vbs, etc.)
Detects MIME type mismatches (e.g., .jpg files that are actually executables)
Real-time alerts for suspicious uploads
Preserves uploaded files for forensic analysis

Admin Commands

!setlog #channel - Set the logging channel
!checkuser @user - View user statistics and information

📋 Requirements

Python 3.8 or higher
Discord Bot Token with proper intents enabled

🚀 Installation

Clone the repository

bash git clone https://github.com/michaelrayfire/guardian.git
cd discord-security-bot

Install dependencies

bash pip install -r requirements.txt

Create a Discord Bot

Go to Discord Developer Portal
Create a new application
Go to the "Bot" section and create a bot
Enable Message Content Intent under Privileged Gateway Intents
Copy your bot token


Configure the bot

Open mod_bot.py
Replace YOUR_BOT_TOKEN_HERE with your bot token
Replace LOG_CHANNEL_ID with your logging channel ID


Invite the bot to your server

Go to OAuth2 → URL Generator
Select scopes: bot
Select permissions: Read Messages, Send Messages, Embed Links, Attach Files, Read Message History, Mention Everyone
Use the generated URL to invite the bot



💻 Usage

Start the bot

bash python mod_bot.py

Set up logging channel

!setlog #your-log-channel

The bot will automatically:

Log all messages to the designated channel
Scan file uploads for security threats
Alert moderators of suspicious activity



⚙️ Configuration
You can customize these settings in mod_bot.py:
pythonLOG_CHANNEL_ID = 123456789  # Your log channel ID
MAX_FILE_SIZE = 50 * 1024 * 1024  # Maximum file size (50MB)
SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.jar', '.app']
SCAN_DIR = './scanned_files'  # Directory for storing scanned files
📁 Project Structure
discord-security-bot/
├── mod_bot.py          # Main bot script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── scanned_files/     # Folder for downloaded files (created automatically)
🛡️ Security Features Explained
File Type Verification
The bot uses python-magic to detect the true file type, preventing attackers from disguising malicious files with fake extensions.
Hash Fingerprinting
SHA-256 hashes allow you to identify known malicious files and track file distributions across your server.
Persistent Storage
All scanned files are saved locally for evidence and further analysis if needed.
⚠️ Important Notes

The bot requires Message Content Intent to be enabled in the Discord Developer Portal
Scanned files are stored in ./scanned_files/ - manage disk space accordingly
This bot logs ALL messages - ensure compliance with your server's privacy policy
Administrator permissions are required for setup commands

🤝 Contributing
Contributions are welcome! Feel free to:

Report bugs
Suggest new features
Submit pull requests

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🔗 Links

Discord.py Documentation
Discord Developer Portal

⚡ Future Enhancements

 VirusTotal API integration
 URL scanning and phishing detection
 Database integration for persistent logging
 User reputation system
 Automatic message deletion for threats
 Customizable alert thresholds
 Multi-language support


Protect your Discord server with automated security monitoring! 🛡️
