import discord
import asyncio
import configparser
import time
import csv
import youtube
import logging
from datetime import datetime

logging.basicConfig(level=logging.ERROR)

client = discord.Client()
check_channel_dict = dict()
server = None
DISCORD_INTERVAL = 5
YOUTUBE_INTERVAL = 15

ini_file = configparser.ConfigParser()
ini_file.read('./settings.ini', 'UTF-8')
token = ini_file.get('Discord', 'token')
server_id = ini_file.get('Discord', 'server')


with open('./channellist.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    #skip header
    header = next(reader)
    for row in reader:
        check_channel_dict[row[0].lower()] = {'youtube_id': row[1]}

@client.event
async def on_ready():
    global server, server_id
    server = client.get_server(str(server_id))
    print('Logged in as ', client.user.name, client.user.id)
    print('------')
    discord_channels = client.get_all_channels()
    for channel in discord_channels:
        if channel.name in check_channel_dict:
            channel = client.get_channel(channel.id)
            check_channel_dict[channel.name]['discord_channel'] = channel

    for key in check_channel_dict:
        # discordにチャンネルがない場合は作成
        print("get discord channel info", key)
        if 'discord_channel' not in check_channel_dict[key]:
            check_channel_dict[key]['discord_channel'] = await create_channel(key)
        # discordの該当チャンネルに投稿してある最新メッセージをキャッシュ
        channel = check_channel_dict[key]['discord_channel']
        check_channel_dict[key]['discord_latest_msg'] = await get_latest_message(channel)
        await asyncio.sleep(DISCORD_INTERVAL)

    count = 0
    while True:
        print("loop count : ", str(count), " | ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        count += 1
        for key in check_channel_dict:
            # discordの最新メッセージ(キャッシュ)とyoutubeの最新動画URLを取得
            channel = check_channel_dict[key]['discord_channel']
            discord_latest_msg = check_channel_dict[key]['discord_latest_msg']
            logging.info("search youtube %s %s", key, check_channel_dict[key]['youtube_id'])
            url = youtube.search(check_channel_dict[key]['youtube_id'])
            # discordの最新メッセージと、youtubeの最新動画URLが等しく無ければdiscordにpost
            if discord_latest_msg != url:
                logging.info("post_message %s", key)
                await post_message(channel, url)
                check_channel_dict[key]['discord_latest_msg'] = url
            await asyncio.sleep(YOUTUBE_INTERVAL)


async def get_latest_message(channel):
    async for message in client.logs_from(channel, limit=1):
        return message.content
    return 'none'


async def create_channel(channel_name):
    print("create channel", channel_name);
    return await client.create_channel(server, channel_name, type=discord.ChannelType.text)


@client.event
async def on_message(message):
    if message.content.startswith('/neko'):
        reply = 'にゃーん'
        await client.send_message(message.channel, reply)


async def post_message(channel,msg):
    print('post_message ', msg)
    await client.send_message(channel, msg)


client.run(token)


