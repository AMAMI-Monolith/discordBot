import discord
import traceback
from discord.ext import commands
from os import getenv

# Botの起動とDiscordサーバーへの接続
token = getenv('DISCORD_BOT_TOKEN') # herokuにtokenを入力している。
bot = commands.Bot(command_prefix = "!")

 
@bot.command()
async def nya(ctx):
    """ テスト:nyaa """
    if message.author.bot:
        return
    else:
        await ctx.send('にゃー')


@bot.command()
async def hello(ctx):
    """ 挨拶を返す """
    reply = f'こんにちは、{ctx.author.mention}プロデューサー。'
    await ctx.channel.send(reply)


@bot.command()
async def site(ctx):
    """ 公式サイトへの案内 """
    embed=discord.Embed(
                        title='シャイニーカラーズ',
                        url='https://shinycolors.idolmaster.jp/',
                        description='公式サイトはこちらから',
                        color=0x00f900)
    embed.set_thumbnail(
                        url='https://shinycolors.idolmaster.jp/pc/static/img/download/thumb_lantica_sakuya.png'
                        )
    await ctx.send(embed=embed)


@bot.command()
async def cleanup(ctx):
    """ テキストチャンネル内のログが消える。 (管理者のみ)"""
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge()
        await ctx.channel.send('チャンネルを綺麗にしたよ。')
    else:
        await ctx.channel.send('管理者以外は使用できないよ。')


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


@bot.event
async def on_ready():
    # このbotのサーバーにオンラインになった時に私にDM(ダイレクトメッセージ)を送信する。
    print('------')
    print('Login infomation>>>')
    print(f'{bot.user.name}がログインしたよ。')
    print('------')
    await bot.change_presence(activity=discord.Game(name="!help"))
    embed = discord.Embed(
                      title="Hello Sakuya",
                      color=0x00ff00,
                      description="オンラインになったよ。",
                      )
    embed.set_author(name=bot.user,
                     icon_url=bot.user.avatar_url
                    )
    fname="BotOnline.png "
    file = discord.File(fp="/BotOnline.png",filename=fname,spoiler=False)
    embed.set_image(url=f"attachment://{fname}")
    user =bot.get_user(260333442489647105)
    await user.send(embed=embed)

    
bot.run(token)
