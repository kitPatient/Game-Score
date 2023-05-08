import discord
import csv
from datetime import date
import sys

try:
    with open("token.token", "r") as tokenFile:
        bot_token: str = tokenFile.read()
except FileNotFoundError:
    print("Token is not found in: ", '''"token.token"''')
    sys.exit(-1)

commandPrefix: str = "!"
reactionMessage: str = "To Save The Scores: React to This Message"
OutputFileName: str = "allGames.csv"

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

client: discord.Client = discord.Client(intents=intents)

fm: list = []


def formantScore(scores: list, gameName: str) -> list:
    formated: list = [f"{date.today()}", f"{gameName}"]
    for playerGame in scores:
        formated.append(f"{playerGame[0]}: {playerGame[1]}")
    return formated


def saveCSV(formattedScore: list, filename: str = OutputFileName) -> None:
    with open(filename, "a", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(formattedScore)


async def interpret(content: str) -> list:
    cmd_list: list = content.split()
    print(cmd_list)

    if len(cmd_list) <= 2:
        print("Not Enough Args Given")

    cmd_list.pop(0)

    game_name = cmd_list.pop(0)
    # print(game_name)

    if len(cmd_list) % 2 != 0:
        print("Not Enough Args Given")

    x: int = len(cmd_list)
    scores: list = []
    while x != 0:
        scores.append((cmd_list.pop(0), cmd_list.pop(0)))
        x = len(cmd_list)

    return scores


def gameFrom(content: str) -> str:
    cmd_list: list = content.split()
    print(cmd_list)

    if len(cmd_list) <= 2:
        print("Not Enough Args Given")

    cmd_list.pop(0)

    return cmd_list.pop(0)


def cmd(content: str, command: str) -> bool:
    return content.lower().startswith(commandPrefix + command.lower())


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.message) -> None:
    content: str = message.content
    if message.author == client.user:
        return

    if cmd(content, "ping"):
        await message.channel.send("Pong!")

    if cmd(content, "score"):
        scores: list = await interpret(content)
        global fm
        fm = formantScore(scores, gameFrom(content))
        await message.channel.send(fm)
        await message.channel.send(reactionMessage)

    if cmd(content, "file"):
        await message.channel.send(file=discord.File(OutputFileName))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User) -> None:
    global fm
    message: str = reaction.message.content
    if message == reactionMessage:
        if len(fm) > 2:
            saveCSV(fm)
            fm = []
            await reaction.message.channel.send("Saved")
        else:
            await reaction.message.channel.send("Unable To Save Scores")


client.run(bot_token)
