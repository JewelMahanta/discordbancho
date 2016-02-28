# discordbancho

This is a small bot script written in python. It basically acts as an interface between osu! Bancho server and Discord app. To use it, follow these simple instructions:

### Requirements
1. [Python 3.5+](https://www.python.org/downloads/release/python-351/)

### Steps
1. Download a zip of this repository and extract the contents to a folder.
2. Install the requirements. To do that:
  * Goto the folder where you extracted the files in step 1.
  * Open a command prompt in that folder by using **shift + right-click** and select **Open command window here**
  * Type this in the command window `pip install -r requirements.txt`
 
3. Create a new Discord account : https://discordapp.com/
4. Goto https://osu.ppy.sh/p/irc and get you `Username` and `Server Password`
5. Edit the `config.yaml` file. This file is inside the zip that you downloaded in step 3.
6. Once you have filled up the `config.yaml` file, save it and double-click on `run.bat`.

P.S. If you are having problem getting the channel_id then [go to this section](https://github.com/lapoozza/discordbancho/blob/master/README.md#how-to-get-bancho_dump-channel_id)

## Commands List
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

## How to get bancho_dump Channel_ID
* Create a new server or channel(You can name it anything. I named it lapzbot in this case). **Right click** on the channel and click **Copy Link**

![](http://i.imgur.com/XODoBcp.png)

* Open a text editor or a browser and paste this link ( Ctrl + V )
 
![](http://i.imgur.com/JMQ67Rx.png)

* Once you paste this link select the digits after the last `/` and copy it ( Ctrl + C )

![](http://i.imgur.com/TpKl8ba.png)

* Paste this value in the `config.yaml` file

**MAKE SURE that both - your account and irc bots account are on the same server where the bancho_dump channel is present.**

##Additional Information
* If you encounter any bugs, feel free to report it using the github issue tracker
* If you are encountering any issues, try reinstalling the requirements.
