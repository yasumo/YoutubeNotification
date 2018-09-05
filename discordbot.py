import discord
import asyncio
import csv
import youtube
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.ERROR)

client = discord.Client()
check_channel_dict = dict()
server = None
DISCORD_INTERVAL = 5
YOUTUBE_INTERVAL = 10

token = os.environ['DISCORD_TOKEN']
server_id = os.environ['DISCORD_SERVER']


with open('./channellist.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    # skip header
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
        check_channel_dict[key]['discord_latest_msgs'] = await get_latest_messages(channel)
        await asyncio.sleep(DISCORD_INTERVAL)

    count = 0
    while True:
        print("loop count : ", str(count), " | ", datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        count += 1
        for key in check_channel_dict:
            # discordの最新メッセージ(キャッシュ)とyoutubeの最新動画URLを取得
            channel = check_channel_dict[key]['discord_channel']
            discord_latest_msgs = check_channel_dict[key]['discord_latest_msgs']
            logging.info("search youtube %s %s", key, check_channel_dict[key]['youtube_id'])
            url = youtube.search(check_channel_dict[key]['youtube_id'])
            await asyncio.sleep(YOUTUBE_INTERVAL)
            # discordの最新メッセージと、youtubeの最新動画URLが等しく無ければdiscordにpost
            need_post = True
            for msg in discord_latest_msgs:
                if msg == url:
                    need_post = False
                    break
            if need_post:
                logging.info("post_message %s", key)
                await post_message(channel, url)
                if len(check_channel_dict[key]['discord_latest_msgs']) > 4:
                    check_channel_dict[key]['discord_latest_msgs'].pop(-1)
                check_channel_dict[key]['discord_latest_msgs'].insert(0,url)


async def get_latest_messages(channel):
    ret_msgs = []
    async for message in client.logs_from(channel, limit=5):
        ret_msgs.append(message.content)
    return ret_msgs


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


