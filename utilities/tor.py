import discord
import asyncio
from io import BytesIO
from PIL import Image
from pyppeteer import launch


async def capture_screenshot(url):
    browser = await launch(args=['--proxy-server=socks5://127.0.0.1:9150'])
    page = await browser.newPage()
    # await page.setDefaultNavigationTimeout(60000)
    await page.goto(url)
    screenshot = await page.screenshot()
    await browser.close()

    image = Image.open(BytesIO(screenshot))

    bytes = BytesIO()
    image.save(bytes, format="PNG")
    bytes.seek(0)

    return discord.File(bytes, filename="tor.png")