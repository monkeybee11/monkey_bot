from datetime import datetime as clock
import discord, asyncio, time, os, json, random, requests, python_weather
from discord.ext import commands, tasks
from pynput.keyboard import Key, Controller
from discord import Guild
from dotenv import load_dotenv
from os import getenv

os.chdir("/home/pi/Desktop/monkey bot discord")

load_dotenv()

token = getenv("monkey_bot")



# to do list
# banana game
# come up with more games


password = False
egg = clock.now()
sausage = egg.strftime("%I:%M %p")  # strftime format to put time in to a string
pocketwatch = clock.utcnow()
oimate = commands.Bot(command_prefix = "!") # set hte prefix
fishNchips = Controller()

@oimate.event
async def on_ready(): #this is where the bot brain starts to work
    print("discord")  # print() sends to the CMD not to discord

@oimate.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        WAIT = "placeholder text for cooldown comeback in {:.2f}s".format(error.retry_after)
        await ctx.send(WAIT)

#saving this emoji id for later
    # <a:TargetAnim:927671875834875974>
    
#######################################
##         random stuff              ##
#######################################

@oimate.command(help = "nailed it")
async def nailedit(ctx):
    nail = random.randint(1,2)
    if nail == 1:
        await ctx.send("<:NailedItDan:887162185166516256>")
    elif nail == 2:
        await ctx.send("<:mnkyNailedIt:739908983833362433>")
        
        
@oimate.command(help = "#dadjoke")
async def dadjoke(ctx):
    joke = random.randint(1,2)
    if joke == 1:
        await ctx.send("<:DadJokeDan:887164212261056574>")
    elif joke == 2:
        await ctx.send(" <:mnkyDadJoke:704518638706753588>")
        
        
@oimate.command(help = "rolls a d20")
async def d20(ctx):
    roll_time = random.randint(1,10)
    await ctx.send("https://tenor.com/view/neverwinter-d20-dice-gif-22267317", delete_after=roll_time)
    await asyncio.sleep(roll_time)
    d20 = random.randint(1,20)
    await ctx.send(f"{ctx.author.name} rolled a {d20}")

###########################
##        a hug          ##
###########################

@oimate.command(help = "hugs a member")
async def hug(ctx,member:discord.Member):
    miss = random.randint(1,100)
    if miss >= 90 and miss < 95:
        await ctx.send(f"u went to hug {member.name} but fell over :adhesive_bandage: ")
    elif miss <= 89:
        await ctx.send(f"{ctx.author.name} gave {member.name} a big")
        await ctx.send("<a:hug:766704436625670166>")
    elif miss >= 95:
        await ctx.send(f"u ran past {member.name} and huged a random bear")
        

#############################
##     get others wet      ##
#############################

@oimate.command(help = "shoot someone with a water gun")
async def pew(ctx,member:discord.Member):
    miss = random.randint(1,100)
    if miss <= 89:
        await ctx.send(f"{member.name} got shot by {ctx.author.name}")
        await ctx.send("<a:TargetAnim:927671875834875974>")
    elif miss >= 90:
        name = []
        for member in ctx.guild.members:
            name.append(member.name)
        await ctx.send(f"{ctx.author.name} missed there target and shot {random.choice(name)}") 
        await ctx.send("<a:TargetAnim:927671875834875974>")
        await ctx.send(f"{ctx.author.name} may want to pratice there aim at the target game")



##########################################
##               weather                ##
##########################################

## this was easyer then making my own weather system

@oimate.command(help ="tells you the weather over the wildwestcarni AND the jungle party")
async def weather(ctx):
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.find("Boston")
    weather_check = weather.current.sky_text
    if weather_check == "Partly Sunny": # little cloudy but sunny
        await ctx.send(":partly_sunny:")
    elif weather_check == "Mostly Cloudy": # sunny cloud
        await ctx.send(":white_sun_cloud:")
    elif weather_check == "Sunny" or weather_check == "Clear": #lots of sun
        await ctx.send(":sunny:")
    elif weather_check == "Rain" or weather_check == "Light Rain": #rain
        await ctx.send(":cloud_rain:")
    elif weather_check == "Cloudy": #clouds
        await ctx.send(":cloud:")
    elif weather_check == "Thunderstorm":
        await ctx.send(":thunder_cloud_rain:")
    elif weather_check == "Partly Cloudy":
        await ctx.send(":white_sun_small_cloud:")
    else:
        await ctx.send(weather_check)#posts name of weather to discord if not above

    await client.close() #we dont need weather api anymore close it



###########################################
##            ticket crunecy             ##
###########################################


   # await ctx.send(f"{ticket} <:DanTix:919966342797463552>")

@oimate.command(help = "shows u whats in your pocket")
async def pocket(ctx):

    await open_account(ctx.author)
    user = ctx.author
    users = await get_ticket_data()


    # note if any new items are added to this list manualy add them to the ticketbank.json file
    ticket_amt = users[str(user.id)]["ticket"]
    banana_amt = users[str(user.id)]["banana"]
    snow_amt = users[str(user.id)]["snowball"]

    em = discord.Embed(title = f"inside {ctx.author.name}'s pocket is", color = discord.Color.red())
    em.add_field(name = "<:DanTix:919966342797463552>", value = ticket_amt, inline = True)
    em.add_field(name = "<:mnkyThrow:704518598764527687>", value = banana_amt, inline = True)
    em.add_field(name = "<:2021_Snowsgiving_Emojis_001_Snow:917929344914030642>",value = snow_amt, inline = True)
    await ctx.send(embed = em)

async def open_account(user):

    users = await get_ticket_data()


    if str(user.id) in users:
        return False
    else:
        #this is where we set the names for the database in the json file
        users[str(user.id)] = {}
        users[str(user.id)]["ticket"] = 0
        users[str(user.id)]["banana"] = 0
        users[str(user.id)]["snowball"] = 0

    with open("ticketbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_ticket_data():
    with open ("ticketbank.json","r") as f:
        users = json.load(f)
    return users

async def update_pocket(user,change = 0,mode = "ticket"):
    users = await get_ticket_data()
    users[str(user.id)][mode] += change

    with open("ticketbank.json","w") as f:
        json.dump(users,f)

    bal = [user[str(user.id)]["ticket"]]
    return bal


############################################
##            ticket shop                 ##
############################################

shopshelf = [
    {"name":"banana","price":2,"desc":"<:mnkyThrow:704518598764527687>"}
    ]

@oimate.command(help = "see what u can extange tickets for(useless atm)")
async def shop(ctx):
    shopbed = discord.Embed(title = "ticket booth")

    for item in shopshelf:
        name = item["name"]
        price = item["price"]
        desc = item["desc"]
        shopbed.add_field(name = name, value = f"{price} | {desc}")

    await ctx.send(embed = shopbed)
###########################################
##               top 10                  ##
###########################################


@oimate.command(help = "shows the top10 ticket holders(broken)")
async def top10(ctx,x = 10):

    users = await get_ticket_data()

    top10 = {}
    total = []

    for user in users:
        name = int(user)
        total_amt = users[user]["ticket"]
        top10[total_amt] = name
        total.append(total_amt)

    total = sorted(total,reverse=True)

    em = discord.Embed(title=f"top {x} ticket holders")

    index = 1
    for amt in total:
        id_ = top10[amt]
        member = await oimate.fetch_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt} <:DanTix:919966342797463552>", inline = False)

        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)
    
    
@oimate.command(help = "shows the top10 banana holders")
async def topb(ctx,x = 10):

    users = await get_ticket_data()

    top10 = {}
    total = []

    for user in users:
        name = int(user)
        total_amt = users[user]["banana"]
        top10[total_amt] = name
        total.append(total_amt)

    total = sorted(total,reverse=True)

    em = discord.Embed(title=f"top banana")

    index = 1
    for amt in total:
        id_ = top10[amt]
        member = await oimate.fetch_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt} <:mnkyThrow:704518598764527687>", inline = False)

        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

############################################
##              snow game                 ##
############################################

@oimate.command(help = "when its snowing over the wildwestcarni u can scoop up some snowballs")
@commands.cooldown(1,30,commands.BucketType.user)
async def scoop(ctx):

    #declare the client. format defults to the metric system(C, km/h, ect)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    #fetch a weather forcast from a city
    weather = await client.find("Boston")

    snow = random.randint(1,3)

    check_weather = weather.current.sky_text

    if check_weather == "Light Snow" and snow == 1:

        await ctx.send(f"{ctx.author} gathered a snowball")

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        users[str(user.id)]["snowball"] += 1
        with open("ticketbank.json","w") as f:
            json.dump(users,f)

    elif check_weather == "Light Snow" and snow == 2:

        await ctx.send(f"{ctx.author} was gathering snowballs when they stumbled apon someones hidden stash")

        stash = random.randint(1,5)

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        users[str(user.id)]["snowball"] += stash
        with open("ticketbank.json","w") as f:
            json.dump(users,f)

    elif check_weather == "Light Snow" and snow == 3:

        await ctx.send(f"{ctx.author} was a bout to scoop up some snow when they heard some one yelling ***next time dont wear yellow tinted goggles***")

    elif check_weather != "Light Snow":

        await ctx.send("there is no snow on the ground")

    await client.close()


@oimate.command(help = "throws a snowball at someone")
async def shoke(ctx,member:discord.Member):
    
    aim = random.randint(1,100)
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    
    if users[str(user.id)]["snowball"] == 0:
        
        no_snow=discord.Embed(title = "snowball fight")
        no_snow.set_author(name = (ctx.author.name))
        no_snow.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        no_snow.add_field(name = f"you have no snowballs....did they melt? and" , value = "<:puppy_eye_monkey:894525128807940096>", inline = True)
        no_snow.add_field(name = f"{member.name} is proberly anoyed at the ping", value = "<:blob_fail:777073048389419009>" , inline = True)
        await ctx.send(embed=no_snow)


    elif users[str(user.id)]["snowball"] > 0 and aim <= 59:
        
        users[str(user.id)]["snowball"] -=1
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        snow_hit =discord.Embed(title = "snowball fight")
        snow_hit.set_author(name = (ctx.author.name))
        snow_hit.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_hit.add_field(name = f"{ctx.author.name} throws a snowball at" , value = "<:laughtingmonkey:894525186655780864>", inline = True)
        snow_hit.add_field(name = f"{member.name} is now a snowman", value = "<:2021_Snowsgiving_Emojis_001_Snum:917929344997937162>" , inline = True)
        await ctx.send(embed=snow_hit)
        
    elif users[str(user.id)]["snowball"] >1 and aim >= 60:
        
        users[str(user.id)]["snowball"] -= 1
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        snow_miss = discord.embed(title = "snowball fight")
        snow_miss.set_author(name = (ctx.author.name))
        snow_miss.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_miss.add_field(name = f"{ctx.author.name} throws a snowball at" , value = "<:mnkyDKS:780614148068605983>", inline = True)
        snow_miss.add_field(name = f"{member.name} but it misses", value = "come up with something better later", inline = True)
        await ctx.send(embed=snow_miss)
        
############################################
##   banana game for DKS server           ##
############################################

@oimate.command(help ="shake the banana tree")
@commands.cooldown(1,60,commands.BucketType.user)
async def shake(ctx):

    tree_shake = random.randint(1,3)
    failed_shake = random.randint(1,4)


    if tree_shake == 1:
        await ctx.send(f"{ctx.author.name} shook the banana tree and gained 1 <:mnkyThrow:704518598764527687>  ")

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author

        users[str(user.id)]["banana"] += 1

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

    elif tree_shake == 2:

        if failed_shake == 1:
            await ctx.send(f"{ctx.author.name} shook the tree to hard and it fell over woops")

        elif failed_shake == 2:
            await ctx.send(f"{ctx.author.name} gave the banana tree a good shake BUT u upset a sleeping parrot who swooped down and attacked. you lost 1 <:mnkyThrow:704518598764527687>")

            await open_account(ctx.author)
            users = await get_ticket_data()
            user = ctx.author

            users[str(user.id)]["banana"] -= 1
            if users[str(user.id)]["banana"] < 0:
                users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f)

        elif failed_shake == 3:
            await ctx.send(f"{ctx.author.name} shook the banana tree and a disco ball fell down and went SMASH")

        elif failed_shake == 4:
            await ctx.send(f"{ctx.author.name} shook the banana tree and angered a monkey you now have monkey poop on your head and no banans")

            await open_account(ctx.author)
            users = await get_ticket_data()
            user = ctx.author

            users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f)

    elif tree_shake == 3:
        await ctx.send(f"{ctx.author.name} shook the tree AND OH WOW 2 <:mnkyThrow:704518598764527687>  fell from the tree")

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author

        users[str(user.id)]["banana"] += 2

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

#######################
## catch throw block ##
#######################



## Defines a custom select containing the options
## that the user can chose, the callback function
##of this class is called when the user changes there choice
#class Dropdown(discord.ui.select):
#    def __init__(self):
#
#
##        #set the options that will be presented inside the dropdown
#        options = [
#            discord.SelectOption(label="DODGE",description="dodge the banana 50%"),
#            discord.SelectOption(label="BLOCK",description="block the banana 30%"),
#            discord.SelectOption(label="CATCH",description="catch the banana 15%"),
#            ]
#
##        #the placeholder is whatwill be shown when no option is chosen
##        #the min max value indicates we can only pick 1 of the 3 options
##        #the options parameter defines the dropdown option. we defined this above
#        super().__init__(
#            placeholder="click here to dodge block catch",
#            min_values =1,
#            max_values=1,
#            options=options,
#        )
#
#    async def callback(self, interaction: discord.Interaction):
##        #user the interaction object to send a responce message containing
##        # the users answer the self object refers to the
##        #select object, and the values attribute gets a list of the users
##        #selected options we only want the 1st one
#        await interaction.response.send_message("if u see this monkey forgot to remove this...or u picked {self.values[0]}")
#
#        if self.value == [1]:
#
#            await ctx.send(f"{member.name} has tryed to dodge")
#            doge = random.randint(0,100)
#            if doge <=49 :
#                await ctx.send(f"{ctx.author} dodges the banana with monkey-like reflexes!")
#
#            elif doge >= 50:
#                await ctx.send(f"{ctx.author} dodges but the banana was TOO quick {ctx.author} gets smacked in the face and drops some bananas")
#                l = random.randint(2,4)
#                await update_pocket(member, - l)
#
#                with open("ticketbank.json","w") as f:
#                    json.dump(users,f)
#
#        elif self.value == [2]:
#            await ctx.send(f"{ctx.author} has tryed to block")
#            block = random.randint(0,100)
#            if block <= 25 :
#                await ctx.send(f"{ctx.author} blocks the banana Whew that was close!")
#
#            elif block >= 26:
#                b = random.randint(3,7)
#                await ctx.send(f"{ctx.author} trys to block the banana but it slips through and smacks {ctx.author} right in the face and they drop {b} more bananas!")
#                await update_pocket(member, - b)
#
#                with open("ticketbank.json","w") as f:
#                    json.dump(users,f)
#
#        elif self.value == [3]:
#            await ctx.send(f"{ctx.author} is trying to catch")
#            catch = random.randint(0,100)
#            if catch <= 15:
#                cw = random.randint(5,15)
#                await ctx.send(f"displaying amazing reflexes {ctx.author} catches the banana backs into the banana tree and catches {cw} more bananas")
#                await update_pocket(member, + cw)
#
#                with open("ticketbank.json","w") as f:
#                    json.dump(users,f)
#
#
#class DropdownView(discord.ui.View):
#    def __init__(self):
#        super().__init__()
#
##        # adds the dropdown to our view object
#        self.add_item(Dropdown())
#
#@oimate.command(help = "throw a banana at someone else (broken)")
#async def throw(ctx, member:discord.Member):
#
#
#    view = DropDownView()
#
#    await ctx.send(f"{ctx.author.name} picked", view=view)


############################################
##target minigame for DKS server          ##
############################################

@oimate.command(help = "try your luck come win a prize")
@commands.cooldown(1,60,commands.BucketType.user) #1 time , 60seccon cooldown , per user
async def target(ctx):

    #declare the client. format defults to the metric system(C, km/h, ect)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    #fetch a weather forcast from a city
    weather = await client.find("Boston")
    weather_check = weather.current.sky_text
    target_chance = ["1", "5", "0", "-1", "lilly"] #we make a list of the random options
    randomList = random.choices( target_chance, weights=(48, 2, 25, 25, 0.01), k=1) # weighted the random chances so some options happen more then others , k=howmeny options form the list we want


    if weather_check == "Light Rain" or weather_check == "Rain":

        await ctx.send("the carni is shutdown becase of rain come back later")


    elif randomList == ["1"]: # 1 ticket

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        ticket_amt = users[str(user.id)]["ticket"]

        users[str(user.id)]["ticket"] += 1

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game")
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:DanWater5:919977398164914227>", value = "WOOO BOY you won ya self a ticket partner <:DanTix:919966342797463552>", inline = True)
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.send(embed=em)

    elif randomList == ["5"]: # 5 ticket

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        ticket_amt = users[str(user.id)]["ticket"]

        users[str(user.id)]["ticket"] += 5

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game")
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:CactusDan:884518308404162590>", value = "ABB BUW BA BA hey now partner ya soaked my new jacket won 5 <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552>", inline = True)
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.send(embed=em)

    elif randomList == ["0"]: # miss

        em=discord.Embed(title = "target game")
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:Target:887076837392527400>", value = "well well welly well well looks like ya missed the target you get nothing")
        await ctx.send(embed=em)

    elif randomList == ["-1"]: # stop hitting your self

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        ticket_amt = users[str(user.id)]["ticket"]

        users[str(user.id)]["ticket"] -= 1
        if users[str(user.id)]["ticket"] < 0:
            users[str(user.id)]["ticket"] = 0

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game")
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name ="<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:SplashDan:887167642417373246>", value = "how in tar nashens did u mannage to soak your self? ***you droped a ticket***")
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.send(embed = em)

    elif randomList == ["lilly"]: # Y DID U HIT LILLY

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        ticket_amt = users[str(user.id)]["ticket"]

        users[str(user.id)]["ticket"] -= 10
        if users[str(user.id)]["ticket"] < 0:
            users[str(user.id)]["ticket"] = 0


        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game")
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:DanCat:704518407822901339>", value = "WO WO WOOOOOOO now you just gona soaked lilly ill be taking 10 tickets to dry her fur")
        em.add_field(name="you now have" , value = new_amt + "<:DanTix:919966342797463552>",inline = False)
        await ctx.send(embed = em)

    await client.close()


############################################
##monkeys attempted at gameing for discord##
############################################

##the stuff in this area exsplains it self no need for comments

@oimate.command(help = "only monkey can use this to start discordplays gamein VC")
async def gamestart(ctx):
    global password
    if ctx.author.id == 113051316225368064: #this is MY discord id so only me can use this commarnd
        password = True
    elif ctx.author.id == 119791596681166848: #this is monkeyDKS id so me can be cheaky and give him a specal responce
        await ctx.send("sorry DKS you are not the right monkey for this command ***froundy face*** BUT heres a ticket to the carnie <:DanTix:919966342797463552>")
    else:
        await ctx.send("you are not monkey only he can start games")

@oimate.command(help = "only monkey can use this to end the game")
async def gamestop(ctx):
    global password
    if ctx.author.id == 113051316225368064:
        password = False
    elif ctx.author.id == 119791596681166848:
        await ctx.send("sorry DKS you are not the right monkey for this command ***froundy face*** BUT heres a ticket to the carnie <:DanTix:919966342797463552>")
    else:
        await ctx.send("you are not monkey only he can stop games")

@oimate.command(help = "presses the up arrow")
async def up(ctx):
    global password
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.tap(Key.up)

@oimate.command(help = "presses the down arrow")
async def down(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.tap(Key.down)

@oimate.command(help = "presses the left arrow")
async def left(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.tap(Key.left)

@oimate.command(help = "presses the right arrow")
async def right(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.tap(Key.right)

@oimate.command(help = "moves the mouse up")
async def mup(ctx):
    if password == False:
        await ctx.send("theres no game playing atm check with monkey")
    elif password == True:
        fishNchips.move(0, 15)

@oimate.command(help = "moves the mouse down")
async def mdown(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.move(0,-15)

@oimate.command(help = "moves the mouse left")
async def mleft(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.move(-15,0)

@oimate.command(help = "moves the mouse right")
async def mright(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.move(15,0)

@oimate.command(help = "clicks left mouse button")
async def lclick(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.press(Button.left)
        fishNchips.release(Button.left)

@oimate.command(help = "clicks right mouse button")
async def rclick(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    elif password == True:
        fishNchips.press(Button.right)
        fishNchips.release(Button.right)


@oimate.command(help = "presses the backspace")
async def reset(ctx):
    if password == False:
        await ctx.send("there is no game playing atm check with monkey")
    if password == True:
        fishNchips.tap(Key.backspace)

##########################################################################
## time stuff for choco server so ppl get pinged to colect there cookies##
##########################################################################

@oimate.command(help = "displays the local time for monkeybot")
async def time(ctx): #say 8time in discord to have monkeybot say the time....this was added for testing resons
    await ctx.send(sausage) #was hungery when typing out the veriables


@oimate.command(help = "dont use this commarnd unless your monkeybee11")
async def start(ctx): #the blue word is the commarnd u type in discord
    if ctx.author.id == 113051316225368064:
        print("ok")
        while True:

            await asyncio.sleep(5)
            timer = clock.now() #monkey this veriable is here to refresh its time check
            if(timer.hour == 17 and timer.minute == 35): #checking if the time is what ever numbers ive typed
                await ctx.send('<@&888038726154993714> oi oi paycheck time come and get your<:Galaxy_Cookie:776762120686927896><:Galaxy_Cookie:776762120686927896><:Galaxy_Cookie:776762120686927896>') # ALLWAYS PUT "await ctx.send('') if u want it to speak in discord
                print("do we have to pay the workers?") # print will only post to my CMD so dosnt matter if its a little mean
                await asyncio.sleep(60) #this is ment to be a 60secon timer so it only says the message once insted of everytick for that minnet
    elif ctx.author.id != 113051316225368064:
        await ctx.send(f"sry {ctx.author.name} only <@113051316225368064> can use this command to stop me from spamming in random channels :thumbsup:")

@oimate.command(help = "ignore this")
async def test(ctx):
    if ctx.author.id == 113051316225368064:
        await ctx.send("<@&888038726154993714> this is a test let me know if u got pinged")

oimate.run(token)
