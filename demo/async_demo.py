import asyncio

from src.consumers.examples.print_consumer import PrintConsumer
from src.consumers.examples.save_to_db import SaveToDBConsumer
from src.core.contracts.event import Event
from src.transport.in_memory.in_memory_transport import InMemoryTransport


async def main():
    transport = InMemoryTransport(number_of_workers=1)
    transport.subscribe(PrintConsumer())
    transport.subscribe(SaveToDBConsumer())
    await transport.start()
    for i in range(5):
        event = Event(0, "test")
        await transport.publish(event)
    await transport.flush()


if __name__ == "__main__":

    asyncio.run(main())
