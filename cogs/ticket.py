import discord
from discord.ext import commands
from config import  Bot
from discord.ui import Button, button, View
from discord import app_commands
import asyncio
from cogs import helper_function


class CreateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Create Ticket", style= discord.ButtonStyle.blurple, emoji="🎟️", custom_id="ticketopen")
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
            ),
            view= CloseButton()
        )
        await interaction.followup.send( 
            embed= discord.Embed(
                    description = "Created your ticket in {0}".format(channel.mention),
                    color = discord.Color.blurple()), 
                    ephemeral=True
                    )
        await helper_function.send_log(
            title= "Ticket Created",
            description= "**Created by** {0}".format(interaction.user.mention),
            color= discord.Color.green(),
            guild=interaction.guild
        )
        
class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Close the ticket", style= discord.ButtonStyle.red, custom_id="closeticket",emoji="🔒")
    async def close(self, interaction : discord.Interaction, button:Button):
        await interaction.response.defer(ephemeral=True)

        await interaction.channel.send("Closing this ticket....")
        await asyncio.sleep(3)

        category : discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id = 1244541449307951144)

        r1: discord.Role = interaction.guild.get_role(1244520453045751930)
        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages = False),
            r1: discord.PermissionOverwrite(read_messages = True, send_messages = True, manage_messages= True),
            interaction.guild.me :  discord.PermissionOverwrite(read_messages = True, send_messages = True)
        }

        await interaction.channel.edit(category= category, overwrites= overwrites)
        await interaction.channel.send(
            embed= discord.Embed(
                description="Ticket is closed",
                color= discord.Color.red()
            ),
            view=Trushbutton()
        )

        # Extract member ID from channel topic and validate
        topic_parts = interaction.channel.topic.split(" ")
        member_id = topic_parts[0] if topic_parts else None
        
        # Debug statement for parsed member ID
        print(f"Debug: Parsed member ID from topic: {member_id}")
        
        if member_id:
            try:
                # Use fetch_member to ensure we are getting the most up-to-date member object
                member = await interaction.guild.fetch_member(int(member_id))
                
                # Debug statement for retrieved member
                print(f"Debug: Retrieved member: {member}")
            except (ValueError, discord.NotFound):
                member = None
                
                # Debug statement for invalid member ID format or member not found
                print(f"Debug: Invalid member ID format or member with ID {member_id} not found.")
            
            if member:
                await helper_function.get_transcript(member=member, channel=interaction.channel)
                file_name = helper_function.upload(f'{member.id}.html',member.name)
                link = f"https://ihazratummar.github.io/ticket-transcript/tickets/{file_name}"
                await helper_function.send_log(
                    title="Ticket Closed",
                    description=f"**Closed by:** {interaction.user.mention}\n[Click for Transcript]({link})",
                    color=discord.Color.yellow(),
                    guild=interaction.guild
                )
            else:
                await interaction.followup.send("Error: Unable to find the member associated with this ticket.", ephemeral=True)
        else:
            await interaction.followup.send("Error: Invalid topic format. Member ID not found.", ephemeral=True)

class Trushbutton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="Delete the Ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id= "trash")
    async def trah(self, interaction : discord.Interaction, button:Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Deleting channel .....")
        await asyncio.sleep(3)

        await interaction.channel.delete()

        await helper_function.send_log(
            title= "Ticket Deleted",
            description= f"**Deleted by:** {interaction.user.mention},\n**Ticket Name:** {interaction.channel.name}",
            color= discord.Color.red(),
            guild=interaction.guild
        )

class Ticket(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="ticket")
    @app_commands.checks.has_permissions(administrator = True)
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Create a Ticket to Contact Our Support Team",
            description="To Create a Ticket React with 🎟️",
            color= discord.Color.brand_green()
        )
        
        embed.set_author(name=f"{interaction.guild.name}")
        view = CreateButton()
        await interaction.response.send_message(embed= embed, view= view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))