import pycord

@bot.event
async def on_message(message):
    
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
            await message.channel.send(embed=embed)