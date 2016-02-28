# discordbancho

This is a small script written in python. It basically acts as an interface between osu! Bancho server and Discord app. To use it, follow these simple instructions:

1. Create a new Discord account : https://discordapp.com/

2. Goto https://osu.ppy.sh/p/irc and get you `Username` and `Server Password`

3. Download a zip of this repository

4. Edit the `config.yaml` file. This file is inside the zip that you downloaded in step 3.

        # CONFIGURATION file for irc script.
        # DO NOT change the variables in this file. Only change the values.

        DISCORD:
          # Enter the discord login credentials: email and password.
          # Make sure to use single quotes
          # The admin_id is your discord user_id. This is used as a safeguard so that only you are able to send messages.
        
          email: 'discord_email'
          password: 'discord_password'
          admin_id: 'discord_user_id'
        OSU:
          # You can get these details from this link: https://osu.ppy.sh/p/irc
          # Make sure to enter the details as is or validation will fail
          # Make sure to use single quotes
        
          Username: 'Your Username'
          Server Password: 'Your Server Password'
        CHANNEL:
          # Enter the channel_id of a channel/server that you want to use
          # Remember all the message to/from bancho will be dumped here
          # It is adviced that you generally make a new server or a private channel for this purpose
        
          bancho_dump: 'Channel_ID'

5. Once you have filled up the `config.yaml` file, save it and double-click on `run.bat`.
6. Enjoy

###Commands List
|Command|Information|
|-------|-----------|
|`!bancho`|Logs you into the osu!bancho server.|
|`!join #channel`|Joins a specified channel.|
|`!leave #channel`|Leaves a specified channel.|
|`!setch channel/user`|Sets the channel or user for your texts.|
|`!ch`|The channel or user your texts are currently going to.|
|`!list`|The available list of channels.|

**P.S.** to send messages, the message must be tagged with a initial `?` mark to be sent.
For example:

        ?hello ->will be sent
        but,
        hello ->will NOT be sent
