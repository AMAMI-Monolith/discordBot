from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='/')
intents=discord.Intents.all()
client = discord.Client(intents=intents)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def sakuya(ctx):
    await ctx.send('こんにちは、私の名前は白瀬咲耶。')
    
@client.event
async def on_member_join(member):
    guild = member.guild
    channel=discord.utils.get(guild.text_channels, name="beta_welcome")
    embed=discord.Embed(title=f"{member.author.name}さんが参加しました", url="https://bit.ly/2JahfiF", color=0x00ffff)
    embed.set_thumbnail(url="https://nureyon.com/sample/84/check_mark-2-p53.svg?2020-09-09")
    embed.add_field(name="参加者", value="f{member.author.mention}", inline=False)
    embed.set_footer(text="サーバー参加を検知しました")
    await channel.send(f'{member.author.mention}',embed=embed)



token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
