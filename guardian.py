import discord
from discord.ext import commands
import aiohttp
import hashlib
import magic
import os
from datetime import datetime
import json

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
LOG_CHANNEL_ID = 123456789  # Replace with your log channel ID
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
SUSPICIOUS_EXTENSIONS = ['.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.jar', '.app']
SCAN_DIR = './scanned_files'

# Create scan directory
os.makedirs(SCAN_DIR, exist_ok=True)

@bot.event
async def on_ready():
    print(f'{bot.user} is online and monitoring!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Log all messages
    await log_message(message)
    
    # Check for attachments
    if message.attachments:
        await scan_attachments(message)
    
    await bot.process_commands(message)

async def log_message(message):
    """Log user messages to a dedicated channel"""
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return
    
    embed = discord.Embed(
        title="Message Log",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{message.author} ({message.author.id})", inline=False)
    embed.add_field(name="Channel", value=f"#{message.channel.name}", inline=False)
    embed.add_field(name="Content", value=message.content[:1024] or "*No text content*", inline=False)
    
    if message.attachments:
        files = "\n".join([f"- {att.filename}" for att in message.attachments])
        embed.add_field(name="Attachments", value=files, inline=False)
    
    await log_channel.send(embed=embed)

async def scan_attachments(message):
    """Download and examine file attachments"""
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    
    for attachment in message.attachments:
        # Check file size
        if attachment.size > MAX_FILE_SIZE:
            await alert_suspicious(message, attachment, "File exceeds size limit")
            continue
        
        # Check extension
        ext = os.path.splitext(attachment.filename)[1].lower()
        is_suspicious = ext in SUSPICIOUS_EXTENSIONS
        
        try:
            # Download file
            file_path = os.path.join(SCAN_DIR, f"{message.id}_{attachment.filename}")
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        with open(file_path, 'wb') as f:
                            f.write(data)
            
            # Calculate hash
            file_hash = hashlib.sha256(data).hexdigest()
            
            # Detect MIME type
            mime = magic.from_file(file_path, mime=True)
            
            # Check for mismatched extension/MIME type
            if ext and not mime.startswith('application/octet-stream'):
                if (ext in ['.jpg', '.jpeg', '.png', '.gif'] and not mime.startswith('image')) or \
                   (ext in ['.pdf'] and mime != 'application/pdf') or \
                   (ext in ['.txt'] and not mime.startswith('text')):
                    is_suspicious = True
            
            # Log scan results
            embed = discord.Embed(
                title="🔍 File Scan Report",
                color=discord.Color.orange() if is_suspicious else discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="File", value=attachment.filename, inline=False)
            embed.add_field(name="User", value=f"{message.author} ({message.author.id})", inline=False)
            embed.add_field(name="Size", value=f"{attachment.size:,} bytes", inline=True)
            embed.add_field(name="MIME Type", value=mime, inline=True)
            embed.add_field(name="SHA-256", value=file_hash[:32] + "...", inline=False)
            embed.add_field(name="Status", value="⚠️ SUSPICIOUS" if is_suspicious else "✅ Clean", inline=False)
            
            if log_channel:
                await log_channel.send(embed=embed)
            
            # Alert if suspicious
            if is_suspicious:
                await alert_suspicious(message, attachment, "Suspicious file type or mismatch detected")
            
            # Clean up (optional - keep for evidence or delete)
            # os.remove(file_path)
            
        except Exception as e:
            print(f"Error scanning file: {e}")
            if log_channel:
                await log_channel.send(f"⚠️ Error scanning {attachment.filename}: {str(e)}")

async def alert_suspicious(message, attachment, reason):
    """Send alert for suspicious files"""
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return
    
    embed = discord.Embed(
        title="🚨 SECURITY ALERT",
        description=reason,
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="File", value=attachment.filename, inline=False)
    embed.add_field(name="Uploaded by", value=f"{message.author.mention} ({message.author.id})", inline=False)
    embed.add_field(name="Channel", value=message.channel.mention, inline=False)
    embed.add_field(name="Message Link", value=f"[Jump to message]({message.jump_url})", inline=False)
    
    await log_channel.send(content="@here", embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel: discord.TextChannel):
    """Set the logging channel"""
    global LOG_CHANNEL_ID
    LOG_CHANNEL_ID = channel.id
    await ctx.send(f"✅ Logging channel set to {channel.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def checkuser(ctx, user: discord.Member):
    """Get message statistics for a user"""
    # This would require a database for full functionality
    embed = discord.Embed(
        title=f"User Info: {user}",
        color=discord.Color.blue()
    )
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Joined", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=", ".join([r.name for r in user.roles[1:]]) or "None", inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
bot.run('YOUR_BOT_TOKEN_HERE')