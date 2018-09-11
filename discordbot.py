import discord
import asyncio
import csv
import youtube
import logging
from datetime import datetime
import os
import traceback

logging.basicConfig(level=logging.ERROR)

client = discord.Client()
server = None
DISCORD_INTERVAL = 5
YOUTUBE_INTERVAL = 9
ERROR_INTERVAL = 60
DISCORD_CACHE_LIMIT = 20

TOKEN = os.environ['DISCORD_TOKEN']
SERVER_ID = os.environ['DISCORD_SERVER']


@client.event
async def on_ready():
    global server
    check_channel_dict = get_channel_dict()
    server = client.get_server(str(SERVER_ID))
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
            # url = youtube.search(check_channel_dict[key]['youtube_id'])
            url_list = await get_latest_url(check_channel_dict[key]['youtube_id'])
            await asyncio.sleep(YOUTUBE_INTERVAL)
            # discordの最新メッセージと、youtubeの最新動画URLが等しく無ければdiscordにpost
            for url in url_list:
                need_post = True
                if url in discord_latest_msgs:
                    need_post = False
                if need_post:
                    logging.info("post_message %s", key)
                    await post_message(channel, url)
                    check_channel_dict[key]['discord_latest_msgs'].insert(0, url)
            check_channel_dict[key]['discord_latest_msgs'] = check_channel_dict[key]['discord_latest_msgs'][:DISCORD_CACHE_LIMIT]


@client.event
async def on_message(message):
    if message.content.startswith('/neko'):
        reply = 'にゃーん'
        try:
            await client.send_message(message.channel, reply)
        except:
            print(traceback.format_exc())


def get_channel_dict():
    ret_dict = dict()
    with open('./channellist.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        # skip header
        header = next(reader)
        for row in reader:
            ret_dict[row[0].lower()] = {'youtube_id': row[1]}
        return ret_dict


async def get_latest_url(youtube_channel_id):
    while True:
        try:
            url = youtube.search(youtube_channel_id)
            return url
        except:
            print(traceback.format_exc())
            await asyncio.sleep(ERROR_INTERVAL)
            continue


async def get_latest_messages(channel):
    while True:
        ret_msgs = []
        try:
            async for message in client.logs_from(channel, limit=DISCORD_CACHE_LIMIT):
                ret_msgs.append(message.content)
            return ret_msgs
        except:
            print(traceback.format_exc())
            await asyncio.sleep(ERROR_INTERVAL)
            continue


async def create_channel(channel_name):
    print("create channel", channel_name)
    while True:
        try:
            return await client.create_channel(server, channel_name, type=discord.ChannelType.text)
        except:
            print(traceback.format_exc())
            await asyncio.sleep(ERROR_INTERVAL)
            continue


async def post_message(channel,msg):
    print('post_message ', msg)
    while True:
        try:
            await client.send_message(channel, msg)
            return
        except:
            print(traceback.format_exc())
            await asyncio.sleep(ERROR_INTERVAL)
            continue

client.run(TOKEN)


