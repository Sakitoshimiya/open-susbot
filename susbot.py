import commands
import discord, os

try:
    import config_override as config
except:
    import config

# Config
prefix = config.prefix
bot_version = config.bot_version

TOKEN = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

# j4f
emojis = ["🇬","🇰","🇪","🇻","🇦","🇾","🇸","🅰️","🇴","😳"]

# Send feedback
class FeedbackButtons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Đưa tiền đây",style=discord.ButtonStyle.red,emoji = "💲")
    async def dua_tien_day(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(f"{interaction.user} kêu ĐƯA TIỀN ĐÂY!!!")
        button.disabled = True
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Bot đào lửa",style=discord.ButtonStyle.gray,emoji = "🔫")
    async def bot_dao_lua(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(f"{interaction.user} kêu BOT ĐÀO LỬA RR!!!")
        button.disabled = True
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="Dev tư bản",style=discord.ButtonStyle.blurple,emoji = "🐧")
    async def dev_tu_ban(self,interaction:discord.Interaction,button:discord.ui.Button):
        print(f"{interaction.user} kêu DEV TƯ BẢN QUÁ!!!")
        button.disabled = True
        await interaction.response.edit_message(view=self)

# Slash command

# Feedback
@tree.command(name = "feedback", description = "Gửi feedback cho dev")
async def button(ctx):
    view = FeedbackButtons()
    view.add_item(discord.ui.Button(label="Forms đòi tiền",style=discord.ButtonStyle.link,url="https://SussyGuy35.github.io/duatienday.html",emoji="😏"))
    print(f"{ctx.user} used feedback commands!")
    await ctx.response.send_message("Nhấn vào nút để gửi feedback cho dev. Nó sẽ làm ngập cái log của thằng dev luôn 😳",view=view)

# Help
@tree.command(name = "help", description = "Hiện hướng dẫn 🐧") 
async def help(ctx):
    print(f"{ctx.user} used help commands!")
    await ctx.response.send_message(commands.help.command_response(prefix))

# Ping
@tree.command(name = "ping", description = "Ping pong ping pong") 
async def ping(ctx):
    print(f"{ctx.user} used ping commands!")
    await ctx.response.send_message(commands.ping.command_response())

# Avatar
@tree.command(name = "avatar", description = "Lấy avatar của ai đó 👀") 
async def get_avatar(ctx,user:discord.User):
    print(f"{ctx.user} used avatar commands!")
    if user.avatar != None:
        embed = discord.Embed(title="Avatar link", description=f"Avatar của {user}", color=0x03e3fc)
        embed.set_image(url = user.avatar.url)
        await ctx.response.send_message(embed = embed)
    else:
        await ctx.response.send_message(f'{user} còn không có avatar 🐧')

# Emoji
@tree.command(name = "emoji", description = "Lấy emoji nào đó 👀") 
async def get_emoji(ctx,emoji: str):
    print(f"{ctx.user} used emoji commands!")
    
    try:
        emoji_to_get = client.get_emoji(int(emoji.split()[0].split(":")[2].replace(">","")))
    except:
        print(f"ERROR: Failed to get emoji. Message: {emoji}")
        emoji_to_get = None
    
    if emoji_to_get != None:
        embed = discord.Embed(title=emoji_to_get.name, description = f"được thêm vào <t:{int(emoji_to_get.created_at.timestamp())}>", color=0x03e3fc)
        embed.set_image(url = emoji_to_get.url)
        await ctx.response.send_message(embed = embed)
    else:
        await ctx.response.send_message('Đã có lỗi xảy ra 🐧. Có thể là do bạn không cung cấp 1 custom emoji đúng 👀.')



# On ready event
@client.event
async def on_ready():
    #tree.clear_commands(guild = None) # Uncomment this to clear all commands
    await tree.sync()
    await client.change_presence(activity = discord.Streaming(name = 'My creator hates me',url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    print(f'open-susbot v{bot_version}')
    print(f'Logged in as {client.user}. Currently on {str(len(client.guilds))} server(s)!')
    print("List of current joined server(s):")
    for guild in client.guilds:
        print(guild)



# On message event
@client.event
async def on_message(message):
    global date, cardgame_data, cardshop_data
    
    # log console
    if message.author == client.user:
        print(">Bot:",message.content)
        return   
    
    # If Eden Eldersong post an annoucemant
    if message.author.id == 915111567299850270 and message.channel.id == 919945978902106134:
        for emoji in emojis:
            await message.add_reaction(emoji)
        return
    
    # Auto react when someone say "gvs"
    if "gvs" in message.content.lower():
        for emoji in emojis:
            await message.add_reaction(emoji)
    
    # If someone use command
    if message.content.startswith(prefix):
        
        # log console
        print(f"{message.author.global_name} at #{message.channel} on {message.guild} : {message.content}")  
        
        # bot user can not use this bot's commands
        if message.author.bot:
            if message.author != client.user:
                await message.channel.send("Bot mà đòi dùng lệnh của bot à 🐧")
                return
        
        # Get requested command
        command = message.content.split()[0].replace(prefix,'')
        
        arg = message.content.replace(f"{prefix}{command} ","")
        
        # Main thing
        match command:
            
            # Debug
            case 'debug':
                await message.channel.send(f"user_id: {message.author.id}, channel_id: {message.channel.id}, guild: {message.guild}")
            
            # Help
            case 'help':
                await message.channel.send(commands.help.command_response(prefix))
            
            # Ping pong ping pong
            case 'ping':
                await message.channel.send(commands.ping.command_response())

            # Echo
            case 'echo':
                await message.channel.send(commands.echo.command_response(arg))
            
            # Pick
            case 'pick':
                await message.channel.send(commands.pick.command_response(arg))  
            
            # Random caps
            case 'randcaps':
                await message.channel.send(commands.randcaps.command_response(arg))  
            
            # Gacha
            case 'gacha':
                userid = str(message.author.id)
                username = message.author.global_name
                command_response = commands.gacha.command_response(message.content,prefix,userid,username)
                user_level_up_response = commands.gacha.check_if_user_level_up(userid,username)
                if command_response != None:
                    await message.channel.send(command_response)
                if user_level_up_response != None:
                    await message.channel.send(user_level_up_response)
                commands.gacha.save()    
            
            # osu!
            case 'osu':
                await message.channel.send(commands.osu.command_response(message.content))
            
            # emoji
            case 'emoji':
                rs = commands.emoji.command_response(client,arg)
                if type(rs) == str:
                    await message.channel.send(rs)
                else:
                    await message.channel.send(embed = rs)
            
            # Invalid command
            case _:
                await message.channel.send("Lệnh đó không tồn tại!")
        
client.run(TOKEN)