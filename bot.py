import discord
from discord.ext import commands
import os

# Intents are required for bot features like reading member updates
intents = discord.Intents.default()
intents.members = True

# Bot prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot Ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

# Command: Kick a user
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked. Reason: {reason}")

# Command: Ban a user
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned. Reason: {reason}")

# Command: Unban a user
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"{user.name} has been unbanned.")
            return
    await ctx.send(f"User {member_name} not found.")

# Command: Add a role to a user
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"Added {role.name} role to {member.display_name}.")

# Command: Remove a role from a user
@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"Removed {role.name} role from {member.display_name}.")

# Command: Clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Cleared {amount} messages.")

# Command: List server roles
@bot.command()
async def roles(ctx):
    roles = [role.name for role in ctx.guild.roles]
    await ctx.send(f"Roles in this server: {', '.join(roles)}")

# Error handler for missing permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide all required arguments.")
    else:
        raise error

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
