# Internet Radio Discord Bot

The Internet Radio Discord Bot allows you to play your internet radio stations in your Discord voice channels. Enjoy endless music streaming and share your favorite radio station with your server members!

Add Twilight Jukebox to your discord server to check out this bot and how it works.
https://discord.com/api/oauth2/authorize?client_id=1124004480560681081&permissions=3145728&scope=bot

## Features

- Play internet radio station in voice channels.
- Show the currently playing song.
- Stop playback and leave the voice channel.

## Requirements

- Python 3.6 or higher
- discord.py 2.x

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/YourUsername/InternetRadioBot.git
   cd InternetRadioBot
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Configuration:
   - Go to config.json
   - Replace `"YOUR_BOT_TOKEN"` with your bot's token.
   - Set `"YOUR_PREFIX"` to your desired command prefix.
   - set `"STREAMURL"` with your radio station url.
   - set `"BOTNAME"` with your radio station name.
   - set `"BOTDESCRIPTION"` with your radio station description for the about command.
   - set `"WEBSITE"` with your radio station website url.

## Usage

1. Start the bot:
   ```sh
   python bot.py
   ```
2. Invite the bot to your server using the OAuth2 URL with the `bot` scope and required permissions.

3. Commands:
all the commands are discord slash commands
   - `/play`: Play the radio station.
   - `/stop`: Stop playback and leave the voice channel.
   - `/nowplaying`: Display the currently playing station.
   - `/help`: Display the list of commands.


## Contributing

Contributions are welcome! Feel free to open issues or pull requests for improvements or fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Remember to replace placeholder URLs, images, and other information with your actual bot details.