import logging
import time
import asyncio

logging.basicConfig(
    filename='log/example.log',
    encoding='utf-8',
    format='%(asctime)s.%(msecs)03d (%(created)f) %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)
import simpleobsws
import keyboard

async def record():    
    parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

    ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4455', password = 'DOrttBnTUZ9ASt9V', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete
    
    requests = []

    # requests.append(simpleobsws.Request('GetVersion')) # Build a Request object, then append it to the batch
    # requests.append(simpleobsws.Request('GetStats')) # Build another request object, and append it
    
    # 获取场景列表
    requests.append(simpleobsws.Request('GetSceneList'))
        
    ret = await ws.call_batch(requests, halt_on_failure = False) # Perform the request batch
    outputPath = ""
    keyLogPath = ""
    for result in ret:
        if result.ok(): # Check if the request succeeded
            # print("Request succeeded! Response data: {}".format(result.responseData))
            if result.responseData['currentProgramSceneName'] == 'val-autorecord':
                logging.debug('the val-autorecord scenes found')
                await ws.call(simpleobsws.Request('StopRecord'))
                await ws.call(simpleobsws.Request('StartRecord'))
                print("starting")
                # await asyncio.sleep(1)
                # print("Press 'f6' to stop recording...")
                # 用于存储记录的键位和时间戳
                key_log = [('start', time.time()), ]

                # 定义一个回调函数，当按下键时调用
                def on_key_event(event):
                    if event.event_type == 'down':
                        timestamp = time.time()
                        key_log.append((event.name, timestamp))

                # 注册回调函数来监听所有键事件
                keyboard.hook(on_key_event)

                print("Press ESC to stop...")

                # 等待ESC键被按下
                keyboard.wait('esc')

                # 停止录像和键位录制
                out = await ws.call(simpleobsws.Request('StopRecord'))
                outputPath = out.responseData['outputPath']
                keyboard.unhook_all()    
                # 写入记录的键位和时间戳到文件中
                keyLogPath = f"{outputPath.split('.')[0]}_key_log.txt"
                with open(keyLogPath, 'w') as file:
                    for key, timestamp in key_log:
                        file.write(f"Key: {key}, Timestamp: {timestamp}\n")
                
                print(f"Key log has been written to {keyLogPath}")
                # print(out)

    await ws.disconnect() # Disconnect from the websocket server cleanly
    return outputPath, keyLogPath
if __name__ == "__main__":
    asyncio.run(record())
