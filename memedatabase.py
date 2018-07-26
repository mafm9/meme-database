import mysql.connector
import discord
from discord.ext.commands import Bot

TOKEN = "NDcwMzc2MjkyODI3NTI5MjM4.DjVYBw.-scRlcC6fBB9VkoNtrTNGnLkM4E"
BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)
cnx = mysql.connector.connect(user='bot', database='memes')


@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_message(message):
    channel = message.channel
    embed = discord.Embed()
    if message.content.startswith('!add'):

        cursor = cnx.cursor()
        do_it_right = "Do it right you bastard\nex: !add name link description"
        mess = message.content.lower()
        messa = mess.split()
        position = messa.index("!add")
        name = messa[position + 1]
        link = messa[position + 2]
        description = ""
        for x in messa[position+3:]:
            description = description + " " + x + " "
        add_meme = ("INSERT INTO memes "
                    "(name, link, Description) "
                    "VALUES (%s,%s,%s)")
        if "gif" not in name and "jpg" not in name and "png" not in name:
            if "gif" in link or "jpg" in link or "png" in link:
                if "gif" not in description and "jpg" not in description and "png" not in description:
                    cursor.execute(add_meme, (name, link, description))
                    await channel.send("meme added")
                else:
                    await channel.send(do_it_right)
            else:
                await channel.send(do_it_right)
        else:
            await channel.send(do_it_right)
        cnx.commit()
        cursor.close()

    if message.content.startswith('!calln'):
        cursor = cnx.cursor(buffered=True)
        mess = message.content
        messa = mess.split()
        position = messa.index("!calln")
        name = messa[position+1]
        select_meme = ("SELECT link "
                       "FROM memes "
                       "WHERE name = %s")
        cursor.execute(select_meme, (name,))
        cnx.commit()
        for (link) in cursor:
            imageurl = link[0]
            embed.set_image(url=imageurl)
        await channel.send(embed=embed)
        cursor.close()
    if message.content.startswith('!memes'):
        cursor = cnx.cursor()
        query = "SELECT name, Description FROM memes"
        cursor.execute(query)
        data = cursor.fetchall()
        memes = ""
        for row in data:
            memes = memes + "Meme name: "+ row[0] + "\nDescription: " + row[1] + '\n'
        await channel.send(memes)
        cursor.close()
    if message.content.startswith("!delete"):
        cursor = cnx.cursor()
        mess = message.content
        


cnx.close
client.run(TOKEN)


