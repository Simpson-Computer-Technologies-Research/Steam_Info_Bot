import discord, requests
from datetime import datetime
from discord.ext import commands

# // Default Data Map
DEFAULT_DATA = {"response":{"players":[{"steamid":"Unavailable","communityvisibilitystate":0,"realname": "Unavailable","profilestate":0,"personaname":"Unavailable","profileurl":"Unavailable","avatarmedium":"https://cdn.discordapp.com/attachments/855448636880191499/878268636467429487/6.png","avatarhash":"Unavailable","personastate":0,"primaryclanid":"Unavailable","timecreated":0,"loccountrycode": "Unavailable","locstatecode": "Unavailable","loccityid": "Unavailable","personastateflags":0, "lastlogoff": 0}]}}

# // Your steam api key
STEAM_KEY = "YOUR STEAM WEB API KEY"


# // Core Cog
class Core(commands.Cog):
    def __init__(self, client):
        self.client = client


    # // !steam {user id} command
    @commands.command(aliases=['s'])
    async def steam(self, ctx, id: str):
        with requests.Session() as session:
            # // Send the http request to the steam api
            r: requests.Response = session.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids={id}&format=json")
            
            # // Create user constant
            USER: dict[str, any] = DEFAULT_DATA['response']['players'][0]

            # // Get the response body data
            for v in r.json()["response"]["players"][0].items():
                USER[list(v)[0]] = list(v)[1]

            # // Send the embed to the chat
            await ctx.send(embed = self.create_response_embed(USER, discord.Embed(
                title = f"Profile: {USER['personaname']} ({USER['steamid']})", 
                description = f"Avatar Hash: **{USER['avatarhash']}**\nProfile URL: **{USER['profileurl']}**", 
                color = 65535
            )))


    # // Function to convert time to string date
    def time_to_string(self, time: str):
        return datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
    

    # // Function to create the response embed
    def create_response_embed(self, USER: dict[str, any], embed: discord.Embed):
        # // The Account's Real Name
        embed.add_field(
            name=" ‎\nReal Name", 
            value=f"🔹 **{USER['realname']}**"
        )

        # // Add the date the account was created to the embed
        embed.add_field(
            name=" ‎\nAccount Created", 
            value=f"🔹 **{self.time_to_string(USER['timecreated'])}**"
        )

        # // Empty field
        embed.add_field(name='\u200b', value='\u200b')
        
        # // Add the visibility state to the embed
        embed.add_field(
            name = "‏‏‎ ‎\nVisibility State", 
            value = f"🔹 **{USER['communityvisibilitystate']}**"
        )
        
        # // Add the profile state to the embed
        embed.add_field(
            name = " ‎\nProfile State", 
            value = f"🔹 **{USER['profilestate']}**"
        )
        
        # // Empty field
        embed.add_field(name='\u200b', value='\u200b')

        # // Add the last online date to the embed
        embed.add_field(
            name = " ‎\nLast Online", 
            value = f"🔹 **{self.time_to_string(USER['lastlogoff'])}**"
        )
        
        # // Add the primary clan id to the embed
        embed.add_field(
            name = " ‎\nPrimary Clan ID", 
            value = f"🔹 **{USER['primaryclanid']}**"
        )

        # // Empty field
        embed.add_field(name='\u200b', value='\u200b')

        # // Add the country code to the embed
        embed.add_field(
            name = " ‎\nCountry Code", 
            value = f"🔹 **{USER['loccountrycode']}**"
        )
        
        # // Add the state code to the embed
        embed.add_field(
            name = " ‎\nState Code", 
            value = f"🔹 **{USER['locstatecode']}**"
        )

        # // Empty field
        embed.add_field(name='\u200b', value='\u200b')
        
        # // Add the city code to the embed
        embed.add_field(
            name = " ‎\nCity Code", 
            value = f"🔹 **{USER['loccityid']}**"
        )

        # // Set the embed thumbnail
        embed.set_thumbnail(url = f"{USER['avatarmedium']}")

        # // Return the new embed
        return embed


# // Setup the client
def setup(client):
    client.add_cog(Core(client))
