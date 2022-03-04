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
MDISK_API = environ.get('MDISK_API')
DOODSTREAM_API_KEY = environ.get('DOODSTREAM_API_KEY')
API_KEY = environ.get('API_KEY')
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
        "**I am a Mdisk/Doodstream post convertor bot and i am able to upload all direct links to Mdisk/Doodstream,just send me links or full post... \n Join my Group @katmmovieshd1**")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Mdisk/Doodstream Links, texts & images... Than I'll convert & replace all Mdisk/Doodstream links with your Mdisk/Doodstream links \nMessage me @shinukat For more help-**")

@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @shinukat or for more join @katmovieshd1**")
    
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



async def Doodstream_up(links):
    if ('bit' in links ):
        #links = urlopen(links).geturl()
        unshortener = UnshortenIt()
        links = unshortener.unshorten(links)
    if ('dood'in links ):
        title_new = urlparse(links)
        title_new = os.path.basename(title_new.path)
        title_Doodstream = '@' + CHANNEL + title_new
        res = requests.get(
             f'https://doodapi.com/api/upload/url?key={DOODSTREAM_API_KEY}&url={links}&new_title={title_Doodstream}')
         
        data = res.json()
        data = dict(data)
        print(data)
        v_id = data['result']['filecode']
        #bot.delete_messages(con)
        v_url = 'https://dood.ws/d/' + v_id


    if ('entertainvideo' in links or 'mdisk' in links):
        url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
        param = {'token': MDISK_API,'link': links}
        res = requests.post(url, json = param)
        data = res.json()
        data = dict(data)
        v_url = data['sharelink']



    
    
    
    url = 'https://droplink.co/api'
    params = {'api': API_KEY, 'url': v_url}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            v_url =  data["shortenedUrl"]
    #s = Shortener(api_key=BITLY_KEY)
    #v_url = s.bitly.short(v_url)
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
        #if ('entertainvideo' in urls or 'mdisk' in urls or 'bit' in urls or 'bit' in urls):
        time.sleep(0.2)
        new_urls.append(await Doodstream_up(i))
        #else:
            #continue
    return new_urls


async def remove_username(new_List):
    count = 0
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i or 'https://t.me/+' in i or 'instagram' in i or 'Porn' in i):
            count+=1
    while(count):
      
        for i in new_List:
            if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i or 'https://t.me/+' in i or 'instagram' in i or 'Porn' in i):
                new_List.remove(i)
        count-=1
    return new_List

async def addFooter(str):
    footer = """
    ━━━━━━━━━━━━━━━
How to Download / Watch Online :-""" + HOWTO + """
━━━━━━━━━━━━━━━
JOIN CHANNEL :- t.me/""" + CHANNEL
    return str + footer

bot.run()
