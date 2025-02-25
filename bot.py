from os import environ
import os
import time
from unshortenit import UnshortenIt
from urllib.request import urlopen
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from pyshorteners import Shortener
from bs4 import BeautifulSoup
#from doodstream import DoodStream
import requests
import re

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
DOODSTREAM_API_KEY = environ.get('DOODSTREAM_API_KEY')
BITLY_KEY = environ.get('BITLY_KEY')
CHANNEL = environ.get('CHANNEL')
HOWTO = environ.get('HOWTO')
bot = Client('Doodstream bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**This is a Doodstream URL convertor bot and able to upload all direct links to Doodstream,just send me link or full post... Developed By @ManyaDon007**")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Doodstream Links.....  I'll convert & replace all Doodstream links with your Doodstream links \nReport Bugs at @Manya@007**")

@bot.on_message(filters.command('report') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @Manya@007**")
    
@bot.on_message(filters.text & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{Doodstream_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        if(len(Doodstream_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{Doodstream_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{Doodstream_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


'''async def get_ptitle(url):
    if ('bit' in url ):
      url = urlopen(url).geturl()
      
      
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for title in soup.find_all('title'):
        pass
    title = list(title.get_text())
    title = title[8:]
    str = 't.me/' + CHANNEL + ' '
    for i in title:
        str = str + i
    lst = list(html_text.split(","))
    c = 0
    for i in lst:
        if ("""/e/""" in i):
            found = lst[c]
            break
        c += 1

    # Doodstream.com link
    Doodstream_video_id = list(found.split(":"))
    video_id = Doodstream_video_id[2]
    video_id = list(video_id.split(","))
    v_id = video_id[0]
    #v_len = len(v_id)
    #v_id = v_id[1:v_len - 2]

    v_url = 'https://dood.ws/d/' + v_id
    v_url = url
    res = [str, v_url]
    return res'''


async def Doodstream_up(link):
    if ('bit' in link ):
        #link = urlopen(link).geturl()
        unshortener = UnshortenIt()
        link = unshortener.unshorten(link)
    
    title_new = urlparse(link)
    title_new = os.path.basename(title_new.path)
    title_Doodstream = '@' + CHANNEL + title_new
    res = requests.get(
         f'https://doodapi.com/api/upload/url?key={DOODSTREAM_API_KEY}&url={link}&new_title={title_Doodstream}')
         
    data = res.json()
    data = dict(data)
    print(data)
    v_id = data['result']['filecode']
    #bot.delete_messages(con)
    v_url = 'https://dood.ws/d/' + v_id
    s = Shortener(api_key=BITLY_KEY)
    v_url = s.bitly.short(v_url)
    return (v_url)


async def multi_Doodstream_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_Doodstream_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)


async def new_Doodstream_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await Doodstream_up(i))
    return new_urls


async def remove_username(new_List):
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i):
            new_List.remove(i)
    return new_List

async def addFooter(str):
    footer = """
━━━━━━━━━━━━━━━
✪ »JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer

bot.run()
