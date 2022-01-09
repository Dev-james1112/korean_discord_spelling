import discord
import asyncio
from hanspell import spell_checker
from hanspell.constants import CheckResult
from discord.ext import commands
from pip.req import parse_requirements
bot = commands.Bot(command_prefix='!')

token = 'OTIzMTYzOTIyNTcwMzAxNDkx.YcMBZg.Ueiwr2gob83X_WFzK__v0-6YozE'
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
@bot.event
async def on_ready():
    print(bot.user.name)
    game = discord.Game('맞춤법 검사')
    await bot.change_presence(status=discord.Status.online, activity=game)


errors = ""
@bot.event
async def on_message(message):
    sent = message.content
    result = spell_checker.check(sent)
    result.as_dict()
    for key, value in result.words.items():
        print(key, value)
    if value == 1:
        errors = '맞춤법'
    elif value == 2:
        errors = '띄어쓰기'
    elif value == 3:
        errors = '표준어 의심'
    elif value == 4:
        errors = '통계적 의심'
    embed = discord.Embed(title='{}'.format(errors), description=f"멍청아  `{sent}`(이)가 아니라 `{result.checked}`임 ㅅㄱ\n\n{message.author.mention}", color=0xFF4500) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
    embed.set_footer(text=f"{message.author.name} | made by james1112",icon_url = message.author.avatar_url)

 # 하단에 들어가는 조그마한 설명을 잡아줍니다 
    await message.channel.send(embed=embed) # embed를 포함 한 채로 메시지를 전송합니다. 


bot.run(token)
