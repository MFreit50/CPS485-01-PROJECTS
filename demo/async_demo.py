import asyncio

from src.consumers.examples.print_consumer import PrintConsumer
from src.consumers.examples.save_to_db import SaveToDBConsumer
from src.core.events.base.base_event import BaseEvent
from src.transport.in_memory.in_memory_transport import InMemoryTransport


async def main():
    transport = InMemoryTransport(number_of_workers=1)
    print_consumer = PrintConsumer()
    db_consumer = SaveToDBConsumer()
    transport.subscribe(print_consumer)
    transport.subscribe(db_consumer)

    print(print_consumer)
    print(db_consumer)

    await transport.start()
    for i in range(5):
        event = BaseEvent(0, "test")
        await transport.publish(event)
    await transport.flush()


if __name__ == "__main__":

    asyncio.run(main())
