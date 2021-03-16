# (c) @AbirHasan2005

import os

class Config(object):
	API_ID = int(os.environ.get("API_ID", 1578262))
	API_HASH = os.environ.get("API_HASH", "664ecb8d62405ae3e3e015216f6e2615")
	BOT_TOKEN = os.environ.get("BOT_TOKEN", "1710870592:AAEusuXOt7Lg88VBRC_5ymENtGyQzG3wfhY")
	GOFILE_API = os.environ.get("GOFILE_API")
	STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS", "e4P6D8bm97HkJo")
	STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME", "d49e7f9cf0d9dbb89468")
	SESSION_NAME = os.environ.get("SESSION_NAME", "CloudManagerBot")
	BOT_OWNER = int(os.environ.get("BOT_OWNER", 1445283714))
	HELP_TEXT = """
Send me any Media & Choose Upload Server,
I will Upload the Media to that server.

Currently I can Upload to:
> GoFile.io
> streamtape.com

Also I can do a lot of things from Inline!
__Check Below Buttons >>>__
"""
	PROGRESS = """
Percentage : {0}%
Done ✅: {1}
Total 🌀: {2}
Speed 🚀: {3}/s
ETA 🕰: {4}
"""