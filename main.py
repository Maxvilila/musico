import discord
from discord.ext import commands
import asyncio
import random
import youtube_dl
from youtubesearchpython import VideosSearch
import requests
from lyricsgenius import Genius
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")

bot = commands.Bot(command_prefix="!")
stop_ping = 1
waiting_numbers = 0

def is_stop():
    return stop_ping

def isOwner(context):
    return context.message.author.id == 213078092162400257

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!thamo'))

    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    print("Ready !")

@bot.command()
async def stopping(ctx):
    await ctx.send("Les pings s'arrêtent !")
    global stop_ping
    stop_ping = 2
    await asyncio.sleep(2)
    stop_ping = 1

@bot.command()
async def coucou(context):
    await context.send("Coucou !")

@bot.command()
async def bonjour(context):
    server = context.guild
    server_name = server.name
    await context.send(f"Salut jeune *padawan*, tu te trouve sur le serveur {server_name} qui est un serveur génial, la preuve, **JE** suis dedans !")

@bot.command()
async def say(context, *text):
    await context.send(" ".join(text))

@bot.command()
async def repeat(context, number, *text):
    number_remaining = int(number)
    while number_remaining > 0:
        await context.send(" ".join(text))
        number_remaining -= 1
        if is_stop() != 1:
            break

@bot.command()
async def getinfo(context, text, *reste):
    server = context.guild
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    number_of_channels = text_channels + voice_channels
    server_name = server.name
    reste_true = len(reste)
    if reste_true == 0:
        if text == "MemberCount":
            await context.send(f"Ce serveur à actuellement {member_count} membres")
        elif text == "NumberOfChannels":
            await context.send(f"Ce serveur possède {number_of_channels} channels")
        elif text == "Name":
            await context.send(f"Ce serveur s'appelle {server_name}")
        else:
            await context.send("Etrange... je ne trouve pas cela")
    else:
        await context.send("Vérifie ton message il y a peut-être quelque chose en trop")

@bot.command()
@commands.check(isOwner)
async def clearall(context):
    messages = await context.channel.history().flatten()
    for message in messages:
        await message.delete()

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

@bot.command()
async def thamo(context):
    await context.send("Voici mes commandes :\n!play (titre)\n!loop (titre) **(A ARRETER AVEC LE !LEAVE)**\n!url (url)\n!loop_url (url) **(A ARRETER AVEC LE !LEAVE)**\n**✱NEW✱**!paroles\n!pause\n!resume\n!skip\n!leave\n!clear (nombre)\n!bonjour\n!say (chose à dire)\n!repeat (nombre de fois) (chose à dire)\n!stopping\n**✱NEW✱**!champions\n**✱NEW✱**!tas")

@bot.command()
@commands.check(isOwner)
async def roulette(context):
    await context.send("La roulette Russe commencera dans 10 seconde dites 'moi' pour y participer!")

    player_say = []
    def checkMessage(message):
        return message.content == "moi" and message.channel == context.message.channel and message.author not in player_say

    try:
         while True:
             participation = await bot.wait_for("message", timeout=10, check=checkMessage)
             player_say.append(participation.author)
             await context.send(f"Nouveau participant : **{participation.author.name}**, le tirage commence dans 10 seconde !")
    except:
        gagner = ["Mute", "Ban", "Kick", "gage"]
        gage_list = ["logobi", ]
        await context.send("Début du tirage dans 3...")
        await asyncio.sleep(1)
        await context.send("2")
        await asyncio.sleep(1)
        await context.send("1")
        await asyncio.sleep(1)
        loser_say = random.choice(player_say)
        price = random.choice(gagner)
        if price == "Mute":
            await context.send(f"Et c'est **{loser_say}** qui ce prend un mute pour 2 minutes ! Ce sera effectif dans 5 secondes !")
            await asyncio.sleep(5)
            await loser_say.edit(mute=True)
            await asyncio.sleep(120)
            await loser_say.edit(mute=False)
        elif price == "Kick":
            await context.send(f"Et c'est **{loser_say}** qui se prend un kick dans 5")
            await asyncio.sleep(1)
            await context.send("4")
            await asyncio.sleep(1)
            await context.send("3")
            await asyncio.sleep(1)
            await context.send("2")
            await asyncio.sleep(1)
            await context.send("1")
            await asyncio.sleep(1)
            await context.send("👋")
            await context.guild.kick(loser_say, reason="T'as perdu !")
        elif price == "Ban":
            await context.send(f"Et c'est **{loser_say}** qui se mange un Ban dans 5")
            await asyncio.sleep(1)
            await context.send("4")
            await asyncio.sleep(1)
            await context.send("3")
            await asyncio.sleep(1)
            await context.send("2")
            await asyncio.sleep(1)
            await context.send("1")
            await asyncio.sleep(1)
            await context.send("👋")
            await context.guild.ban(loser_say, reason="T'as joué, t'as perdu !")
        else:
            await context.send(f"C'est {loser_say} qui gagne un gage, décidez le entre-vous !")


@bot.command()
@commands.check(isOwner)
async def rouletteGage(context):
    await context.send("La roulette Russe commencera dans 10 seconde dites 'moi' pour y participer!")

    player = []
    def checkMessage(message):
        return message.content == "moi" and message.channel == context.message.channel and message.author not in player

    try:
         while True:
             participation = await bot.wait_for("message", timeout=10, check=checkMessage)
             player.append(participation.author.name)
             await context.send(f"Nouveau participant : **{participation.author.name}**, le tirage commence dans 10 seconde !")
    except:
        gage_list = ["logobi"]
        await context.send("Début du tirage d'un gage dans 3...")
        await asyncio.sleep(1)
        await context.send("2")
        await asyncio.sleep(1)
        await context.send("1")
        await asyncio.sleep(1)
        loser = random.choice(player)
        price = random.choice(gage_list)
        await context.send(f"Bravo **{loser}** ton gage sera : **{price}** !")


@bot.command()
async def champions(ctx):
    try:
        free_champions = []
        url_patch = "https://ddragon.leagueoflegends.com/api/versions.json"
        response_patch = requests.get(url_patch)
        responseJSON_patch = response_patch.json()[0]
        url_id = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=RGAPI-4567d2b4-c0c9-40c5-a936-fff7c8271007"
        response_id = requests.get(url_id)
        responseJSON_id = response_id.json()['freeChampionIds']
        url = "http://ddragon.leagueoflegends.com/cdn/" + responseJSON_patch + "/data/en_US/champion.json"
        response = requests.get(url)
        responseJSON = response.json()
        for champions in responseJSON['data']:
            if int(responseJSON['data'][champions]['key']) in responseJSON_id:
                free_champions.append(champions)
        await ctx.send(f"Les champions gratuits en ce moment sont :\n-{free_champions[0]}\n-{free_champions[1]}\n-{free_champions[2]}\n-{free_champions[3]}\n-{free_champions[4]}\n-{free_champions[5]}\n-{free_champions[6]}\n-{free_champions[7]}\n-{free_champions[8]}\n-{free_champions[9]}\n-{free_champions[10]}\n-{free_champions[11]}\n-{free_champions[12]}\n-{free_champions[13]}\n-{free_champions[14]}\n-{free_champions[15]}")
    except:
        await ctx.send("La clé de l'API Riot n'est plus valide, merci d'en informer le mec bg qui a conçu musico.")


@bot.command()
async def tas(ctx):
    tas = []
    def checkMessage(message):
        return message.channel == ctx.message.channel and message.author == ctx.message.author
    try:
        await ctx.send("Le tirage au sort va commencer, indiquez le premier élément, une fois tout les éléments pris en compte attendez 20 sec ou envoyez 'lancer tas' et le tirage au sort commencera.")
        message_1 = await bot.wait_for("message", timeout=20, check=checkMessage)
        tas.append(message_1.content)
        while True:
            await ctx.send("Envoyez l'élément suivant ou dites 'lancer tas'.")
            message = await bot.wait_for("message", timeout=20, check=checkMessage)
            tas.append(message.content)
            if message.content == "lancer tas":
                tas.remove("lancer tas")
                ctx.sejsvhnvsf("jdsfgfjdsgfjsgh")
    except:
        tas_result = random.choice(tas)
        await ctx.send(f"L'élément tiré au sort est : {tas_result}")


musics = {}
ytdl = youtube_dl.YoutubeDL()



class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    global waiting_numbers
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    await asyncio.sleep(1)
    waiting_numbers = 0

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

@bot.command()
async def geturl(ctx, *title):
    videosSearch = VideosSearch(str(title), limit=0)
    lien = videosSearch.result()['result'][0]['link']
    title_of = videosSearch.result()['result'][0]['title']
    await ctx.send(f"Voici l'url de **{title_of}** : **{lien}**")

@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        global waiting_numbers
        if len(queue) > 0:
            waiting_numbers -= 1
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)
            waiting_numbers = 0

    client.play(source, after=next)


def play_song_loop(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next_loop(_):
            play_song_loop(client, queue, song)

    client.play(source, after=next_loop)


@bot.command()
async def play(ctx, *title):
    global waiting_numbers
    videosSearch = VideosSearch(str(title), limit=0)
    lien = videosSearch.result()['result'][0]['link']
    title_of = videosSearch.result()['result'][0]['title']
    client = ctx.guild.voice_client

    try:
        if client and client.channel:
            video = Video(lien)
            musics[ctx.guild].append(video)
            waiting_numbers += 1
            await ctx.send(f"J'ajoute à la file d'attente : **{title_of}**, position dans la file d'attente : **{waiting_numbers}**")
        else:
            channel = ctx.author.voice.channel
            video = Video(lien)
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : **{title_of}**")
            play_song(client, musics[ctx.guild], video)

    except:
        print()
        await ctx.send("Laisse moi dormir zebi !")

@bot.command()
async def loop(ctx, *title):
    videosSearch = VideosSearch(str(title), limit=0)
    lien = videosSearch.result()['result'][0]['link']
    title_of = videosSearch.result()['result'][0]['title']
    client = ctx.guild.voice_client

    try:
        if client and client.channel:
            video = Video(lien)
            musics[ctx.guild].append(video)
        else:
            channel = ctx.author.voice.channel
            video = Video(lien)
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : **{title_of}**")
            play_song_loop(client, musics[ctx.guild], video)

    except:
        await ctx.send("Laisse moi dormir zebi !")

@bot.command()
async def url(ctx, url):
    global musics
    global waiting_numbers
    client = ctx.guild.voice_client
    with youtube_dl.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)

    try:
        if client and client.channel:
            video = Video(url)
            musics[ctx.guild].append(video)
            waiting_numbers += 1
            await ctx.send(f"J'ajoute à la file d'attente : **{video_title}**, position dans la file d'attente : **{waiting_numbers}**")
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            musics[ctx.guild] = []
            client = await channel.connect()
            await ctx.send(f"Je lance : **{video_title}**")
            play_song(client, musics[ctx.guild], video)

    except:
        await ctx.send("Laisse moi dormir zebi !")


@bot.command()
async def loop_url(ctx, url):
    client = ctx.guild.voice_client
    with youtube_dl.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : **{video_title}**")
        play_song_loop(client, musics[ctx.guild], video)


@bot.command()
async def paroles(ctx):
    def checkMessage(message):
        return message.channel == ctx.message.channel and message.author == ctx.message.author
    await ctx.send("Quel est le titre de la chanson ?")
    try:
        titre = await bot.wait_for("message", timeout=30, check=checkMessage)
        await ctx.send("Par qui a été interprété cette chanson ?")
        artiste = await bot.wait_for("message", timeout=30, check=checkMessage)
        genius = Genius("09e2HwTsUQwZzfBO_UFy8upuVQEct5iImrwCDiQXdqMAvLBFzzkHRA2lNoVKlBoA")
        song = genius.search_song(titre.content, artiste.content)
        await ctx.send(f"Voici les paroles de {song.title} par {song.artist}.")
        await asyncio.sleep(2)
        try:
            await ctx.send(song.lyrics)
        except:
            song_url = song.url
            await ctx.send(f"Les paroles sont trop longues et ne tiennent pas dans un message discord. Voici donc les paroles sur internet : {song_url}")

    except:
        await ctx.send("Erreur, soit le temps pour saisir les valeurs est écoulé soit il n'y a pas de résultats pour votre recherche.")


bot.run(token)