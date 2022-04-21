from PIL import Image
import deeppyer, asyncio

async def main():
    img = Image.open('../img/unfried.png')
    img = await deeppyer.deepfry(img)
    img.save('../fried.png')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
