import asyncio

import discord
import argparse

from llm_preparation import create_retriever, create_chain


# formats the message to make the response a little cooler looking
# title: Title of the embedded message
# color: color of the top bar of the message given in hex
# channel: The text channel in which the message should be posted
# content: The actual contents of the message
async def print_embedded_message(title, color, channel, content):
    embed = discord.Embed(title=title, color=color, description=content)
    message = await channel.send(embed=embed)
    return message


class Bot(discord.Client):

    chain = None

    async def async_chain_invoke_wrapper(self, question):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.chain.invoke, question)
        return result

    async def on_ready(self):
        print('Bot is successfully running')
        print('Retriever is successfully created')
        self.chain = create_chain()
        # self.chain = ChainStub()
        print('Chain is successfully created')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!question '):
            await print_embedded_message("Please wait while I look up an answer", 0x00ff00, message.channel, "")
            question = message.content[10:]
            # made the blocking call async so the bot doesn't crash if the response takes to long
            answer = await self.async_chain_invoke_wrapper(question)
            await print_embedded_message("Answer", 0x00ff00, message.channel, answer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Your token value")
    args = parser.parse_args()
    token = args.token
    print("Token:", token)
    # set up the bots intents, so it can have the right permissions to read messages
    intents = discord.Intents.default()
    intents.message_content = True
    # start bot
    client = Bot(intents=intents)
    client.run(token)
