from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='/',activity=discord.Activity(name='起動中!',type=discord.ActivityType.watching))

@bot.event
async def on_command_error(ctx, error):
    #エラー
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

async def on_ready():
    #ログイン
    print('Login infomation>>>')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    #あいさつ
    await ctx.send('こんにちは、私の名前は白瀬咲耶。')



token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
