from discord.ext import commands
from os import getenv
import traceback
import discord

prefix = '!'
CHANNEL_ID = 948457438728835073 #⌘Command


@bot.command()
async def ping(ctx):
    """ テスト:ping->pong """
    await ctx.send('pong')


@bot.command()
async def hello(ctx):
    """ 挨拶を返す """
    await ctx.send('こんにちは、プロデューサー。')


@bot.command()
async def site(ctx):
    """ 公式サイトへの案内 """
    embed = discord.Embed(
                          title="シャイニーカラーズ",
                          color=0x00ff00,
                          description="公式サイトはこちらから",
                          )
    embed.set_author(
                     icon_url=bot.user.avatar_url
                    )
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send(embed=embed)


@bot.command()
async def cleanup(message):
    """ テキストチャンネル内のログが消える """
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
        await message.channel.send('塵一つ残らないね！')
    else:
        await message.channel.send('管理者以外は使用できないよ。')


@bot.event
async def on_ready():
    #サーバーにオンラインになった時にメッセージを送信する。
    print('------')
    print('Login infomation>>>')
    print(bot.user.name)
    print('------')
    embed = discord.Embed(
                          title="Hello Sakuya",
                          color=0x00ff00,
                          description="ログインしたよ。コマンドは'!'をはじめに入力してね。",
                          )
    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url
                    )
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print(ctx.message.content + " は未知のコマンドだよ。")



# Botの起動とDiscordサーバーへの接続
bot = commands.Bot(command_prefix=prefix)
token = getenv('DISCORD_BOT_TOKEN') # herokuにtokenを入力している。

bot.run(token)
