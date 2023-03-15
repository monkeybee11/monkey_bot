############################################################################################################################################################################
## if you are reading this on github and your not monkey 99.9% of the comments are for me 4 weeks later from typing the code so sry if theres to much comments for you XD ##
############################################################################################################################################################################
from datetime import time , timezone, datetime as clock
import discord, asyncio, os, json, random, requests, python_weather
from discord.ui import Button , View
from discord.ext import commands, tasks
from pynput.keyboard import Key, Controller
from dotenv import load_dotenv
from os import getenv
from PIL import Image, ImageDraw, ImageFont
import datetime


os.chdir("/home/pi/Desktop/monkey bot discord")

load_dotenv()

token = getenv("monkey_bot")



# to do list
# come up with more games

monkey = int(113051316225368064)
dks = int(119791596681166848)


password = False
oimate = commands.Bot()
fishNchips = Controller()
t1 = ""
t2 = ""
t3 = ""
b1 = ""
b2 = ""
b3 = ""

# these are veriables im using for banana game
# the targets they get set to the user and target for banana game so
# only they can intaract and no random person jumps in
thrower = "b"
splater = "a"


# create slash commarnd groups here
banana = oimate.create_group("banana")
dunk = oimate.create_group("dunk")
snows = oimate.create_group("snow")
pocket = oimate.create_group("pocket")
top = oimate.create_group("top")
pets = oimate.create_group("pet")
shop = oimate.create_group("shop")
fish_command = oimate.create_group("fish")

@oimate.event
async def on_ready(): #this is where the bot brain starts to work
    print("discord")  # print() sends to the CMD not to discord

    
@oimate.event
async def on_application_command_error(ctx, error):
    global monkey
    
    if isinstance(error, commands.MissingRequiredArgument): #if command wasnot not right
        await ctx.respond("you shoudnt see this message ping monkeybee11(monkeysock) and the command is on cooldown(if it has one) dont retry it")      
        
    elif isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        
        await ctx.respond(error)
        
    else:
        raise error
        await ctx.respond(f"uhh ohh....something broke <@!{monkey}> go get some help")

#######################################
##          testing ground           ##
#######################################

#if this block of code is empty im not testing anything
#this is just so im able to find it in like 4 weeks time
# and me proberly forgotten how to use python :P


###########################################
##         your pocket                   ##
###########################################

@pocket.command(description = "shows u whats in your pocket")
async def item(ctx):
    await ctx.response.defer()

    await open_account(ctx.author)
    user = ctx.author
    users = await get_ticket_data()


    # note if any new items are added to this list manualy add them to the ticketbank.json file
    ticket_amt = users[str(user.id)]["ticket"]
    banana_amt = users[str(user.id)]["banana"]
    snow_amt = users[str(user.id)]["snowball"]
    cracker_amt = users[str(user.id)]["ccracker"]

    em = discord.Embed(title = f"inside {ctx.author.name}'s pocket is", colour = discord.Colour.red())
    em.add_field(name = "<:DanTix:919966342797463552>", value = ticket_amt, inline = True)
    em.add_field(name = "<:mnkyThrow:704518598764527687>", value = banana_amt, inline = True)
    em.add_field(name = "<:2021_Snowsgiving_Emojis_001_Snow:917929344914030642>",value = snow_amt, inline = True)
    em.add_field(name = "<:christmas_cracker:1040655557171871794>",value = cracker_amt, inline = True)
    await ctx.followup.send(embed = em)

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
        users[str(user.id)]["ccracker"] = 0
        users[str(user.id)]["snowman_cursed"] = 0
        users[str(user.id)]["splat"] = 0
        users[str(user.id)]["twitch"] = ""

    with open("ticketbank.json","w") as f:
        json.dump(users,f, indent=4)
    return True

async def get_ticket_data():
    with open ("ticketbank.json","r") as f:
        users = json.load(f)
    return users

#######################################
##          statis immunitys         ##
#######################################

@oimate.slash_command(name ="immunity_card" , description = "looks at your immunity card to see what your immune to")
async def immunty_card(ctx):
    await ctx.response.defer()
    
    await check_immunty(ctx.author)
    suser = ctx.author
    susers = await get_immunty_data()
    
    snow_imune = susers[str(suser.id)]["snow_immune"]
    banana_imune = susers[str(suser.id)]["banana_immune"]
    
    em = discord.Embed(title = f"{ctx.author.name}")
    em.add_field(name = "snowman statis", value = f"{snow_imune}", inline = True)
    em.add_field(name = "banana statis", value = f"{banana_imune}", inline = True)
    await ctx.followup.send(embed = em)
    
    
async def check_immunty(user):

    users = await get_immunty_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["snow_immune"] = 0
        users[str(user.id)]["banana_immune"] = 0
        
    with open("immunityCARD.json","w") as f:
        json.dump(users,f, indent=4)
            
    return True
        
async def get_immunty_data():
    with open("immunityCARD.json","r") as f:
        users = json.load(f)
        
    return users
    
##############
# map link   #
##############
@oimate.slash_command(name = "monkeymines_map" , description = "link to the monkeymines map")
async def map(ctx):
    await ctx.response.defer()
    
    await ctx.followup.send("http://monkeyminesmap.net/")
    
###############
#set immunty  #
###############
    
@oimate.slash_command(name = "immune" , description ="set your immuntys")
async def immune(ctx, message = None):
    await ctx.response.defer()
    
    await check_immunty(ctx.author)
    users = await get_immunty_data()
    user = ctx.author
    
    if message == "add_snowman":
        
        users[str(user.id)]["snow_immune"] = 1
        
        await ctx.followup.send(f"{user.name} has become immune to the snowman curse")
    
    elif message == "remove_snowman":
        
        users[str(user.id)]["snow_immune"] = 0
        
        await ctx.followup.send(f"{user.name} is no longer immune to the snowman curse")
        
    elif message == "add_banana":
        
        users[str(user.id)]["banana_immune"] = 1
        
        await ctx.followup.send(f"{user.name} no longer will have banana stuck on there face")
        
    elif message == "remove_banana":
        
        users[str(user.id)]["banana_immune"] = 0
        
        await ctx.followup.send(f"{user.name} will have banana stuck to there face when thrown at them")
        
    else:
        
        await ctx.followup.send("use this commarnd to add or remove immuitys to effects from this bot")
        
    with open("immunityCARD.json","w") as f:
        json.dump(users,f, indent=4)


#######################################
##          pet pocket               ##
#######################################

@pocket.command(description = "looks at your pet related things")
async def pet(ctx):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    user = ctx.author
    users = await get_petPocket_data()
    
    fish = users[str(user.id)]["fish"]
    monkey = users[str(user.id)]["monkey"]
    snowman = users[str(user.id)]["snowman"]
    petfood = users[str(user.id)]["petfood"]
    petmed = users[str(user.id)]["petmed"]
    
    em = discord.Embed(title = f"{ctx.author.name}")
    em.add_field(name = "🐟", value = f"{fish}", inline = True)
    em.add_field(name = "🐒" , value = f"{monkey}",inline = True)
    em.add_field(name = "⛄" , value = f"{snowman}",inline = True)
    em.add_field(name = "🥫", value = f"{petfood}", inline = True)
    em.add_field(name = "💊", value = f"{petmed}", inline = True)
    await ctx.followup.send(embed = em)    
    
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
        users[str(user.id)]["active_pet"] = ""
        
        users[str(user.id)]["pet_hunger"] = 10
        users[str(user.id)]["pet_clean"] = 10
        users[str(user.id)]["pet_health"] = 10
        users[str(user.id)]["pet_fun"] = 10
        users[str(user.id)]["pet_sickness"] = 0
        users[str(user.id)]["pet_freeze"] = 0
        
        users[str(user.id)]["health_tick"] = 10
        users[str(user.id)]["hunger_tick"] = 10
        users[str(user.id)]["fun_tick"] = 10
        users[str(user.id)]["clean_tick"] = 10
        users[str(user.id)]["pet name"] = ""

        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
            
    return True
        
async def get_petPocket_data():
    
    with open ("petPocket.json","r") as f:
        users = json.load(f)
    return users
    
@tasks.loop(time = time(17 , 35, tzinfo=datetime.timezone.utc))
async def choco_loop():
    channel = oimate.get_channel(672550204213297174)
    await channel.send('<@&888038726154993714> oi oi paycheck time come and get your<:Galaxy_Cookie:776762120686927896><:Galaxy_Cookie:776762120686927896><:Galaxy_Cookie:776762120686927896>') 
    

@tasks.loop(hours=1)
async def trophy_check():
    
    global t1, t2, t3 ,b1 ,b2 ,b3
    with open("ticketbank.json","r") as f:
        users = json.load(f)
        
        ticket_check = sorted(users.items(), key=lambda x: x[1]["ticket"], reverse=True)
        banana_check = sorted(users.items(), key=lambda x: x[1]["banana"], reverse=True)
        
        t1 = int(ticket_check[0][0])
        t2 = int(ticket_check[1][0])
        t3 = int(ticket_check[2][0])
        b1 = int(banana_check[0][0])
        b2 = int(banana_check[1][0])
        b3 = int(banana_check[2][0])
        
        
            

@tasks.loop(minutes=30)
async def pet_tick():
    with open("petPocket.json","r") as f:
        users = json.load(f)
        check1 = random.randint(1,2)
        check2 = random.randint(1,2)
        sicky = random.randint(0,10)
        
    for user, value in users.items():
        
        if users[user]["active_pet"] != "" and users[user]["pet_freeze"] == 0:
            if check1 == 1 and check2 == 1:
                users[user]["hunger_tick"] -= 1
                if users[user]["hunger_tick"] <= 0:
                    users[user]["hunger_tick"] = 10
                    users[user]["pet_hunger"] -= 1
                    if users[user]["pet_hunger"] <= 0:
                        users[user]["pet_hunger"] = 0
                        users[user]["pet_health"] -= 1

            elif check1 == 1 and check2 == 2:
                users[user]["clean_tick"] -= 1
                if users[user]["clean_tick"] <= 0:
                    users[user]["clean_tick"] = 10
                    users[user]["pet_clean"] -= 1
                    if users[user]["pet_clean"] <= 3:
                        if sicky > 5:
                            users[user]["pet_sickness"] = 1
                            if users[user]["pet_sickness"] == 1:
                                users[user]["pet_health"] -= 2
                                
            elif check1 == 2 and check2 == 1 and users[user]["active_pet"] != "fish":
                users[user]["fun_tick"] -= 1
                if users[user]["fun_tick"] <= 0:
                    users[user]["fun_tick"] = 10
                    users[user]["pet_fun"] -= 1
                    
            elif users[user]["pet_health"] > 0 and users[user]["pet_health"] < 10:
                users[user]["pet_hunger"] -= 1
                users[user]["pet_health"] += 1
                    
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        

#######################################
##           fish cooler             ##
#######################################
    
async def check_fish_cooler(user):

    users = await get_fishcooler_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["fish name"] = []
        
    with open("fishCooler.json","w") as f:
        json.dump(users,f, indent=4)
            
    return True
        
async def get_fishcooler_data():
    
    with open ("fishCooler.json","r") as f:
        users = json.load(f)
    return users
    
@fish_command.command(description = "better list of your fish cooler")
async def list(ctx):
    await ctx.response.defer()
    
    await check_fish_cooler(ctx.author)
    users = await get_fishcooler_data()
    user = ctx.author
    fish = users[str(user.id)]["fish name"]
    
    em = discord.Embed(title = f"{ctx.author.name} fish list")
    em.add_field(name = "cod", value = fish.count("cod") , inline = True)
    em.add_field(name = "salamon", value = fish.count("salamon"), inline = True)
    em.add_field(name = "catfish", value = fish.count("catfish"), inline = True)
    em.add_field(name = "kitchen sink", value = fish.count("kitchen sink"), inline = True)
    em.add_field(name = "shark", value = fish.count("shark"), inline = True)
    em.add_field(name = "whale", value = fish.count("whale"), inline = True)
    em.add_field(name = ":fish:", value = fish.count(":fish:"), inline = True)
    em.add_field(name = ":wood:", value = fish.count(":wood:"), inline = True)
    em.add_field(name = ":shark:", value = fish.count(":shark:"), inline = True)
    em.add_field(name = "👓", value = fish.count("👓"), inline = True)
    em.add_field(name = "BEAR-acuda", value = fish.count("BEAR-acuda"), inline = True)
    em.add_field(name = "old boot", value = fish.count("old boot"), inline = True)
    em.add_field(name = "the other old boot", value = fish.count("the other old boot"), inline = True)
    em.add_field(name = "a new boot", value = fish.count("a new boot"), inline = True)
    em.add_field(name = "a strange glowing book something about mending" , value = fish.count("a strange glowing book something about mending"), inline = True)
    em.add_field(name = "a peanut butter jelly fish", value = fish.count("a peanut butter jelly fish"), inline = True)
    em.add_field(name = "NEMO", value = fish.count("NEMO"), inline = True)
    em.add_field(name = "frozen tuna", value = fish.count("frozen tuna"), inline = True)
    em.add_field(name = "some legobricks from the 1969 LEGO satun V rocket", value = fish.count("some legobricks from the 1969 LEGO satun V rocket"), inline = True)
    await ctx.followup.send(embed = em)  
    
#######################################
##            rpg data               ##
#######################################

#removed for now coming back later
        
#######################################
##         random stuff              ##
#######################################

@oimate.slash_command(name = "nailed_it", description = "nailed it")
async def nailedit(ctx):
    await ctx.response.defer()
    
    nail = random.randint(1,2)
    if nail == 1:
        await ctx.followup.send("<:NailedItDan:887162185166516256>")
    elif nail == 2:
        await ctx.followup.send("<:mnkyNailedIt:739908983833362433>")
        
        
@oimate.slash_command(name = "dadjokes", description = "dadjoke emoji")
async def dadjoke(ctx):
    await ctx.response.defer()
    
    joke = random.randint(1,2)
    if joke == 1:
        await ctx.followup.send("<:DadJokeDan:887164212261056574>")
    elif joke == 2:
        await ctx.followup.send(" <:mnkyDadJoke:704518638706753588>")
        
        
@oimate.slash_command(name = "d20", description = "rolls a d20")
async def d20(ctx):
    await ctx.response.defer()
    
    roll = random.randint(1,20)
    await ctx.followup.send(file = discord.File(f"/home/pi/Desktop/monkey bot discord/img/dice/gif/D20_{roll}.gif"))
        
#############################
##     get others wet      ##
#############################

@oimate.slash_command(name = "pew" ,description = "shoot someone with a water gun")
async def pew(ctx,member:discord.Member):
    await ctx.response.defer()
    
    miss = random.randint(1,100)
    if miss <= 80:
        
        await ctx.followup.send(f"<@!{member.id}> got shot by <@!{ctx.author.id}>")
        await ctx.send("<a:TargetAnim:927671875834875974>")
        
    elif miss > 80 and miss < 90:
        
        await open_account(ctx.author)
        await open_account(member)
        users = await get_ticket_data()
        user = ctx.author
        mem = member
        
        aim = random.randint(1,5)
        
        users[str(user.id)]["ticket"] += aim
        users[str(mem.id)]["ticket"] -= aim
        if users[str(mem.id)]["ticket"] < 0:
            users[str(mem.id)]["ticket"] = 0
            
        await ctx.followup.send(f"showing off there cowboy skills <@!{user.id}> not only got <@!{member.id}> wet but shot {aim} tickets out of there hand and grabed them mid air")
        
    elif miss >= 90:
        name = []
        for member in ctx.guild.members:
            name.append(member.id)
        await ctx.followup.send(f"<@!{ctx.author.id}> missed there target and shot <@!{random.choice(name)}>") 
        await ctx.send("<a:TargetAnim:927671875834875974>")
        await ctx.send(f"<@!{ctx.author.id}> may want to pratice there aim at the target game")

##########################################
##             dad jokes                ##
##########################################

@commands.cooldown(1,1200,commands.BucketType.user)
@oimate.slash_command(name= "joke", description = "tells a joke")
async def joke(ctx):
    await ctx.response.defer()

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
    await ctx.followup.send(embed=jokebed)
    
    
##########################################
##              bubble wrap             ##
##########################################

@oimate.slash_command(name = "bubble_wrap", description = "discord stress releave")
async def stress(ctx):
    await ctx.response.defer()
    
    await ctx.followup.send(f"you seem stressed {ctx.author}....here have some bubble wrap")
    await ctx.send("||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||\n||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||")

##########################################
##               weather                ##
##########################################

######################
# weather list       #
######################
partly_sunny = "Partly Sunny"
mostly_cloudy = ["Mostly Cloudy" , "Overcast" ]
sunny = ["Sunny","Clear"]
rainy = ["Rain","Light Rain","Rain Showers", "Light rain, mist"]
cloudy = "Cloudy"
thunder = "Thundery Showers"
sunnycloud = ["Partly Cloudy" , "Mostly Sunny"]
slush = "Light Rain and Snow"
snow = "Snow"
ninja_cloud = ["Mist", "Rain, mist"]


## this was easyer then making my own weather system
@oimate.slash_command(name = "weather", description ="tells you the weather over the wildwestcarni AND the jungle party")
async def weather(ctx):
    await ctx.response.defer()
    
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.get("Boston")
    weather_check = weather.current.description
    
    if weather_check == partly_sunny: # little cloudy but sunny
        await ctx.followup.send(":partly_sunny:")
        
    elif weather_check in mostly_cloudy: # sunny cloud
        await ctx.followup.send(":white_sun_cloud:")
        
    elif weather_check in sunny: #lots of sun
        await ctx.followup.send(":sunny:")
    
    elif weather_check in rainy: #rain
        await ctx.followup.send(":cloud_rain:")
        
    elif weather_check == cloudy: #clouds
        await ctx.followup.send(":cloud:")
        
    elif weather_check == thunder: # thunder storms
        await ctx.followup.send(":thunder_cloud_rain:")
        
    elif weather_check in sunnycloud: # dont knwo y ive made this its own thing
        await ctx.followup.send(":white_sun_small_cloud:")
        
    elif weather_check == slush: # slush
        await ctx.followup.send(":cloud_snow: :cloud_rain:")
        
    elif weather_check == snow: # snow
        await ctx.followup.send(":cloud_snow:")
        
    elif weather_check in ninja_cloud: # WATCH OUT THATS NINJAS SMOKEBOMBS
        await ctx.followup.send("🥷😶‍🌫️")
    
    elif weather_check == "Partly cloudy":
        await ctx.followup.send("🌥️")

    else:
        await ctx.followup.send(weather_check)#posts name of weather to discord if not above

    await client.close() #we dont need weather api anymore close it



############################################
##            ticket shop                 ##
############################################


@shop.command(description = "see what u can extange tickets for")
async def browse(ctx):
    await ctx.response.defer()
    
    shopbed = discord.Embed(title = "ticket booth")

    for item in shopshelf:
        name = item["name"]
        price = item["price"]
        desc = item["desc"]
        shopbed.add_field(name = name, value = f"{price} | {desc}")

    await ctx.followup.send(embed = shopbed)
    
    
@shop.command(description = "buy items from the shop")
async def buy(ctx,item = None, amount = 1):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    await check_pet_pocket(ctx.author)
    pocket = await get_ticket_data()
    pet = await get_petPocket_data()
    user = ctx.author
    ticket = pocket[str(user.id)]["ticket"]
    
    if item == None:
        await ctx.followup.send("pick a item \n say !shop to see what u can buy")
        buy.reset_cooldown()
        
    
    elif item == "pet_food" and ticket < 2:
        
        await ctx.followup.send("you dont have the tickets for this item")
    
    elif item == "pet_food" and ticket >=2:
        
        pocket[str(user.id)]["ticket"] -= 2*int(amount)
        pet[str(user.id)]["petfood"] += 1*int(amount)
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f ,indent=4)
        
        new_amt = pocket[str(user.id)]["ticket"]
        await ctx.followup.send(f"thanks for the tickets heres your pet food and u now have {new_amt} tickets")

        
    elif  item == "pet_meds" and ticket < 5:
        
        await ctx.followup.send("you dont have the tickets for this item")
        
    elif item == "pet_meds" and ticket >= 5:
        
        pocket[str(user.id)]["ticket"] -= 5*int(amount)
        pet[str(user.id)]["petmed"] += 1*int(amount)
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f, indent=4)
        
        new_amt = pocket[str(user.id)]["ticket"]
        await ctx.followup.send(f"thanks for the tickets heres your pet meds and u now have {new_amt} tickets")
    
    elif item == "christmas_cracker" and ticket < 20:
        
        await ctx.followup.send("you dont have the tickets for this item")
        
    elif item == "christmas_cracker" and ticket >= 20:
        
        pocket[str(user.id)]["ticket"] -= 20*int(amount)
        pocket[str(user.id)]["ccracker"] += 1*int(amount)
        
        with open("ticketbank.json","w") as f:
            json.dump(pocket,f ,indent=4)
            
        new_amt = pocket[str(user.id)]["ticket"]
        await ctx.followup.send(f"thanks for the tickets heres your christmas cracker you now have {new_amt} of tickets")

    with open("petPocket.json","w") as f:
        json.dump(pet,f, indent=4)
        
###########################################
##           christmas crackers          ##
###########################################

@oimate.slash_command(name = "christmas_cracker", description = "crack open a cracker with a friend")
async def christmas_cracker(ctx,member:discord.Member = None):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    cracker = users[str(user.id)]["ccracker"]
    
    junk = [
        "🎾",
        "🧩",
        "🎲",
        "♟️",
        "🧷",
        "📎",
        "🖇️",
        "📏",
        "🖊️",
        "🔋",
        "🧻",
        "🖌️",
        "✏️",
        "🔐"
    ]
    
    junkname = len(junk)
    randomname = random.randrange(junkname)
    junk_prize = junk[randomname]
    
    cracker_jokes = [
        "What does Santa suffer from if he gets stuck in a chimney? ||Claustrophobia!||",
        "Why does Santa have three gardens? ||So he can 'ho ho ho'!||",
        "Why did Santa go to the doctor? ||Because of his bad 'elf'!||",
        "Why did Santa's helper see the doctor? ||Because he had a low 'elf' esteem!||",
        "What kind of motorbike does Santa ride? ||A Holly Davidson!||",
        "What do you call a cat in the desert? ||Sandy Claws!||",
        "Who delivers presents to cats? ||Santa Paws!||",
        "What do you call a dog who works for Santa? ||Santa Paws!||",
        "What do you call Father Christmas in the beach? ||Sandy Clause!||",
        "What do you get if you cross Santa with a detective? ||Santa Clues!||",
        "What did the sea Say to Santa? ||Nothing! It just waved!||",
        "What do you get if you cross Santa with a duck? ||A Christmas Quacker!||",
        "Who delivers presents to baby sharks at Christmas? ||Santa Jaws||"
    ]
    
    crackername = len(cracker_jokes)
    randomjoke = random.randrange(crackername)
    picked_joke = cracker_jokes[randomjoke]
    
    if member is None:
        
        await ctx.followup.send("you cant open a cracker by your self its not as fun")
        
    elif cracker < 1:
        
        await ctx.followup.send("you dont have any crackers")
        
    elif cracker >= 1:
        
        await ctx.followup.send(f"{user.name} and {member.name} pull on one of {user.name} christmas crackers")
        
        users[str(user.id)]["ccracker"] -= 1
        
        
        a = random.randint(0,20)
        b = 20 - a
        c = random.randint(1,3)
        d = random.randint(1,3)
        prize = ""
        prizeb = ""
        
            
        if c == 1:
            users[str(user.id)]["ticket"] += a
            prize = "<:DanTix:919966342797463552>"
        elif c == 2:
            users[str(user.id)]["banana"] += a
            prize = "<:mnkyThrow:704518598764527687>"
        elif c == 3:
            users[str(user.id)]["snowball"] += a
            prize = "<:2021_Snowsgiving_Emojis_001_Snow:917929344914030642>"
        if d == 1:
            users[str(member.id)]["ticket"] += b
            prizeb = "<:DanTix:919966342797463552>"
        elif d == 2:
            users[str(member.id)]["banana"] += b
            prizeb = "<:mnkyThrow:704518598764527687>"
        elif d == 3:
            users[str(member.id)]["snowball"] += b
            prizeb = "<:2021_Snowsgiving_Emojis_001_Snow:917929344914030642>"
        
        if a > b:
            
            await ctx.followup.send(f"{user.name} got {a} {prize} and a paper crown™️ \n {member.name} got {b} {prizeb} and a {junk_prize} heres your cracker joke {picked_joke}")
            await ctx.send("this is temp going to make it better looking soon....ish")
            
            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
            
        elif a == b:
            
            await ctx.followup.send(f"{user.name} got {a} {prize} \n {member.name} got {b} {prizeb} \n AND YOU BOTH GOT A CROWN™️ \n heres your cracker joke {picked_joke}")
            await crx.send("this is temp going to make it better looking soon......ish")
            
            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
                
        elif a < b:
            
            await ctx.followup.send(f"{user.name} got {a} {prize} and a {junk_prize} \n {member.name} got {b} {prizeb} and a paper crown™ \n heres your cracker joke {picked_joke}")
            await ctx.send("this is temp going to make it better looking soon......ish")

            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
    
    
    

###########################################
##               top 10                  ##
###########################################

@top.command(description = "say ticket / banana to look at there top 10 boards")
async def ten(ctx,score = None):
    await ctx.response.defer()
    
    ticket = ["ticket", "tickets"]
    banana = ["banana", "bananas"]
    

        
    if score in banana or score in ticket:
    
        global b1,b2,b3,t1,t2,t3
    
        users = await get_ticket_data()
        
        if score in ticket:
            score = "ticket"
        elif score in banana:
            score = "banana"

    
        # reverse sort by ticket number in user dictionary ty sebi
        users_sorted = sorted(users.items(), key=lambda x: x[1][score], reverse=True)
        
        if score in banana:
    
            b1 = int(users_sorted[0][0])
            b2 = int(users_sorted[1][0])
            b3 = int(users_sorted[2][0])
            emojii = "<:mnkyThrow:704518598764527687>"
        
        elif score in ticket:
            
            t1 = int(users_sorted[0][0])
            t2 = int(users_sorted[1][0])
            t3 = int(users_sorted[2][0])
            emojii = "<:DanTix:919966342797463552>"

        em = discord.Embed(title=f"top 10 {score} holders")
        placement = 0
        user_name = 0
        user_banana = 0

        for x in range(0,10):

            placement += 1
        
            id_ = users_sorted[user_name][0]
            user_name += 1
        
            amt1 = users_sorted[user_banana][1][score]
            user_banana +=1
        
            names = await oimate.fetch_user(id_)
            namess = names.name
            em.add_field(name = f"{placement}.  {namess}" , value = f"{amt1} {emojii}", inline = False)
    
        await ctx.followup.send(embed = em)
        
    else:
        await ctx.followup.send(f"we only have leader boards for banana and ticket we dont have one for {score} ....yet")

############################################
##              snow game                 ##
############################################

@snows.command(description = "when its snowing over the wildwestcarni u can scoop up some snowballs")
@commands.cooldown(1,3600,commands.BucketType.user)
async def scoop(ctx):
    await ctx.response.defer()
    
    global snow

    client = python_weather.Client(format=python_weather.IMPERIAL)

    #fetch a weather forcast from a city
    weather = await client.get("Boston")
    

    snowRANDOM = random.randint(1,3)

    check_weather = weather.current.description
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author

    if check_weather in snow and snowRANDOM == 1:
    #if snowRANDOM == 1:

        users[str(user.id)]["snowball"] += 1
        snow_get = users[str(user.id)]["snowball"]
            
        await ctx.followup.send(f"{user.name} gathered a snowball \n you now have {snow_get}")

    elif check_weather in snow and snowRANDOM == 2:
    #elif snowRANDOM == 2:

        stash = random.randint(1,5)
        pet_event = random.randint(1,100)
        print("pet event is " + str(pet_event))

        users[str(user.id)]["snowball"] += stash
        snow_get = users[str(user.id)]["snowball"]


        await ctx.followup.send(f"{user.name} was gathering snowballs when they stumbled apon someones hidden stash \n you now have {snow_get}")
        if pet_event > 95:
            
            await check_pet_pocket()
            pets = get_petPocket_data()
            
            pet_amount = pets[str(user.id)]["snowman"]
            
            with open("petPocket.json","w") as f:
                json.dump(pets,f, indent=4)
            
            await ctx.followup.send(f"you found a pet snowman at the back of the hidden stash YAY COOL PET ....get it ....snow....cool....ill leave now \n {ctx.author.name} has {pet_amount} :snowman:")
            
    elif check_weather in snow and snowRANDOM == 3:
    #elif snowRANDOM == 3:

        await ctx.followup.send(f"{user.name} was a bout to scoop up some snow when they heard some one yelling ***next time dont wear yellow tinted goggles***")
        

    else:
        await ctx.followup.send("there is no snow on the ground")
        
    with open("ticketbank.json","w") as f:
        json.dump(users,f, indent=4)

    await client.close()


@snows.command(description = "throws a snowball at someone")
async def throw(ctx,member:discord.Member):
    await ctx.response.defer()
    
    global snowdict
    
    aim = random.randint(1,100)
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    mem = member

    await check_immunty(ctx.author)
    await check_immunty(member)
    susers = await get_immunty_data()
    suser = ctx.author
    smem = member
    
    if users[str(user.id)]["snowball"] == 0:
        
        await ctx.followup.send(f"<@!{member.id}> WATCH OUT")
        
        no_snow=discord.Embed(title = "snowball fight")
        no_snow.set_author(name = (ctx.author.name))
        no_snow.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        no_snow.add_field(name = f"you have no snowballs....did they melt? and" , value = "<:puppy_eye_monkey:894525128807940096>", inline = True)
        no_snow.add_field(name = f"{member.name} is proberly anoyed at the ping", value = "<:blob_fail:777073048389419009>" , inline = True)
        await ctx.send(embed=no_snow)


    elif users[str(user.id)]["snowball"] >= 1 and aim <= 59:
        
        users[str(user.id)]["snowball"] -=1
        
        await ctx.followup.send(f"<@!{member.id}> WATCH OUT")
        
        balls_left = users[str(user.id)]["snowball"]
        snow_hit =discord.Embed(title = "snowball fight")
        snow_hit.set_author(name = (ctx.author.name))
        snow_hit.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_hit.add_field(name = f"{ctx.author.name} throws a snowball at" , value = f"<:laughtingmonkey:894525186655780864> you have {balls_left} remaining", inline = True)
        snow_hit.add_field(name = f"{member.name} is now a snowman", value = "<:2021_Snowsgiving_Emojis_001_Snum:917929344997937162>" , inline = True)
        await ctx.send(embed=snow_hit)
        
        if susers[str(smem.id)]["snow_immune"] == 0:
        
            users[str(mem.id)]["snowman_cursed"] = 10
            
            
        else:
            
            await ctx.followup.send(f"{member.name} is immune to the snowman curse")
        
    elif users[str(user.id)]["snowball"] >= 1 and aim >= 60:
        
        users[str(user.id)]["snowball"] -=1
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        await ctx.followup.send(f"<@!{member.id}> WATCH OUT")

        balls_left = users[str(user.id)]["snowball"]
        snow_miss = discord.Embed(title = "snowball fight")
        snow_miss.set_author(name = (ctx.author.name))
        snow_miss.set_thumbnail(url="https://cdn.discordapp.com/emojis/914587417355386950.gif?size=96&quality=lossless")
        snow_miss.add_field(name = f"{ctx.author.name} throws a snowball at" , value = "<:mnkyDKS:780614148068605983>", inline = True)
        snow_miss.add_field(name = f"{member.name} but it misses", value = "<:mnkyDKS:780614148068605983>", inline = True)
        snow_miss.add_field(name = "you now have" , value = f"{balls_left}", inline = True)
        await ctx.send(embed=snow_miss)
        
    with open("ticketbank.json","w") as f:
        json.dump(users,f, indent=4)
            
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
        
    elif users[str(user.id)]["splat"] > 0:
        await message.add_reaction("<:mnkySplat:704517946277494834>")
        users[str(user.id)]["splat"] -= 1
        if users[str(user.id)]["splat"] < 0:
            users[str(user.id)]["splat"] = 0
            
    with open("ticketbank.json","w") as f:
        json.dump(users,f, indent=4)
        
    if "!|dea" in message.content:
        with open("idea.txt" , "a") as f:
            f.write(message.content + "\n")
        await message.channel.send("your idea has been noted down")
        
    await oimate.process_commands(message)
                    
    
        
############################################
##   banana game for DKS server           ##
############################################

@banana.command(description ="shake the banana tree")
@commands.cooldown(1,3600,commands.BucketType.user)
async def shake(ctx):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    await check_pet_pocket(ctx.author)
    pet = await get_petPocket_data()
    
    
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.get("Boston")
    weather_check = weather.current.description

    tree_chance = ["1_banana", "bad_shake", "2_banana", "pet"] #we make a list of the random options
    randomList = random.choices( tree_chance, weights=(50, 50, 50, 1), k=1) # weighted the random chances so some options happen more then others , k=howmeny options form the list we want


    if randomList == ["1_banana"]:
                
        users[str(user.id)]["banana"] += 1
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f ,indent=4)
        
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the banana tree and gained 1 <:mnkyThrow:704518598764527687>", value = f"you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        await ctx.followup.send(embed = shakebed)

    elif randomList == ["bad_shake"]:
        
        #monkey remember REMEMBER this list starts from 0 not 1
        uhoh = [
        f"{ctx.author.name} shook the tree to hard and it fell over woops",
        f"{ctx.author.name} gave the banana tree a good shake BUT u upset a sleeping parrot who swooped down and attacked. you lost 1 <:mnkyThrow:704518598764527687>",
        f"{ctx.author.name} shook the banana tree and a disco ball fell down and went SMASH",
        f"{ctx.author.name} shook the banana tree and angered a monkey you now have monkey poop on your head and no banans",
        f"{ctx.author.name} gave the banana tree a good few shakes but nothing droped down",
        f"{ctx.author.name} shoot the banana tree and a coconut droped in there head OWCH.....how did that get in a banana tree anyway?",
        f"{ctx.author.name} gave the banana tree a good shake but a empty 1969 LEGO satun V rocket box fell on your head",
        ]
        
        muddy = [
        f" the rain at the jungleparty has made the ground muddy {ctx.author.name} sliiped in the mud befor getting to a tree",
        f" with all the rain in the jungle party latly the tree was to slippery and {ctx.author.name} coudnt get a grip",
        f" {ctx.author.name} saw a really nice rain puddle and got distracting jumping in it",
        f" {ctx.author.name} shock the tree but all that did was make the rain water it was holding drop on your head",
        ]
        
        if weather_check in rainy:
            
            uhoh.extend(muddy)

        ohno = len(uhoh)
        quack = random.randrange(ohno)
        RUN = uhoh[quack]

        if quack == 1:


            users[str(user.id)]["banana"] -= 1
            if users[str(user.id)]["banana"] < 0:
                users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)

        elif quack == 3:
            
            users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
                
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name =f"{RUN}" , value =f"you now have {banana_amount} <:mnkyThrow:704518598764527687>", inline = True)
        await ctx.followup.send(embed=shakebed)

    elif randomList == ["2_banana"]:
        
        users[str(user.id)]["banana"] += 2
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f,indent=4)
        
        banana_amount = users[str(user.id)]["banana"]
        shakebed=discord.Embed(title= "BANANA GAME", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the tree AND OH WOW 2 <:mnkyThrow:704518598764527687>  fell from the tree", value = f"you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        await ctx.followup.send(embed = shakebed)
            
    elif randomList == ["pet"]:
        
        users[str(user.id)]["banana"] -= 3
        if users[str(user.id)]["banana"] < 0:
            users[str(user.id)]["banana"] = 0

            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
            
        pet[str(user.id)]["monkey"] += 1
        
        banana_amount = pocket[str(user.id)]["banana"]
        pet_amount = pet[str(user.id)]["monkey"]
        
        shakebed=discord.Embed(title= "PET EVENT!!!!", colour = discord.Colour.gold())
        shakebed.set_author(name = (ctx.author.name))
        shakebed.set_thumbnail(url="https://cdn.discordapp.com/emojis/894525128807940096.webp?size=96&quality=lossless")
        shakebed.add_field(name= f"{ctx.author.name} shook the tree AND a baby monkey fell out of a tree and started to cry", value = f"you felt bad and gave the monkey 3 bananas you now have {banana_amount}<:mnkyThrow:704518598764527687>" ,inline = True)
        shakebed.add_field(name=f"the baby monkey jumped on to your back as u walked off ....looks like u have a new furry friend take care of him now", value =f"you have {pet_amount} <:puppy_eye_monkey:894525128807940096>", inline = True)
        await ctx.followup.send(embed = shakebed)
        
    with open("ticketbank.json","w") as f:
        json.dump(users,f, indent=4)
            
    with open("petPocket.json","w") as f:
        json.dump(pet,f, indent=4)
        
    await client.close()

#######################
## catch throw block ##
#######################

class bananaView(discord.ui.View):
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="the target must of fallen a sleep", view=self)
        
    @discord.ui.button(label = "dodge", style= discord.ButtonStyle.primary)
    async def dodge(self, button, interaction):
        global thrower, splater
        
        dodge_chance = random.randint(1,100)
        await open_account(interaction.user)
        users = await get_ticket_data()
        user = interaction.user
        banana_lost = random.randint(2,4)
        bb= users[str(user.id)]["banana"]
        eww = users[str(user.id)]["splat"]
        
        if splater == user.id:
            
            be = discord.Embed(title = "BANANA GAMES")
            be.set_author(name = (user.name))
            be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
            
            if dodge_chance <= 49:
                
                
                be.add_field(name = f"{user.name} dodges the banana with monkey like reflexes!!!!!!", value = f"your have {bb} <:mnkyThrow:704518598764527687> ", inline = True)
                
            elif dodge_chance >= 50:
                    
                bb -= banana_lost
                eww = 10
                    
                if bb <= 0:
                    bb = 0
                        
                with open("ticketbank.json","w") as f:
                    json.dump(users,f,indent = 4)
                    
                bbb = bb
                        

                be.add_field(name = f"{user.name} dodges but the banana was TOO quick!", value = f"{user.name} gets smacked in the face and drops {banana_lost}<:mnkyThrow:704518598764527687>", inline = True)
                be.add_field(name = f"{user.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bbb}", inline = True)
                    
                    
            for child in self.children:
                child.disabled = True
            button.label = "ended"
                    
            await interaction.response.edit_message(embed = be,view=self)
        
            splater = "a"
            thrower = "b"
                    
                    
            
        elif splater != user.id:
            await interaction.response.send_message(f"no one is throwing a banana at you {user.name} y are you dodgeing???")
            
    @discord.ui.button(label = "block", style= discord.ButtonStyle.primary)
    async def block(self, button, interaction):
        
        global thrower, splater
        block_chance = random.randint(1,100)
        banana_lost = random.randint(3,7)
        await open_account(interaction.user)
        users = await get_ticket_data()
        user = interaction.user
        bb = users[str(user.id)]["banana"]
        eww = users[str(user.id)]["splat"]
        
        if user.id == splater:
            
            
            be = discord.Embed(title = "BANANA GAMES")
            be.set_author(name = (user.name))
            be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
            
            if block_chance <= 30:
                
                be.add_field(name = f"{user.name} blocks the banana. whew, that was close!", value = f"{user.name} has {bb} bananas", inline = True)
                
            elif block_chance >= 31:
                
                bb-= banana_lost
                eww = 10
                if bb <= 0:
                    bb = 0
                    
                with open("ticketbank.json","w") as f:
                    json.dump(users,f, indent=4)
                    
                bbb = bb
                
                be.add_field(name = f"{user.name} trys to block the banana but", value = f"it slips through and smacks {user.name} right in the face and they drop {banana_lost} more <:mnkyThrow:704518598764527687>", inline = True)
                be.add_field(name = f"{user.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bbb}", inline = True)
                
        
            for child in self.children:
                child.disabled = True
            button.label = "ended"
                    
            await interaction.response.edit_message(embed = be,view=self)
            
            splater = "a"
            thrower = "b"
        
        elif user.id != splater:
            await interaction.response.send_message(f"no one threw a banana at you {user.name} y are you blocking ???")
            
    @discord.ui.button(label = "catch", style= discord.ButtonStyle.primary)
    async def catch(self, button, interaction):
        
        global thrower, splater
        
        catch_chance = random.randint(1,100)
        banana_get = random.randint(1,3)
        user = interaction.user
        await open_account(user)
        users = await get_ticket_data()
        bb = users[str(user.id)]["banana"]
        
        if user.id == splater:
            
            be = discord.Embed(title = "BANANA GAMES")
            be.set_author(name = (user.name))
            be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
            
            if catch_chance <= 15:
                
                bb += banana_get
                
                with open("ticketbank.json","w") as f:
                    json.dump(users,f, indent=4)
                    
                bbb = bb
                
                be.add_field(name = f"DISPLAYING amazing reflezes {user.name} catches the banana", value = f"backs into the banana tree and catches {banana_get} more <:mnkyThrow:704518598764527687> ", inline = True)
                be.add_field(name = f"{user.name} now has", value = f"{bbb} <:mnkyThrow:704518598764527687>" , inline = True)
                
            elif catch_chance >= 16:
                
                bb -= banana_get
                eww = 10
                if bb <= 0:
                    bb = 0
                    
                bbb = bb
                    
                be.add_field(name = f"{user.name} trys to catch the banana gets hit in the face", value = f"slips on a banana peel and drops {banana_get} more <:mnkyThrow:704518598764527687>", inline = True)
                be.add_field(name = f"{user.name} now has" , value = f"<:mnkyThrow:704518598764527687>{bbb}", inline = True)
                
            for child in self.children:
                child.disabled = True
            button.label = "ended"
                    
            await interaction.response.edit_message(embed = be,view=self)
            
            splater = "a"
            thrower = "b"
        
        elif user.id != splater:
            
            await interaction.response.send_message(f"no one threw a banana at you {user.name}....your not trying to steal the banana are you???")
                


@commands.cooldown(3,3600,commands.BucketType.user)
@banana.command(description = "throw your banana at someone")
async def throw(ctx, member:discord.Member):
    await ctx.response.defer()
    
    global thrower
    global splater
    
    await open_account(ctx.author)
    await open_account(member)
    users = await get_ticket_data()
    user = ctx.author
    me = member
    user_banana = users[str(user.id)]["banana"]
    member_banana = users[str(me.id)]["banana"]
    
    if splater == "a" and user_banana >= 1:
        
        thrower = int(ctx.author.id)
        splater = int(member.id)
        
        users[str(user.id)]["banana"] -= 1
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        await ctx.followup.send(f"<@!{ctx.author.id}> has thrown a banana at <@!{member.id}>")
            
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name= f"{ctx.author.name} has thrown a <:mnkyThrow:704518598764527687> at" , value = f"{user_banana}", inline = True)
        be.add_field(name= f"{member.name} has to respond by clicking dodge, catch or block" , value = f"{member_banana}", inline = True)
        await ctx.send(embed = be, view=bananaView(timeout=(2*60*60)))

                
        await asyncio.sleep(2*60*60)
        if splater == member.id:
            await ctx.send(f"{member.name} seems to be sleeping and didt reacte (you got your banana back)")
            users[str(user.id)]["banana"] += 1
            thrower = "b"
            splater = "a"
        
    elif splater != "a":
        
        be = discord.Embed(title = "BANANA GAMES")
        be.set_author(name = (ctx.author.name))
        be.set_thumbnail(url="https://cdn.discordapp.com/emojis/729464173783810130.webp?size=96&quality=lossless")
        be.add_field(name = "theres allready a banana flying throu the air at the moment", value = "we dont want bananas to hit mid air", inline = True)
        await ctx.followup.send(embed = be)
        
    elif user_banana <= 0:
        
        await ctx.followup.send("you donthave any bananas to throw")
        
    with open("ticketbank.json", "w") as f:
        json.dump(users,f,indent=4)
                

@banana.command(description = "used for checking if this commarnd worked properly")
async def check(ctx): #check what the thrower and splater values are in case the game buged out
    await ctx.response.defer()
    
    global splater
    global thrower
    
    await ctx.followup.send(f"thrower = {thrower} , splater = {splater}")
    
        
@banana.command(description = "only monkey and wildwestdan can use this command")
async def refund(ctx, member:discord.Member):
    await ctx.response.defer()
    
    global splater
    global thrower
    global monkey
    global dks
    
    if ctx.author.id == monkey or ctx.author.id == dks: #this is right ive got thrower and splatter verables in reverse :P
        if splater == "a":
            await ctx.followup.send("nobody need a refund")
            
        elif splater != "a":
            
            
            await open_account(ctx.author)
            users = await get_ticket_data()
            user = member
            bb = users[str(user.id)]["banana"]
            
            await ctx.followup.send(f"{member.name} has {bb} refunding....")
            
            users[str(user.id)]["banana"] += 1
            bb = users[str(user.id)]["banana"]
            
            await ctx.send(f" {member.name} now has {bb}")
            with open("ticketbank.json","w") as f:
                json.dump(users,f, indent=4)
            
            splater = "a"
            thrower = "b"
            
            await ctx.name(f"spalter and thrower has been reset to {splater} {thrower}")
            
    elif ctx.author.id != monkey or ctx.author.id != dks:
        await ctx.followup.send("only monkey and DKS can use this commarnd :P")


############################################
##target minigame for DKS server          ##
############################################

@oimate.slash_command(name = "web_games", description = "link to the targetpratice web game")
async def webgame(ctx):
    await ctx.response.defer()
    
    await ctx.followup.send("heres a link to the target pratice web game(more games coming soon(tm) \n https://monkeybee11.github.io/targetpratices/")

@oimate.slash_command(name = "target", description = "try your luck come win a prize")
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def target(ctx):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    ticket_amt = users[str(user.id)]["ticket"]

    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.get("Boston")
    weather_check = weather.current.description
    
    target_chance = ["1", "5", "0", "-1", "lilly"] #we make a list of the random options
    randomList = random.choices( target_chance, weights=(48, 2, 25, 25, 1), k=1) # weighted the random chances so some options happen more then others , k=howmeny options form the list we want
    
    if weather_check in rainy:

        await ctx.followup.send("the carni is shutdown becase of rain come back later")
        
    elif weather_check in ninja_cloud:
        
        await ctx.followup.send("what in tarnations its thicker then pea soup out there how do u exspect to hit the target in this weather?")

    elif randomList == ["1"]: # 1 ticket

        users[str(user.id)]["ticket"] += 1

        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:DanWater5:919977398164914227>", value = "WOOO BOY you won ya self a ticket partner <:DanTix:919966342797463552>", inline = True)
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.followup.send(embed=em)

    elif randomList == ["5"]: # 5 ticket

        users[str(user.id)]["ticket"] += 5

        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:CactusDan:884518308404162590>", value = "ABB BUW BA BA hey now partner ya soaked my new jacket won 5 <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552> <:DanTix:919966342797463552>", inline = True)
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.followup.send(embed=em)

    elif randomList == ["0"]: # miss

        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:Target:887076837392527400>", value = "well well welly well well looks like ya missed the target you get nothing")
        await ctx.followup.send(embed=em)

    elif randomList == ["-1"]: # stop hitting your self

        users[str(user.id)]["ticket"] -= 1
        if users[str(user.id)]["ticket"] < 0:
            users[str(user.id)]["ticket"] = 0

        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name ="<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:SplashDan:887167642417373246>", value = "how in tar nashens did u mannage to soak your self? ***you droped a ticket***")
        em.add_field(name="you now have <:DanTix:919966342797463552>" , value = new_amt,inline = False)
        await ctx.followup.send(embed = em)

    elif randomList == ["lilly"]: # Y DID U HIT LILLY

        users[str(user.id)]["ticket"] -= 10
        if users[str(user.id)]["ticket"] < 0:
            users[str(user.id)]["ticket"] = 0


        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)

        new_amt = users[str(user.id)]["ticket"]
        em=discord.Embed(title = "target game", colour = discord.Colour.purple())
        em.set_author(name = (ctx.author.name))
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/887076837392527400.webp?size=44&quality=lossless")
        em.add_field(name = "<:DanWater1:919977398127165440><:DanWater2:919977398357868564><:DanWater3:919977398118776864><:DanWater4:919977398013919274><:DanCat:704518407822901339>", value = "WO WO WOOOOOOO now you just gona soaked lilly ill be taking 10 tickets to dry her fur")
        em.add_field(name="you now have" , value = f" {new_amt} <:DanTix:919966342797463552>",inline = False)
        await ctx.followup.send(embed = em)
    await client.close()
    
#####################################
## temp command for webgame scores ##
#####################################

@oimate.slash_command(name = "score" , description = "turn your webgame score in to discord tickets HONNOR SYSTEM NO CHEATING THE SYSTEM....prity plz")
@commands.cooldown(1,604800,commands.BucketType.user) # 1 week
async def score(ctx,amount = None ):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    
    amount = int(amount)
    if amount == None:
        
        await ctx.followup.send("tell me the score u got from playing the webgame....in a weeks time bc coding is hard >.> and go noidea how to reset cooldowns")
        score.reset_cooldown()
        
    elif amount > 0:
        
        users[str(user.id)]["ticket"] += amount
        
        score = users[str(user.id)]["ticket"]
        
        await ctx.followup.send(f"{amount} has been added to your ticket count its now {score}")
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
        
        
        
            
##################
##  dunk tank   ##
##################

@dunk.command(description = "put your friend in the dunk tank and bet (2+) tickets ", aliases = ["dunk"])
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def tank(ctx,member:discord.Member,amount = None ):
    await ctx.response.defer()
    
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.get("Boston")
    weather_check = weather.current.description
    
    dunk_aim = random.randint(1,100)
    
    await open_account(ctx.author)
    await open_account(member)
    users = await get_ticket_data()
    user = ctx.author
    mem = member
    
    amount = int(amount)
    if amount == None:
        await ctx.followup.send("you need to place a bet")
        dunk_tank.reset_cooldown()
        
    elif amount > users[str(user.id)]["ticket"] or amount > users[str(mem.id)]["ticket"]:
        
        await ctx.followup.send("you cant bet more then you or your friend own")
        
    elif weather_check in rainy:
        
        await ctx.followup.send("sorry partner with the rain going on its not as fun if you and your friend are allready wet")
        
    elif weather_check in snow:
        
        await ctx.followup.send("sorry partner the dunktank is frozen solid")
        
    elif amount >= 2 and dunk_aim >= 55 and weather_check in ninja_cloud:
        
        users[str(user.id)]["ticket"] += amount
        users[str(mem.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        await ctx.followup.send(f"<@!{member.id}> sat in the dunk tank \n{amount} <:DanTix:919966342797463552> are put on the line")
        
        dunkbed = discord.Embed(title= "DUNK TANK",colour = discord.Colour.purple())
        dunkbed.set_author(name = (ctx.author.name))
        dunkbed.set_thumbnail(url="https://cdn.discordapp.com/emojis/887167642417373246.webp?size=96&quality=lossless")
        dunkbed.add_field(name =f"{ctx.author.name} threw a ball and hit the <:Target:887076837392527400>", value = f"you now have {ubal}", inline = True)
        dunkbed.add_field(name =f"{member.name} fell in to the tank and lost the bet", value = f"they now have {mbal}",inline = True)
        await ctx.send(embed = dunkbed)
        
        await ctx.send("https://tenor.com/view/fell-into-the-water-mark-chernesky-konas2002-fall-dunk-tank-gif-17968100")
        
    elif amount >= 2 and dunk_aim <= 54 and weather_check in ninja_cloud:
        
        users[str(mem.id)]["ticket"] += amount
        users[str(user.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        await ctx.followup.send(f"<@!{member.id}> sat in the dunk tank \n{amount} <:DanTix:919966342797463552> are put on the line")
        
        dunkbed = discord.Embed(title= "DUNK TANK",colour = discord.Colour.purple())
        dunkbed.set_author(name = (ctx.author.name))
        dunkbed.set_thumbnail(url ="https://cdn.discordapp.com/emojis/887167642417373246.webp?size=96&quality=lossless")
        dunkbed.add_field(name =f"{ctx.author.name} threw a ball but missed the <:Target:887076837392527400>", value = f"you now have {ubal}", inline = True)
        dunkbed.add_field(name =f"{member.name} won the bet and is dry", value = f"they now have {mbal}",inline = True)
        await ctx.send(embed = dunkbed)


    elif amount >= 2 and dunk_aim >= 50:
        
        users[str(user.id)]["ticket"] += amount
        users[str(mem.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        await ctx.followup.send(f"<@!{member.id}> sat in the dunk tank \n{amount} <:DanTix:919966342797463552> are put on the line")

        
        dunkbed = discord.Embed(title= "DUNK TANK",colour = discord.Colour.purple())
        dunkbed.set_author(name = (ctx.author.name))
        dunkbed.set_thumbnail(url="https://cdn.discordapp.com/emojis/887167642417373246.webp?size=96&quality=lossless")
        dunkbed.add_field(name =f"{ctx.author.name} threw a ball and hit the <:Target:887076837392527400>", value = f"you now have {ubal}", inline = True)
        dunkbed.add_field(name =f"{member.name} fell in to the tank and lost the bet", value = f"they now have {mbal}",inline = True)
        await ctx.send(embed = dunkbed)
        
        await ctx.send("https://tenor.com/view/fell-into-the-water-mark-chernesky-konas2002-fall-dunk-tank-gif-17968100")
        
    elif amount >= 2 and dunk_aim <= 49:
        
        users[str(mem.id)]["ticket"] += amount
        users[str(user.id)]["ticket"] -= amount
        
        with open("ticketbank.json","w") as f:
            json.dump(users,f, indent=4)
            
        ubal = users[str(user.id)]["ticket"]
        mbal = users[str(mem.id)]["ticket"]
        
        await ctx.followup.send(f"<@!{member.id}> sat in the dunk tank \n{amount} <:DanTix:919966342797463552> are put on the line")
        
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

@oimate.slash_command(name = "fishing",description = "fishing")
@commands.cooldown(1,3600,commands.BucketType.user) #1 time , 1hr cooldown , per user
async def fishing(ctx):
    await ctx.response.defer()
    
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.get("Boston")
    weather_check = weather.current.description
    
    await check_fish_cooler(ctx.author)
    await check_pet_pocket(ctx.author)
    fish = await get_fishcooler_data()
    pet = await get_petPocket_data()
    user = ctx.author
    
    
    if weather_check in rainy:
        
        cast = random.randint(5,30)
    else:
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
        "👓",
        "BEAR-acuda",
        "fish in a fish bowl",
        "old boot",
        "the other old boot",
        "a new boot",
        "a strange glowing book something about mending",
        "a peanut butter and jelly fish",
        "NEMO",
        "frozen tuna",
        "some legobricks from the 1969 LEGO satun V rocket",
    ]
    
    fishname = len(fish_name)
    randomname = random.randrange(fishname)
    named_fish = fish_name[randomname]

    fishsize = round(random.uniform(0.8,1500),2) #cm
    fishweight = random.randint(8,42624) # OZ

    if cast == 60:
        
        await ctx.followup.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        
        fishbed = discord.Embed(title="nope",colour = discord.Colour.blue())
        fishbed.set_author(name = (ctx.author.name))
        fishbed.set_thumbnail(url="https://www.emoji.co.uk/files/twitter-emojis/activity-twitter/10839-fishing-pole-and-fish.png")
        fishbed.add_field(name ="...not even a nibble", value = " ", inline = True)
        await ctx.send(embed = fishbed)
        
    elif cast < 60 and randomname != 11:
        
        await ctx.followup.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        
        fishbed = discord.Embed(title=(named_fish),colour = discord.Colour.blue())
        fishbed.set_author(name = (ctx.author.name))
        fishbed.set_thumbnail(url="https://www.emoji.co.uk/files/twitter-emojis/activity-twitter/10839-fishing-pole-and-fish.png")
        fishbed.add_field(name =f"{ctx.author.name}has fished up a {named_fish}", value = f"its {fishsize}cm and  weighs {fishweight} OZ", inline = True)
        await ctx.send(embed = fishbed)
        
        fish[str(user.id)]["fish name"].append(named_fish)
        
    elif cast < 60 and randomname == 11:
        
        await ctx.followup.send(f"{ctx.author.name} casts their line 🎣 ...")
        await asyncio.sleep(cast)
        
        pet[str(user.id)]["fish"] += 1
        
        petfish = pet[str(user.id)]["fish"]
        
        petbed = discord.Embed(title = "PET EVENT!!", colour = discord.Colour.gold())
        petbed.set_author(name = (ctx.author.name))
        petbed.set_thumbnail(url="https://www.emoji.co.uk/files/twitter-emojis/animals-nature-twitter/10682-fish.png")
        petbed.add_field(name = f"{ctx.author.name} has fished up a {named_fish} oooo looks like they have a new fishy pet friend" , value = f"they now have {petfish} :fish:" , inline = True)
        await ctx.send(embed = petbed)
                
        with open("petPocket.json" ,"w") as f:
            json.dump(pet,f, indent=4)
        
    with open("fishCooler.json","w") as f:
        json.dump(fish,f, indent=4)
            
    await client.close()
            
@fish_command.command(description = "slap someone with the fish u caught")
async def slap(ctx, member:discord.Member = None):
    await ctx.response.defer()
    
    await check_fish_cooler(ctx.author)
    fish = await get_fishcooler_data()
    user = ctx.author

    if member == None:
        await ctx.followup.send("u cant fish slap the air")

    elif len(fish[str(user.id)]["fish name"]) == 0:
        await ctx.followup.send("you have no fish")
    
    else:
        slap = fish[str(user.id)]["fish name"][-1]
        
        fish[str(user.id)]["fish name"].pop()

        with open ("fishCooler.json","w") as f:
            json.dump(fish,f, indent=4)
        
        slapbed = discord.Embed(title = "FISH SLAP",colour = discord.Colour.blue())
        slapbed.set_author(name = (ctx.author.name))
        slapbed.add_field(name = f"{ctx.author.name} just fish slaped {member.name} with", value = f"{slap}", inline = True)
        await ctx.followup.send(embed = slapbed)
        
        

###########################################
##              pets                     ##
###########################################
@pets.command(description = "sets your pet")
async def pick(ctx, *, message = None):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    
    if message == "fish" and users[str(user.id)]["fish"] > 0:
        users[str(user.id)]["active_pet"] = ""
        users[str(user.id)]["fish"] -= 1
        users[str(user.id)]["active_pet"] = "fish"
        users[str(user.id)]["pet_hunger"] = 10
        users[str(user.id)]["pet_clean"] = 10
        users[str(user.id)]["pet_health"] = 10
        users[str(user.id)]["pet_fun"] = 10
        users[str(user.id)]["pet_sickness"] = 0
        users[str(user.id)]["pet_freeze"] = 0
        await ctx.followup.send("you took your fish out of the pet_pocket and put the bowl on a table")
        
    elif message == "monkey" and users[str(user.id)]["monkey"] > 0:
        users[str(user.id)]["active_pet"] = ""
        users[str(user.id)]["monkey"] -= 1
        users[str(user.id)]["active_pet"] = "monkey"
        users[str(user.id)]["pet_hunger"] = 10
        users[str(user.id)]["pet_clean"] = 10
        users[str(user.id)]["pet_health"] = 10
        users[str(user.id)]["pet_fun"] = 10
        users[str(user.id)]["pet_sickness"] = 0
        users[str(user.id)]["pet_freeze"] = 0
        await ctx.followup.send("you took your monkey out of the pet_pocket and let him run around the living room")
        
    elif message == "snowman" and users[str(user.id)]["snowman"] > 0:
        users[str(user.id)]["active_pet"] = ""
        users[str(user.id)]["snowman"] -= 1
        users[str(user.id)]["active_pet"] = "snowman"
        users[str(user.id)]["pet_hunger"] = 10
        users[str(user.id)]["pet_clean"] = 10
        users[str(user.id)]["pet_health"] = 10
        users[str(user.id)]["pet_fun"] = 10
        users[str(user.id)]["pet_sickness"] = 0
        users[str(user.id)]["pet_freeze"] = 0
        await ctx.followup.send("you took your snowman out of the pet_pocket and let him in your house ....keep him away from the fireplace")
    
    else:
        await ctx.followup.send("your iver forgot to say what pet OR dont have any use !pet_pocket to check")
        
    with open ("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
            
@pets.command(description = "freeze pets stats for when you need to step away from discord")
async def freeze(ctx, message = None):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    if message == None:
        await ctx.followup.send("say \"!freeze on\" to freeze your pet stats  \n or \n say  \"!freeze off\" to unfreeze there stats")
    
    elif message == "on":
        users[str(user.id)]["pet_freeze"] = 1
        await ctx.followup.send("your pets stats have been frozen dont forget to unfreeze when your back ^_^")

        
    elif message == "off":
        users[str(user.id)]["pet_freeze"] = 0
        await ctx.followup.send("your pets stats are unfrozzen wellcome back :3")
        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
@pets.command( description = "name your pet")
async def name(ctx,message = None):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    if message == None:
        await ctx.followup.send("say !name_pet name to name your pet name")
        
    else:
        users[str(user.id)]["pet name"] = message
        await ctx.followup.send(f"your pet is now named {message}")
        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
            
@pets.command(description = "feed your pet")
async def feed(ctx):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    name = users[str(user.id)]["pet name"]
 
    if users[str(user.id)]["petfood"] == 0:
        await ctx.followup.send("you dont have any pet food buy some with !shop and !buy")
            
    elif users[str(user.id)]["petfood"] > 0:
        users[str(user.id)]["petfood"] -= 1
        users[str(user.id)]["pet_hunger"] += 5
        if users[str(user.id)]["pet_hunger"] > 10:
            users[str(user.id)]["pet_hunger"] = 10
        await ctx.followup.send(f"you feed {name} munches away happerly")
        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
@pets.command(description = "give your pet medicen")
async def meds(ctx):
    await ctx.response.defer()

    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author

    if users[str(user.id)]["petmed"] == 0:
        await ctx.followup.send(f"you dont have any meds for {name} but some with !shop and !buy")
            
    elif users[str(user.id)]["petmed"] > 0:
        users[str(user.id)]["petmed"] -= 1
        if users[str(user.id)]["pet_sickness"] == 1:
            users[str(user.id)]["pet_sickness"] = 0
            await ctx.followup.send(f"{name} is no longer sick")

        elif users[str(user.id)]["pet_sickness"] == 0:
            users[str(user.id)]["pet_health"] - 5
            await ctx.followup.send(f"{name} wasnt sick but now he looks worce for wear")

    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
@pets.command(description = "play with your pet")     
async def play(ctx):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    fun = random.randint(1,10)
        
    await ctx.followup.send(f"you played with {name} he fun went up by{fun} (this will be upgraded later)")
    users[str(user.id)]["pet_fun"] += fun
    if users[str(user.id)]["pet_fun"] > 10:
        users[str(user.id)]["pet_fun"] = 10
        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
@pets.command(description = "clean your pet")
async def clean(ctx):
    await ctx.response.defer()

    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
            
    await ctx.followup.send(f"you gave {name} a bath")
    users[str(user.id)]["pet_clean"] = 10
        
    with open("petPocket.json","w") as f:
        json.dump(users,f, indent=4)
        
@oimate.slash_command(name ="testt", description = "this is a commarnd to check hidden pet stats")
async def testt(ctx):
    await ctx.response.defer()
    
    await check_pet_pocket(ctx.author)
    users = await get_petPocket_data()
    user = ctx.author
    
    a = users[str(user.id)]["health_tick"]
    b = users[str(user.id)]["hunger_tick"]
    c = users[str(user.id)]["fun_tick"]
    d = users[str(user.id)]["clean_tick"]
    e = users[str(user.id)]["pet_health"]
    f = users[str(user.id)]["pet_hunger"]
    g = users[str(user.id)]["pet_fun"]
    h = users[str(user.id)]["pet_clean"]
    i = users[str(user.id)]["pet_sickness"]
    j = users[str(user.id)]["pet_freeze"]
    k = users[str(user.id)]["pet name"]
    
    
    await ctx.followup.send(f" health_tick {a} | hunger_tick {b} | fun_tick {c} | clean_tick {d} \n health {e} | hunger {f} | fun {g} | hygien {h} \n sickness (0 = good 1 = bad) {i} | frozen (0 = unfrozen 1 = frozen) {j} | name = {k}")
    
@pets.command(description = "checks on your pet")
async def check(ctx):
    await ctx.response.defer()
    
    global t1,t2,t3,b1,b2,b3
    
    
    await check_pet_pocket(ctx.author)
    await open_account(ctx.author)
    ticket = await get_ticket_data()
    users = await get_petPocket_data()
    user = ctx.author

    food = users[str(user.id)]["petfood"]
    med = users[str(user.id)]["petmed"]
    pet_monkey = users[str(user.id)]["monkey"]
    pet_snowman = users[str(user.id)]["snowman"]
    pet_fish = users[str(user.id)]["fish"]
    petname = users[str(user.id)]["pet name"]
    
    home = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/pet_home_empty.png")
    char = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/char.png")
    you = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/you.png")
    
    draw = ImageDraw.Draw(home)
    font = ImageFont.truetype(font ="/home/pi/.fonts/ZakirahsCasual.ttf",size=30)
    sont = ImageFont.truetype(font ="/home/pi/.fonts/Symbola.ttf",size = 20)

    home.paste(char, (0,0), char) #puts a char in the living room
    
    await ctx.author.display_avatar.save("/home/pi/Desktop/monkey bot discord/img/pet/face.png")
    face = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/face.png")
    face = face.resize((38,39))
    
    
    if ticket[str(user.id)]["snowman_cursed"] > 0: # check to see if the user has effects or not befor sitting in the chair
        you = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman_curse.png")
    elif ticket[str(user.id)]["splat"] > 0:
        banana = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/banana.png")
        you.paste(banana, (0,0), banana)
    else:
        you = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/you.png")

    home.paste(face, (253, 99))
        
    home.paste(you, (0,0), you)
    
    if ctx.author.id == t1:
        t = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/ticket1.png")
        home.paste(t,(0,0), t)
    elif ctx.author.id == t2:
        t = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/ticket2.png")
        home.paste(t,(0,0), t)
    elif ctx.author.id == t3:
        t = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/ticket3.png")
        home.paste(t,(0,0), t)
    if ctx.author.id == b1:
        b = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/banana1.png")
        home.paste(b,(0,0),b)
    elif ctx.author.id == b2:
        b = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/banana2.png")
        home.paste(b,(0,0),b)
    elif ctx.author.id == b3:
        b = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/top10/banana3.png")
        home.paste(b,(0,0),b)
        
    if users[str(user.id)]["active_pet"] == "monkey":
        
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
            
        draw.text((335,200),"SICKNESS",font=font,size =20)
        if users[str(user.id)]["pet_sickness"] == 0:
            draw.text((351,230),"Healthy", font=font)
        else:
            draw.text((351,230),"Sick", font=font)
            
        draw.text((335,260), "health",font = font)
        if users[str(user.id)]["pet_health"] > 8:
            draw.text((351,290),"💙 💙 💙 💙 💙",font = sont,fill = "red")
        elif users[str(user.id)]["pet_health"] == 8 or users[str(user.id)]["pet_health"] == 7:
            draw.text((351,290),"💙 💙 💙 💙",font = sont, fill = "red")
        elif users[str(user.id)]["bet_health"] == 6 or users[str(user.id)]["pet_health"] == 5:
            draw.text((351,290),"💙 💙 💙", font = sont, fill= "red")
        elif users[str(user.id)]["pet_health"] == 4 or users[str(user.id)]["pet_health"] == 3:
            draw.text((351,290),"💙 💙",font = sont, fill="red")
        elif users[str(user.id)]["pet_health"] == 2 or users[str(user.id)]["pet_health"] == 1:
            draw.text((351,290),"💙",font = sont, fill = "red")
        else:
            draw.text((351,290),"DEAD", font = sont, fill = "red")
            
        monkey = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_normal.png")
            
        if users[str(user.id)]["pet_health"] == 0:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_dead.png")
        elif users[str(user.id)]["pet_fun"] <= 6 :
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_bored.png")
        elif users[str(user.id)]["pet_hunger"] <= 6 :
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_hungry.png")
        elif users[str(user.id)]["pet_sickness"] == 1:
            monkey = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_sick.png")
        
        if users[str(user.id)]["pet_clean"] < 6:
            mess = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/monkey/monkey_dirty.png")
            home.paste(mess, (0,0), mess)
            
        home.paste(monkey, (0,0), monkey)

        home.save("/home/pi/Desktop/monkey bot discord/img/pet/monkey_home.png", "PNG")

        await ctx.followup.send(file = discord.File("/home/pi/Desktop/monkey bot discord/img/pet/monkey_home.png"))
        await ctx.send(f"{ctx.author.name} has {food}🥫 in the cupboards | {med} 💊 in the first-aid box | {petname}")
        os.remove("/home/pi/Desktop/monkey bot discord/img/pet/monkey_home.png") 
    
    elif users[str(user.id)]["active_pet"] == "snowman":

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
            
        draw.text((335,200),"SICKNESS",font=font,size =20)
        if users[str(user.id)]["pet_sickness"] == 0:
            draw.text((351,230),"Healthy", font=font)
        else:
            draw.text((351,230),"Sick", font=font)
            
        draw.text((335,260), "health",font = font)
        if users[str(user.id)]["pet_health"] > 8:
            draw.text((351,290),"💙 💙 💙 💙 💙",font = sont,fill = "red")
        elif users[str(user.id)]["pet_health"] == 8 or users[str(user.id)]["pet_health"] == 7:
            draw.text((351,290),"💙 💙 💙 💙",font = sont, fill = "red")
        elif users[str(user.id)]["bet_health"] == 6 or users[str(user.id)]["pet_health"] == 5:
            draw.text((351,290),"💙 💙 💙", font = sont, fill= "red")
        elif users[str(user.id)]["pet_health"] == 4 or users[str(user.id)]["pet_health"] == 3:
            draw.text((351,290),"💙 💙",font = sont, fill="red")
        elif users[str(user.id)]["pet_health"] == 2 or users[str(user.id)]["pet_health"] == 1:
            draw.text((351,290),"💙",font = sont, fill = "red")
        else:
            draw.text((351,290),"DEAD", font = sont, fill = "red")
            
        snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_normal.png")
        
        if users[str(user.id)]["pet_health"] == 0:
            snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_dead.png")
        elif users[str(user.id)]["pet_health"] >=1 and users[str(user.id)]["pet_sickness"] == 1:
            snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_sick.png")
        elif users[str(user.id)]["pet_clean"] <= 6:
            snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_dirty.png")
        elif users[str(user.id)]["pet_hunger"] <=6:
            snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_hungery.png")
        elif users[str(user.id)]["pet_fun"] <= 6:
            snowman = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/snowman/snowman_bored.png")
            
        home.paste(snowman,(0,0),snowman)
        
        home.save("/home/pi/Desktop/monkey bot discord/img/pet/snowman_home.png", "PNG")
    
        await ctx.followup.send(file = discord.File("/home/pi/Desktop/monkey bot discord/img/pet/snowman_home.png"))
        await ctx.send(f"{ctx.author.name} has {food}🥫 in the cupboards | {med} 💊 in the first-aid box | {petname}")
        os.remove("/home/pi/Desktop/monkey bot discord/img/pet/snowman_home.png")  
    
    elif users[str(user.id)]["active_pet"] == "fish":

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
            
        draw.text((335,270), "health",font = font)
        if users[str(user.id)]["pet_health"] > 8:
            draw.text((351,300),"💙 💙 💙 💙 💙",font = sont,fill = "red")
        elif users[str(user.id)]["pet_health"] == 8 or users[str(user.id)]["pet_health"] == 7:
            draw.text((351,300),"💙 💙 💙 💙",font = sont, fill = "red")
        elif users[str(user.id)]["bet_health"] == 6 or users[str(user.id)]["pet_health"] == 5:
            draw.text((351,300),"💙 💙 💙", font = sont, fill= "red")
        elif users[str(user.id)]["pet_health"] == 4 or users[str(user.id)]["pet_health"] == 3:
            draw.text((351,300),"💙 💙",font = sont, fill="red")
        elif users[str(user.id)]["pet_health"] == 2 or users[str(user.id)]["pet_health"] == 1:
            draw.text((351,300),"💙",font = sont, fill = "red")
        else:
            draw.text((351,300),"DEAD", font = sont, fill = "red")

        fishbowl = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/fishbowl.png")
    
        if users[str(user.id)]["pet_health"] == 0:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/fish_dead.png")
    
        elif users[str(user.id)]["pet_health"] >= 1 and users[str(user.id)]["pet_sickness"] == 1:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/fish_sick.png")
        else:
            fish = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/fish_happy.png")
        
        if users[str(user.id)]["pet_clean"] <= 6:
            fishwater = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/dirty_water.png")
        else:
            fishwater = Image.open("/home/pi/Desktop/monkey bot discord/img/pet/fish/clean_water.png")
    
        fishwater.paste(fish, (0,0), fish)

        fishbowl.paste(fishwater, (0,0), fishwater)

        home.paste(fishbowl, (0, 0), fishbowl)
        
        
        
        home.save("/home/pi/Desktop/monkey bot discord/img/pet/fish_home.png", "PNG")
    
        await ctx.followup.send(file = discord.File("/home/pi/Desktop/monkey bot discord/img/pet/fish_home.png"))
        await ctx.send(f"{ctx.author.name} has {food}🥫 in the cupboards | {med} 💊 in the first-aid box | {petname}")
        os.remove("/home/pi/Desktop/monkey bot discord/img/pet/fish_home.png")  
        
    elif users[str(user.id)]["active_pet"] == "":
        home.save("/home/pi/Desktop/monkey bot discord/img/pet/you_home.png", "PNG")
        await ctx.followup.send(file = discord.File("/home/pi/Desktop/monkey bot discord/img/pet/you_home.png"))
        await ctx.send(f"you dont have a active in your pet pocket ther is {pet_monkey} 🐒 | {pet_snowman} ⛄ | {pet_fish} 🐟 \n more pets coming soon:tm:")
        os.remove("/home/pi/Desktop/monkey bot discord/img/pet/you_home.png")
        
    os.remove("/home/pi/Desktop/monkey bot discord/img/pet/face.png")
     
     
     
###########################################
##         twitch tickets               ###
###########################################

@oimate.slash_command(name = "name", description = "let monkeybot know your name makes it easyer to find u in the .json files")
async def login(ctx, message = None):
    await ctx.response.defer()
    
    await open_account(ctx.author)
    users = await get_ticket_data()
    user = ctx.author
    
    if message == None:
        await ctx.followup.send("use !login'your twitch name' so monkeybot knows who you are for twitch ticket giving :P")
    
    elif message != None:
    
        users[str(user.id)]["twitch"] = message
        
        await ctx.followup.send(f"ok your twitch name is {message} right? reuse the commarnd if its wrong")
    
    with open("ticketbank.json","w") as f:
        json.dump(users,f,indent=4)
        
############################################
##monkeys attempted at gameing for discord##
############################################


@oimate.slash_command(name = "gamestart", description = "only monkey can use this to start discordplays gamein VC")
async def gamestart(ctx):
    await ctx.response.defer()
    
    global password
    global monkey
    global dks
    if ctx.author.id == monkey: #this is MY discord id so only me can use this commarnd
        password = True
        await ctx.followup.send("games enabled")
    elif ctx.author.id == dks: #this is monkeyDKS id so me can be cheaky and give him a specal responce
        await ctx.followup.send("sorry DKS you are not the right monkey for this command ***froundy face*** BUT heres a ticket to the carnie <:DanTix:919966342797463552>")
    else:
        await ctx.followup.send("you are not monkey only he can start games")


@oimate.slash_command(name = "gamestop", description = "only monkey can use this to end the game")
async def gamestop(ctx):
    await ctx.response.defer()
    
    global password
    global monkey
    global dks
    if ctx.author.id == monkey:
        password = False
        await ctx.followup.send("games disabled")
    elif ctx.author.id == dks:
        await ctx.followup.send("sorry DKS you are not the right monkey for this command ***froundy face*** BUT heres a ticket to the carnie <:DanTix:919966342797463552>")
    else:
        await ctx.followup.send("you are not monkey only he can stop games")
        
@oimate.slash_command(name= "dpad", description = "dpad gui for discord plays...")
async def dpad(ctx):
    global password
    button0 = Button(label = "left click")
    button1 = Button(label = "up")
    button2 = Button(label = "right clock")
    button3 = Button(label = "m up")
    button4 = Button(label = "m left")
    button5 = Button(label = "left")
    button6 = Button(label = " ")
    button7 = Button(label = "right")
    button8 = Button(label = "m down")
    button9 = Button(label = "m right")
    
    button10 = Button(label = " ")
    button11 = Button(label = "down")
    button12 = Button(label = " ")
    button13 = Button(label = " ")
    button14 = Button(label = " ")
    
    async def button1_callback(interaction):
        if password == True:
            fishNchips.tap(Key.up)
        
    button1.callback = button1_callback
    
    async def button5_callback(interaction):
        if password == True:
            fishNchips.tap(Key.left)
        
    button5.callback = button5_callback
    
    async def button7_callback(interaction):
        if password == True:
            fishNchips.tap(Key.right)
        
    button7.callback = button7_callback
    
    async def button11_callback(interaction):
        if password == True:
            fishNchips.tap(Key.down)
        
    button11.callback = button11_callback
    
    async def button0_callback(interaction):
        if password == True:
            fishNchips.press(Button.left)
            fishNchips.release(Button.left)
        
    button0.callback = button0_callback
    
    async def button2_callback(interaction):
        if password == True:
            fishNchips.press(Button.right)
            fishNchips.release(Button.right)
        
    button2.callback = button2_callback
    
    async def button3_callback(interaction):
        fishNchips.move(0, 15)
        
    button3.callback = button3_callback
    
    async def button8_callback(interaction):
        if password == True:
            fishNchips.move(0, -15)
        
    button8.callback = button3_callback
    
    async def button4_callback(interaction):
        if password == True:
            fishNchips.move(-15, 0)
        
    button4.callback = button4_callback
    
    async def button9_callback(interaction):
        if password == True:
            fishNchips.move(15, 0)
        
    button9.callback = button9_callback
        
    
    view = View()
    view.add_item(button0)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    view.add_item(button6)
    view.add_item(button7)
    view.add_item(button8)
    view.add_item(button9)
    view.add_item(button10)
    view.add_item(button11)
    view.add_item(button12)
    view.add_item(button13)
    view.add_item(button14)
    if password == False:
        await ctx.followup.send("there is no game playing atm check with monkey")
    elif password == True:
        print(1)
        await ctx.followup.send("chicken", view = view)

choco_loop.start()
pet_tick.start()
trophy_check.start()

oimate.run(token)
