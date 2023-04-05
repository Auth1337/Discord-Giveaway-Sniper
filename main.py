import os
def uninstall_and_install():
  os.system("pip uninstall discord -y && pip uninstall discord.py -y && pip uninstall discord.py-self -y && pip install -r requirements.txt")
uninstall_and_install()
import discord
from discord.ext import commands
import sys
import requests
import json

os.system("clear||cls")

BASE_URL = "https://canary.discord.com/api/v10"

discord.http.Route.BASE = BASE_URL


with open("config.json", "r") as f:
  cf = json.load(f)

token = cf.get("Token")
hook = cf.get("Webhook")


def log(content, doeveryone=False, save=False):
  print(f"[!] LOG: {content}")
  with open("logs.txt", "a+") as f:
    if save:
      f.write(content+"\n")
  if doeveryone:
    content = f"@everyone {content}"
  with requests.Session() as session:
    with session.post(hook, json=dict(content=content)) as response:
      print(f"[!] Sent Log To Webhook, Response Status -> [{response.status_code}]")

client = commands.Bot(command_prefix=";", help_command=None, self_bot=True)


@client.event
async def on_ready():
  log(f"Giveaway Sniper | Connected To {client.user} | {client.user.id}")

@client.event
async def on_raw_reaction_add(payload):
  if not payload.member.bot:
    return
  message = await client.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)
  if not message.embeds:
    print(message.author)
    return
  try:
    if "winners" or "winners:" in message.embeds[0].description.lower():
      hasdesc = True
  except:
    hasdesc = False
  if 'giveaway' in message.content.lower() or ":gift:" in message.content.lower() or hasdesc or ":tada:" in message.content.lower():
    try:
      await message.add_reaction(payload.emoji)
    except Exception as e:
      #print(e)
      pass
    else:
      if "giveaway" in message.content.lower():
        log(f"Sniped A Giveaway!\n[Click Here]({message.jump_url})", save=True)
      else:
        log(f"Probably Not A Giveaway!\n[Click Here]({message.jump_url})\nClicked Reaction", save=True)



@client.event
async def on_message(message):
  isin = message.guild.get_member(message.author.id)
  if message.author.bot and client.user.mentioned_in(message) and isin:
    log(f"Bot Mention\nMaybe Won Giveaway\n[Click Here]({message.jump_url})\nMessage Content: {message.content}", save=True)
  if not message.author.bot:
    return
  if not message.embeds:
    return
  try:
    if "winners" or "winners:" in message.embeds[0].description.lower():
      hasdesc = True
  except:
    hasdesc = False
  if 'giveaway' in message.content.lower() or ":gift:" in message.content.lower() or hasdesc or ":tada:" in message.content.lower():
    try:
      await message.components[0].children[0].click()
    except:
      pass
    else:
      if "giveaway" in message.content.lower():
        log(f"Sniped A Giveaway\n[Click Here]({message.jump_url})", save=True)
      else:
        log(f"Probably Not A Giveaway\nClicked Button\n[Click Here]({message.jump_url})", save=True)
  await client.process_commands(message)

  
    
client.run(token, reconnect=True)
