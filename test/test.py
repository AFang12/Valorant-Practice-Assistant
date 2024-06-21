import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # 模拟I/O操作
    print("Data fetched!")

async def process_data():
    print("Processing data...")
    await asyncio.sleep(1)  # 模拟I/O操作
    print("Data processed!")

async def main():
    await asyncio.gather(fetch_data(), process_data())

# 使用 asyncio.run 作为入口函数
if __name__ == "__main__":
    asyncio.run(main())
