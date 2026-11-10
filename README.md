# Discord Mod Showcase Bot

Mod Showcase Bot is a Discord bot for publishing Minecraft mod showcases with slash commands. Server members with a configured moderator role can post a mod’s name, Minecraft version, category, image attachment, download link, and up to five tags in an embed.

## Install

1. Create a Discord application and bot in the Discord Developer Portal, then invite the bot to your server with permission to use application commands and send messages.
2. Install Python 3.10 or newer.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` and `MODERATOR_ROLE_ID`. Optionally set `GUILD_ID` to sync commands to one server during development.
5. Start the bot:
   ```bash
   python main.py
   ```

## Use

1. Give the configured moderator role to members who should be allowed to upload showcases.
2. In a server, run `/mod upload`.
3. Enter the mod name, Minecraft version, download link, and category, and attach an image. Optionally provide up to five comma-separated tags.
4. Submit the command to post the showcase embed.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/e64c8689-ff9c-45ba-b17c-2ce066a7d528?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=e64c8689-ff9c-45ba-b17c-2ce066a7d528
