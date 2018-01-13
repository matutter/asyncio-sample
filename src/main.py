import json
import logging
import coloredlogs

import asyncio
import aiofiles

class App(object):

  def __init__(self):
    self.name = self.__class__.__name__
    self.log = logging.getLogger(self.name)
    self.loop = asyncio.get_event_loop()
    coloredlogs.install(
      milliseconds=False,
      level='DEBUG',
      logger=self.log)

  async def load_tasks(self, path):
    tasks = []

    self.log.debug('Loading tasks from %s' % (path))

    async with aiofiles.open(path, mode='r') as fd:
        json_text = await fd.read()
        obj = json.loads(json_text)
        tasks = obj.get('tasks', [])

    self.log.debug('%d tasks received' % (len(tasks)))

    for task in asyncio.as_completed([self.run(t) for t in tasks]):
      res = await task
      print(res)

  def start_loop(self):

    self.loop.run_until_complete(
      asyncio.gather(self.load_tasks('./test/sample.json'))
    )
    self.loop.close()

    return self

  async def run(self, task):
    self.log.debug('Start task: %s' % (task['id']))
    await asyncio.sleep(task['wait'])
    self.log.debug('Done task: %s' % (task['id']))
    return task


if __name__ == '__main__':
  p = App().start_loop()
  
