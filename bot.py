# PWNZ Copyright 2021 By Zan4eg#5557
# Импорты библиотек

import discord
import random
from discord.ext import commands
import asyncio
import socket
import smtplib
import datetime
import pyowm
import json
from datetime import timedelta
import os
from Cybernator import Paginator as pag
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json, socket, threading, time, concurrent.futures
from six.moves import urllib
from random import choice
import string
import requests
import pyshorteners

PREFIX = '.' # Переменная префикса

Bot = commands.Bot( command_prefix = PREFIX ) # Установка префикса бота
@Bot.remove_command('help') #Удаление стандартной комманды help

def get_random_string(length):
	letters = string.ascii_letters + string.digits
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

# При загрузке бота
@Bot.event
async def on_ready():
    activity = discord.Game(name = "PWNZ | .help", url='https://twitch.com/zan4egpayne')
    await Bot.change_presence( status = discord.Status.online, activity = activity )
    print("Logged in as PWNZ!")
    print("PWNZ Copyright 2021 By Zan4eg#5557")
    print("Бот запущен и готов к работе!")
    while True:
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = ".help | PWNZ") )
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = "Бот создан специально для сервера PWNZ'a") )
        await asyncio.sleep(8)
        await Bot.change_presence( status = discord.Status.online, activity = discord.Game(name = "Бот создан Zan4eg#5557") )

@Bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, команда не найдена!', colour = discord.Color.red()))

# Идеи
@Bot.command()
async def suggest( ctx, *, suggest = None):
    if suggest is None:
        await ctx.send(":x: | Вы не указали идею!")

    else:
        channel = Bot.get_channel(870959982185680946)
        emb=discord.Embed( title = '', colour= 0x04ff00 )
        emb.set_author(name=ctx.author.name + "#" + ctx.author.discriminator + ", отправил своё улучшение!", icon_url = ctx.author.avatar_url)
        emb.add_field( name = 'Текст идеи:', value = '** ```{}``` **'.format( suggest ) )
        emb.set_footer(text= "© PWNZ Bot 💚 | Идеи")
        emb.timestamp = datetime.datetime.utcnow()
        message = await channel.send(embed=emb)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await ctx.message.delete()
        await ctx.send("Вы успешно отправили свою идею!")

# Закрытие канала
@Bot.command( pass_context=True )
async def close(ctx):
    role = discord.utils.get(ctx.guild.roles, id=870959126929358858)
    if role not in ctx.author.roles:
        await ctx.send(":x: | Вы не состоите в **Support Team**!")
    else:
        if ctx.channel.category.id == 870960366388129842 and ctx.channel.name != 'обращение-close':
            member = await Bot.fetch_user(ctx.channel.name)
            await ctx.channel.set_permissions(member, send_messages=False,read_messages=True)
            await ctx.send(f"{member.mention}, **саппорт {ctx.author.mention} установил вашему обращению статус: 'Закрыто'**")
            message = await ctx.send(f"Поставьте пожалуйста свою оценку саппорту!")
            await message.add_reaction('👍')
            await message.add_reaction('👎')
            cursor.execute(f"INSERT INTO reactions VALUES ('{message.channel.id}', '{message.id}', '{ctx.message.author.id}')")
            connection.commit()
            mss = await ctx.send("Идёт закрытие канала! Пожалуйста, подождите")
            await ctx.channel.edit(name="обращение-close")
            await ctx.channel.set_permissions(role, send_messages=False,read_messages=True)
            await ctx.message.delete()
            #await Bot.get_channel(829756582581370890).send(ctx.message.author.mention+" +1 балл (" +ctx.channel.mention+")")
            await mss.delete()
        else:
        	await ctx.send(":x: | Этот канал не является каналом поддержки")

# Поддержка
@Bot.event
async def on_message(message):
    await Bot.process_commands(message)
    channel = message.channel
    support_channel = Bot.get_channel(870960257613066251)
    isBot = message.author.bot
    if(message.author.bot): return
    if(channel != support_channel): return
    await message.delete()
    guild = message.guild
    channel2 = await guild.get_channel(870960366388129842).create_text_channel(message.author.id)
    await channel2.set_permissions(message.author, read_messages=True,send_messages=True)
    emb=discord.Embed( title = '', colour= 0x04ff00 )
    emb.set_author(name="Обращение к команде поддержки")
    emb.set_footer(text=f"{message.author.display_name}", icon_url = message.author.avatar_url)
    emb.add_field( name = 'Суть обращения:', value = '{}'.format(message.content) )
    await channel2.send(message.author.mention+", **`для команды поддержки`** <@&870959126929358858>")
    await channel2.send(embed=emb)
    #message2 = await channel.send(message.author.mention + ", вы успешно оставили своё обращение! Перейдите в канал " + channel2.mention + " для просмотра ответа.")
    await asyncio.sleep(5)
    #await message2.delete()

# Эмбед ТП
@Bot.command( pass_context=True )
async def embed(ctx):
    if ctx.message.author.guild_permissions.administrator:
        emb1 = discord.Embed( title="Тех.Поддержка сервера PWNZ", colour=0xff8c00 ) # Создаем ембед
        emb1.add_field( name='Правила подачи обращения', value='```1) Запрещено отправлять оскорбительные сообщения\n2) Запрещено отправлять сообщения с непристойным материалом\n3) Запрещено создавать обращения без причины```', inline=False)
        emb1.add_field( name='Всего', value='`обработанных обращений:` ?', inline=True)
        emb1.add_field( name='Всего', value='`обращений на рассмотрении:` ?', inline=True)
        emb1.add_field( name='Всего', value='`закрытых обращений:` ?', inline=True)
        emb1.set_footer(text= "© PWNZ Support | Тех.Поддержка")
        emb1.set_image( url='https://images-ext-2.discordapp.net/external/cQxwDjOv26SB4UNSoL58YRtmhJFOediiOfT8tVSqAGw/https/images-ext-2.discordapp.net/external/uxj2OXVnN-UuIlbnrx9bTD7aYuLJoUmSC8uInIL9b9Q/https/images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif' )
        emb1.timestamp = datetime.datetime.utcnow()
        await ctx.send( embed = emb1)
        await ctx.message.delete()
    else:
        await ctx.send(":x: | У вас нет прав!")

# Информация о пользователе
@Bot.command( pass_context=True )
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send(f"**{ctx.author}**, укажите участника сервера \n Пример команды: ***.info `@Пользователь`***")
    else:
        emb = discord.Embed( title="Информация об {}".format(user.name), colour=0x04ff00 ) # Создаем ембед
        emb.add_field( name='Имя', value=user.name ) # Получаем имя пользователя
        emb.add_field( name='Присоединился', value=user.joined_at ) # Получаем присоедение пользователя
        emb.add_field( name='Айди', value=user.id ) # Получаем айди пользователя
        emb.set_thumbnail( url=user.avatar_url ) # Получаем аватар пользователя
        emb.set_footer(text= "Упомянули: {}".format(user.name), icon_url= user.avatar_url) # Получаем имя пользователя и его аву (опять же)
        await ctx.send( embed = emb )

# Информация о создателе
@Bot.command( pass_context=True )
async def botcreater(ctx):
    emb = discord.Embed( title="Дискорд **Zan4eg#5557**", colour=0x04ff00 )  # Создаем ембед
    emb.set_footer(text= "Бот создан: 15.05.2021") # Получаем имя пользователя и его аву (опять же)
    await ctx.send( embed = emb )

# Очистка сообщений
@Bot.command( pass_context = True )
@commands.has_permissions( administrator = True ) # Установка нужных прав для комманды
async def clear ( ctx, amount : int = None):  # Создание комманды/функции
    if amount is None:
        await ctx.send(f"**{ctx.author}**, укажите количество сообщений для удаления \n Пример команды: ***.clear `кол-во сообщений`***")
    else:
        await ctx.channel.purge( limit = amount ) # Сама очистка
        emb = discord.Embed( description=f'✅  Очищено {amount} сообщений!', colour=0x04ff00 ) # Создание отчета об очистке
        await ctx.send( embed = emb )

# Информация о сервере
@Bot.command()
async def serverinfo(ctx):
    # Задаем переменные
    channels = len(ctx.guild.channels)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    members = len(ctx.guild.members)
    embed = discord.Embed(title = 'Информация о сервере:', description = f'Название сервера: `{ctx.guild.name}`\nАйди сервера: `{ctx.guild.id}`\nВсего участников: `{members}`\nВсего каналов и категорий: `{channels}`\nТекстовые каналы: `{text_channels}`\nГолосовые каналы: `{voice_channels}`\nКатегорий: `{categories}`', colour= 0x04ff00)
    await ctx.send( embed=embed )

# Статистика каналов
@Bot.command() 
async def stat(ctx, channel: discord.TextChannel = None):
    if not channel: #проверяем ввели ли канал
        channel = ctx.channel
        text = 'в данном канале'
    else:
        text = f'в #{channel.name}'
    await ctx.send(f"{ctx.author.mention}, я начинаю вычисления, подождите немного...") #отправляем сообщение о начале отсчёта
    counter = 0
    yesterday = datetime.datetime.today() - timedelta(days = 1)
    #начинаем считать сообщения
    async for message in channel.history(limit=None, after=yesterday):
        counter += 1
    counter2 = 0
    weekago = datetime.datetime.today() - timedelta(weeks = 1)
    async for message in channel.history(limit=None, after=weekago):
        counter2 += 1
    counter3 = 0
    monthago = datetime.datetime.today() - timedelta(weeks = 4)
    async for message in channel.history(limit=None, after=monthago):
        counter3 += 1
    embed = discord.Embed(title = f'Статиститка сообщений {text}', colour= 0x04ff00) #создаём embed-сообщение о подсчётах 
    embed.add_field(name = 'За сегодня', value = f'{counter}', inline = False) #добавляем поле "За сегодня"
    embed.add_field(name = 'За неделю', value = f'{counter2}', inline = False) #добавляем поле "За неделю" 
    embed.add_field(name = 'За месяц', value = f'{counter3}', inline = False) #добавляем поле "За месяц" 
    await ctx.send( f'{ctx.author.mention}', embed = embed ) #вывод сообщения с информацией о подсчётах

# Генератор паролей
lenght = int( '20' )
chars = '+-/*$#?=@<>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
@Bot.command()
async def passgen( ctx ):
    password = ''
    for i in range( lenght ):
        password += random.choice( chars )
    emb = discord.Embed( description=f'✅ Ваш пароль был сгенерирован и отправлен вам в лс!', colour=0x04ff00 )
    em = discord.Embed( description=f'✅ Ваш пароль: {password}\n⚠️ Никому не показывайте этот пароль!', colour=0x04ff00 )
    await ctx.send( embed = emb )
    await ctx.author.send( embed = em )
	
@Bot.command()
async def randcolor(ctx):
	await ctx.message.delete()
	random_number = random.randint(0,16777215)
	hex_number = str(hex(random_number))
	hex_number ='#'+ hex_number[2:]
	em = discord.Embed(title="Random Color Hex", description = f'Hex color: {hex_number}', color=random_number)
	await ctx.send(embed = em)

@commands.cooldown(1, 5, commands.BucketType.user)
@Bot.command()
async def ping(ctx):
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=0x04ff00)
    em.set_author(name="")
    em.add_field(name="Ping", value='Понг! :ping_pong:', inline=True)
    em.add_field(name="MS", value=f'Пинг бота: **{ctx.bot.latency * 1000:,.2f}ms**', inline=True)
    await ctx.send(embed=em)

        
@Bot.command()
async def slot(ctx):
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
    if (a == b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} Все совпадения, вы выиграли!"}))
    elif (a == b) or (a == c) or (b == c):
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} 2 подряд вы выиграли!"}))
    else:
        await ctx.send(embed=discord.Embed.from_dict({"title":"Казино", "description":f"{slotmachine} Нет совпадения, вы проиграли"}))

@Bot.command()
async def userpic(ctx, *, avamember: discord.Member):
    emb = discord.Embed(title = f"Аватар {avamember.name}", colour = 0x04ff00)
    emb.set_image(url = avamember.avatar_url)
    await ctx.send(embed = emb)

@Bot.command()
async def botinfo(ctx):
    guilds = await Bot.fetch_guilds(limit = None).flatten()  
    emb = discord.Embed(title = "Статистика", colour = 0x04ff00)
    emb.add_field(name = "Основная:", value = f"Серверов: **{len(guilds)}**\nУчастников: **{len(set(Bot.get_all_members()))}**")    # 1: Количество серверов, 2: количество уникальных участников на всех серверах
    emb.add_field(name = "Бот:", value = f"Задержка: **{int(Bot.latency * 1000)} мс**") # Скорость соединения бота с API дискорда
    await ctx.send(embed = emb)


@Bot.command()
async def tinyurl(ctx, url : str = None):
    if url is None:
        await ctx.send(embed = discord.Embed(
                title = "Укоротитель ссылок",
                description = "Ошибка | Укажите ссылку которую хотите укоротить",
                colour = 0x04ff00
            ))
    else:
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        await ctx.send("Ваша ссылка готова : " + short_url)

# Навигация по командам
@Bot.command( pass_context = True )
async def help( ctx, amount = 1 ):
    
    emb1=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x04ff00 )
    emb1.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295278927216670/e52a182a29690cf9.png' )
    emb1.add_field( name = '``{}info``'.format( PREFIX ), value = 'Информация об пользователе.' )
    emb1.add_field( name = '``{}botcreater``'.format( PREFIX ), value = 'Создатель бота.' )
    emb1.add_field( name = '``{}stat``'.format( PREFIX ), value = 'Стистика каналов.' )
    emb1.add_field( name = '``{}serverinfo``'.format( PREFIX ), value = 'Информация о сервере.' )
    emb1.add_field( name = '``{}ping``'.format( PREFIX ), value= 'Узнать задержку бота.' )
    emb1.add_field( name = '``{}userpic``'.format( PREFIX ), value= 'Узнать аватар пользователя.' )
    emb1.add_field( name = '``{}botinfo``'.format( PREFIX ), value= 'Узнать статистику бота.' )
    emb1.add_field( name = '``{}tinyurl``'.format( PREFIX ), value= 'Укоротить ссылку.' )
    emb2=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x04ff00 )
    emb2.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295281406181437/1abb1364301a30c7.png' )
    emb2.add_field( name = '``{}clear``'.format( PREFIX ), value = 'Очистка чата.' )
    emb2.add_field( name = '``{}suggest``'.format( PREFIX ), value = 'Предложить идею серверу.' )
    emb2.add_field( name = '``{}ticket``'.format( PREFIX ), value = 'Задать свой вопрос в поддержку.' )
    emb3=discord.Embed( title = 'Навигация по командам :pushpin:', colour= 0x04ff00 )
    emb3.set_thumbnail( url='https://cdn.discordapp.com/attachments/724886353065803778/766295277001768990/e2104f40da530197.png' )
    emb3.add_field( name = '``{}passgen``'.format( PREFIX ), value= 'Сгенерировать сложный пароль.' )
    emb3.add_field( name = '``{}slot``'.format( PREFIX ), value= 'Казино.' )
    emb3.add_field( name = '``{}randcolor``'.format( PREFIX ), value= 'Рандомный цвет.' )


    embeds = [emb1, emb2, emb3]

    message = await ctx.send(embed=emb1)
    page = pag(Bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()

token = os.environ.get('BOT_TOKEN')
Bot.run( str(token) )
