import logging
import os
from urllib.parse import urlparse

import discord
from discord import app_commands
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=ENV_PATH)
logging.basicConfig(level=logging.INFO)


def setting(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] == "(" and value[-1] == ")":
        value = value[1:-1].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1].strip()
    return value or None


TOKEN = setting("DISCORD_TOKEN")
GUILD_ID = setting("GUILD_ID")
MODERATOR_ROLE_ID = setting("MODERATOR_ROLE_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

mod_group = app_commands.Group(name="mod", description="Share Minecraft mod showcases")


@mod_group.command(name="upload", description="Post a Minecraft mod showcase")
@app_commands.describe(
    name="The name of the mod",
    minecraft_version="The Minecraft version supported by the mod",
    image="An image of the mod",
    download_link="A direct link to download the mod",
    category="The mod category, such as Technology or Adventure",
    tags="Optional comma-separated tags, up to five",
)
async def upload_mod(
    interaction: discord.Interaction,
    name: app_commands.Range[str, 1, 100],
    minecraft_version: app_commands.Range[str, 1, 32],
    image: discord.Attachment,
    download_link: str,
    category: app_commands.Range[str, 1, 50],
    tags: app_commands.Range[str, 1, 100] | None = None,
) -> None:
    try:
        moderator_role_id = int(MODERATOR_ROLE_ID or "")
    except ValueError:
        logging.error("MODERATOR_ROLE_ID is missing or invalid")
        await interaction.response.send_message(
            "Uploads are not configured. Ask a server administrator to set the moderator role.",
            ephemeral=True,
        )
        return

    if interaction.guild is None or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "Mod showcases can only be uploaded in a server.", ephemeral=True
        )
        return

    if not any(role.id == moderator_role_id for role in interaction.user.roles):
        await interaction.response.send_message(
            "You need the configured moderator role to upload mod showcases.",
            ephemeral=True,
        )
        return

    parsed_url = urlparse(download_link)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        await interaction.response.send_message(
            "Enter a valid download URL starting with http:// or https://.",
            ephemeral=True,
        )
        return

    if image.content_type is None or not image.content_type.startswith("image/"):
        await interaction.response.send_message(
            "The attached file must be an image.", ephemeral=True
        )
        return

    normalized_tags = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    if len(normalized_tags) > 5 or any(len(tag) > 24 for tag in normalized_tags):
        await interaction.response.send_message(
            "Provide up to five tags, with each tag 24 characters or fewer.",
            ephemeral=True,
        )
        return

    description = (
        f"**Minecraft version:** {minecraft_version}\n"
        f"**Category:** {category.strip()}\n"
        f"**Download:** [Download this mod]({download_link})"
    )
    if normalized_tags:
        description += "\n**Tags:** " + " · ".join(f"`{tag}`" for tag in normalized_tags)

    embed = discord.Embed(
        title=name,
        description=description,
        color=discord.Color.green(),
    )
    embed.set_image(url=image.url)
    embed.set_footer(text=f"Shared by {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)


tree.add_command(mod_group)


@client.event
async def on_ready() -> None:
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
        logging.info("Synced application commands to guild %s", GUILD_ID)
    else:
        await tree.sync()
        logging.info("Synced global application commands")
    logging.info("Logged in as %s", client.user)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set. Add it to your .env file.")
    client.run(TOKEN)
