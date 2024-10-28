import discord
from discord.ext import commands, tasks
import asyncio
import random
from discord import app_commands,Webhook,SyncWebhook
from discord import interactions
#discord.utils.setup_logging()

token = "MTI4NjA0MDczMDM3MTg4NzE3OQ.GwiCDr.4Ix1lx984bFO6AE5eQOjzj_G8RkRgUcjQgGSHY"

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


file = open("D:/Code/Python/Bot2.0/All_Words.txt", "r")
listOfWords = file.read().splitlines()
#Colors
fail_colour =  discord.Color.red()
success_colour = discord.Color.green()
error_colour = discord.Color.brand_red()
question_colour = discord.Color.blurple()
#Error Embed
error_embed = discord.Embed(title="Error in Code,Ping Mr.Pancakes")
 
 
def choose_random_word(length):
    # Filter words by the specified length
    
    words = [word for word in listOfWords if len(word) == length]
    return random.choice(words)

@client.event
async def on_ready():
    activity = discord.Game(name="I am human")
    await client.change_presence(status=discord.Status.online, activity=activity)
    await tree.sync()
    print("Ready!")

@tree.command(name="guess", description="Starts a Guessing Minigame") 
async def guess(interaction: interactions.AppCommandContext): 
    #Variables
    randword1 = random.choice(listOfWords)
    randword2 = random.choice(listOfWords)
    randword3 = random.choice(listOfWords)
    right_ans = random.choice([randword3, randword2, randword1])
    attempts = 2
    channel = interaction.channel
    #Channel is the channel the interaction was sent in
     
    
    
    
    def check(m):
        return m.channel == channel and m.author == interaction.user 
    
    



    #First Embed
    embeded_msg = discord.Embed(title="Guess the Password!", description="Guess the Password", color=question_colour)
    embeded_msg.add_field(name="The password is either", value=f"{randword2} or {randword3} or {randword1}", inline=False)
    await interaction.response.send_message(embed=embeded_msg) # type: ignore



    #check if the user and channel are correct


    while attempts > 0:
        
        msg = await client.wait_for('message', check=check)
        msg_content = msg.content.lower().strip(' ')  


        if msg_content == right_ans.lower():
            embeded_msg = discord.Embed(title="Good job", color=success_colour)
            embeded_msg.add_field(name="You guessed the password Correctly!", value="Congrats Here is your reward!", inline=False)
            await msg.add_reaction('✅')
            await channel.send(embed=embeded_msg)
            delete = await channel.send(f"+add-money {msg.author.mention}  {random.randint(5000,10000)}")
            await delete.delete()
            break
            
        elif msg_content != right_ans.lower():
            attempts = attempts - 1
            await msg.add_reaction('❌')
            embeded_msg = discord.Embed(title="Guess the Password!", description="", color=question_colour)
            embeded_msg.add_field(name="The password is either", value=f"{randword2} or {randword3} or {randword1}", inline=False)
            embeded_msg.add_field(name="Attempts Left", value=f"{attempts}", inline=False)
            await channel.send(embed=embeded_msg)

        

    if attempts == 0:
        embeded_msg = discord.Embed(title="Game Over", color=fail_colour)
        embeded_msg.add_field(name="You didn't guess the password", value=f"The correct answer was **{right_ans}**", inline=False)
        await msg.add_reaction('❌')
        await channel.send(embed=embeded_msg)  
        

#---------------------------------------------------------------------------------------------------------------------------------------
@tree.command(name="completion",description="Starts a Minigame where you have to complete the word") 
async def completion(interaction: interactions.AppCommandContext): 
    chosen_word = random.choice(listOfWords)#Choose a random Word from the text file
    attempts = 3
    channel = interaction.channel #Define channel for easier use

    try:
        listified=list(chosen_word)#Convert the chosen word into a list
        random_items = random.sample(listified, 1)#Randomly Take 1 item from the list



        for item in random_items:#Iterate through the list
            listified[listified.index(item)] = "_"#Replace the 1 Random Item and replace with #


        joined = (''.join(listified))
        random_items = (''.join(random_items))
        #Send the first embed
        embeded_msg = discord.Embed(title="Complete the word!",color=question_colour)
        embeded_msg.add_field(name=f"Word to complete is:\n{joined}",value="",inline=False)
        embeded_msg.add_field(name=f"Attempts Left: {attempts}", value="Good Luck!", inline = False)
        await interaction.response.send_message(embed=embeded_msg) # type: ignore
            
        def check(m):#Subprogram to check if user is in right channel and IS the right user
            return m.channel == channel and m.author == interaction.user # type: ignore

        msg = await client.wait_for('message', check=check)#Wait for Client Message
        msg_content = msg.content.lower().strip(' ')  #.lower the message


        while len(msg_content)!= 1:#Message Can't be longer than one 1 word
            

            await msg.add_reaction('🚫')
            await channel.send("**Your answer can't be longer than 1 letter!**")
            await asyncio.sleep(0.5)#Wait/Sleep for 0.5 seconds
            embeded_msg = discord.Embed(title="Complete the word!",description="", color = question_colour)
            embeded_msg.add_field(name=f"Word to complete is:\n{joined}",value="",inline=False)
            embeded_msg.add_field(name=f"Attempts Left: {attempts}", value="Good Luck!", inline = False)
            await channel.send(embed=embeded_msg)
            
            msg = await client.wait_for('message', check=check)
            msg_content = msg.content.lower().strip(' ')        
        while attempts > 0:
            

            
            print(random_items)
            if msg_content == random_items.lower():
                
                right = msg_content
                index = listified.index('_')
                listified.remove('_')
                listified.insert(index, right)
                joined = (''.join(listified))
                
                
                embeded_msg=discord.Embed(title="**Congrats you guessed the letter correctly!**",color=success_colour)
                embeded_msg.add_field(name=f"The Completed word was **{joined}!**",value="",inline = True)
                await channel.send(embed=embeded_msg)
                await msg.add_reaction('✅')
                delete = await channel.send(f"+add-money {msg.author.mention}  {random.randint(5000,129000)}")
                await asyncio.sleep(0.1)
                await delete.delete()
                break
                
            elif msg_content != random_items.lower():
                attempts = attempts - 1
                embeded_msg=discord.Embed(title="Wrong Guess",color=fail_colour)
                embeded_msg.add_field(name="Try again\n",value="",inline=True)
                embeded_msg.add_field(name=f"Attempts Left - {attempts}",value="Good Luck",inline=False)
                await msg.add_reaction('❌')   
                await channel.send(embed=embeded_msg)
                
                if attempts == 0:
                    embeded_msg = discord.Embed(title="Game Over", color=fail_colour)
                    embeded_msg.add_field(name="You didn't guess the right letter", value=f"The correct letter was: '{''.join(random_items)}'\n and the full word was: {chosen_word}", inline=False)
                    await msg.add_reaction('❌')
                    await channel.send(embed=embeded_msg)
                    
                        
            msg = await client.wait_for('message', check=check)
            msg_content = msg.content.lower()        

    except  Exception as e:
        await interaction.response.send(embed = error_embed)
        print(f"Error recording feedback for {interaction.user} due to {e}")

#---------------------------------------------------------------------------------------------------------------------------------------    
@tree.command(name="feedback",description="Give Feedback to Mr. Pancakes!")
async def feedback(interaction: discord.Interaction, feedback: str):
    
    try:
        with open("D:/Code/Python/Bot2.0/User_suggestions.txt","a") as file:
            file.write(f"{interaction.user}'s feedback is - ('{feedback}')\n")
            await interaction.response.send_message("Feedback Recorded!")    
    
    except Exception as e:
        await interaction.channel.send(embed = error_embed)
        print(f"Error recording feedback for {interaction.user} due to {e}")
file.close()
    
    
    
#---------------------------------------------------------------------------------------------------------------------------------------    
@tree.command(name="hangman", description="Starts a game of hangman")
@app_commands.describe(difficulty="Choose a difficulty level")
@app_commands.choices(difficulty=[
    app_commands.Choice(name="5-letter", value= 5),
    app_commands.Choice(name="6-letter", value= 6),
    app_commands.Choice(name="7-letter", value= 7)
])
async def hangman(interaction: discord.Interaction, difficulty: int):
    channel = interaction.channel
    attempts = difficulty + 2
    chosen_word = choose_random_word(difficulty)
    print(chosen_word)
    
    # Initialize display with first letter revealed and rest as underscores
    display = chosen_word[0] + '_' * (len(chosen_word) - 1)
    
    def check(m):
        return m.channel == channel and m.author == interaction.user
    
    try:        
        embeded_msg = discord.Embed(title="Hangman Begin!", description=f"Your Hangman game has started\nAttempts left: {attempts}\nWord: {display}\nGuessed Letters: None")
        await interaction.response.send_message(embed=embeded_msg)
        
        guessed_letters = []
        while attempts > 0:
            msg = await client.wait_for('message', check=check)
            guess = msg.content.lower().strip()
            
            if len(guess) != 1:
                await channel.send("Please guess a single letter.")
                continue
            
            if guess in guessed_letters:
                await channel.send("You've already guessed that letter!")
                continue
            
            guessed_letters.append(guess)
            
            if guess in chosen_word:
                new_display = ""
                for i, letter in enumerate(chosen_word):
                    if letter == guess or display[i] != '_':
                        new_display += letter
                    else:
                        new_display += '_'
                display = new_display
                
                if display == chosen_word:
                    embeded_msg = discord.Embed(title="Congratulations!", description=f"You won the game! The word was: {chosen_word}")
                    await channel.send(embed=embeded_msg)
                    return
            else:
                attempts -= 1
            
            embeded_msg = discord.Embed(title="Hangman", description=f"Attempts left: {attempts}\nWord: {display}\nGuessed Letters: {', '.join(guessed_letters)}")
            await channel.send(embed=embeded_msg)
        
        if attempts == 0:
            embeded_msg = discord.Embed(title="Game Over!", description=f"You lost the game. The word was: {chosen_word}")
            await channel.send(embed=embeded_msg)

    except Exception as e:
        await interaction.channel.send(embed=error_embed)
        print(f"Error in hangman game for {interaction.user} due to {e}")
        
#---------------------------------------------------------------------------------------------------------------------------------------
            





client.run(token)