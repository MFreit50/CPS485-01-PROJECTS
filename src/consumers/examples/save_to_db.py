import asyncio

from src.consumers.base.asynchronous_consumer import AsynchronousConsumer


class SaveToDBConsumer(AsynchronousConsumer):

    async def _handle(self, event):
        # Simulate saving to a database
        print("Saving event to the database...")
        await asyncio.sleep(1)  # Simulate I/O delay
        print(f"Event {event} saved to the database.")
