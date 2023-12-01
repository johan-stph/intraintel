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
        self.chain = create_chain()
        # self.chain = ChainStub()
        print('Chain is successfully created')
        print('Bot is successfully running')

    async def request_question(self, message):
        waiting_text = "Please wait while I look up an answer."
        answer_message = await print_embedded_message(waiting_text, 0x00ff00, message.channel, "")
        question = message.content[10:]
        # made the blocking call async so the bot doesn't crash if the response takes to long
        task = asyncio.create_task(self.async_chain_invoke_wrapper(question))
        counter = 0
        while not task.done():
            counter = (counter + 1) % 3
            await asyncio.sleep(0.1)
            embed = discord.Embed(title=waiting_text + ("." * counter), color=0x00ff00, description="")
            await answer_message.edit(embed=embed)
        answer = task.result()
        embed = discord.Embed(title="Answer", color=0x00ff00, description=answer)
        await answer_message.edit(embed=embed)

    async def request_help(self, message):
        embed = discord.Embed(title="Hi, I'm IntraIntel!", color=0x00ff00, description="Ask me a question about "
                                                                                       "Enactus by writing "
                                                                                       "'!question' followed by "
                                                                                       "your question.")
        embed.add_field(name="Example:", value="!question Am I allowed to throw a party in the office?", inline=True)
        await message.channel.send(embed=embed)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!question '):
            await self.request_question(message)
        elif message.content.startswith('!help'):
            await self.request_help(message)


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
