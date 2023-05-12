import discord
from csv import writer, reader
from datetime import date
from sys import exit

try:
    with open("token.token", "r") as tokenFile:
        bot_token: str = tokenFile.read()
except FileNotFoundError:
    print("Token is not found in: ", '''"token.token"''')
    exit(-1)

commandPrefix: str = "!"
reactionMessage: str = "To Save The Scores: React to This Message"
OutputFileName: str = "allGames.csv"

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

client: discord.Client = discord.Client(intents=intents)

tempScores: list = []


def splitAtUpperCase(text: str) -> list[str]:
    result: str = ""
    for char in text:
        if char.isupper():
            result += " " + char
        else:
            result += char
    return result.split()


def formantScore(scores: list, gameName: str) -> list:
    formated: list = [f"{date.today()}", f"{gameName}"]
    for playerGame in scores:
        formated.append(f"{playerGame[0]}: {playerGame[1]}")
    return formated


def saveCSV(formattedScore: list, filename: str = OutputFileName) -> None:
    with open(filename, "a", newline="") as csvFile:
        CSVwriter = writer(csvFile)
        CSVwriter.writerow(formattedScore)


async def interpretScore(content: str) -> list:
    cmd_list: list = argsList(content)

    game_name: str = cmd_list.pop(0)

    if len(cmd_list) % 2 != 0:
        print("Not Enough Args Given")

    x: int = len(cmd_list)
    scores: list = []
    while x != 0:
        scores.append((cmd_list.pop(0), cmd_list.pop(0)))
        x = len(cmd_list)

    return scores


def argsList(content: str, MinLength: int = 2) -> list:
    cmd_list: list = content.split()
    print(cmd_list)

    if len(cmd_list) < MinLength:
        print("Not Enough Args Given")

    cmd_list.pop(0)
    return cmd_list


def gameFrom(content: str) -> str:
    cmd_list: list = argsList(content)
    return cmd_list.pop(0)


def getLastPlayed(game: str, allGames: list) -> list[str]:
    last: list[str] = []
    for played in allGames:
        if len(played) >= 2:
            # print(f"Testing {played[1]} Against {game}")
            if played[1] == game:
                last.append(played[0])
    if len(last) < 1:
        last.append("Not Played Yet")
    return last[len(last) - 1]


@client.event
async def on_ready() -> None:
    print(f"Successfully logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    content: str = message.content

    def cmd(command: str) -> bool:
        return content.lower().startswith(commandPrefix + command.lower())

    async def post(messageTxt: str = None, file: discord.File = None) -> None:
        return await message.channel.send(messageTxt, file=file)

    if message.author == client.user:
        return

    if cmd("ping"):
        await post("Pong!")

    if cmd("score"):
        scores: list = await interpretScore(content)
        global tempScores
        tempScores = formantScore(scores, gameFrom(content))
        await post(tempScores)
        await post(reactionMessage)

    if cmd("file"):
        outputFile: discord.File = discord.File(OutputFileName)
        await post(file=outputFile)
        await message.delete()

    if cmd("last"):
        stored: list = []
        with open(OutputFileName, newline="") as csvFile:
            CSVreader: reader = reader(csvFile, delimiter=",", quotechar='"')
            for row in CSVreader:
                stored.append(row)
        Args: list[str] = argsList(content, 1)
        lastPlayed: str = getLastPlayed(Args[0], stored)
        await post(lastPlayed)

    if cmd("show"):
        with open(OutputFileName, newline="") as csvFile:
            lg = csvFile.readlines()[-1]

        lastGameHolder = lg.split(",")

        gameName = lastGameHolder[1]
        words = splitAtUpperCase(gameName)
        FormatedName = " ".join(words).capitalize()

        if FormatedName == "Spirit island":
            advisory = lastGameHolder.pop()
            datePlayed = lastGameHolder[0]
            playerScores = lastGameHolder[2:]

            file = discord.File("images/spiritisland.jpg", filename="spiritisland.png")
            embed = discord.Embed(title="Spirit Island", color=0x202020)
            advisory = advisory.split(": ")[1]
            for player in playerScores:
                t = player.split(": ")
                board = " ".join(splitAtUpperCase(t[1])).capitalize()
                embed.add_field(name=f"{t[0].capitalize()}", value=board, inline=False)

            embed.add_field(name="Advisory", value=advisory.capitalize())
            embed.add_field(name="Date", value=datePlayed)
            embed.set_image(url="attachment://spiritisland.png")
            await message.channel.send(file=file, embed=embed)
            await message.delete()


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User) -> None:
    global tempScores
    message: str = reaction.message.content
    if message == reactionMessage:
        if len(tempScores) > 2:
            saveCSV(tempScores)
            tempScores = []
            await reaction.message.channel.send("Saved")
        else:
            await reaction.message.channel.send("Unable To Save Scores")


client.run(bot_token)
