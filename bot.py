import os
import sys
from user import User
from pyrogram import Client
from presets import Presets as Msg

if bool(os.environ.get("ENV", False)):
    from sample_config import Config
    from sample_config import LOGGER
else:
    from config import Config
    from config import LOGGER

bot_user_name = []


class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            "mediaBuddy",
            api_hash=Config.API_HASH,
            api_id=Config.APP_ID,
            bot_token=Config.TG_BOT_TOKEN,
            sleep_threshold=60,
            plugins={
                "root": "plugins"
            }
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username}  started! "
        )
        self.USER, self.USER_ID = await User().start()
        #
        bot_spec = await self.get_me()
        bot_user_name.append('@' + str(bot_spec.username))
        #
        try:
            await self.USER.send_message(usr_bot_me.username, "/index")
        except Exception:
            print(Msg.BOT_BLOCKED_MSG)
            sys.exit()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
