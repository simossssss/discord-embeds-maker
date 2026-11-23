import discord
from discord.ext import commands, tasks
from pathlib import Path
from datetime import datetime

#main variable
root=Path.cwd()
items=Path().iterdir()
with open("bot_token","r") as f:
    token=f.read()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
channelId = #YOUR CHANNEL ID HERE

#for debugging
def list_dir():
    for _ in items:
        if _.is_dir():
            print(_," dir")
        else:
            print(_," file")

#<---- discord bot from now on ---->

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    synced = await bot.tree.sync()
    print(f"Logged in as {bot.user} | Synced {len(synced)} slash command(s)")

    if not announcement.is_running():
        announcement.start()
    
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! ({round(bot.latency * 1000)} ms)")

@tasks.loop(minutes=1)
async def announcement():
    if Path("./count").is_file():
        with open("count", "r") as f:
            count=int(f.readline())
        with open("countCurrent", "r") as f:
            countCurrent=int(f.readline())

        if count != countCurrent:
            while countCurrent < count:
                embedFlag = False
                title, description, timestamp, color = "", "", None, None
                thumbnail, image, footer, author = None, None, None, None
                countCurrent += 1
                ann_dir = Path(f"./ann/{countCurrent}-announcement")

                if (ann_dir / "Title").is_file():
                    with open(ann_dir / "Title") as f:
                        title = f.readline().strip()
                        embedFlag = True

                if (ann_dir / "Description").is_file():
                    with open(ann_dir / "Description") as f:
                        description = f.read().strip()
                        embedFlag = True

                if (ann_dir / "Thumbnail").is_file():
                    with open(ann_dir / "Thumbnail") as f:
                        thumbnail = f.readline().strip()

                if (ann_dir / "Color").is_file():
                    with open(ann_dir / "Color", encoding="utf-8") as f:
                        color_raw = f.readline().strip().lstrip("#").removeprefix("0x")
                    try:
                        color = int(color_raw, 16)
                        embedFlag = True
                    except ValueError:
                        color = None

                fieldNames, fieldBodies, fieldInlines = [], [], []
                if (ann_dir / "FieldCount").is_file():
                    with open(ann_dir / "FieldCount") as f:
                        fieldCount = int(f.readline().strip())

                    for i in range(fieldCount):
                        if (ann_dir / f"{i}-FieldName").is_file():
                            with open(ann_dir / f"{i}-FieldName", "r") as f:
                                fieldNames.append(f.readline().strip())

                        if (ann_dir / f"{i}-FieldBody").is_file():
                            with open(ann_dir / f"{i}-FieldBody", "r") as f:
                                fieldBodies.append(f.read().strip())

                        if (ann_dir / f"{i}-FieldInline").is_file():
                            with open(ann_dir / f"{i}-FieldInline", "r") as f:
                                fieldInlines.append(f.readline().strip().lower() == "true")

                if (ann_dir / "Image").is_file():
                    with open(ann_dir / "Image") as f:
                        image = f.readline().strip()

                if (ann_dir / "Footer").is_file():
                    with open(ann_dir / "Footer") as f:
                        footer = f.readline().strip()

                if (ann_dir / "Author").is_file():
                    with open(ann_dir / "Author") as f:
                        author = f.readline().strip()

                if (ann_dir / "Timestamp").is_file():
                    with open(ann_dir / "Timestamp") as f:
                        ts_str = f.readline().strip()
                        timestamp = datetime.fromisoformat(ts_str) if ts_str else None
                        embedFlag = True

                if embedFlag:
                    embed = discord.Embed(
                        title=title,
                        description=description,
                        timestamp=timestamp,
                        color=color,
                    )
                    
                    if thumbnail:
                        embed.set_thumbnail(url=thumbnail)
                    if image:
                        embed.set_image(url=image)
                    if footer:
                        embed.set_footer(text=footer)
                    if author:
                        embed.set_author(name=author)

                    for name, body, inline in zip(fieldNames, fieldBodies, fieldInlines):
                        embed.add_field(name=name, value=body, inline=inline)

                    await bot.get_channel(channelId).send(embed=embed)
        with open("countCurrent", "w") as f:
            f.write(str(count))
    else:
        print("no announcement files exist")
        

@announcement.before_loop
async def before_announcement():
    await bot.wait_until_ready()

if __name__=="__main__":
    bot.run(token)
