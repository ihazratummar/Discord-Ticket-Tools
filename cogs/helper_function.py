import discord
import chat_exporter
from github import Github
from dotenv import load_dotenv
import os
import time

load_dotenv()

async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = guild.get_channel(1244549170883330078)
    t = time.localtime()
    formatted_time = time.strftime("%y-%m-%d %H:%M:%S", t)
    embed = discord.Embed(
        title= title,
        description= description,
        color= color
    )
    embed.add_field(name="Time", value=formatted_time)
    await log_channel.send(embed= embed)

##GET TRANSCRIPT
async def get_transcript(member : discord.Member, channel:discord.TextChannel):
    export  = await chat_exporter.export(channel= channel)
    file_name = f'{member.id}.html'
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(export)

#UPLOAD TO GITHUB
git_token = os.getenv("GITHUB_TOKEN")
def upload(file_path: str, member_name: str):

    github = Github(git_token)
    repo = github.get_repo("ihazratummar/ticket-transcript")
    file_name = f"{int(time.time())}"
    repo.create_file(
        path=f"tickets/{file_name}.html",
        message="Ticket Log for {0}".format(member_name),
        branch="main",
        content=open(f"{file_path}","r",encoding="utf-8").read()
    )
    os.remove(file_path)

    return file_name
