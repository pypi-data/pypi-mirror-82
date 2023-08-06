import asyncio
import contextlib

from .event import Event, EventRouter, EventRouterHost, Eventful
from .util import int_to_ordinal


def aiorun(startup, cleanup):
   loop = asyncio.get_event_loop()
   try:
      loop.create_task(startup)
      loop.run_forever()
   except KeyboardInterrupt:
      pass
   finally:
      loop.run_until_complete(cleanup)
      try:
         all_tasks = asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True)
         all_tasks.cancel()
         with contextlib.suppress(asyncio.CancelledError):
            loop.run_until_complete(all_tasks)
         loop.run_until_complete(loop.shutdown_asyncgens())
      finally:
         loop.close()


__all__ = ["Event", "Eventful", "EventRouterHost", "EventRouter", "int_to_ordinal"]
