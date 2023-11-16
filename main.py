import discord
import argparse

# formats the message to make the response a little cooler looking
# title: Title of the embedded message
# color: color of the top bar of the message given in hex
# channel: The text channel in which the message should be posted
# content: The actual contents of the message
async def print_embedded_message(title, color, channel, content):
    embed = discord.Embed(title=title, color=color, description=content)
    await channel.send(embed=embed)


class Bot(discord.Client):

    async def on_ready(self):
        print('Bot is successfully running')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        await print_embedded_message("Echo", 0x00ff00, message.channel, message.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Your token value")
    parser.add_argument("--chat", help="Your ChatGPT API TOKEN")
    args = parser.parse_args()
    token = args.token
    chat_token = args.chat
    print("Token:", token)
    print("Chat-Token:", chat_token)


    # set up the bots intents, so it can have the right permissions to read messages
    intents = discord.Intents.default()
    intents.message_content = True
    # start bot
    client = Bot(intents=intents)
    client.run(token)
