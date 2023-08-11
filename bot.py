import discord
from discord.ext import commands, tasks
import json
import re
import struct
import urllib.request as urllib2

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    url = data["STREAMURL"]
    prefix = data["PREFIX"]
    bot_name = data["BOTNAME"]
    bot_description = data["BOTDESCRIPTION"]
    bot_website = data["WEBSITE"]

vol = 0.5

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

DANGER = 0xff0000
SUCCESS = 0x00d5ff

voice_channel = None
voice_client = None

@tasks.loop(seconds=10)
async def check_reconnect():
    global voice_channel, voice_client
    if voice_channel and voice_client and not voice_client.is_connected():
        print("Rejoining voice channel...")
        try:
            audiosource = discord.FFmpegPCMAudio(url)
            audiosource = discord.PCMVolumeTransformer(audiosource, vol)
            voice_client = await voice_channel.connect()
            voice_client.play(audiosource)
            print("Rejoined voice channel successfully!")
        except Exception as e:
            print(f"Failed to rejoin voice channel: {e}")

@client.event
async def on_ready():
    print("------------------------------------")
    print("Bot Name: " + client.user.name)
    print("Discord Version: " + discord.__version__)
    print("Bot Version: 1.0")
    print("Made By: YukioKoito https://github.com/OugiFormula")
    print("------------------------------------")
    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)
    await client.change_presence(activity=discord.Game(name=bot_name))

@client.event
async def on_voice_state_update(member, before, after):
    global voice_channel, voice_client

    if voice_channel and voice_client:
        # Check if the bot is the only member in the voice channel
        if len(voice_channel.members) == 1 and voice_channel.members[0] == client.user:
            print("Leaving empty voice channel...")
            await voice_client.disconnect()
            voice_channel = None
            voice_client = None
            print("Left empty voice channel.")
            return

encoding = 'utf-8'

def np():
    request = urllib2.Request(url, headers={'Icy-MetaData': 1})
    response = urllib2.urlopen(request)
    metaint = int(response.headers['icy-metaint'])
    for _ in range(10):
        response.read(metaint)
        metadata_length = struct.unpack('B', response.read(1))[0] * 16
        metadata = response.read(metadata_length).rstrip(b'\0')
        m = re.search(br"StreamTitle='([^']*)';", metadata)
        if m:
            title = m.group(1)
            if title:
                break
        else:
            print('no title found')
    songtitle = title.decode(encoding, errors='replace')
    return str(songtitle)

@client.tree.command(name="nowplaying", description="show the currently playing song")
async def nowplaying(interaction):
    songtitle = np()
    embed = discord.Embed(title="Now Playing:", description=str(songtitle), color=SUCCESS)
    embed.set_author(name=bot_name)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/823563186833063996/1122279275698081894/RDT_20230623_1641443370880576874776347.gif")
    embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJkMmxjbHF4MHFzbDA1eTV4Z3pzcXlzMm9nbjRoNzd1dHZwZDk5MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/dTVhr6QuWHSbGCT2co/giphy.gif")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="play", description="join the channel the user wants to play the radio")
async def play(interaction):
    global voice_channel, voice_client
    try:
        audiosource = discord.FFmpegPCMAudio(url)
    except Exception as e:
        print("ERROR: " + str(e))
        embed = discord.Embed(title="Unable to play radio", description=str(e), color=DANGER)
        await interaction.response.send_message(embed=embed)
        return

    audiosource = discord.PCMVolumeTransformer(audiosource, vol)

    user_state = interaction.user.voice
    if not user_state or not user_state.channel:
        embed = discord.Embed(title=bot_name, description="User not in a voice chat!", color=DANGER)
        await interaction.response.send_message(embed=embed)
        return

    voice_channel = interaction.user.voice.channel
    voice_client = await voice_channel.connect()

    voice_client.play(audiosource)
    songtitle = np()
    embed = discord.Embed(title="Now Playing!", description=songtitle, color=SUCCESS)
    embed.set_author(name=bot_name)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/823563186833063996/1122279275698081894/RDT_20230623_1641443370880576874776347.gif")
    embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWJkMmxjbHF4MHFzbDA1eTV4Z3pzcXlzMm9nbjRoNzd1dHZwZDk5MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/dTVhr6QuWHSbGCT2co/giphy.gif")
    await interaction.response.send_message(embed=embed)

    if not check_reconnect.is_running():
        check_reconnect.start()

@client.tree.command(name="leave", description="leave the voice chat")
async def leave(interaction):
    global voice_channel, voice_client
    voice_client = interaction.guild.voice_client

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        voice_channel = None
        voice_client = None

        embed = discord.Embed(title=bot_name, description="Left the voice chat", color=SUCCESS)
        embed.set_image(url="https://i.imgur.com/0kVHOMh.gif")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=bot_name, description="The bot isn't in a voice channel!", color=DANGER)
        embed.set_image(url="https://i.imgur.com/0kVHOMh.gif")
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="about", description="information about the bot")
async def about(interaction):
    guild_count = len(client.guilds)
    embed = discord.Embed(title="The ultimate Radio Discord Bot.", description=bot_description, color=SUCCESS)
    embed.add_field(name="Guild Count", value=guild_count)
    embed.set_author(name=bot_name, url=bot_website)
    #Change the image to the radio logo image, I set it for now to a image of a funny cat
    embed.set_image(url="https://i.pinimg.com/280x280_RS/06/6e/33/066e339604d9890200fa15817246e48b.jpg")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="help", description="list of all commands")
async def help(interaction):
    embed = discord.Embed(title=f"{bot_name} Help", description="Here are the available commands:", color=SUCCESS)
    embed.add_field(name="!play", value="Play the radio on a specific voice channel.", inline=False)
    embed.add_field(name="!leave", value="Disconnect from the voice channel.", inline=False)
    embed.add_field(name="!about", value="Display information about the bot.", inline=False)
    embed.add_field(name="!help", value="Display this help message.", inline=False)
    embed.set_image(url="https://i.imgur.com/0kVHOMh.gif")
    await interaction.response.send_message(embed=embed)

client.run(token)
