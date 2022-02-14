import asyncio
import json
import discord
from discord.ext import commands
from hanspell import spell_checker
from hanspell.constants import CheckResult

bot = commands.Bot(command_prefix='!')

with open('token.json', 'r') as f:
    tokens = json.load(f)
token = tokens['token']

with open('server.json', 'r') as g:
    server = json.load(g)
@bot.event
async def on_ready():
    print(bot.user.name)
    game = discord.Game('맞춤법 검사')
    await bot.change_presence(status=discord.Status.online, activity=game)

grammar = True
errors = ""
except_word = ['ㅇㅇ','ㅁㄹ','ㅇㄴ', '흐으음']




@bot.event
async def on_guild_join(guild):
    global server
    print(guild.name)
    if server.get(str(guild.id)) == None:
        server[str(guild.id)] = {"grammar":"True","except":[]}
        with open("server.json", "w") as json_file:
            json.dump(server, json_file, indent=4, ensure_ascii=False)
        with open('server.json', 'r') as g:
            server = json.load(g)
@bot.event
async def on_message(message):
    global server
    global except_csv
    global errors
    global grammar
    global except_word
    global servers
    sent = message.content
    author = message.author
    print(sent, author, message.channel.guild.name)
    if server.get(str(message.channel.guild.id)) == None:
        server[str(message.channel.guild.id)] = {"grammar":"True","except":[]}
        with open("server.json", "w") as json_file:
            json.dump(server, json_file, indent=4, ensure_ascii=False)
        with open('server.json', 'r') as g:
            server = json.load(g)
    if sent == "!도움" or sent == "!도움말" or sent == "!help":
        embed = discord.Embed(title='Made by james1112#9248') # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
        embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/690152774478069787/5386334eea41bbf178a099e7c1342237.png")
        embed.add_field(name='!맞춤법 알림 <on/off> [채널]', value=f'맞춤법 기능을 키거나 끕니다.', inline=True)
        embed.add_field(name='!제외어 <추가/제거> <단어>', value=f'맞춤법 검사에서 제외할 단어를 지정합니다.', inline=True)
        await message.channel.send(embed=embed)
    elif sent == "!맞춤법 알림" or sent == "!맞춤법검사 알림":
        embed = discord.Embed(title="맞춤법 알림", description=f"현재 맞춤법 알림이 {'켜져있습니다.' if server.get(str(message.channel.guild.id)).get('grammar') == 'True' else '꺼져있습니다.'}\n `!맞춤법 알림 <on/off>`을 사용하여 맞춤법 기능을 키거나 끌수있습니다.") # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
        embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        await message.channel.send(embed=embed)
    elif sent == "!맞춤법 알림 끄기" or sent == "!맞춤법 알림 off" or sent == "!맞춤법검사 알림 끄기" or sent == "!맞춤법검사 알림 off":
        #if message.author.guild_permissions.administrator or message.author.id == 690152774478069787:
            server[str(message.channel.guild.id)]['grammar'] = 'False'
            with open("server.json", "w") as json_file:
                json.dump(server, json_file, indent=4, ensure_ascii=False)
            with open('server.json', 'r') as g:
                server = json.load(g)
            await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')
        #else:
        #    embed = discord.Embed(title='오류', description=f"이 명령어를 사용하려면 관리자 권한이 필요합니다.")
        #    embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        #    await message.channel.send(embed=embed)
    elif sent == "!맞춤법 알림 켜기" or sent == "!맞춤법 알림 on" or sent == "!맞춤법검사 알림 켜기" or sent == "!맞춤법검사 알림 on":
        #if message.author.guild_permissions.administrator or message.author.id == 690152774478069787:
            server[str(message.channel.guild.id)]['grammar'] = 'True'
            with open("server.json", "w") as json_file:
                json.dump(server, json_file, indent=4, ensure_ascii=False)
            with open('server.json', 'r') as g:
                server = json.load(g)
            await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')
        #else:
        #    embed = discord.Embed(title='오류', description=f"이 명령어를 사용하려면 관리자 권한이 필요합니다.")
        #    embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        #    await message.channel.send(embed=embed)
    elif sent.startswith("!제외어") or sent.startswith("!금지어"):
        if message.author.guild_permissions.administrator or message.author.id == 690152774478069787:
            if sent[5::] == "":
                embed = discord.Embed(title='맞춤법 제외어', description=f"현재 맞춤법 제외어는 `{server.get(str(message.channel.guild.id)).get('except')}`가 있습니다. \n `!제외어 추가 <단어>`를 사용하여 맞춤법에서 제외할 단어를 추가하거나\n`!제외어 제거 <단어>`를 사용하여 맞춤법에서 제외할 단어에서 제거하세요.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                await message.channel.send(embed=embed)
            elif sent[5::] == "추가":
                server[str(message.channel.guild.id)]["except"].append(sent[5::])
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                await message.channel.send(f"`{sent[5::]}`을(를) 맞춤법 제외어에 추가하였습니다.")
            elif sent[5::] == "제거":
                if sent[5::] in server.get(str(message.channel.guild.id)).get("except"):
                    server[str(message.channel.guild.id)]["except"].remove(sent[5::])
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send(f"`{sent[5::]}`을(를) 맞춤법 제외어에서 제거하였습니다.")
                else:
                    pass
        else:
            embed = discord.Embed(title='오류', description=f"이 명령어를 사용하려면 관리자 권한이 필요합니다.")
            embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
            await message.channel.send(embed=embed)
    elif sent == "!문의" or sent == "!버그" or sent == "!오류":
        embed = discord.Embed(title='버그 리포트', description=f"`!버그 신고 <버그 내용>`를 사용하여 버그를 신고 하거나 깃허브 issue를 통해 버그신고 하세요.\n 버그는 개발자에게 전달되기 때문에 개발자의 대한 모욕 또는 불쾌감을 줄 수 있는 메세지를 보내시면 서비스 사용이 불가해질 수 있습니다.")
        embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        await message.channel.send(embed=embed)
    elif sent.startswith("!버그 신고"):
        if sent[6::] == "":
            embed = discord.Embed(title='버그 리포트', description=f"`!버그 신고 <버그 내용>`를 사용하여 버그를 신고 하세요. \n 버그는 개발자에게 전달되기 때문에 개발자의 대한 모욕 또는 불쾌감을 줄 수 있는 메세지를 보내시면 서비스 사용이 불가해질 수 있습니다.")
            embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            user = await bot.fetch_user(690152774478069787)
            await user.send(f"새로운 버그: {sent[6::]}")
            embed = discord.Embed(title='버그 리포트', description=f"버그가 정상적으로 신고 되었습니다.")
            embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
            await message.channel.send(embed=embed)
        
    elif not message.author.bot and server.get(str(message.channel.guild.id)).get("grammar") == "True" and not sent in server.get(str(message.channel.guild.id)).get("except") and not sent in except_word:
        result = spell_checker.check(sent)
        result.as_dict()
        values = []
        for key, value in result.words.items():
            values.append(value)

        if value == 1:
            errors = '맞춤법'
        elif value == 2:
            errors = '띄어쓰기'
        elif value == 3:
            errors = '표준어 의심'
        elif value == 4:
            errors = '통계적 의심'
        if value != 0:
            embed = discord.Embed(title='{}'.format(errors), description=f"`{sent}`(이)가 아니라 `{result.checked}`입니다. \n\n{message.author.mention}", color=0xFF4500) # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
            embed.set_footer(text=f"{message.author.name} | made by james1112#9248",icon_url = message.author.avatar_url)
            # 하단에 들어가는 조그마한 설명을 잡아줍니다 
            await message.channel.send(embed=embed) # embed를 포함 한 채로 메시지를 전송합니다.
    
bot.run(token)
