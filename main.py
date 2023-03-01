import discord
from discord.ext import commands, tasks
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="#", intents=discord.Intents.all())


def get_dust_price():
  payload = {'address': 'DUSTawucrTsGU8hcqRdHDCbuYhCPADMLM2VcCb8VnFnQ'}
  response = requests.get("https://public-api.birdeye.so/public/price",
                          payload)
  response_json = response.json()
  price = response_json["data"]["value"]
  return price


def get_degods_price():
  response = requests.get(
    "https://api-mainnet.magiceden.dev/v2/collections/degods/stats")
  response_json = response.json()
  floorPrice = response_json["floorPrice"]
  return floorPrice


def get_y00ts_price():
  response = requests.get(
    "https://api-mainnet.magiceden.dev/v2/collections/y00ts/stats")
  response_json = response.json()
  floorPrice = response_json["floorPrice"]
  return floorPrice


@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))
  change_status.start()


@tasks.loop(seconds=600)
async def change_status():
  pricestatus = get_dust_price()
  priceformatted = "{:.3f}".format(pricestatus)
  await client.change_presence(activity=discord.Game("$" + priceformatted))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == '$dust':
    price = get_dust_price()
    priceformatted = "{:.3f}".format(price)
    await message.channel.send('Dust price: ' + priceformatted)

  if message.content == '$degods':
    degodsprice = get_degods_price()
    priceformatted =  degodsprice / 1000000000
    await message.channel.send('degods floor price: ' + str(priceformatted))

  if message.content == '$y00ts':
    y00tsprice = get_y00ts_price()
    priceformatted =  y00tsprice / 1000000000
    await message.channel.send('y00ts floor price: ' + str(priceformatted))


@client.command()
async def dust(ctx):
  await ctx.send("Dust price:")


client.run(os.getenv('OL'))
