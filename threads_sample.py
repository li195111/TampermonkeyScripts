import threading
import time
from typing import List


class SampleThread(threading.Thread):

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.is_kill = False

  def run(self) -> None:
    try:
      while True:

        if self.is_kill:
          raise KeyboardInterrupt

        time.sleep(1)
    except KeyboardInterrupt:
      print('Sub Thread Interrupt')


if __name__ == '__main__':
  ts: List[SampleThread] = []
  for i in range(10):
    t = SampleThread()
    t.start()
    ts.append(t)

  interrupt = False
  while not interrupt:
    try:
      for t in ts:
        if not t.is_alive():
          t.join()
    except KeyboardInterrupt:
      print('Main Thread Interrupt')
      for t in ts:
        t.is_kill = True
      interrupt = True

  magic_char = '\33[F'
  multi_line = 'First ... {}\nSecond ... {}\nThird ... {}\n'
  ret_depth = magic_char * multi_line.count('\n')
  for i in range(3):
    print(f'{multi_line.format(i,i,i)}{ret_depth}', end='', flush=True)
    time.sleep(1)
