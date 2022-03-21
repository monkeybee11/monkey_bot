############################################################################################################################################################################
## if you are reading this on github and your not monkey 99.9% of the comments are for me 4 weeks later from typing the code so sry if theres to much comments for you XD ##
############################################################################################################################################################################
from datetime import datetime as clock
import discord, asyncio, time, os, json, random, requests, python_weather
from discord.ext import commands, tasks
from pynput.keyboard import Key, Controller
from discord import Guild
from dotenv import load_dotenv
from os import getenv
from PIL import Image, ImageDraw, ImageFont
import numpy

os.chdir("/home/pi/Desktop/monkey bot discord")

load_dotenv()

token = getenv("monkey_bot")



# to do list
# come up with more games
# pets


password = False
pocketwatch = clock.utcnow()
oimate = commands.Bot(command_prefix = "!") # set hte prefix
fishNchips = Controller()

# these are veriables im using for banana game
# the targets they get set to the user and target for banana game so
# only they can intaract and no random person jumps in
thrower = "b"
splater = "a"

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
##          testing ground           ##
#######################################

#if this block of code is empty im not testing anything
#this is just so im able to find it in like 4 weeks time
# and me proberly forgotten how to use python :P

###########################################
##         your pocket                   ##
###########################################

@oimate.command(help = "shows u whats in your pocket")
async def pocket(ctx):

    await open_account(ctx.author)
    user = ctx.author
    users = await get_ticket_data()


    # note if any new items are added to this list manualy add them to the ticketbank.json file
    ticket_amt = users[str(user.id)]["ticket"]
    banana_amt = users[str(user.id)]["banana"]
    snow_amt = users[str(user.id)]["snowball"]

    em = discord.Embed(title = f"inside {ctx.author.name}'s pocket is", colour = discord.Colour.red())
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
        users[str(user.id)]["snowman_cursed"] = 0
        users[str(user.id)]["splat"] = 0

    with open("ticketbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_ticket_data():
    with open ("ticketbank.json","r") as f:
        users = json.load(f)
    return users

#######################################
##          statis immunitys         ##
#######################################

@oimate.command(help = "looks at your immunity card to see what your immune to")
async def immunty_card(ctx):
    await check_immunty(ctx.author)
    suser = ctx.author
    susers = await get_immunty_data()
    
    snow_imune = susers[str(suser.id)]["snow_immune"]
    
    em = discord.Embed(title = f"{ctx.author.name}")
    em.add_field(name = "snowman statis", value = f"{snow_imune}", inline = True)
    await ctx.send(embed = em)
    
    
async def check_immunty(user):

    users = await get_immunty_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["snow_immune"] = 0
        
    with open("immunityCARD.json","w") as f:
        json.dump(users,f)
            
    return True
        
async def get_immunty_data():
    with open("immunityCARD.json","r") as f:
        users = json.load(f)
        
    return users


#######################################
##          pet pocket               ##
#######################################

@oimate.command(help = "looks at your pet related things")
async def pet_pocket(ctx):
    await check_pet_pocket(ctx.author)
    user = ctx.author
    users = await get_petPocket_data()
    
    fish = users[str(user.id)]["fish"]
    monkey = users[str(user.id)]["monkey"]
    snowman = users[str(user.id)]["snowman"]
    petfood = users[str(user.id)]["petfood"]
    petmed = users[str(user.id)]["petmed"]
    petreminder = users[str(user.id)]["petreminder"]    
    
    em = discord.Embed(title = f"{ctx.author.name}")
    em.add_field(name = "🐟", value = f"{fish}", inline = True)
    em.add_field(name = "🐒" , value = f"{monkey}",inline = True)
    em.add_field(name = "⛄" , value = f"{snowman}",inline = True)
    em.add_field(name = "🥫", value = f"{petfood}", inline = True)
    em.add_field(name = "💊", value = f"{petmed}", inline = True)
    em.add_field(name = "⏰", value = f"{petreminder}", inline = True)
    await ctx.send(embed = em)    
    
async def check_pet_pocket(user):

    users = await get_petPocket_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["fish"] = 0
        users[str(user.id)]["monkey"] = 0
        users[str(user.id)]["snowman"] = 0
        users[str(user.id)]["petfood"] = 0
        users[str(user.id)]["petmed"] = 0
        users[str(user.id)]["petreminder"] = 0
        users[str(user.id)]["active_pet"] = []
        
        users[str(user.id)]["pet_hunger"] = 10
        users[str(user.id)]["pet_clean"] = 10
        users[str(user.id)]["pet_helth"] = 10
        users[str(user.id)]["pet_fun"] = 10
        users[str(user.id)]["pet_sickness"] = 0
        users[str(user.id)]["pet_freeze"] = 0

        
    with open("petPocket.json","w") as f:
        json.dump(users,f)
            
    return True
        
async def get_petPocket_data():
    
    with open ("petPocket.json","r") as f:
        users = json.load(f)
    return users

#######################################
##           fish cooler             ##
#######################################

@oimate.command(help = "looks at your pet related things")
async def fish_cooler(ctx):
    await check_fish_cooler(ctx.author)
    user = ctx.author
    users = await get_fishcooler_data()
    look = users[str(user.id)]["fish name"]
    
    await ctx.send(f"this is a temp message in till buttons are a thing  \n {ctx.author.name} opened there fish cooler to see what they caught \n {look}")   
    
async def check_fish_cooler(user):

    users = await get_fishcooler_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["fish name"] = []
        
    with open("fishCooler.json","w") as f:
        json.dump(users,f)
            
    return True
        
async def get_fishcooler_data():
    
    with open ("fishCooler.json","r") as f:
        users = json.load(f)
    return users

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
##             dad jokes                ##
##########################################

@commands.cooldown(1,1200,commands.BucketType.user)
@oimate.command(help = "tells a joke")
async def joke(ctx):

    jokeimg = " "
    
    dadjoke = random.randint(1,3)
    if dadjoke == 1:
        jokeimg = "https://cdn.discordapp.com/emojis/887164212261056574.webp?size=96&quality=lossless"
    elif dadjoke == 2:
        jokeimg ="https://cdn.discordapp.com/emojis/704518638706753588.webp?size=96&quality=lossless"
    elif dadjoke ==3:
        jokeimg = "https://cdn.discordapp.com/emojis/894525186655780864.webp?size=44&quality=lossless"
    
    joke = [
            "why coudnt the pony sing a lullaby? ||she was a little horse||",
            "what do u call a boomerang that wont come back? ||a stick||",
            "what does a cloud wear under his raincoat? ||thunderwear||",
            "two pickles fell out of a jar onto the floor what did one say to the other? ||dill with it||",
            "what time is it when the clock strikes 13? ||time to get a new clock||",
            "how dose acucumber become a pickle? || it goes through a jarring experience||",
            "what did one toilet say to the other? ||you look a bit flushed||",
            "what do u think of that new diner on the moon? ||food was good but there really wasnt much atmosphre||",
            "why did the dinosaur cross the road?||because the chicken wasnt born yet||",
            "why cant elsa from frozen have a baloon?||because she will \"let it go\"||",
            "what musical instrument is found in the bathroom?||a tuba toothpaste||",
            "why did the kid bring a ladder to school?||because he wanted to go to high school||",
            "what do you call a dog magician?||a labracadabrador||",
            "where woud you find an elephant?||the same place you lost her||",
            "how do you get a squirrel to like you?||act like a nut||",
            "what do you call two birds in love?||tweethearts||",
            "how dose a scientist freshen her breath?||with experi-mints||",
            "how are false teeth like stars?||they come out at night||",
            "what building in your town has the most stories?||the public library||",
            "whats a computers favrout snack?||computer chips||",
            "what did one vocano say to the other?||i lava you||",
            "how do we know that the ocean is frendly?||it waves||",
            "what is a tornados favrout game to play?||twister||",
            "how dose the moon cut his hair?||eclipes it||",
            "how do you talk to a giant?||use BIG words||",
            "what animal is allways at the baseball game?||a bat||",
            "what falls in winter but never gets hurt?||snow||",
            "what did the dalmatian say after lunch?||that hit the spot||",
            "why did the kid cross the playground?||to get to the other side||",
            "what do you call a droid that takes the long way around?||R2 detour||",
            "why did the cookie go to the hospital?||because he felt crummy||",
            "why was the baby strawberry crying?||because her mum and dad was in a jam||",
            "what did the little corn say to the mama corn?||wheres is pop corn?||",
            "how do you make a lemon drop?||just let it fall||",
            "what did the limestone say to the geologist?||dont take me for granite||",
            "why dose a seagul fly over the sea?||because if they flew over the bay it woud be a baygull||",
            "what kind of water cant freeze?||hot water||",
            "what kind of tree fits in your hand?||a palm tree||",
            "what do you call a dinosaur that is a sleep?||a dino-snore||",
            "whats fast loud and crunchy?||a rocket chip||",
            "why did the teddybear say no to desserts?||he was stuffed||",
            "what has ears but cant hear?||a corn field||",
            "what did the left eye say to the right eye?||between us something smells||",
            "what did one plate say to the other plate?||dinner is on me||",
            "why did the student eat his homework?||the teacher told him it was a piece of cake||",
            "when you look for something why is it allways in the last place you look?||because when u find it you stop looking||",
            "what is brown hairy and wears sunglasses?||a coconut on vacation||",
            "what do you say to a rabbit on his birthday?||hoppy birthday||",
            "whats the one thing u get every year on your birthday guaranteed?||one year older||",
            "why do candles allways go on top of the cake?||because its hard to light them form the bottom||",
            "what do cakes and baseball teams have in common?||they both need a good batter||",
            "two monkeys are in a bath one says oo ahh ahh eeeeeek||the other said turn the cold tap on then||",
            "FUN FACT!! \"sugar\" is the only word in the english language where \"su-\" makes a \"sh\" sound .... || at leace im pritty sure thats correct||"

    ]
    haha = len(joke)
    hoho = random.randrange(haha)
    JOKE = joke[hoho]
    
    jokebed=discord.Embed(title= "DAD JOKE")
    jokebed.set_author(name =(ctx.author.name))
    jokebed.set_thumbnail(url=(jokeimg))
    jokebed.add_field(name = f"{JOKE}" , value = "<:laughtingmonkey:894525186655780864>", inline = True)
    await ctx.send(embed=jokebed)

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
    elif weather_check in ["Sunny" , "Clear"]: #lots of sun
        await ctx.send(":sunny:")
    elif weather_check in ["Rain" , "Light Rain" , "Rain Showers"]: #rain
        await ctx.send(":cloud_rain:")
    elif weather_check == "Cloudy": #clouds
        await ctx.send(":cloud:")
    elif weather_check == "Thunderstorm":
        await ctx.send(":thunder_cloud_rain:")
    elif weather_check in ["Partly Cloudy" , "Mostly Sunny"]:
        await ctx.send(":white_sun_small_cloud:")
    elif weather_check == "Light Rain and Snow":
        await ctx.send(":cloud_snow: :cloud_rain:")
    elif weather_check == "Snow":
        await ctx.send(":cloud_snow:")
    else:
        await ctx.send(weather_check)#posts name of weather to discord if not above

    await client.close() #we dont need weather api anymore close it



############################################
##            ticket shop                 ##
############################################

shopshelf = [
    {"name":"pet_food","price":2,"desc":"🥫 magical pet food all pets love"},
    {"name":"pet_meds","price":5,"desc":"💊 magic medicen to cure pet sickness"},
    {"name":"reminder","price":10,"desc":"⏰ a alarm clock (monkeybot will DM if your pet needs you)"}
    ]

@oimate.command(help = "see what u can extange tickets for")
async def shop(ctx):
    shopbed = discord.Embed(title = "ticket booth")

    for item in shopshelf:
        name = item["name"]
        price = item["price"]
        desc = item["desc"]
        shopbed.add_field(name = name, value = f"{price} | {desc}")

    await ctx.send(embed = shopbed)
    
    
@oimate.command(help = "buy items from the shop")
async def buy(ctx,item = None):
    
    await open_account(ctx.author)
    await check_pet_pocket(ctx.author)
    pocket = await get_ticket_data()
    pet = await get_petPocket_data()
    user = ctx.author
    ticket = pocket[str(user.id)]["ticket"]
    
    with open("ticketbank.json","w") as f:
        json.dump(pocket,f)
            
    with open("petPocket.json","w") as f:
        json.dump(pet,f)
        
    if item == None:
        await ctx.send("pick a item")
    
    elif item == "pet_food" and ticket < 2:
        
        ctx.send("you dont have the tickets for this item")
    
    elif item == "pet_food" and ticket >=2:
        
        await open_account(ctx.author)
        await check_pet_pocket(ctx.author)
        pocket = await get_ticket_data()
        pet = await get_petPocket_data()
        user = ctx.author
    
        pocket[str(user.id)]["ticket"] -= 2
        pet[str(user.id)]["petfood"] += 1
        
        b = pocket[str(user.id)]["ticket"]
        await ctx.send(f"thanks for the tickets heres your pet food and u now have {b} tickets")
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f)
            
        with open("petPocket.json","w") as f:
            json.dump(pet,f)
        return
        
    elif  item == "pet_meds" and ticket < 5:
        
        ctx.send("you dont have the tickets for this item")
        
    elif item == "pet_meds" and ticket >= 5:
        
        await open_account(ctx.author)
        await check_pet_pocket(ctx.author)
        pocket = await get_ticket_data()
        pet = await get_petPocket_data()
        user = ctx.author
        
        pocket[str(user.id)]["ticket"] -= 5
        pet[str(user.id)]["petmed"] += 1
        
        b = pocket[str(user.id)]["ticket"]
        await ctx.send(f"thanks for the tickets heres your pet meds and u now have {b} tickets")
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f)
            
        with open("petPocket.json","w") as f:
            json.dump(pet,f)
        return
        
    elif item == "reminder" and ticket < 10:
        
        ctx.send("you dont have the tickets for this item")
        
    elif item == "reminder" and ticket >= 10:
        
        await open_account(ctx.author)
        await check_pet_pocket(ctx.author)
        pocket = await get_ticket_data()
        pet = await get_petPocket_data()
        user = ctx.author

        pocket[str(user.id)]["ticket"] -= 10
        pet[str(user.id)]["petreminder"] += 1
        
        b = pocket[str(user.id)]["ticket"]
        await ctx.send(f"thanks for the tickets heres your reminder and u now have {b} tickets")
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f)
            
        with open("petPocket.json","w") as f:
            json.dump(pet,f)
        return
###########################################
##               top 10                  ##
###########################################


@oimate.command(help = "shows the top10 ticket holders")
async def top10(ctx,x = 10):

    users = await get_ticket_data()

    top10 = {}
    total = []
    allready = []

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
            total.pop()

    await ctx.send(embed = em)

############################################
##              snow game                 ##
############################################

@oimate.command(help ="makes you immune to snowman statis")
async def snowman_immunty(ctx):
    
    await check_immunty(ctx.author)
    users = await get_immunty_data()
    user = ctx.author
    users[str(user.id)]["snow_immune"] = 1
    with open("immunityCARD.json","w") as f:
        json.dump(users,f)
        
    await ctx.send(f"{ctx.author.name} is now immune to snowman_statis use \"remove_snow_immunty\" to undo this")
    
@oimate.command(help ="makes u errr...mmune? to the snowman statis")
async def remove_snow_immunty(ctx):
    
    await check_immunty(ctx.author)
    users = await get_immunty_data()
    user = ctx.author
    users[str(user.id)]["snow_immune"] = 0
    with open("immunityCARD.json","w") as f:
        json.dump(users,f)
        
    await ctx.send(f"{ctx.author.name} has undone the immunity to snowman_statis")
    
    


@oimate.command(help = "when its snowing over the wildwestcarni u can scoop up some snowballs")
@commands.cooldown(1,120,commands.BucketType.user)
async def scoop(ctx):

    #declare the client. format defults to the metric system(C, km/h, ect)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    #fetch a weather forcast from a city
    weather = await client.find("Boston")

    snow = random.randint(1,3)

    check_weather = weather.current.sky_text

    if check_weather in ["Snow", "Light Rain and Snow" , "light Snow"] and snow == 1:

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        users[str(user.id)]["snowball"] += 1
        snow_get = users[str(user.id)]["snowball"]
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
        await ctx.send(f"{ctx.author.name} gathered a snowball \n you now have {snow_get}")


    elif check_weather in ["Snow", "Light Rain and Snow" , "light Snow"] and snow == 2:

        stash = random.randint(1,5)
        pet_event = random.randint(1,100)

        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        users[str(user.id)]["snowball"] += stash
        snow_get = users[str(user.id)]["snowball"]
        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        await ctx.send(f"{ctx.author.name} was gathering snowballs when they stumbled apon someones hidden stash \n you now have {snow_get}")
        if pet_event > 95:
            
            await check_pet_pocket()
            users = get_petPocket_data()
            user = ctx.author
            pet_amount = users[str(user.id)]["snowman"]
            
            with open("petPocket.json","w") as f:
                json.dump(users,f)
            
            
            await ctx.send(f"you found a pet snowman at the back of the hidden stash YAY COOL PET ....get it ....snow....cool....ill leave now \n {ctx.author.name} has {pet_amount} :snowman:")

    elif check_weather in ["Snow", "Light Rain and Snow" , "light Snow"] and snow == 3:

        await ctx.send(f"{ctx.author.name} was a bout to scoop up some snow when they heard some one yelling ***next time dont wear yellow tinted goggles***")

    else:
        await ctx.send("there is no snow on the ground")

    await client.close()


@oimate.command(help = "throws a snowball at someone")
async def shoke(ctx,member:discord.Member):
    
    global snowdict
    
    aim = random.randint(1,100)
    #print(aim)  #this is for debugging comment out when not debugging
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author

    await check_immunty(ctx.author)
    susers = await get_immunty_data()
    suser = ctx.author
    smem = member
    
    if users[str(user.id)]["snowball"] == 0:
        
        no_snow=discord.Embed(title = "snowball fight")
        no_snow.set_author(name = (ctx.author.name))
        no_snow.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        no_snow.add_field(name = f"you have no snowballs....did they melt? and" , value = "<:puppy_eye_monkey:894525128807940096>", inline = True)
        no_snow.add_field(name = f"{member.name} is proberly anoyed at the ping", value = "<:blob_fail:777073048389419009>" , inline = True)
        await ctx.send(embed=no_snow)


    elif users[str(user.id)]["snowball"] >= 1 and aim <= 59:
        
        users[str(user.id)]["snowball"] -=1
        balls_left = users[str(user.id)]["snowball"]
        snow_hit =discord.Embed(title = "snowball fight")
        snow_hit.set_author(name = (ctx.author.name))
        snow_hit.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_hit.add_field(name = f"{ctx.author.name} throws a snowball at" , value = f"<:laughtingmonkey:894525186655780864> you have {balls_left} remaining", inline = True)
        snow_hit.add_field(name = f"{member.name} is now a snowman", value = "<:2021_Snowsgiving_Emojis_001_Snum:917929344997937162>" , inline = True)
        await ctx.send(embed=snow_hit)
        
        if susers[str(smem.id)]["snow_immune"] == 0:
        
            users[str(member.id)]["snowman_cursed"] = 10
            
        else:
            
            await ctx.send(f"{member.name} is immune to the snowman curse")
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
    elif users[str(user.id)]["snowball"] >= 1 and aim >= 60:
        
        users[str(user.id)]["snowball"] -=1

        snow_miss = discord.Embed(title = "snowball fight")
        snow_miss.set_author(name = (ctx.author.name))
        snow_miss.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_miss.add_field(name = f"{ctx.author.name} throws a snowball at" , value = "<:mnkyDKS:780614148068605983>", inline = True)
        snow_miss.add_field(name = f"{member.name} but it misses", value = "<:mnkyDKS:780614148068605983>", inline = True)
        await ctx.send(embed=snow_miss)
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
@oimate.event 
async def on_message(message):
    
    await open_account(message.author)
    users = await get_ticket_data()
    user = message.author
    
    if users[str(user.id)]["snowman_cursed"] > 0:
        await message.add_reaction("⛄")
        users[str(user.id)]["snowman_cursed"] -= 1
        if users[str(user.id)]["snowman_cursed"] < 0:
            users[str(user.id)]["snowman_cursed"] = 0
            with open("ticketbank.json","w") as f:
                json.dump(users,f)
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
    elif users[str(user.id)]["splat"] > 0:
        users[str(user.id)]["splat"] -= 1
        if users[str(user.id)]["splat"] < 0:
            users[str(user.id)]["splat"] = 0
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
    with open("ticketbank.json","w") as f:
        json.dump(users,f)
    await oimate.process_commands(message)
    
        
############################################
##   banana game for DKS server           ##
############################################

@oimate.command(help ="shake the banana tree")
@commands.cooldown(1,3600,commands.BucketType.user)
async def shake(ctx):
    
    
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("Boston")
    weather_check = weather.current.sky_text

    #tree_shake = random.randint(1,3)
    tree_chance = ["1_banana", "bad_shake", "2_banana", "pet"] #we make a list of the random options
    randomList = random.choices( tree_chance, weights=(50, 50, 50, 1), k=1) # weighted the random chances so some options happen more then others , k=howmeny options form the list we want


    if randomList == ["1_banana"]:
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        
        users[str(user.id)]["banana"] += 1
        
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the banana tree and gained 1 <:mnkyThrow:704518598764527687>", value = f"you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        await ctx.send(embed = shakebed)

        with open("ticketbank.json","w") as f:
            json.dump(users,f)

    elif randomList == ["bad_shake"]:
        
        #monkey remember REMEMBER this list starts from 0 not 1
        uhoh = [
        f"{ctx.author.name} shook the tree to hard and it fell over woops",
        f"{ctx.author.name} gave the banana tree a good shake BUT u upset a sleeping parrot who swooped down and attacked. you lost 1 <:mnkyThrow:704518598764527687>",
        f"{ctx.author.name} shook the banana tree and a disco ball fell down and went SMASH",
        f"{ctx.author.name} shook the banana tree and angered a monkey you now have monkey poop on your head and no banans",
        f"{ctx.author.name} gave the banana tree a good few shakes but nothing droped down",
        f"{ctx.author.name} shoot the banana tree and a coconut droped in there head OWCH.....how did that get in a banana tree anyway?"
        ]
        
        #monkey dont make anything in this list effect pocket values 
        muddy = [
        f" the rain at the jungleparty has made the ground muddy {ctx.author.name} sliiped in the mud befor getting to a tree",
        f" with all the rain in the jungle party latly the tree was to slippery and {ctx.author.name} coudnt get a grip",
        f" {ctx.author.name} saw a really nice rain puddle and got distracting jumping in it",
        f" {ctx.author.name} shock the tree but all that did was make the rain water it was holding drop on your head",
        ]
        
        if weather_check in ["Light Rain" , "Rain" , "Rain Showers"]:
            
            uhoh.extend(muddy)

            
        ohno = len(uhoh)
        quack = random.randrange(ohno)
        RUN = uhoh[quack]
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author


        with open("ticketbank.json","w") as f:
            json.dump(users,f)

        if quack == 1:

            await open_account(ctx.author)
            users = await get_ticket_data()
            user = ctx.author

            users[str(user.id)]["banana"] -= 1
            if users[str(user.id)]["banana"] < 0:
                users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f)

        elif quack == 3:
            
            await open_account(ctx.author)
            users = await get_ticket_data()
            user = ctx.author

            users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f)
                
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name =f"{RUN}" , value =f"you now have {banana_amount} <:mnkyThrow:704518598764527687>", inline = True)
        await ctx.send(embed=shakebed)

    elif randomList == ["2_banana"]:
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        
        users[str(user.id)]["banana"] += 2
        
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the tree AND OH WOW 2 <:mnkyThrow:704518598764527687>  fell from the tree", value = f"you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        await ctx.send(embed = shakebed)

        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
    elif randomList == ["pet"]:
        
        await open_account(ctx.author)
        await check_pet_pocket(ctx.author)
        pocket = await get_ticket_data()
        pet = await get_petPocket_data()
        user = ctx.author
        
        pocket[str(user.id)]["banana"] -= 3
        if pocket[str(user.id)]["banana"] < 0:
            pocket[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(pocket,f)
            
        pet[str(user.id)]["monkey"] += 1
        
        banana_amount = pocket[str(user.id)]["banana"]
        pet_amount = pet[str(user.id)]["monkey"]
        
        shakebed=discord.Embed(title= "PET EVENT!!!!", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/894525128807940096.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the tree AND a baby monkey fell out of a tree and started to cry", value = f"you felt bad and gave the monkey 3 bananas you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        shakebed.add_field(name=f"the baby monkey jumped on to your back as u walked off ....looks like u have a new furry friend take care of him now", value =f"you have {pet_amount} <:puppy_eye_monkey:894525128807940096>", inline = True)
        await ctx.send(embed = shakebed)
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f)
            
        with open("petPocket.json","w") as f:
            json.dump(pet,f)
        
    await client.close()

#######################
## catch throw block ##
#######################

@commands.cooldown(3,3600,commands.BucketType.user)
@oimate.command(help = "throw banana at someone")
async def throw(ctx, member:discord.Member):
    global thrower
    global splater
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    bb = users[str(user.id)]["banana"]
        
    with open("ticketbank.json","w") as f:
        json.dump(users,f)

    
    if splater == "a" and bb >= 1:
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        me = member
        bb = users[str(user.id)]["banana"]
        cc = users[str(me.id)]["banana"]
        
        users[str(user.id)]["banana"] -= 1
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name= f"{ctx.author.name} has thrown a <:mnkyThrow:704518598764527687> at" , value = f"{bb}", inline = True)
        be.add_field(name= f"{member.name} has to respond with !dodge !block !catch" , value = f"{cc}", inline = True)
        await ctx.send(embed = be)
        await ctx.send("if no one responce in like 1hr or something >.> ping monkey to return your banana, code for \"if no one respocnes with in x amount of time reset\" is coming soonTM")
        thrower = (ctx.author.id)
        splater = (member.id)
        
    elif splater != "a":
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = "theres allready a banana flying throu the air at the moment", value = "we dont want bananas to hit mid air", inline = True)
        await ctx.send(embed = be)
        
    elif bb <= 0:
        
        await ctx.send("you donthave any bananas to throw")
        
@oimate.command(help = "dodges the banana")
async def dodge(ctx):
    global thrower
    global splater
    dodge_chance = random.randint(1,100)
    
    if ctx.author.id != splater:
        await ctx.send("no one is throwing a banana at you y are you dodgeing?")
        
    elif ctx.author.id == splater and dodge_chance <= 49:
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        bb = users[str(user.id)]["banana"]
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"{ctx.author.name} dodges the banana with monkey like reflexes!!!!!!", value = f"your have {bb} <:mnkyThrow:704518598764527687> ", inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
    
    elif ctx.author.id == splater and dodge_chance >= 50:
        
        banana_lost = random.randint(2,4)
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        me = member
        bb = users[str(user.id)]["banana"]
        cc = users[str(me.id)]["banana"]
        
        users[str(user.id)]["banana"] -= banana_lost
        users[str(user.id)]["splat"] = 10
        if users[str(user.id)]["banana"] < 0:
            users[str(user.id)]["banana"] = 0
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"{ctx.author.name} dodges but the banana was TOO quick!", value = f"{ctx.author.name} gets smacked in the face and drops {banana_lost}<:mnkyThrow:704518598764527687>", inline = True)
        be.add_field(name = f"{ctx.author.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bb}", inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
        
@oimate.command(help = "blocks the banana")
async def block(ctx):
    global thrower
    global splater
    block_chance = random.randint(1,100)
    
    if ctx.author.id != splater:
        await ctx.send("no one is throwing a banana at you y are u blocking?")
        
    elif ctx.author.id == splater and block_chance <= 30:
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        bb = users[str(user.id)]["banana"]
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"{ctx.author.name} blocks the banana. Whew, that was close!", value = f"<@{ctx.user.id}> has {bb} bananas", inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
        
    elif ctx.author.id == splater and block_chance >= 31:
        
        banana_lost = random.randint(3,7)
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        bb = users[str(user.id)]["banana"]
        
        users[str(user.id)]["banana"] -= banana_lost
        users[str(user.id)]["splat"] = 10
        if users[str(user.id)]["banana"] < 0:
            users[str(user.id)]["banana"] = 0
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"{ctx.author.name} trys to block the banana but", value = f"it slips through and smacks {ctx.author.name} right in the face and they drop {banana_lost} more <:mnkyThrow:704518598764527687>", inline = True)
        be.add_field(name = f"{ctx.author.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bb}", inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
        
@oimate.command(help = "catches the banana")
async def catch(ctx):
    global thrower
    global splater
    catch_chance = random.randint(1,100)
    
    if ctx.author.id != splater:
        await ctx.send("no one is throwing a banana at you...what are u trying to catch?")
    
    elif ctx.author.id == splater and catch_chance <= 15:
        
        banana_get = random.randint(5,15)
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        bb = users[str(user.id)]["banana"]
        
        users[str(user.id)]["banana"] += banana_get

        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        bbb = users[str(user.id)]["banana"]
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"DISPLAYING amazing reflezes {ctx.author.name} catches the banana", value = f"backs into the banana tree and catches {banana_get} more <:mnkyThrow:704518598764527687> ", inline = True)
        be.add_field(name = f"{ctx.author.name} now has", value = f"{bbb} <:mnkyThrow:704518598764527687>" , inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
    elif ctx.author.id == splater and catch_chance >=16:
        
        banana_lost = random.randint(6,12)
        
        await open_account(ctx.author)
        users = await get_ticket_data()
        user = ctx.author
        bb = users[str(user.id)]["banana"]
        
        users[str(user.id)]["banana"] -= banana_lost
        users[str(user.id)]["splat"] = 10
        if users[str(user.id)]["banana"] < 0:
            users[str(user.id)]["banana"] = 0
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = f"{ctx.author.name} trys to catch the banana gets hit in the face", value = f"slips on a banana peel and drops {banana_lost} more <:mnkyThrow:704518598764527687>", inline = True)
        be.add_field(name = f"{ctx.author.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bb}", inline = True)
        await ctx.send(embed = be)
        
        splater = "a"
        thrower = "b"
        
        

@oimate.command(help = "used for checking !throw worked properly")
async def check_throw(ctx): #check what the thrower and splater values are in case the game buged out
    global splater
    global thrower
    
    await ctx.send(f"thrower = {thrower} , splater = {splater}")
    
        
@oimate.command(help = "only monkey and monkeydks can use this command")
async def refund_banana(ctx, member:discord.Member):
    global splater
    global thrower
    
    if ctx.author.id == 113051316225368064 or ctx.author.id == 119791596681166848:
        if splater == "a":
            await ctx.send("nobody need a refund")
            
        elif splater != "a":
            
            
            await open_account(ctx.author)
            users = await get_ticket_data()
            user = member
            bb = users[str(user.id)]["banana"]
            
            await ctx.send(f"{splater} has {bb} refunding....")
            users[str(user.id)]["banana"] += 1
            bb = users[str(user.id)]["banana"]
            await ctx.send(f" {splater} now has {bb}")
            with open("ticketbank.json","w") as f:
                json.dump(users,f)
            
            splater = "a"
            thrower = "b"
            
            await ctx.send(f"spalter and thrower has been reset to {splater} {thrower}")


############################################
##target minigame for DKS server          ##
############################################

@oimate.command(help = "try your luck come win a prize")
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def target(ctx):

    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("Boston")
    weather_check = weather.current.sky_text
    await client.close()
    
    target_chance = ["1", "5", "0", "-1", "lilly"] #we make a list of the random options
    randomList = random.choices( target_chance, weights=(48, 2, 25, 25, 1), k=1) # weighted the random chances so some options happen more then others , k=howmeny options form the list we want


    if weather_check in ["Light Rain" , "Rain" , "Rain Showers"]:

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
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
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
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:CactusDan:884518308404162590>", value = "ABB BUW BA BA hey now partner ya soaked my new jacket won 5 <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552>", inline = True)
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.send(embed=em)

    elif randomList == ["0"]: # miss

        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
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
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
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
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:DanCat:704518407822901339>", value = "WO WO WOOOOOOO now you just gona soaked lilly ill be taking 10 tickets to dry her fur")
        em.add_field(name="you now have" , value = new_amt + "<:DanTix:919966342797463552>",inline = False)
        await ctx.send(embed = em)
            
##################
##  dunk tank   ##
##################

@oimate.command(help = "put your friend in the dunk tank and bet (2+) tickets ", aliases = ["dunk"])
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def dunk_tank(ctx,member:discord.Member,amount = None ):
    
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("Boston")
    weather_check = weather.current.sky_text
    
    dunk_aim = random.randint(1,100)
    
    await open_account(ctx.author)
    await open_account(member)
    users = await get_ticket_data()
    user = ctx.author
    mem = member
    
    amount = int(amount)
    if amount == None:
        await ctx.send("you need to place a bet")
        
    elif amount > users[str(user.id)]["ticket"] or amount > users[str(mem.id)]["ticket"]:
        await ctx.send("you cant bet more then you or your friend own")
        
    elif weather_check in ["Light Rain" , "Rain" , "Rain Showers"]:
        
        await ctx.send("sorry partner with the rain going on its not as fun if you and your friend are allready wet")
        
    elif weather_check in ["Light Snow" , "Snow" , "Light Rain and Snow"]:
        
        await ctx.send("sorry partner the dunktank is frozen solid")

    elif amount >= 2 and dunk_aim >= 50:
        
        await open_account(ctx.author)
        await open_account(member)
        users = await get_ticket_data()
        user = ctx.author
        mem = member
        
        users[str(user.id)]["ticket"] += amount
        users[str(mem.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        dunkbed = discord.Embed(title= "DUNK TANK",colour = discord.Colour.purple())
        dunkbed.set_author(name = (ctx.author.name))
        dunkbed.set_thumbnail(url="https://cdn.discordapp.com/emojis/887167642417373246.webp?size=96&quality=lossless")
        dunkbed.add_field(name =f"{ctx.author.name} threw a ball and hit the <:Target:887076837392527400>", value = f"you now have {ubal}", inline = True)
        dunkbed.add_field(name =f"{member.name} fell in to the tank and lost the bet", value = f"they now have {mbal}",inline = True)
        await ctx.send(embed = dunkbed)
        
        await ctx.send("https://tenor.com/view/fell-into-the-water-mark-chernesky-konas2002-fall-dunk-tank-gif-17968100")
        
    elif amount >= 2 and dunk_aim <= 49:
        
        await open_account(ctx.author)
        await open_account(member)
        users = await get_ticket_data()
        user = ctx.author
        mem = member
        
        users[str(mem.id)]["ticket"] += amount
        users[str(user.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        dunkbed = discord.Embed(title= "DUNK TANK",colour = discord.Colour.purple())
        dunkbed.set_author(name = (ctx.author.name))
        dunkbed.set_thumbnail(url ="https://cdn.discordapp.com/emojis/887167642417373246.webp?size=96&quality=lossless")
        dunkbed.add_field(name =f"{ctx.author.name} threw a ball but missed the <:Target:887076837392527400>", value = f"you now have {ubal}", inline = True)
        dunkbed.add_field(name =f"{member.name} won the bet and is dry", value = f"they now have {mbal}",inline = True)
        await ctx.send(embed = dunkbed)
        
    await client.close()
        

###########################
#####     fishing     #####
###########################

@oimate.command(help = "fishing")
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def fishing(ctx):
    
    cast = random.randint(5,60)

    fish_name = [
        "cod",
        "salamon",
        "catfish",
        "kitchen sink",
        "shark",
        "whale",
        ":fish:",
        ":wood:",
        ":shark:",
        "🕶️",
        "BEAR-acuda",
        "fish in a fish bowl",
        "old boot",
        "the other old boot",
        "a new boot",
        "a strange glowing book something about mending",
        "a peanut butter and jelly fish",
        "NEMO",
        "frozen tuna",
    ]
    
    fishname = len(fish_name)
    randomname = random.randrange(fishname)
    named_fish = fish_name[randomname]
    
    fishsize = round(random.uniform(0.8,1500),2) #cm
    fishweight = random.randint(8,42624) # OZ

    if cast == 60:
        await ctx.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        await ctx.send("...not even a nibble")
        
    elif cast < 60 and randomname != 11:
        await ctx.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        
        fishbed = discord.Embed(title=(named_fish),colour = discord.Colour.blue())
        fishbed.set_author(name = (ctx.author.name))
        fishbed.set_thumbnail(url="https://www.emoji.co.uk/files/twitter-emojis/activity-twitter/10839-fishing-pole-and-fish.png")
        fishbed.add_field(name =f"{ctx.author.name}has fished up a {named_fish}", value = f"its {fishsize}cm and  weighs {fishweight} OZ", inline = True)
        await ctx.send(embed = fishbed)
        
        await check_fish_cooler(ctx.author)
        fish = await get_fishcooler_data()
        user = ctx.author
        
        fish[str(user.id)]["fish name"].append(named_fish)
        print("updated")
        
        with open("fishCooler.json","w") as f:
            json.dump(fish,f)
        
        
    elif cast < 60 and randomname == 11:
        
        await check_pet_pocket(ctx.author)
        pet = await get_ticket_data()
        user = ctx.author
        
        await ctx.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        
        pet[str(user.id)]["fish"] += 1
        
        petfish = pet[str(user.id)]["fish"]
        
        petbed = discord.Embed(title = "PET EVENT!!", colour = discord.Colour.gold())
        petbed.set_author(name = (ctx.author.name))
        petbed.set_thumbnail(url="https://www.emoji.co.uk/files/twitter-emojis/animals-nature-twitter/10682-fish.png")
        petbed.add_field(name = f"{ctx.author.name} has fished up a {named_fish} oooo looks like they have a new fishy pet friend" , value = f"they now have {petfish} :fish:" , inline = True)
        await ctx.send(embed = petbed)
        
        with open("petPocket.json" ,"w") as f:
            json.dump(pet,f)
            
@oimate.command(help = "slap someone with the fish u caught")
async def fish_slap(ctx, member:discord.Member = None):
    
    await check_fish_cooler(ctx.author)
    fish = await get_fishcooler_data()
    user = ctx.author

    if member == None:
        await ctx.send("u cant fish slap the air")

    elif len(fish[str(user.id)]["fish name"]) == 0:
        await ctx.send("you have no fish")
    
    else:
        await check_fish_cooler(ctx.author)
        fish = await get_fishcooler_data()
        user = ctx.author
        slap = fish[str(user.id)]["fish name"][-1]
        
        fish[str(user.id)]["fish name"].pop()

        with open ("fishCooler.json","w") as f:
            json.dump(fish,f)
        
        await ctx.send(f"{ctx.author.name} just fishslaped {member.name} with {slap} \n this will have fancy embed later:tm:")
        
        

###########################################
##              pets                     ##
###########################################

@oimate.command(help ="puts pet stats on freese (we know real life is more inporatnt)")
async def pet_freeze(ctx, *, message = None):
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    if message == "on":
        users[str(user.id)]["pet_freeze"] = 1
        await ctx.send(f"{ctx.author.name} has froze there pet stats dont forget to unfreeze them when your not busy ^_^")
    elif message == "off":
        users[str(user.id)]["pet_freeze"] = 0
        await ctx.send(f"{ctx.author.name} has unfroze there pet stats dont worry it defrozed properly ^w^")

@oimate.command(help = "sets your pet")
async def set_pet(ctx, *, message = None):
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    
    if message == "fish" and users[str(user.id)]["fish"] > 0:
        users[str(user.id)]["active_pet"].clear()
        users[str(user.id)]["fish"] -= 1
        users[str(user.id)]["active_pet"] = ["fish"]
        await ctx.send("you took your fish out of the pet_pocket and put the bowl on a table")
        
        with open ("petPocket.json","w") as f:
            json.dump(users,f)
        
    elif message == "monkey" and users[str(user.id)]["monkey"] > 0:
        users[str(user.id)]["active_pet"].clear()
        users[str(user.id)]["monkey"] -= 1
        users[str(user.id)]["active_pet"] = ["monkey"]
        await ctx.send("you took your monkey out of the pet_pocket and let him run around the living room")
        
        with open ("petPocket.json","w") as f:
            json.dump(users,f)
        
    elif message == "snowman" and users[str(user.id)]["snowman"] > 0:
        users[str(user.id)]["active_pet"].clear()
        users[str(user.id)]["snowman"] -= 1
        users[str(user.id)]["active_pet"] = ["snowman"]
        await ctx.send("you took your snowman out of the pet_pocket and let him in your house ....keep him away from the fireplace")
        
        with open ("petPocket.json","w") as f:
            json.dump(users,f)
    
    else:
        await ctx.send("your iver forgot to say what pet OR dont have any use !pet_pocket to check")
        
        with open ("petPocket.json","w") as f:
            json.dump(users,f)

@oimate.command()
async def give_pet(ctx):
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    users[str(user.id)]["fish"] = 10
    await ctx.send(" 10 fish added")
    users[str(user.id)]["monkey"] = 10
    await ctx.send(" 10 monkeys added")
    users[str(user.id)]["snowman"] = 10
    await ctx.send("10 snowman added")
    
    with open("petPocket.json","w") as f:
        json.dump(users,f)

    
@oimate.command(help = "checks on your pet")
async def check_pet(ctx): 
    
    await check_pet_pocket(ctx.author)
    await open_account(ctx.author)
    ticket = await get_ticket_data()
    users = await get_petPocket_data()
    user = ctx.author
    
    home = Image.open("/home/pi/Desktop/monkey bot discord/pet/pet_home_empty.png")
    char = Image.open("/home/pi/Desktop/monkey bot discord/pet/char.png")
    you = Image.open("/home/pi/Desktop/monkey bot discord/pet/you.png")
        
    home.paste(char, (0,0), char) #puts a char in the living room
    
    if ticket[str(user.id)]["snowman_cursed"] > 0: # check to see if the user has effects or not befor sitting in the chair
        you = Image.open("/home/pi/Desktop/monkey bot discord/pet/snowman_curse.png")
    elif ticket[str(user.id)]["splat"] > 0:
        banana = Image.open("/home/pi/Desktop/monkey bot discord/pet/banana.png")
        you.paste(banana, (0,0), banana)
    else:
        you = Image.open("/home/pi/Desktop/monkey bot discord/pet/you.png")
        
    home.paste(you, (0,0), you)
        
    if users[str(user.id)]["active_pet"] == ["monkey"]:
        
        draw = ImageDraw.Draw(home)
        font = ImageFont.truetype(font ="/home/pi/.fonts/ZakirahsCasual.ttf",size=30)
        sont = ImageFont.truetype(font ="/home/pi/.fonts/Symbola.ttf",size = 20)


        draw.text((353, 12), "HUNGER", font = font)
        if users[str(user.id)]["pet_hunger"] > 8:
            draw.text((351,45),"🍏 🍏 🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 7 or users[str(user.id)]["pet_hunger"] == 8:
            draw.text((351,45),"🍏 🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 6 or users[str(user.id)]["pet_hunger"] == 5:
            draw.text((351,45),"🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 3 or users[str(user.id)]["pet_hunger"] == 4:
            draw.text((351,45),"🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 2 or users[str(user.id)]["pet_hunger"] == 1:
            draw.text((351,45),"🍏",font = sont)
        else:
            draw.text((351,45),"empty",font = font)
            
        draw.text((356, 81),"HYGIEN", font=font)
        if users[str(user.id)]["pet_clean"] >8:
            draw.text((351,115),"💩 💩 💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 8 or users[str(user.id)]["pet_clean"] == 7:
            draw.text((351,115),"💩 💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 5 or users[str(user.id)]["pet_clean"] == 6:
            draw.text((351,115),"💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 4 or users[str(user.id)]["pet_clean"] == 3:
            draw.text((351,115),"💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 2 or users[str(user.id)]["pet_clean"] == 1:
            draw.text((351,115),"💩",font=sont)
        else:
            draw.text((352,115),"empty",font = font)
            
        draw.text((354,145),"FUN",font=font)
        if users[str(user.id)]["pet_fun"] > 8:
            draw.text((351,175),"☻ ☻ ☻ ☻ ☻", font = sont)
        elif users[str(user.id)]["pet_fun"] == 8 or users[str(user.id)]["pet_fun"] == 7:
            draw.text((351,175),"☻ ☻ ☻ ☻", font = sont)
        elif users[str(user.id)]["pet_fun"] == 6 or users[str(user.id)]["pet_fun"] == 5:
            draw.text((351,175),"☻ ☻ ☻", font = sont)
        elif users[str(user.id)]["pet_fun"] == 4 or users[str(user.id)]["pet_fun"] == 3:
            draw.text((351,175),"☻ ☻", font = sont)
        elif users[str(user.id)]["pet_fun"] == 2 or users[str(user.id)]["pet_fun"] == 1:
            draw.text((351,175),"☻", font = sont)
        else:
            draw.text((351,175),"BORED", font = font)
            
        draw.text((335,215),"SICKNESS",font=font,size =20)
        if users[str(user.id)]["pet_sickness"] == 0:
            draw.text((351,245),"Healthy", font=font)
        else:
            draw.text((351,237),"Sick", font=font)
            
        if users[str(user.id)]["pet_helth"] == 0:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_dead.png")
        elif users[str(user.id)]["pet_fun"] < 5 and users[str(user.id)]["pet_sickness"] == 0:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_bored.png")
        elif users[str(user.id)]["pet_hunger"] < 5 and users[str(user.id)]["pet_sickness"] == 0:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_hungery.png")
        elif users[str(user.id)]["pet_health"] >= 1 and users[str(user.id)]["pet_sickness"] == 1:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_sick.png")
        else:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_normal.png")

        if users[str(user.id)]["pet_clean"] < 5:
            print(6)
            mess = ("/home/pi/Desktop/monkey bot discord/pet/monkey/monkey_dirty.png")
            home.paste(mess,(0,0),mess)
        print(7)
        home.paste(monkey, (0,0), monkey)
        print(8)


        home.save("/home/pi/Desktop/monkey bot discord/pet/monkey_home.png", "PNG")
        print(9)

        await ctx.send(file = discord.File("/home/pi/Desktop/monkey bot discord/pet/monkey_home.png"))
        print(10)
        os.remove("/home/pi/Desktop/monkey bot discord/pet/monkey_home.png")  
        print(11)
    
    elif users[str(user.id)]["active_pet"] == ["fish"]:
        
        draw = ImageDraw.Draw(home)
        font = ImageFont.truetype(font ="/home/pi/.fonts/ZakirahsCasual.ttf",size=30)
        sont = ImageFont.truetype(font ="/home/pi/.fonts/Symbola.ttf",size = 20)
        draw.text((353, 12), "HUNGER", font = font)
        if users[str(user.id)]["pet_hunger"] > 8:
            draw.text((351,45),"🍏 🍏 🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 7 or users[str(user.id)]["pet_hunger"] == 8:
            draw.text((351,45),"🍏 🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 6 or users[str(user.id)]["pet_hunger"] == 5:
            draw.text((351,45),"🍏 🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 3 or users[str(user.id)]["pet_hunger"] == 4:
            draw.text((351,45),"🍏 🍏",font = sont)
        elif users[str(user.id)]["pet_hunger"] == 2 or users[str(user.id)]["pet_hunger"] == 1:
            draw.text((351,45),"🍏",font = sont)
        else:
            draw.text((351,45),"empty",font = font)
            
        draw.text((356, 81),"HYGIEN", font=font)
        if users[str(user.id)]["pet_clean"] >8:
            draw.text((351,115),"💩 💩 💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 8 or users[str(user.id)]["pet_clean"] == 7:
            draw.text((351,115),"💩 💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 5 or users[str(user.id)]["pet_clean"] == 6:
            draw.text((351,115),"💩 💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 4 or users[str(user.id)]["pet_clean"] == 3:
            draw.text((351,115),"💩 💩",font=sont)
        elif users[str(user.id)]["pet_clean"] == 2 or users[str(user.id)]["pet_clean"] == 1:
            draw.text((351,115),"💩",font=sont)
        else:
            draw.text((352,115),"empty",font = font)
            
        draw.text((354,145),"FUN",font=font)
        draw.text((351,175),"N/A  (fish)", font = font)
        
        draw.text((335,215),"SICKNESS",font=font,size =20)
        if users[str(user.id)]["pet_sickness"] == 0:
            draw.text((351,245),"Healthy", font=font)
        else:
            draw.text((351,237),"Sick", font=font)

        fishbowl = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/fishbowl.png")
    
        if users[str(user.id)]["pet_helth"] == 0:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/fish_dead.png")
    
        elif users[str(user.id)]["pet_helth"] >= 1 and users[str(user.id)]["pet_sickness"] == 1:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/fish_sick.png")
        else:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/fish_happy.png")
        
        if users[str(user.id)]["pet_clean"] < 5:
            fishwater = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/dirty_water.png")
        else:
            fishwater = Image.open("/home/pi/Desktop/monkey bot discord/pet/fish/clean_water.png")
    
        fishwater.paste(fish, (0,0), fish)

        fishbowl.paste(fishwater, (0,0), fishwater)

        home.paste(fishbowl, (0, 0), fishbowl)
        
        
        
        home.save("/home/pi/Desktop/monkey bot discord/pet/fish_home.png", "PNG")
    
        await ctx.send(file = discord.File("/home/pi/Desktop/monkey bot discord/pet/fish_home.png"))
        os.remove("/home/pi/Desktop/monkey bot discord/pet/fish_home.png")  
        
    else:
        home.save("/home/pi/Desktop/monkey bot discord/pet/you_home.png", "PNG")
        await ctx.send(file = discord.File("/home/pi/Desktop/monkey bot discord/pet/you_home.png"))
        await ctx.send("you dont have a active pet")
        os.remove("/home/pi/Desktop/monkey bot discord/pet/you_home.png")
     
     
     
############################################
##monkeys attempted at gameing for discord##
############################################


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
    EGG = clock.now()
    sausage = EGG.strftime("%I:%M %p")
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
