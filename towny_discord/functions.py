import discord
from towny_discord import token
from discord.ext import commands
from towny.functions import player_by_info

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

roles_prefix = 'Nation: '


def make_nation_role(nation):
    global roles_prefix
    return f'{roles_prefix}{nation}'


def is_it_nation_role(nation_role_name):
    global roles_prefix
    if nation_role_name[:len(roles_prefix)] == roles_prefix:
        return True
    return False


async def remove_nation_roles(user):
    for role in user.roles:
        if is_it_nation_role(role.__str__()):
            print('try removing: ', role)
            member = bot.get_user(user.id)

            await user.remove_roles(role)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("------")


@bot.command()
async def update(ctx):
    role_name = '@everyone'
    players = player_by_info()

    role = discord.utils.find(
        lambda r: r.name == role_name, ctx.guild.roles)

    for user in ctx.guild.members:
        player_nick1 = user.nick
        player_nick2 = user.display_name

        # trying to serach nick of player
        player = players.get(player_nick1)
        if not player:
            player = players.get(player_nick2)
        if not player:
            await remove_nation_roles(user)  # if user don't has nickname of some player,  
            # we will remove all nation roles from him
            continue
        nation = player.get('nation')

        # we have role?
        if not make_nation_role(nation) in [role.__str__() for role in ctx.guild.roles]:
            await ctx.guild.create_role(name=make_nation_role(nation))
            await ctx.send(f"Create role of nation: __***{nation}***__")

        # do user has role? 
        elif make_nation_role(nation) in [role.__str__() for role in user.roles]:
            continue  # if has - skip

        # remove old nation (if he has it)
        await remove_nation_roles(user)

        # add role to user
        nation_role = discord.utils.get(ctx.guild.roles, name=make_nation_role(nation))
        await user.add_roles(nation_role)
        await ctx.send(f"Player {player.get('nick')} is from *{nation}*!")
    await ctx.send(f"Successfull update nations for all players in this chat!")


bot.run(token)
