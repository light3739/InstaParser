import asyncio
from pyppeteer import launch
from contextlib import asynccontextmanager


@asynccontextmanager
async def browser_context():
    browser = await launch(headless=True)
    try:
        yield browser
    finally:
        await browser.close()


async def check_history(name: str, page):
    await page.setCacheEnabled(False)
    await page.goto(f"https://instastories.net/story/{name}")
    await page.waitForSelector('.num', timeout=60000)
    text = await page.querySelector('.last-story_container')
    content = await text.getProperty('textContent')
    content_str = await content.jsonValue()
    return content_str


async def check_for_new_stories(name: str, page):
    previous_num_stories = 0
    history_str = await check_history(name, page)
    if history_str:
        previous_num_stories = int(history_str.split()[0])
    while True:
        history_str = await check_history(name, page)
        if history_str:
            history = int(history_str.split()[0])
            print(f"History: {history}, Previous: {previous_num_stories}")
            if history != previous_num_stories:
                with open("output.txt", "a") as f:
                    f.write("The person added a story.\n")
            previous_num_stories = history
        else:
            previous_num_stories = 0
        await asyncio.sleep(60)


async def main(person):
    async with browser_context() as browser:
        page = await browser.newPage()
        await check_for_new_stories(person, page)


if __name__ == "__main__":
    asyncio.run(main("andziasheerio"))
