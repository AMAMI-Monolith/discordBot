from ast import Lambda
from ntpath import join
from tabnanny import check
import discord
import traceback
from importlib.resources import contents
from discord.ext  import commands
from discord_buttons_plugin import *
from discord.utils import get
from dislash import InteractionClient, SelectMenu, SelectOption
#from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from os import getenv

# Botの起動とDiscordサーバーへの接続
ADMIN_ID = '260333442489647105'

#token = getenv('DISCORD_BOT_TOKEN')
token = 'OTQ4NDQ1Mzc3MjM1OTMxMjA4.Yh76lw.K5DHomY8LQVirPKqa10JVqu14-8'

#-------------------------------
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix = "!",
    case_insensitive= True, #コマンドの大文字小文字を無視する(True)
    help_command = None, #標準のhelpコマンドを無効化する(None)
    intents=intents
)
InteractionClient(bot)
discord.member = True
#DiscordComponents(bot)
buttons = ButtonsClient(bot)
slash = InteractionClient(bot)
#-------------------------------


#--- bot.commands ---
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
        await message.send(f'{message.author.mention}チャンネルを綺麗にしたよ。')
    else:
        await message.channel.send('管理者専用コマンドだよ。')


@bot.command()
async def clear(message, num):
    async for message in message.channel.history(limit=int(num)+1):
        await message.delete(delay=1.2)


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
    # 上のmkchから呼ばれる新規テキストチャンネルを作成する。
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel


@bot.command()
async def help(message):
    if message.author.bot:
        return
    else:
        embed=discord.Embed(title="ヘルプ機能", description="コマンドの説明。最初に『!』をつけてください。", color=0xff9300)
        embed.add_field(name="!clear X", value="Xのだけメッセージを消す。(Xは数値)", inline=True)
        embed.add_field(name="!site", value="『シャニマス公式』などへのリンクを表示する。", inline=True)
        embed.add_field(name="!mkch", value="同カテゴリにテキストチャンネルを作成する。", inline=True)
        embed.add_field(name="!Support", value="管理人にサポートメッセージを送る(DM)", inline=False)
        embed.add_field(name="!cleanup (※管理人のみ)", value="テキストチャンネルのメッセージをすべて消す", inline=False)
        fname="help.png" # アップロードするときのファイル名 自由に決めて良いですが、拡張子を忘れないように
        file = discord.File(fp="img/help.png",filename=fname,spoiler=False) # ローカル画像からFileオブジェクトを作成
        embed.set_image(url=f"attachment://{fname}") # embedに画像を埋め込むときのURLはattachment://ファイル名
        await message.channel.send(file=file, embed=embed) # ファイルとembedを両方添えて送信する


"""Sakuyaselect =[
                    SelectOption(label= "[P]白いツバサ", value= "白いツバサ"),
                    SelectOption(label= "[P]真紅一輪",value= "真紅一輪"),
                    SelectOption(label= "[P]雪染めロマンティカ",value= "雪染めロマンティカ"),
                    SelectOption(label= "[P]ふれあい、おもいあい",value= "ふれあい、おもいあい"),
                    SelectOption(label= "[P]秘めやかファンサービス",value= "秘めやかファンサービス"),
                    SelectOption(label= "[P]アイドルロード",value= "アイドルロード"),
                    SelectOption(label="✕ キャンセル", value= "Cancel")
]"""

#------
@bot.command()
async def sakuyainfo(ctx):
    msg = await ctx.send(
        "調べたいPアイドルを選択してください。",
        components=[
            SelectMenu(
                custom_id="idolpicks",
                placeholder="カード名を選択して下さい。",
                max_values=1,
                options=[
                    SelectOption(label= "[P]白いツバサ", value= "白いツバサ"),
                    SelectOption(label= "[P]真紅一輪",value= "真紅一輪"),
                    SelectOption(label= "[P]雪染めロマンティカ",value= "雪染めロマンティカ"),
                    SelectOption(label= "[P]ふれあい、おもいあい",value= "ふれあい、おもいあい"),
                    SelectOption(label= "[P]秘めやかファンサービス",value= "秘めやかファンサービス"),
                    SelectOption(label= "[P]アイドルロード",value= "アイドルロード"),
                    SelectOption(label="✕ キャンセル", value= "Cancel")
                ]
            )
        ]
    )

@bot.event
async def on_dropdown(inter):
    labels = [option.label for option in inter.select_menu.selected_options]
    values= [option.value for option in inter.select_menu.selected_options]
    #res =  inter.select_menu.selected_options
    #await inter.reply(f"Your choices: {labels}") #Your choices: [labels]
    #await inter.reply(f"Your values: {values}") #Your values: ['白いツバサ']
    #interaction = await bot.wait_for("select_option", check=lambda inter: inter.custom_id == 'idolpicks')

    await clear(inter, 0)
    if labels == ['[P]白いツバサ']:
        await inter.reply("選択したカードは[P]白いツバサ 白瀬咲耶です。")
        embed=discord.Embed(title="カード情報", color=0xff0000)
        embed.add_field(name="カード名", value="【アイドルロード】白瀬 咲耶", inline=False)
        embed.add_field(name="ライブスキル", value="咲耶アピール++\nDance2.5倍アピール\n咲耶アピール+++\nDance3倍アピール\n咲耶アピール++++\nDance3.5倍アピール\n", inline=False)
        await inter.reply(embed=embed)
    elif labels == ['[P]真紅一輪']:
        await inter.reply(f"選択したカードは[P]真紅一輪 白瀬咲耶です。")
    elif labels == ['[P]雪染めロマンティカ']:
        await inter.reply("選択したカードは[P]雪染めロマンティカ 白瀬咲耶です。")
    elif labels == ['[P]ふれあい、おもいあい']:
        await inter.reply("選択したカードは" + values + "白瀬咲耶です。")
    elif labels == ['[P]秘めやかファンサービス']:
        await inter.reply("選択したカードは" + values + "白瀬咲耶です。")
    elif labels == ['[P]アイドルロード']:
        await inter.reply("選択したカードは" + values + "白瀬咲耶です。")
    elif labels == ['✕ キャンセル']:
        await inter.reply("キャンセルされました。")
        await clear(inter, 0)
    else:
        await inter.reply("")



#--- bot.event ---------------
@bot.event
async def on_ready():
    # このbotのサーバーにオンラインになった時に管理人にDM(ダイレクトメッセージ)を送信する。
    print('------')
    print('Login infomation>>>')
    print('v1.03   ')
    print(f'{bot.user.name}がログインしたよ。')
    print('------')
    await bot.change_presence(activity=discord.Game(name="!help"))
    admin = await bot.fetch_user(ADMIN_ID)
    embed = discord.Embed(title="Botがオンラインになりました。", color=0x29f306)
    fname="BotOnline.png"
    file = discord.File(fp="img/BotOnline.png",filename=fname,spoiler=False)
    embed.set_image(url=f"attachment://{fname}")
    await admin.send(file=file, embed=embed)


@bot.event
async def on_command_error(message, error):
    if isinstance(error, commands.errors.MissingPermissions): #エラーの内容を判別
        await message.channnel.send(message.content + " は未知のコマンドです。\n!helpでコマンドを確認してください。")


bot.run(token)
