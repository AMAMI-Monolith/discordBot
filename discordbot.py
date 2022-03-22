import discord
import traceback
from discord import Client, Intents, Embed
from discord.ext import commands, pages
from discord_buttons_plugin import *
from discord.utils import get
from discord_slash import SlashCommand, SlashContext
from dislash import InteractionClient, SelectMenu, SelectOption
from dislash import slash_commands
from dislash.interactions import *
from os import getenv

# Botの起動とDiscordサーバーへの接続
ADMIN_ID = '260333442489647105'
bot = commands.Bot(
    command_prefix = "!",
    case_insensitive= True, #コマンドの大文字小文字を無視する(True)
    help_command = None #標準のhelpコマンドを無効化する(None)
)
intents = discord.Intents.all()
client = discord.Client(intents=intents)
buttons = ButtonsClient(bot)
#slash = InteractionClient(bot)
slash = slash_commands.SlashClient(bot)
#slash_client = SlashCommand(bot, sync_commands=True)
#-------------------------------


#--- Slash Commands ---

@bot.slash_command(guild_ids=[427872633468616704])
async def ping(ctx):
    await ctx.respond('pong')


@bot.slash_command(guild_ids=[427872633468616704])
async def hello(ctx):
    await ctx.respond(f'こんにちは、{ctx.author.mention}プロデューサー。')


@bot.slash_command(guild_ids=[427872633468616704])
async def support(ctx):
    admin = await fetch_user('260333442489647105')
    msg = f'{ctx.author.mention} さんからサポートの依頼です。'
    #msg_reply = f'{ctx.author.mention} \n管理人にメッセージを送信しました。'
    await admin.send(msg)
    await ctx.send(f'{ctx.author.mention} \n管理人にメッセージを送信しました。')


#--- bot.commands ---
@bot.command()
async def site(message):
    """ 公式サイトへの案内 """
    if message.author.bot:
        return
    else:
        embed=discord.Embed(
            title = "公式サイト や 関連リンク",
            color = 0xff4d00
        ) 
        fname="logo.png "
        file = discord.File(fp="img/logo.png",filename=fname,spoiler=False)
        embed.set_image(url=f"attachment://{fname}")
        await message.send(file=file, embed=embed)
        await buttons.send(
            channel = message.channel.id,
            components = [
                ActionRow([
                    Button(
                        style   = ButtonType().Link,
                        label   = "公式サイト",
                        url     = 'https://shinycolors.idolmaster.jp/',
                        disabled= False
                    ),
                    Button(
                        style   = ButtonType().Link,
                        label   = "お知らせ",
                        url     = 'https://shinycolors.idolmaster.jp/news/',
                        disabled= False
                    ),
                    Button(
                        style   = ButtonType().Link,
                        label   = "はばたきラジオステーション",
                        url     = 'https://asobistore.jp/content/title/Idolmaster/shinyradio/',
                        disabled= False
                    ),
                    Button(
                        style   = ButtonType().Link,
                        label   = "公式Twitter",
                        url     = 'https://twitter.com/imassc_official/',
                        disabled= False
                    )
                ])
            ]
        )


@bot.command()
async def cleanup(message):
    """ テキストチャンネル内のログが消える。 (管理者のみ)"""
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
        await message.channel.send('チャンネルを綺麗にしたよ。')
    else:
        await message.channel.send('管理者専用コマンドだよ。')


@bot.command()
async def mkch(message):
    """ 発言したチャンネルのカテゴリ内に新規テキストチャンネルを作成。 """
    if message.author.bot:
        return
    else:
        new_channel = await create_channel(message, channel_name = message.author.name)
        # チャンネルのリンクと作成メッセージを送信
        text = f'{new_channel.mention} を作成したよ。'
        await message.channel.send(text)


@bot.event
async def create_channel(message, channel_name):
    # 下のmkchから呼ばれる新規テキストチャンネルを作成する。
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel


@bot.command()
async def stop(message):
    """ Botを停止することができる(管理者のみ) """
    if message.author.guild_permissions.administrator:
        admin = await bot.fetch_user(ADMIN_ID)
        msg = "🌙 status : Offline"
        await admin.send(msg)
        await bot.logout()
    else:
        await message.channel.send("管理者専用コマンドだよ。")

@bot.event
async def on_ready():
    # このbotのサーバーにオンラインになった時に管理人にDM(ダイレクトメッセージ)を送信する。
    print('------')
    print('Login infomation>>>')
    print(f'{bot.user.name}がログインしたよ。')
    print('------')
    await bot.change_presence(activity=discord.Game(name="!help"))
    admin = await bot.fetch_user(ADMIN_ID)
    embed = discord.Embed(title="Botがオンラインになりました。", color=0x29f306)
    fname="BotOnline.png"
    file = discord.File(fp="img/BotOnline.png",filename=fname,spoiler=False) 
    embed.set_image(url=f"attachment://{fname}")
    await admin.send(file=file, embed=embed)


@bot.command()
async def help(message):
    if message.author.bot:
        return
    else:
        embed=discord.Embed(title="ヘルプ機能", description="コマンドの説明。最初に『!』をつけてください。", color=0xff9300)
        embed.add_field(name="!hello", value="こんにちは。と返事する。", inline=True)
        embed.add_field(name="!site", value="『シャニマス公式』などへのリンクを表示する。", inline=True)
        embed.add_field(name="!mkch", value="同カテゴリにテキストチャンネルを作成する。", inline=True)
        embed.add_field(name="!Support", value="管理人にサポートメッセージを送る(DM)", inline=False)
        embed.add_field(name="!cleanup (※管理人のみ)", value="テキストチャンネルのメッセージをすべて消す", inline=False)
        fname="help.png" # アップロードするときのファイル名 自由に決めて良いですが、拡張子を忘れないように
        file = discord.File(fp="img/help.png",filename=fname,spoiler=False) # ローカル画像からFileオブジェクトを作成
        embed.set_image(url=f"attachment://{fname}") # embedに画像を埋め込むときのURLはattachment://ファイル名
        await message.channel.send(file=file, embed=embed) # ファイルとembedを両方添えて送信する

#試験運用 bot.event -> client.event
@client.event
async def on_member_join(member):
    guild = member.guild
    channel=discord.utils.get(guild.text_channels, name="入室ログ")
    await channel.send(f'{member.author.mention}さん、ようこそ。\nまず、#はじめに #サーバールール をお読みください。')


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel=discord.utils.get(guild.text_channels, name="入室ログ")
    await channel.send(f'{member.author.mention}さん、ようこそ。\nまず、#はじめに #サーバールール をお読みください。')


@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.errors.MissingPermissions): #エラーの内容を判別
        await message.channnel.send(message.content + " は未知のコマンドです。\n!helpでコマンドを確認してください。")



token = getenv('DISCORD_BOT_TOKEN')
bot.run('OTQ4NDQ1Mzc3MjM1OTMxMjA4.Yh76lw.K5DHomY8LQVirPKqa10JVqu14-8')
# bot.run(token)
