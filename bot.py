import os
import io
import csv
import aiohttp
import discord
from datetime import datetime
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
            ),
            app_commands.Command(
                name='export_messages_database',
                description='export database of messeges to csv file',
                callback=self.export_database_of_messages_to_csv
            )
        ]

    async def setup_hook(self):
        for command in self.command_list:
            self.tree.add_command(command)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')

    async def export_database_of_messages_to_csv(self, interaction: discord.Interaction):
        is_admin = False
        for role in interaction.guild.roles:
            if role.permissions.administrator:
                is_admin = True
                break

        if not is_admin:
            await interaction.response.send_message("Invalid permissions")
            return 

        csvFile = io.StringIO()

        dbResponse = self.__sql.export_database('messages')
        
        for row in dbResponse:
            for collumn in row:
                csvFile.write(f'{collumn},')
            csvFile.write('\n')
        
        csvFile.seek(0)

        attachment_file = discord.File(csvFile, filename="response.csv")

        embedMessege = discord.Embed(
            title="Database response",
            description=f'responde from messeges table',
            color=discord.Color.from_rgb(46, 255, 137)
        )

        await interaction.response.send_message(embed=embedMessege, file=attachment_file, ephemeral=True)
        
        csvFile.close()


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

        embedMessege = discord.Embed(
            title="Database response",
            description=responsestr,
            color=discord.Color.from_rgb(46, 255, 137)
        )

        await interaction.response.send_message(embed=embedMessege, ephemeral=True)


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
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            attachment_file_name,
            message.content)
        
        await self.process_commands(message)

    async def on_member_join(self, member):

        if member == self.user:
            return

        await self.__sql.save_user(
            member.id,
            member.name,
            str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            1
        )

    async def on_member_remove(self, member):

        if member == self.user:
            return

        await self.__sql.update_removed_user(
            member.id
        )

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

