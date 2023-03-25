import discord
from discord.ext import commands
from io import BytesIO
import base64

ROOMS = {
    'showroom':1089204451253944390,
    'general':1089185073296834612
}

TOKENS = [
    'TVRBNE9URTRPRGsyTnpFeU9USTVNamczTXcuR043SUZuLlJFdk1ueGJxX2VJRzJhSkNob25MeFBCVUhWM1o0dFlIT0pTSkdz'
]

decoded_TOKEN = base64.b64decode(TOKENS[0])

ATTACHMENTS = {

}

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    Channel = bot.get_channel(ROOMS['showroom'])

    async for message in Channel.history(limit=None):
        if message.attachments:
            for attachment in message.attachments:
                ATTACHMENTS[attachment.filename] = attachment.url

    print('Attachment IDs and URLs have been stored in the dictionary.')

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji
    if message.attachments:
        emoji_name = None

        if not emoji.is_unicode_emoji():
            emoji_name = emoji.name
        else:
            emoji_name = str(emoji)

        print(f'{payload.member} reacted with {emoji_name}')
        specific_channel_id = ROOMS['showroom']
        specific_channel = bot.get_channel(specific_channel_id)
        
        if message.attachments[0].filename not in ATTACHMENTS:

            attachment_data = await message.attachments[0].read()
            attachment_io = BytesIO(attachment_data)
            
            attachfile= discord.File(attachment_io, filename=message.attachments[0].filename)
            await specific_channel.send(f"[{payload.member}] Add a new photo to the Showroom. {emoji_name}:\n",file=attachfile)
            ATTACHMENTS[message.attachments[0].filename] = message.attachments[0].url

bot.run(decoded_TOKEN.decode('utf-8'))
