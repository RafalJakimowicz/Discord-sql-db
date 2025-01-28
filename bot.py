import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from databasemodule import Database
from databasemodule import logger


class LoggingBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.__sql = Database('database.db')
        self.command_list = []
        self.commands_setup()


    def commands_setup(self):
        self.command_list = [
            app_commands.Command(
                name='select_by_name',
                description='select logs from database by user',
                callback=self.get_logs_by_name
            )
        ]

    async def setup_hook(self):
        for command in self.command_list:
            self.tree.add_command(command)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')

    async def get_logs_by_name(self, interaction: discord.Interaction, user_name: str):
        is_admin = False
        for role in interaction.guild.roles:
            if role.permissions.administrator:
                is_admin = True
                break
                

        if not is_admin:
            await interaction.response.send_message("Invalid permissions")
            return

        rows = self.__sql.get_query_by_name(user_name)

        responsestr = ''
        for row in rows:
            for item in row:
                responsestr = responsestr + str(item) + "    "
            responsestr = responsestr + '\n'
        
        await interaction.response.send_message(responsestr)


    async def on_message(self, message):

        if message.author == self.user:
            return
        
        attachment_file_name = ''
        for attachment in message.attachments:
            attachment_file_name = await self.download_attachment(attachment, message.id)
        
        await self.__sql.save_message(
            message.id, 
            message.guild.name, 
            message.channel.name,
            message.author.name,
            message.created_at.date(),
            attachment_file_name,
            message.content)
        
        await self.process_commands(message)

    async def download_attachment(self, attachment, message_id) -> str:

        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                file_path = os.path.join(self.__sql.attachment_path() , f"{message_id}_{attachment.filename}")
                if response.status == 200:
                    with open(file_path, 'wb') as im_file:
                        im_file.write(await response.read())

                    logger.info(f"saved {file_path}")
                else:
                    logger.error(f'{self.download_attachment.__name__} {response.status} {file_path}')
        
        return file_path

