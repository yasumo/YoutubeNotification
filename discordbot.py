import discord
import asyncio
import configparser
import time
import csv
import youtube

client = discord.Client()
check_channel_dict = dict()
server = None

inifile = configparser.ConfigParser()
inifile.read('./settings.ini', 'UTF-8')
token = inifile.get('Discord', 'token')
server_id = inifile.get('Discord', 'server')


with open('./channellist.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    #skip header
    header = next(reader)
    for row in reader:
        check_channel_dict[row[0]] = {'youtube_id': row[1]}

@client.event
async def on_ready():
    global server, server_id
    server = client.get_server(str(server_id))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    discord_channels = client.get_all_channels()
    for channel in discord_channels:
        if channel.name in check_channel_dict:
            channel = client.get_channel(channel.id)
            check_channel_dict[channel.name]['discord_channel'] = channel

    while True:
        for key in check_channel_dict:
            # discordにチャンネルがない場合は作成
            if 'discord_channel' not in check_channel_dict[key]:
                check_channel_dict[key]['discord_channel'] = await create_channel(key)
                await asyncio.sleep(5)
            channel = check_channel_dict[key]['discord_channel']
            latest = await get_latest_message(channel)
            url = youtube.search(check_channel_dict[key]['youtube_id'])

            if latest != url:
                await post_message(channel, url)
                await asyncio.sleep(5)
        await asyncio.sleep(60)


async def get_latest_message(channel):
    async for message in client.logs_from(channel, limit=1):
        return message.content
    return 'none'


async def create_channel(channel_name):
    print("create channel");
    print(channel_name);
    return await client.create_channel(server, channel_name, type=discord.ChannelType.text)


@client.event
async def on_message(message):
    if message.content.startswith('/neko'):
        reply = 'にゃーん'
        await client.send_message(message.channel, reply)


async def post_message(channel,url):
    print('post_message')
    print(url)
    await client.send_message(channel, url)


client.run(token)


