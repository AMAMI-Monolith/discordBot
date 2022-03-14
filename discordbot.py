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
    """管理人にサポートを受けるメッセージを送信する。"""
    if message.author.bot:
        return
    else:
        admin = await bot.fetch_user(ADMIN_ID)
        msg = f'{message.author.mention} さんからサポートの依頼です。'
        msg_reply = f'{message.author.mention} \n管理人にメッセージを送信しました。'
        await admin.send(msg)
        await message.channel.send(msg_reply)


@bot.command()
async def nya(message):
    """ テスト:nyaa """
    await message.send('にゃー')


@bot.command()
async def hello(ctx):
    """ 挨拶を返す """
    if message.author.bot:
        return
    else:
        reply = f'こんにちは、{ctx.author.mention}プロデューサー。'
        await ctx.channel.send(reply)


@bot.command()
async def site(message):
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
        await message.send(embed=embed)


@bot.command()
async def cleanup(message):
    """ テキストチャンネル内のログが消える。 (管理者のみ)"""
    if message.author.guild_permissions.administrator:
        await message.channel.purge()
        await message.channel.send('チャンネルを綺麗にしたよ。')
    else:
        await message.channel.send('管理者専用コマンドだよ。')


@bot.event
async def create_channel(message, channel_name):
    # 下のmkchから呼ばれる新規テキストチャンネルを作成する。
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel

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


@client.event
async def on_command_error(message, error):
    if isinstance(error, CommandNotFound):
        print(message.message.content + " は未知のコマンドです。")
        "tts": false,
        "embeds": [
            {
              "type": "rich",
              "title": `Command List`,
              "description": `コマンドの説明、最初に「!」を忘れずに`,
              "color": 0xff5900,
              "fields": [
                {
                  "name": `!hello`,
                  "value": `挨拶を返す`,
                  "inline": true
                },
                {
                  "name": `!nya`,
                  "value": `「nyaa」と返す`,
                  "inline": true
                },
                {
                  "name": `!site`,
                  "value": `【シャニマス公式サイト】へのリンクを返す。`,
                  "inline": true
                },
                {
                  "name": `!mkch`,
                  "value": `新しくテキストチャンネルを作る。`,
                  "inline": true
                },
                {
                  "name": `!support`,
                  "value": `管理人にサポートを受けるメッセージを送信する。(DMに送信)`,
                  "inline": true
                },
                {
                  "name": `!stop`,
                  "value": `このBotを停止できる。(管理人専用)`,
                  "inline": true
                },
                {
                  "name": `!cleanup`,
                  "value": `入力したテキストチャンネルのメッセージが全て消える(管理人専用)`,
                  "inline": true
                }
              ]
            }
          ]
        fname="help.png " # アップロードするときのファイル名 自由に決めて良いですが、拡張子を忘れないように
        file = discord.File(fp="img",filename=fname,spoiler=False) # ローカル画像からFileオブジェクトを作成
        embed.set_image(url=f"attachment://{fname}")
        await message.channel.send(file=file, embed=embed)
        

bot.run('OTQ4NDQ1Mzc3MjM1OTMxMjA4.Yh76lw.K5DHomY8LQVirPKqa10JVqu14-8')


bot.run(token)
