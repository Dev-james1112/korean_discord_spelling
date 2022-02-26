# <----------module---------->
import json
import discord
from discord.ext import commands
from hanspell import spell_checker
from hanspell.constants import CheckResult
import asyncio


# <----------bot prefix---------->
bot = commands.Bot(command_prefix='!')


# <----------token---------->
with open('token.json', 'r') as f:
    tokens = json.load(f)
token = tokens['token']


# <----------server.json---------->
with open('server.json', 'r') as g:
    server = json.load(g)


# <----------봇 상태 설정---------->
@bot.event
async def on_ready():
    print(bot.user.name)
    game = discord.Game('맞춤법 검사')
    await bot.change_presence(status=discord.Status.online, activity=game)


# <----------!변수 설정---------->
grammar = True
errors = ""
except_word = ['ㅇㅇ','ㅁㄹ','ㅇㄴ', '흐으음','뭐해']
commands = ['!맞춤법 알림', '!맞춤법 알림 끄기', '!맞춤법 알림 off', '!맞춤법검사 알림 끄기','!맞춤법검사 알림 off','!맞춤법 알림 켜기','!맞춤법 알림 on','!맞춤법검사 알림 켜기','!맞춤법검사 알림 on']

@bot.command()
async def hello(ctx):
	await ctx.send("Hello!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("명령어를 찾지 못했습니다")
        
# <----------길드 설정---------->
@bot.event
async def on_guild_join(guild):
    global server
    print(guild.name)
    if server.get(str(guild.id)) == None:
        server[str(guild.id)] = {"grammar":"True","except":[],"permission":'3'}
        with open("server.json", "w") as json_file:
            json.dump(server, json_file, indent=4, ensure_ascii=False)
        with open('server.json', 'r') as g:
            server = json.load(g)

@bot.command()
async def asdf(ctx):
    embed = discord.Embed(title='맞춤법 검사기에 대한 도움말', description='Made by james1112#9248') # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다 
    embed.set_footer(text=f"**<필수 옵션>**   **[선택 옵션]**")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/690152774478069787/5386334eea41bbf178a099e7c1342237.png")
    embed.add_field(name='!맞춤법 알림 [채널]', value=f'맞춤법 기능을 키거나 끕니다. (토글) 뒤에 채널을 입력하면 특정 채널에서만 키거나 끕니다.', inline=True)
    embed.add_field(name='!제외어 <추가/제거> <단어>', value=f'맞춤법 검사에서 제외할 단어를 지정합니다.', inline=True)
    embed.add_field(name='!문의', value=f'버그 또는 수정할 내용을 신고합니다. `!버그` 또는 `!오류`로도 사용할수 있습니다.', inline=True)
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    # <----------변수 선언---------->
    global server
    global errors
    global grammar
    global except_word
    sent = message.content
    author = message.author
    permission = server.get(str(message.channel.guild.id)).get("permission")
    print(sent, author, message.channel.guild.name)
    # <----------json 파일 생성---------->
    if server.get(str(message.channel.guild.id)) == None:
        server[str(message.channel.guild.id)] = {"grammar":"True","except":[],"permission":'3'}
        with open("server.json", "w") as json_file:
            json.dump(server, json_file, indent=4, ensure_ascii=False)
        with open('server.json', 'r') as g:
            server = json.load(g)
    # <----------!도움---------->
    if sent == "!도움" or sent == "!도움말" or sent == "!help":
        loop = asyncio.get_event_loop() 
        loop.run_until_complete(help_command(message))    

    '''
    if permission == "1":
        if message.author.guild_permissions.administrator:
            # <----------!맞춤법 알림---------->
            if sent.startswith("!맞춤법 알림"):
                if not sent[7::] == "":
                    pass
                else:
                    if server.get(str(message.channel.guild.id)).get("grammar") == 'True':
                        server[str(message.channel.guild.id)]['grammar'] = 'False'
                        with open("server.json", "w") as json_file:
                            json.dump(server, json_file, indent=4, ensure_ascii=False)
                        with open('server.json', 'r') as g:
                            server = json.load(g)
                        await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')
                    elif server.get(str(message.channel.guild.id)).get("grammar") == 'False':
                        server[str(message.channel.guild.id)]['grammar'] = 'True'
                        with open("server.json", "w") as json_file:
                            json.dump(server, json_file, indent=4, ensure_ascii=False)
                        with open('server.json', 'r') as g:
                            server = json.load(g)
                        await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')

            
            # <----------!맞춤법 알림 끄기---------->
            elif sent == "!맞춤법 알림 끄기" or sent == "!맞춤법 알림 off" or sent == "!맞춤법검사 알림 끄기" or sent == "!맞춤법검사 알림 off":
                    server[str(message.channel.guild.id)]['grammar'] = 'False'
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')

            # <----------!맞춤법 알림 켜기---------->
            elif sent == "!맞춤법 알림 켜기" or sent == "!맞춤법 알림 on" or sent == "!맞춤법검사 알림 켜기" or sent == "!맞춤법검사 알림 on":
                    server[str(message.channel.guild.id)]['grammar'] = 'True'
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')

            # <----------!제외어---------->
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
    elif permission == "2":
        if message.author.guild_permissions.manage_messages or message.author.guild_permissions.administrator:
            # <----------!맞춤법 알림---------->
            if sent == "!맞춤법 알림" or sent == "!맞춤법검사 알림":
                if server.get(str(message.channel.guild.id)).get("grammar") == 'True':
                    server[str(message.channel.guild.id)]['grammar'] = 'False'
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')
                elif server.get(str(message.channel.guild.id)).get("grammar") == 'False':
                    server[str(message.channel.guild.id)]['grammar'] = 'True'
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')
                
            # <----------!맞춤법 알림 끄기---------->
            elif sent == "!맞춤법 알림 끄기" or sent == "!맞춤법 알림 off" or sent == "!맞춤법검사 알림 끄기" or sent == "!맞춤법검사 알림 off":

                server[str(message.channel.guild.id)]['grammar'] = 'False'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')


            # <----------!맞춤법 알림 켜기---------->
            elif sent == "!맞춤법 알림 켜기" or sent == "!맞춤법 알림 on" or sent == "!맞춤법검사 알림 켜기" or sent == "!맞춤법검사 알림 on":
                server[str(message.channel.guild.id)]['grammar'] = 'True'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')


            # <----------!제외어---------->
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
            embed = discord.Embed(title='오류', description=f"이 명령어를 사용하려면 메세지 관리 권한 또는 관리자 권한이 필요합니다.")
            embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
            await message.channel.send(embed=embed)
    elif permission == "3":
        # <----------!맞춤법 알림---------->
        if sent == "!맞춤법 알림" or sent == "!맞춤법검사 알림":
            if server.get(str(message.channel.guild.id)).get("grammar") == 'True':
                    server[str(message.channel.guild.id)]['grammar'] = 'False'
                    with open("server.json", "w") as json_file:
                        json.dump(server, json_file, indent=4, ensure_ascii=False)
                    with open('server.json', 'r') as g:
                        server = json.load(g)
                    await message.channel.send('맞춤법 검사가 꺼졌습니다. 다시 키시려면 `!맞춤법 알림 on`를 입력하세요.')
            elif server.get(str(message.channel.guild.id)).get("grammar") == 'False':
                server[str(message.channel.guild.id)]['grammar'] = 'True'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                await message.channel.send('맞춤법 검사가 켜졌습니다. 끄시려면 `!맞춤법 알림 off`를 입력하세요.')


        # <----------!맞춤법 알림 끄기---------->
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


        # <----------!맞춤법 알림 켜기---------->
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
        

        # <----------!제외어---------->
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
        '''
    # <----------!문의---------->
    if sent == "!문의" or sent == "!버그" or sent == "!오류":
        embed = discord.Embed(title='버그 리포트', description=f"`!버그 신고 <버그 내용>`를 사용하여 버그를 신고 하거나 깃허브 issue를 통해 버그신고 하세요.\n 버그는 개발자에게 전달되기 때문에 개발자의 대한 모욕 또는 불쾌감을 줄 수 있는 메세지를 보내시면 서비스 사용이 불가해질 수 있습니다.")
        embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
        await message.channel.send(embed=embed)
    # <----------!버그 신고---------->
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
    # <----------!권한---------->
    elif sent.startswith('!권한'):
        if message.author.guild_permissions.manage_messages or message.author.guild_permissions.administrator:
            if sent[4::] == "":
                embed = discord.Embed(title='권한 설정', description=f"명령어의 권한을 설정합니다. `!권한 <레벨>`로 사용할수 있습니다.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                embed.add_field(name='레벨 1 (보안 레벨 최상)', value=f'`!맞춤법 알림`,`!제외어` 등의 명령어를 관리자만 사용할수 있습니다.', inline=True)
                embed.add_field(name='레벨 2 (보안 레벨 중)', value=f'`!맞춤법 알림`,`!제외어` 등의 명령어를 관리자와 메세지 관리 권한이 있는 사용자만 사용할수 있습니다.', inline=True)
                embed.add_field(name='레벨 3 (보안 레벨 하)', value=f'`!권한` 명령어를 제외한 모든 명령어를 사용자가 사용할수 있습니다.', inline=True)
                await message.channel.send(embed=embed)
            elif sent[4::] == "1":
                server[str(message.channel.guild.id)]["permission"] = '1'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                embed = discord.Embed(title='권한 설정', description=f"권한이 레벨 `1`로 설정 되었습니다.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                await message.channel.send(embed=embed)
            elif sent[4::] == "2":
                server[str(message.channel.guild.id)]["permission"] = '2'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                embed = discord.Embed(title='권한 설정', description=f"권한이 레벨 `2`로 설정 되었습니다.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                await message.channel.send(embed=embed)
            elif sent[4::] == "3":
                server[str(message.channel.guild.id)]["permission"] = '3'
                with open("server.json", "w") as json_file:
                    json.dump(server, json_file, indent=4, ensure_ascii=False)
                with open('server.json', 'r') as g:
                    server = json.load(g)
                embed = discord.Embed(title='권한 설정', description=f"권한이 레벨 `3`로 설정 되었습니다.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title='권한 설정', description=f"명령어의 권한을 설정합니다. `!권한 <레벨>`로 사용할수 있습니다.")
                embed.set_footer(text=f"{message.author.name}" ,icon_url = message.author.avatar_url)
                embed.add_field(name='레벨 1 (보안 레벨 최상)', value=f'`!맞춤법 알림`,`!제외어` 등의 명령어를 관리자만 사용할수 있습니다.', inline=True)
                embed.add_field(name='레벨 2 (보안 레벨 중)', value=f'`!맞춤법 알림`,`!제외어` 등의 명령어를 관리자와 메세지 관리 권한이 있는 사용자만 사용할수 있습니다.', inline=True)
                embed.add_field(name='레벨 3 (보안 레벨 하)', value=f'`!권한` 명령어를 제외한 모든 명령어를 사용자가 사용할수 있습니다.', inline=True)
                await message.channel.send(embed=embed)
    # <----------!patch---------->
    elif sent.startswith('!patch'):
        await message.channel.send(f'**20220217-1 패치** \n + `!맞춤법 알림 명령어` 토글 기능 추가')
    # <----------맞춤법 검사---------->
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
# <----------봇 실행---------->
bot.run(token)
