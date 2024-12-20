import time 
import asyncio
import grpc
from pyzeebe import ZeebeWorker, ZeebeClient

# Zeebe Gateway details
ZEEBE_GATEWAY = "localhost:26500"

async def main():
    # Explicitly set up the event loop
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # Create a gRPC channel
    grpc_channel = grpc.aio.insecure_channel(ZEEBE_GATEWAY)

    # Create Zeebe worker
    worker = ZeebeWorker(grpc_channel)

    # Create Zeebe client for signal creation
    client = ZeebeClient(grpc_channel)

# Define a job handler with direct variable mapping
    @worker.task(task_type="send-message")
    async def send_message(message_type: str):
       # time.sleep(5)
        try:
            if not message_type:
                raise ValueError("Missing 'message_type' in job variables")

            # Process the task
            print(f"Processing task of type: {message_type}")

            # Publish a message to Zeebe
            await client.publish_message(
                name=message_type,  # Message name
                correlation_key="",
                variables={"status": "message_published"}   # Variables to pass
            )
            print(f"Message '{message_type}' published successfully.")

        except Exception as e:
            print(f"Failed to process job: {e}")


    # Start the worker
    print("Worker started and waiting for messages...")
    await worker.work()


if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

