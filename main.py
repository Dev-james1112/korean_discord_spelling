import discord
import asyncio
from hanspell import spell_checker
from hanspell.constants import CheckResult
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

token = '' #token 입력

@bot.event
async def on_ready():
    print(bot.user.name)
    game = discord.Game('맞춤법 검사')
    await bot.change_presence(status=discord.Status.online, activity=game)
@bot.command()
async def setting(ctx, *, option):

    checks = ['check', '검사', '맞춤법검사','spellcheck','rjatk','akwcnaqjqrjatk','촏차','네디ㅣ촏차']
    options = ['option','options','옵션','dhqtus','ㅐㅔ샤ㅐㅜ','ㅐㅔ샤ㅐㅜㄴ']

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
    embed = discord.Embed(title='{}'.format(errors), description=f"`{sent}` -> `{result.checked}`\n\n{message.author.mention}", color=0xFF4500) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
    embed.set_footer(text=f"{message.author.name} | made by james1112",icon_url = message.author.avatar_url)

 # 하단에 들어가는 조그마한 설명을 잡아줍니다 
    await message.channel.send(embed=embed) # embed를 포함 한 채로 메시지를 전송합니다. 


bot.run(token)
