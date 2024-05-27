import discord
from discord.ext import commands
from config import  Bot
from discord.ui import Button, button, View
from discord import app_commands

class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Create Ticket", style= discord.ButtonStyle.blurple, emoji="🎫", custom_id="ticketopen")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        category : discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1244523604524273764)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHNAGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send("You are already have a ticket in {0}".format(ch.mention), ephemeral= True)
                return
            
        r1: discord.Role = interaction.guild.get_role(1244520453045751930)
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages = False),
            r1: discord.PermissionOverwrite(read_messages = True, send_messages = True, manage_messages= True),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = True),
            interaction.guild.me :  discord.PermissionOverwrite(read_messages = True, send_messages = True)
        }

        channel = await category.create_text_channel(
            name= f"ticket-channel-{interaction.user}", 
            topic = f"{interaction.user.id} DO NOT CHNAGE THE TOPIC OF THIS CHANNEL!", 
            overwrites =overwrites,)

        await channel.send(
            embed= discord.Embed(
                title="Ticket create!", 
                description= "Dont ping the staff member, they will be here soon",
                color= discord.Color.green()
            )
        )
        await interaction.followup.send( 
            embed= discord.Embed(
                    description = "Created your ticket in {0}".format(channel.mention),
                    color = discord.Color.blurple()), ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="ticket")
    @app_commands.checks.has_permissions(administrator = True)
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Support Ticket",
            description="Press the button to create a new ticket"
        )
        view = CreateButton()
        await interaction.response.send_message(embed= embed, view= view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))