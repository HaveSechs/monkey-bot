import discord
import asyncio
from io import BytesIO
from PIL import Image
from pyppeteer import launch


async def capture_screenshot(url, javascript, interaction: discord.Interaction):
    await interaction.response.send_message("`Started job`")

    browser = await launch(args=['--proxy-server=socks5://127.0.0.1:9150'])
    page = await browser.newPage()

    await interaction.edit_original_response(content="`Started browser and proxy`")

    page.setDefaultNavigationTimeout(120000)
    await page.setExtraHTTPHeaders({"user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"})

    await interaction.edit_original_response(content="`Page loading Started`")

    await page.goto(url)
    await page.evaluate(javascript)
    html = await page.content()

    await interaction.edit_original_response(content="`Page loaded!`")

    screenshot = await page.screenshot()
    await browser.close()

    await interaction.edit_original_response(content="`Screenshot done and browser closed`")

    image = Image.open(BytesIO(screenshot))

    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    html_bytes = BytesIO()
    html_bytes.write(html.encode())
    html_bytes.seek(0)

    return discord.File(image_bytes, filename="tor.png"), discord.File(html_bytes, filename="page.html")