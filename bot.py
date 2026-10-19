import asyncio
import random
from playwright.async_api import async_playwright

async def single_bot_task(bot_id):
    delay_seconds = random.randint(7200, 14400)
    print(f"🤖 [بوت {bot_id}] ⏳ الانتظار لفترة عشوائية قبل البدء: حوالي {delay_seconds / 3600:.2f} ساعة...")
    await asyncio.sleep(delay_seconds)

    print(f"🤖 [بوت {bot_id}] 🚀 بدء جلسة التصفح الجديدة...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--start-maximized']
        )

        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        async def handle_new_page(new_page):
            try:
                await asyncio.sleep(random.uniform(5.0, 15.0))
                await new_page.close()
            except:
                pass

        context.on("page", handle_new_page)
        page = await context.new_page()

        try:
            target_url = "https://Almanarah.kesug.com"
            print(f"🤖 [بوت {bot_id}] 🌐 جاري فتح الموقع: {target_url}")
            await page.goto(target_url, wait_until="networkidle")

            await asyncio.sleep(random.uniform(180.0, 360.0))

            for _ in range(random.randint(8, 15)):
                scroll_amount = random.randint(250, 550)
                await page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(random.uniform(15.0, 35.0))

            for page_jump in range(random.randint(3, 6)):
                try:
                    read_more_buttons = page.locator("text='اقرأ المزيد', a:has-text('اقرأ المزيد'), button:has-text('اقرأ المزيد')")
                    count = await read_more_buttons.count()

                    if count > 0:
                        random_index = random.randint(0, count - 1)
                        target_button = read_more_buttons.nth(random_index)

                        if await target_button.is_visible():
                            print(f"🤖 [بوت {bot_id}] 🔗 النقر على زر 'اقرأ المزيد'...")
                            await target_button.scroll_into_view_if_needed()
                            await asyncio.sleep(random.uniform(1.5, 3.0))
                            await target_button.hover()
                            await asyncio.sleep(random.uniform(1.0, 2.0))
                            await target_button.click(timeout=5000)

                            await asyncio.sleep(random.uniform(180.0, 360.0))
                            await page.go_back(wait_until="networkidle")
                            await asyncio.sleep(random.uniform(5.0, 10.0))
                        else:
                            break
                    else:
                        break
                except:
                    break

            print(f"🤖 [بوت {bot_id}] 🎉 اكتملت الجلسة بنجاح!")

        except Exception as e:
            print(f"🤖 [بوت {bot_id}] خطأ: {e}")

        finally:
            await browser.close()

async def main():
    bot_count = random.randint(2, 5)
    print(f"🎯 تم اختيار تشغيل {bot_count} بوتات بالتوازي في هذه الجلسة.")
    tasks = [single_bot_task(i+1) for i in range(bot_count)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())