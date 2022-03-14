import discord
import traceback
from discord.ext import commands
from discord.utils import get
from os import getenv

# Botの起動とDiscordサーバーへの接続
bot = commands.Bot(command_prefix = "!")
ADMIN_ID = '260333442489647105'
token = getenv('DISCORD_BOT_TOKEN')


@bot.command()
async def support(message):
    """"管理人にサポートを受けるメッセージを送信する。"""
        admin = await bot.fetch_user(ADMIN_ID)
        msg = f'{message.author.name}さんからサポートの依頼です。'
        await admin.send(msg)


@bot.command()
async def nya(ctx):
    """ テスト:nyaa """
    await ctx.send('にゃー')


@bot.command()
async def hello(ctx):
    """ 挨拶を返す """
    if message.author.bot:
        return
    else:
        reply = f'こんにちは、{ctx.author.mention}プロデューサー。'
        await ctx.channel.send(reply)


@bot.command()
async def site(ctx):
    """ 公式サイトへの案内 """
    if message.author.bot:
        return
    else:
        embed=discord.Embed(
                            title='シャイニーカラーズ',
                            url='https://shinycolors.idolmaster.jp/',
                            description='公式サイトはこちらから',
                            color=0x00f900)
        embed.set_thumbnail(url='https://shinycolors.idolmaster.jp/pc/static/img/download/thumb_lantica_sakuya.png')
        await ctx.send(embed=embed)


@bot.command()
async def cleanup(ctx):
    """ テキストチャンネル内のログが消える。 (管理者のみ)"""
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge()
        await ctx.channel.send('チャンネルを綺麗にしたよ。')
    else:
        await ctx.channel.send('管理者専用コマンドだよ。')


@bot.event
async def create_channel(message, channel_name):
    # 下のmkchから呼ばれる新規テキストチャンネルを作成する。
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel


@bot.command()
async def mkch(ctx):
    """ 発言したチャンネルのカテゴリ内に新規テキストチャンネルを作成。 """
    if message.author.bot:
        return
    else:
        new_channel = await create_channel(ctx, channel_name = ctx.author.name)
        # チャンネルのリンクと作成メッセージを送信
        text = f'{new_channel.mention} を作成したよ。'
        await ctx.channel.send(text)


@bot.event
async def on_member_join(member):
    # ユーザのサーバーへの参加を検知し、埋め込みでログを残す。
    guild = member.guild
    ready=discord.utils.get(guild.text_channels, name="はじめに") #946633117651836978
    rule =discord.utils.get(guild.text_channels, name="サーバールール") #945589161509941279
    channel=discord.utils.get(guild.text_channels, name="入室ログ")
    embed=discord.Embed(title=f'{member.author.name} さんが参加しました', color=0x00ffff)
    embed.set_thumbnail(url=member.author.avatar_url)
    embed.add_field(name="name", value=f'{member.author.mention}', inline=False)
    await channel.send(f'{member.author.mention}\nようこそ、{ready.mention} と {rule.mention} を最初にお読みください。',
                        embed=embed)


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
    msg = "🔴 status : Online"
    await admin.send(msg)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


bot.run('OTQ4NDQ1Mzc3MjM1OTMxMjA4.Yh76lw.K5DHomY8LQVirPKqa10JVqu14-8')


bot.run(token)
