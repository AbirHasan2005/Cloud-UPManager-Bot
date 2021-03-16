# (c) @AbirHasan2005

import os
import time
import json
import asyncio
# import requests
import aiohttp
from configs import Config
from datetime import datetime
from pyrogram import Client, filters, errors
from core.display_progress import progress_for_pyrogram
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply, InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

Bot = Client(Config.SESSION_NAME, bot_token=Config.BOT_TOKEN, api_id=Config.API_ID, api_hash=Config.API_HASH)

@Bot.on_message(filters.command("start"))
async def start(bot, cmd):
	await cmd.reply_text("I am Alive!")

@Bot.on_message(filters.command("help"))
async def help(bot, cmd):
	await cmd.reply_text(
		Config.HELP_TEXT,
		parse_mode="Markdown",
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[InlineKeyboardButton("Delete GoFile", switch_inline_query_current_chat="!godel "), InlineKeyboardButton("Delete Streamtape", switch_inline_query_current_chat="!stdel ")],
				[InlineKeyboardButton("Rename Streamtape File", switch_inline_query_current_chat="!strename ")],
				[InlineKeyboardButton("Add Remote URL in Streamtape", switch_inline_query_current_chat="!stremote ")],
				[InlineKeyboardButton("Get Status of Streamtape Token", switch_inline_query_current_chat="!show ")]
			]
		)
	)

@Bot.on_message(filters.private & filters.media)
async def main(bot, message):
	admin = message.from_user.id
	await message.reply_text(
		"Where you want to Upload?",
		parse_mode="Markdown",
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[InlineKeyboardButton("Upload to GoFile.io", callback_data="uptogofile"), InlineKeyboardButton("Upload to Streamtape", callback_data="uptostreamtape")]
			]
		),
		quote=True
	)

@Bot.on_inline_query()
async def answer(bot, query: InlineQuery):
	answers = []
	string = query.query.lower()
	search_query = query.query
	if string == "":
	    answers.append(
	        InlineQueryResultArticle(
	            title="Help & Usage",
	            input_message_content=InputTextMessageContent(Config.HELP_TEXT, disable_web_page_preview=True, parse_mode="Markdown"),
	            description="Documention of How to Use this Bot.",
	            thumb_url="https://i.imgur.com/6jZsMYG.png",
	            reply_markup=InlineKeyboardMarkup(
	            	[
	            		[InlineKeyboardButton("Delete GoFile", switch_inline_query_current_chat="!godel "), InlineKeyboardButton("Delete Streamtape", switch_inline_query_current_chat="!stdel ")]
	            	]
	            )
	        )
	    )
	    await bot.answer_inline_query(
	        query.id,
	        results=answers,
	        switch_pm_text="How to Use Me?",
	        switch_pm_parameter="help",
	        cache_time=0
	    )
	elif search_query.startswith("!stdel"):
		if not int(query.from_user.id) == Config.BOT_OWNER:
			answers.append(
				InlineQueryResultArticle(title="You Can't Do That!", description="This is only for Bot Owner!", input_message_content=InputTextMessageContent(message_text="This is only for Bot Owner!\n\nOnly Developer have Streamtape File Delete Rights!"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")], InlineKeyboardButton("Developer", url="https://t.me/linux_repo")]))
			)
		else:
			try:
				await asyncio.sleep(5) # Waiting for 5 Sec for getting Correct User Input!
				async with aiohttp.ClientSession() as session:
					api_link = "https://api.streamtape.com/file/delete?login={}&key={}&file={}"
					main_text = search_query.split("!stdel ")[1]
					splited = main_text.split(" ")[0]
					token = splited.split("/")[4]
					delete = await session.get(api_link.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS, token))
					data = await delete.json()
					status = data['msg']
					if status == "OK":
						answers.append(
							InlineQueryResultArticle(
								title="Deleted File!",
								description=f"Deleted [{token}]",
								input_message_content=InputTextMessageContent(
									message_text=f"**Deleted:** {splited}\n\n**File Token:** `{token}`",
									parse_mode="Markdown",
									disable_web_page_preview=True
								)
							)
						)
					else:
						answers.append(
							InlineQueryResultArticle(title="File Not Deleted!", description=f"Can't Delete [{token}]", input_message_content=InputTextMessageContent(message_text=f"Can't Delete - {splited}\nUsing [{token}]", disable_web_page_preview=True, parse_mode="Markdown"))
						)
			except Exception as err:
				answers.append(
					InlineQueryResultArticle(title="Something Went Wrong!", description=f"Error: {err}", input_message_content=InputTextMessageContent(message_text=f"Something Went Wrong!\n\n**Error:** `{err}`"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]))
				)

		try:
			await query.answer(
				results=answers,
				cache_time=0
			)
		except errors.QueryIdInvalid:
			await query.answer(
				results=answers,
				cache_time=0,
				switch_pm_text="Error: Search timed out!",
				switch_pm_parameter="help"
			)
	elif search_query.startswith("!godel"):
		try:
			await asyncio.sleep(5) # Waiting for 5 Sec for getting Correct User Input!
			async with aiohttp.ClientSession() as session:
				api_link = "https://apiv2.gofile.io/deleteUpload?c={}&ac={}"
				# https://gofile.io/d/{token}
				main_text = search_query.split("!godel ")[1]
				splited = main_text.split(" ")[0]
				token = splited.split("/")[4]
				adminCode = main_text.split(" ", 1)[1]
				response = await session.get(api_link.format(token, adminCode))
				data_f = await response.json()
				status = data_f['status']
				if status == "ok":
					answers.append(
						InlineQueryResultArticle(
							title="Deleted File!",
							description=f"Deleted [{token}], Using [{adminCode}]",
							input_message_content=InputTextMessageContent(
								message_text=f"**Deleted:** {splited}\n\n**Using AdminCode:** `{adminCode}`\n**File Token:** `{token}`",
								parse_mode="Markdown",
								disable_web_page_preview=True
							)
						)
					)
				else:
					answers.append(
						InlineQueryResultArticle(title="File Not Deleted!", description=f"Can't Delete [{token}], Using [{adminCode}]", input_message_content=InputTextMessageContent(message_text=f"Can't Delete - {splited}\nUsing [{adminCode}]", disable_web_page_preview=True, parse_mode="Markdown"))
					)

		except Exception as err:
			answers.append(
				InlineQueryResultArticle(title="Something Went Wrong!", description=f"Error: {err}", input_message_content=InputTextMessageContent(message_text=f"Something Went Wrong!\n\n**Error:** `{err}`"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]))
			)

		try:
			await query.answer(
				results=answers,
				cache_time=0
			)
		except errors.QueryIdInvalid:
			await query.answer(
				results=answers,
				cache_time=0,
				switch_pm_text="Error: Search timed out!",
				switch_pm_parameter="help"
			)
	elif search_query.startswith("!strename"):
		if not int(query.from_user.id) == Config.BOT_OWNER:
			answers.append(
				InlineQueryResultArticle(title="You Can't Do That!", description="This is only for Bot Owner!", input_message_content=InputTextMessageContent(message_text="This is only for Bot Owner!\n\nOnly Developer have Streamtape File Delete Rights!"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")], InlineKeyboardButton("Developer", url="https://t.me/linux_repo")]))
			)
		else:
			input_f = search_query.split("!strename ")[1]
			token = input_f[0:15]
			new_filename = input_f[15:]

			try:
				await asyncio.sleep(5) # Waiting for 5 Sec for getting Correct User Input!
				async with aiohttp.ClientSession() as session:
					api_link = "https://api.streamtape.com/file/rename?login={}&key={}&file={}&name={}"
					hit_api = await session.get(api_link.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS, token, new_filename))
					data_f = await hit_api.json()
					status = data_f['msg']
					if status == "OK":
						answers.append(
							InlineQueryResultArticle(
								text="File Renamed!",
								description=f"Renamed to {new_filename} using {token}",
								input_message_content=InputTextMessageContent(message_text=f"Successfully Renamed file to - `{new_filename}`\n\nUsing `{token}`", parse_mode="Markdown", disable_web_page_preview=True)
							)
						)
					else:
						answers.append(
							InlineQueryResultArticle(text="Can't Rename File!", description=f"Token: {token} is Invalid!", input_message_content=InputTextMessageContent(message_text=f"Can't Rename File to - `{new_filename}`\n\nUsing `{token}`", parse_mode="Markdown", disable_web_page_preview=True))
						)
			except Exception as e:
				answers.append(
					InlineQueryResultArticle(text="Something Went Wrong!", description=f"Error: {e}", input_message_content=InputTextMessageContent(message_text=f"Something Went Wrong!\n\n**Error:** `{e}`", parse_mode="Markdown", disable_web_page_preview=True))
				)

		try:
			await query.answer(
				results=answers,
				cache_time=0
			)
		except errors.QueryIdInvalid:
			await query.answer(
				results=answers,
				cache_time=0,
				switch_pm_text="Error: Search timed out!",
				switch_pm_parameter="help"
			)
	elif search_query.startswith("!stremote"):
		remote_link = search_query.split("!stremote ")[1]
		try:
			async with aiohttp.ClientSession() as session:
				api_link = "https://api.streamtape.com/remotedl/add?login={}&key={}&url={}"
				hit_api = await session.get(api_link.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS, remote_link))
				data_f = await hit_api.json()
				status = data_f['msg']
				if status == "OK":
					token = data_f['result']['id']
					answers.append(
						InlineQueryResultArticle(
							text="URL Added!",
							description="Remote URL Added to List!",
							input_message_content=InputTextMessageContent(message_text=f"Successfully Added Remote URL( {remote_link} ) to Remote List!\n\n**Remote Token:** `{token}`", parse_mode="Markdown", disable_web_page_preview=True),
							reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Show Status", switch_inline_query_current_chat=f"!show {token}")]])
						)
					)
				else:
					answers.append(
						InlineQueryResultArticle(text="Can't Add Remote URL!", description=f"Some Issues with Remote URL!", input_message_content=InputTextMessageContent(message_text=f"Can't Upload Remote URL!\n\nRemote Link: {remote_link}\nHaving Some Issues.", parse_mode="Markdown", disable_web_page_preview=True))
					)
		except Exception as e:
			answers.append(
				InlineQueryResultArticle(text="Something Went Wrong!", description=f"Error: {e}", input_message_content=InputTextMessageContent(message_text=f"Something Went Wrong!\n\n**Error:** `{e}`", parse_mode="Markdown", disable_web_page_preview=True))
			)

		try:
			await query.answer(
				results=answers,
				cache_time=0
			)
		except errors.QueryIdInvalid:
			await query.answer(
				results=answers,
				cache_time=0,
				switch_pm_text="Error: Search timed out!",
				switch_pm_parameter="help"
			)
	elif search_query.startswith("!show"):
		input_f = search_query.split("!show ")[1]
		try:
			async with aiohttp.ClientSession() as session:
				api_link = "https://api.streamtape.com/remotedl/status?login={}&key={}&id={}"
				hit_api = await session.get(api_link.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS, input_f))
				data_f = await hit_api.json()
				status = data_f['msg']
				if status == "OK":
					remote_URL = data_f["result"][f"{input_f}"]["remoteurl"]
					downloaded = data_f["result"][f"{input_f}"]["bytes_loaded"]
					total_size = data_f["result"][f"{input_f}"]["bytes_total"]
					added_at = data_f["result"][f"{input_f}"]["added"]
					last_update = data_f["result"][f"{input_f}"]["last_update"]
					url = data_f["result"][f"{input_f}"]["url"]
					answers.append(
						InlineQueryResultArticle(
							text=f"TOKEN: {input_f}",
							description=f"Uploaded: {downloaded} Bytes, Total: {total_size} Bytes",
							input_message_content=InputTextMessageContent(message_text=f"**Token:** `{input_f}`\n**Uploaded:** `{downloaded}`\n**Total:** `{total_size}`\n**Added Remote at:** `{added_at}`\n**Last Updated at:** `{last_update}`\n\n**URL:** {url}", parse_mode="Markdown", disable_web_page_preview=True),
							reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Show Status", switch_inline_query_current_chat=f"!show {token}")]])
						)
					)
				else:
					answers.append(
						InlineQueryResultArticle(text="Nothing Found!", description="Nothing ...", input_message_content=InputTextMessageContent(message_text="Nothing Found ...", parse_mode="Markdown", disable_web_page_preview=True))
					)
		except Exception as e:
			answers.append(
				InlineQueryResultArticle(text="Something Went Wrong!", description=f"Error: {e}", input_message_content=InputTextMessageContent(message_text=f"Something Went Wrong!\n\n**Error:** `{e}`", parse_mode="Markdown", disable_web_page_preview=True))
			)

		try:
			await query.answer(
				results=answers,
				cache_time=0
			)
		except errors.QueryIdInvalid:
			await query.answer(
				results=answers,
				cache_time=0,
				switch_pm_text="Error: Search timed out!",
				switch_pm_parameter="help"
			)

@Bot.on_callback_query()
async def button(bot, data: CallbackQuery):
	cb_data = data.data
	if "uptogofile" in cb_data:
		downloadit = data.message.reply_to_message
		# if not (int(downloadit.video.file_size) or int(downloadit.document.file_size)) <= 25500:
		# 	await data.message.edit("Sorry, I can only upload 500MB on GoFile.io !!")
		# 	return
		a = await data.message.edit("Downloading to my Server ...", parse_mode="Markdown", disable_web_page_preview=True)
		dl_loc = str(data.from_user.id) + "/"
		if not os.path.isdir(dl_loc):
		    os.makedirs(dl_loc)
		c_time = time.time()
		the_media = await bot.download_media(
			message=downloadit,
			file_name=dl_loc,
			progress=progress_for_pyrogram,
			progress_args=(
				"Download kortasi ...",
				a,
				c_time
			)
		)
		await a.delete(True)
		try:
			async with aiohttp.ClientSession() as session:
				server_api = "https://apiv2.gofile.io/getServer"
				datas = await session.get(server_api)
				main_data = await datas.json()
				server = main_data['data']['server']
				a = await data.message.reply_to_message.reply_text(f"**Selected Server:** `{server}`")
				await a.edit("Uploading ...")
				files = {'file': open(the_media, 'rb')}
				URL = "https://" + server + ".gofile.io/uploadFile"
				response = await session.post(URL, data=files)
				data_f = await response.json()
				token = data_f['data']['code']
				code = data_f['data']['adminCode']
				status = data_f['status']
				filename = the_media.split("/")[-1].replace("_"," ")
				await a.edit(f"**File Name:** `{filename}`\n\n**AdminCode:** `{code}`\n\n**Download Link:** `https://gofile.io/d/{token}`", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Link", url=f"https://gofile.io/d/{token}")]]))
				try:
					os.remove(the_media)
				except:
					pass
		except Exception as err:
			await a.edit(f"Something went wrong!\n\n**Error:** `{err}`")
	elif "uptostreamtape" in cb_data:
		downloadit = data.message.reply_to_message
		# if not (int(downloadit.video.file_size) or int(downloadit.document.file_size)) <= 25500:
		# 	await data.message.edit("Sorry, I can only upload 500MB on GoFile.io !!")
		# 	return
		a = await data.message.edit("Downloading to my Server ...", parse_mode="Markdown", disable_web_page_preview=True)
		dl_loc = str(data.from_user.id) + "/"
		if not os.path.isdir(dl_loc):
		    os.makedirs(dl_loc)
		c_time = time.time()
		the_media = await bot.download_media(
			message=downloadit,
			file_name=dl_loc,
			progress=progress_for_pyrogram,
			progress_args=(
				"Download kortasi ...",
				a,
				c_time
			)
		)
		await a.delete(True)
		async with aiohttp.ClientSession() as session:
			Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"
			hit_api = await session.get(Main_API.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS))
			json_data = await hit_api.json()
			temp_api = json_data["result"]["url"]
			files = {'file1': open(the_media, 'rb')}
			response = await session.post(temp_api, data=files)
			data_f = await response.json(content_type=None)
			status = data_f["status"]
			download_link = data_f["result"]["url"]
			filename = the_media.split("/")[-1].replace("_"," ")
			try:
				os.remove(the_media)
			except:
				pass

			if not int(status) == 200:
				await data.message.reply_to_message.reply_text("Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request!", parse_mode="Markdown", disable_web_page_preview=True)
				return
			else:
				a = await data.message.reply_to_message.reply_text(
					f"**File Name:** `{filename}`\n\n**Download Link:** `{download_link}`",
					parse_mode="Markdown",
					disable_web_page_preview=True,
					reply_markup=InlineKeyboardMarkup(
						[
							[InlineKeyboardButton("Open Link", url=download_link)], [InlineKeyboardButton("Delete File", callback_data="deletestream")]
						]
					)
				)
	elif "deletestream" in cb_data:
		data_revive = data.message.text
		token = data_revive.split("/")[4]
		async with aiohttp.ClientSession() as session:
			del_api = "https://api.streamtape.com/file/delete?login={}&key={}&file={}"
			data_f = await session.get(del_api.format(Config.STREAMTAPE_API_USERNAME, Config.STREAMTAPE_API_PASS, token))
			json_data = await data_f.json()
			status = data_f['msg']
			if status == "OK":
				await data.message.edit(f"File Deleted using `{token}` !!")
			else:
				await data.message.edit("File not Found!")

Bot.run()