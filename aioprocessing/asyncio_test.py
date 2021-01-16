import time
import asyncio
import aioprocessing
from random import randrange
from queue import Empty

proc_ids = [b'0004', b'0002'] # List of proc ids 

def worker_process(board_id: int, queue: aioprocessing.AioQueue, terminate_event: aioprocessing.AioEvent):
  count = 0
  
  while not terminate_event.is_set():
    try:
      message = queue.get(timeout=1)
    except Empty:
      pass
    else:
      print(f'Worker {board_id} recieved message {message=}')
      time.sleep(1)
      queue.put({'id': board_id, 'count': count})
      count += 1
      if count > 3:
        terminate_event.set()
      
  print(f'Worker {board_id} terminated')
  
async def producer(queues: list, terminate_event: aioprocessing.AioEvent):
  while not terminate_event.is_set():
    await asyncio.sleep(3)
    proc_idx = randrange(2)
    await queues[proc_idx].coro_put({'type': 'write_block', 'offset': 2})
    result = await queues[proc_idx].coro_get()
    print(f'Producer recieved message {result=}')
  print('Producer terminated')
  
if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  terminate_event = aioprocessing.AioEvent()
  queues = [aioprocessing.AioQueue() for i in proc_ids]
  procs = [aioprocessing.AioProcess(target=worker_process, args=(id, queues[i], terminate_event)) for i, id in enumerate(proc_ids)]
  for p in procs:
    p.start()
  
  tasks = [
        asyncio.ensure_future(producer(queues, terminate_event))
  ]
  
  loop.run_until_complete(asyncio.wait(tasks))
  loop.close()