# coding=utf-8
"""
    The MIT License (MIT)

    Copyright (c) 2016 lapoozza

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import discord
import socket
import asyncio
import re
import threading
from time import strftime
import yaml


try:
    with open('config.yaml') as f:
        stream1 = yaml.load(f)
except FileExistsError:
    print('config.yaml not found.')
    quit()


class Bot(discord.Client):
    """
    The irc client file. This program is a standalone irc client that bridges osu! bancho server and discord app.

    Some helpful IRC codes for bancho
        cho.ppy.sh 001: Bancho welcome message
        cho.ppy.sh 322: For available channels
        cho.ppy.sh 353: For list of users
        cho.ppy.sh 375: Blank line
        cho.ppy.sh 372: Bancho Related information
    """
    # Loading configurations from config.yaml---------->
    admin_ids = stream1['DISCORD']['admin_id']
    bancho_dump = int(stream1['CHANNEL']['bancho_dump'])

    bancho_usr = stream1['OSU']['Username']
    bancho_pass = stream1['OSU']['Server Password']

    msg_chan = '#osu'
    available_chan = []

    def __init__(self):
        super().__init__()

    async def on_message(self, message):
        """

        :param message:
        """
        if message.author == self.user:
            return

        if message.content.startswith('!id'):
            await self.send_message(message.channel, '{} your id is: {}'
                                    .format(message.author.mention, message.author.id))

        if message.content.startswith('!help'):
            await self.send_message(message.channel, 'The available commands are:\n'
                                                     '`!bancho` Logs you into the osu!bancho server.\n'
                                                     '`!join #channel` Joins a specified channel.\n'
                                                     '`!leave #channel` Leaves a specified channel.\n'
                                                     '`!setch channel/user` Sets the channel or user for your texts.\n'
                                                     '`!ch` The channel or user your texts are currently going to.\n'
                                                     '`!list` The available list of channels.\n'
                                                     '`!id` Shows your discord id.')

        if message.content.startswith("?"):
            """
                This part deals with sending message. The message must be tagged with a
                initial `?` mark to be sent.

                For example:
                    `?hello` ->will be sent

                    but,

                    `hello` ->will NOT be sent
            """
            if message.author.id == self.admin_ids:
                cont = message.content[1:]

                await self.send_message(message.channel, '→`{} {} / {}`: {}'
                                        .format(strftime('%H:%M'), message.author, self.msg_chan, cont))
                irc.send(bytearray('PRIVMSG {} :{}\r\n'.format(self.msg_chan, cont), encoding='utf-8'))

        # BANCHO INTERFACING-------------------->
        if message.content.startswith('!bancho'):
            """
                Connects to the osu! Bancho server. Make sure that your osu credentials
                are correct.
            """
            global t
            t = threading.Thread(target=bancho, args=[self])
            t.start()

        if message.content.startswith('!join'):
            """
                Joins a specified channel.

                Usage: !join #channel
            """
            cont = message.content[6:]
            irc.send(bytearray('JOIN {}\r\n'.format(cont), encoding='utf-8'))
            await self.send_message(message.channel, 'Joined: `{}`'.format(cont))

        if message.content.startswith('!leave'):
            """
                Leaves a specified channel.

                Usage: !leave #channel
            """
            cont = message.content[7:]
            irc.send(bytearray('PART {}\r\n'.format(cont), encoding='utf-8'))
            await self.send_message(message.channel, 'Left: `{}`'.format(cont))

        if message.content.startswith('!leave'):
            """
                Leaves a specified channel.

                Usage: !leave #channel
            """
            cont = message.content[7:]
            irc.send(bytearray('PART {}\r\n'.format(cont), encoding='utf-8'))
            await self.send_message(message.channel, 'Left: `{}`'.format(cont))

        if message.content.startswith('!setch'):
            """
                Sets the channel/user to where your text messages will go.

                Usage: !setch #channel
            """
            cont = message.content[7:]
            self.msg_chan = cont
            await self.send_message(message.channel, 'Channel changed to: `{}`'.format(self.msg_chan))

        if message.content.startswith('!ch'):
            """
                Shows the channel to where your text messages are configured to be sent. Please note
                that by default it is set to #osu.

                Usage: !ch
            """
            await self.send_message(message.channel, 'Current channel: `{}`'.format(self.msg_chan))

        if message.content.startswith('!list'):
            """
                Lists all available channels.

                Usage: !list
            """
            b = ''
            for a in self.available_chan:
                b += str(a) + ', '

            await self.send_message(message.channel, '```Available channels are: {}```'.format(b))

    async def on_ready(self):
        """
        This function is called once lapzirc logs in to discord and its Server list
        is populated.

        :return: This function returns a status message when it is ready.
        :rtype: discord.Client.change_status()
        """
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('SERVERS')
        for server in self.servers:
            print(server)
        # Game Status updating
        now_playing = discord.Game(name='type !bancho to start')
        await self.change_status(game=now_playing, idle=False)


def bancho(self):
    """
    The main thread for handling bancho

    :param self:
    :return:
    """
    network = 'irc.ppy.sh'
    port = 6667

    global irc
    # noinspection PyArgumentEqualDefault
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((network, port))
    irc.send(bytearray('PASS {}\r\n'.format(self.bancho_pass), encoding='utf-8'))
    irc.send(bytearray('NICK {}\r\n'.format(self.bancho_usr), encoding='utf-8'))
    irc.send(bytearray('USER {} {} {}\r\n'.format(self.bancho_usr, self.bancho_usr, self.bancho_usr), encoding='utf-8'))
    print('CONNECTED to BANCHO')

    # Joins the default channel--->
    irc.send(b'JOIN #osu\r\n')

    # Populate the channel list-------------------->
    irc.send(bytearray('LIST\r\n', encoding='utf-8'))

    chan = discord.Object(id=self.bancho_dump)
    while True:
        data = irc.recv(4096)
        dats = data.decode('utf-8')
        # print(dats)

        if data.find(b'PING') != -1:
            irc.send(b'PONG \r\n')

        if 'PRIVMSG' in dats:
            """
                This part handles the messages you receive from user and/or in various channels
            """
            a = dats.split('\n')
            for b in a:
                if 'PRIVMSG' in b:
                    c = b.split(':', maxsplit=2)
                    msg_content = c[2]

                    info = c[1].split()
                    msg_chan = info[2]
                    msg_author = info[0].split('!')[0]

                    """
                        If the bancho username is present in either the message content or in
                        the message channel, then the user is highlighted in discord.

                        This is to make sure that you get to view the messages directed at you
                    """
                    if self.bancho_usr in msg_content:
                        if 'ACTION' in msg_content:
                            msg_content_strip = re.sub('ACTION', '', msg_content, 1)
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '<@{}>\n→`{}` {}{}'
                                                  .format(self.admin_ids, strftime('%H:%M'),
                                                          msg_author, msg_content_strip)),
                                loop=self.loop)
                        else:
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '<@{}>\n→`{} {} / {}`: {}'
                                                  .format(self.admin_ids, strftime('%H:%M'),
                                                          msg_author, msg_chan, msg_content)),
                                loop=self.loop)

                    elif msg_chan == self.bancho_usr:
                        if 'ACTION' in msg_content:
                            msg_content_strip = re.sub('ACTION', '', msg_content, 1)
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '<@{}>\n→`{}` {}{}'
                                                  .format(self.admin_ids, strftime('%H:%M'),
                                                          msg_author, msg_content_strip)),
                                loop=self.loop)
                        else:
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '<@{}>\n→`{} {} / {}`: {}'
                                                  .format(self.admin_ids, strftime('%H:%M'),
                                                          msg_author, msg_chan, msg_content)),
                                loop=self.loop)

                    else:
                        if 'ACTION' in msg_content:
                            msg_content_strip = re.sub('ACTION', '', msg_content, 1)
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '→`{}` {}{}'
                                                  .format(strftime('%H:%M'), msg_author, msg_content_strip)),
                                loop=self.loop)
                        else:
                            asyncio.run_coroutine_threadsafe(
                                self.send_message(chan, '→`{} {} / {}`: {}'
                                                  .format(strftime('%H:%M'), msg_author, msg_chan, msg_content)),
                                loop=self.loop)

        if 'cho.ppy.sh 322' in dats:
            """
                This part is for getting info about the currently available channels.
            """
            a = dats.split('\n')
            for b in a:
                if 'cho.ppy.sh 322' in b:
                    c = b.split(':')
                    chan_name_tup = c[1].split()
                    chan_name = chan_name_tup[3]
                    self.available_chan.append(chan_name)

bot = Bot()

try:
    with open('config.yaml') as f:
        stream2 = yaml.load(f)

    bot.run(stream2['DISCORD']['email'], stream2['DISCORD']['password'])
except FileExistsError:
    print('config.yaml not found.')
    quit()
except discord.LoginFailure:
    print('Discord credentials are wrong. Correct them and rerun this script.')
    quit()


