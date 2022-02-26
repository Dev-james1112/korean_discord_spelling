import discord
from discord.ext import commands
from discord.commands import Option
import json
from hanspell import spell_checker
from discord.ext import *
import os 




# Setting
bot = commands.Bot(command_prefix="!")

with open("token.json", "r") as f:
    tokens = json.load(f)
token = tokens["token"]



@bot.event
async def on_ready():   
    print(bot.user.name)
    game = discord.Game("맞춤법 검사")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    print(message.content)

# 맞춤법 검사 커맨드/g
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'{error}가 발생')
# 슬래쉬 커맨드
@bot.slash_command(guild_ids = [848422099579174952], description="입력한 내용의 맞춤법을 검사합니다.")
@commands.cooldown(1, 15, commands.BucketType.user)
async def 맞춤법검사(ctx,
    message: Option(str, "맞춤법을 검사할 내용을 입력해주세요.")
):
    
    result = spell_checker.check(message)
    result.as_dict()
    values = []
    for key, value in result.words.items():
        values.append(value)
    print(result)
    if value == 1:
        errors = "맞춤법"
    elif value == 2:
        errors = "띄어쓰기"
    elif value == 3:
        errors = "표준어 의심"
    elif value == 4:
        errors = "통계적 의심"
    if value == 0:
        embed=discord.Embed(title="맞춤법 검사", description="맞춤법 오류가 발견되지 않았습니다.", color=0x44b37f)
        await ctx.respond(embed=embed)
    elif value != 0:
        print(1)
        embed=discord.Embed(title="맞춤법 검사", description="맞춤법 오류가 발견되었습니다. ", color=0xfaa41b)
        embed.add_field(name="원문", value=f"```{message}```", inline=True)
        embed.add_field(name="교정 결과", value=f"```{result.checked}```", inline=True)
        embed.add_field(name="", value='```ansi\n\u001b[0;31m맞춤법    \u001b[0;35m표준어의심\n\u001b[0;32m띄어쓰기    \u001b[0;36m통계적교정```', inline=False)
        print(2)
        await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="맞춤법 검사", description="나중에 실행해주세요.", color=0xf04848)
        await ctx.respond(embed=embed)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}')
# 일반 커맨드
@bot.command(name = "h1elp")
async def help_command(ctx) :
    await ctx.respond("help 명령어 테스트 입니다.")



bot.run(token)