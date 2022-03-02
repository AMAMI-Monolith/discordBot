# インストールした discord.py を読み込む
import discord
from discord.ext import commands

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'OTQ4NDQ1Mzc3MjM1OTMxMjA4.Yh76lw.K5DHomY8LQVirPKqa10JVqu14-8'
bot = commands.Bot(command_prefix="!")

#bot = discord.Client()
#client.Bot(command_prefix='/',activity=discord.Activity(name='起動中!',type=discord.ActivityType.watching))

CHANNEL_ID = 948457438728835073 # 任意のチャンネルID(int)


# bot起動時に実行されるイベントハンドラを定義
@bot.event
async def on_ready():
    print('Login infomation>>>')
    print(bot.user.name)
    print('------')
    embed = discord.Embed( # Embedを定義する
                          title="Hello Sakuya",# タイトル
                          color=0x00ff00, # フレーム色指定(今回は緑)
                          description="ログインしたよ。コマンドは'!'をはじめに入力してね。",
                          )
    embed.set_author(name=bot.user, # Botのユーザー名
                     icon_url=bot.user.avatar_url # Botのアイコンを設定してみる
                    )
    embed.set_footer(text="made by AMAMI", # フッターには開発者の情報でも入れてみる
                     icon_url="https://twitter.com/amami_ew")

    channel = bot.get_channel(CHANNEL_ID)

    await channel.send(embed=embed) # embedの送信には、embed={定義したembed名}
#新規メンバー参加時に実行されるイベントハンドラ

#テキストチャンネル内のログが消える
@bot.event
async def on_message(message):
    if message.content == '!cleanup':
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            await message.channel.send('キレイになったよ、プロデューサー。')
        else:
            await message.channel.send('ごめんね、このコマンドは管理者にしか使えないんだ。')
    elif message.content == '!hello':
        await message.channel.send('こんにちは、プロデューサー。')

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
