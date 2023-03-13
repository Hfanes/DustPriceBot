import discord
from discord.ext import commands, tasks
import os
import requests
from server import serverRun
from asyncio import sleep as s

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
stop = False


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
  pricehour.start()


@tasks.loop(seconds=600)
async def change_status():
  pricestatus = get_dust_price()
  priceformatted = "{:.3f}".format(pricestatus)
  await client.change_presence(activity=discord.Game("$" + priceformatted))
  return priceformatted


@tasks.loop(seconds=7200)  #2h
async def pricehour():
  channel = client.get_channel(1080342658901364777)
  dustprice = get_dust_price()
  dustpriceformatted = "{:.3f}".format(dustprice)

  degodsprice = get_degods_price()
  degodspriceformatted = degodsprice / 1000000000

  y00tsprice = get_y00ts_price()
  y00tspriceformatted = y00tsprice / 1000000000

  await channel.send('Dust: ' + str(dustpriceformatted) + " - " + "DeGods: " +
                     str(degodspriceformatted) + " - " + "Y00ts: " +
                     str(y00tspriceformatted))



@client.command()
async def degodsS(ctx):
  response = requests.get(
    "https://api-mainnet.magiceden.dev/v2/collections/degods/activities?offset=0&limit=100"
  )
  response_json = response.json()
  for obj in response_json:
    if obj["type"] == "buyNow":
      embed = discord.Embed(title="DeGods sold",
                            description="has been sold for" + str(obj["price"]),
                            color=0x4cf08b)
      embed.add_field(name="From", value=obj["seller"], inline=True)
      embed.add_field(name="From", value=obj["buyer"], inline=True)
      embed.set_thumbnail(url=obj["image"])
      await ctx.send(embed=embed)

@client.command()
async def y00tsS(ctx):
  response = requests.get(
    "https://api-mainnet.magiceden.dev/v2/collections/y00ts/activities?offset=0&limit=100"
  )
  response_json = response.json()
  for obj in response_json:
    if obj["type"] == "buyNow":
      embed = discord.Embed(title="Y00t sold",
                            description="has been sold for" + str(obj["price"]),
                            color=0x4cf08b)
      embed.add_field(name="From", value=obj["seller"], inline=True)
      embed.add_field(name="From", value=obj["buyer"], inline=True)
      embed.set_thumbnail(url=obj["image"])
      await ctx.send(embed=embed)


@client.command()
async def ajuda(ctx):
  await ctx.send('Commands: $all,  $dust,  $degods,  $y00ts, $alert {value}')


@client.command()
async def dust(ctx):
  price = get_dust_price()
  priceformatted = "{:.3f}".format(price)
  await ctx.send(f'Dust price: {priceformatted}, {ctx.author.mention}')


@client.command()
async def degods(ctx):
  degodsprice = get_degods_price()
  priceformatted = degodsprice / 1000000000
  await ctx.send('degods floor price: ' + str(priceformatted))


@client.command()
async def y00ts(ctx):
  y00tsprice = get_y00ts_price()
  priceformatted = y00tsprice / 1000000000
  await ctx.send('y00ts floor price: ' + str(priceformatted))


@client.command()
async def all(ctx):
  dustprice = get_dust_price()
  dustpriceformatted = "{:.3f}".format(dustprice)

  degodsprice = get_degods_price()
  degodspriceformatted = degodsprice / 1000000000

  y00tsprice = get_y00ts_price()
  y00tspriceformatted = y00tsprice / 1000000000

  await ctx.send('Dust: ' + str(dustpriceformatted) + " - " + "DeGods: " +
                 str(degodspriceformatted) + " - " + "Y00ts: " +
                 str(y00tspriceformatted))


@client.command()
async def alert(ctx, price: float):
  while not stop:
    payload = {'address': 'DUSTawucrTsGU8hcqRdHDCbuYhCPADMLM2VcCb8VnFnQ'}
    response = requests.get("https://public-api.birdeye.so/public/price",
                            payload)
    response_json = response.json()
    priceget = response_json["data"]["value"]
    priceformatted = "{:.3f}".format(priceget)
    floatpriceformatted = float(priceformatted)
    print("input" + str(price))
    print("get" + str(floatpriceformatted))

    if price <= floatpriceformatted:
      if price >= floatpriceformatted:
        await ctx.send(f'Dust price: {priceformatted} {ctx.author.mention}')
        break
    elif price >= floatpriceformatted:
      if price >= floatpriceformatted:
        await ctx.send(f'Dust price: {priceformatted} {ctx.author.mention}')
        break
    await s(45)


@client.command()
async def alertcancel(ctx):
  global stop
  stop = True
  await ctx.send(f'Alert canceled {ctx.author.mention}')


serverRun()
client.run(os.environ['OL'])
