import asyncio
import grpc
from pyzeebe import ZeebeWorker

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

    # Define a job handler

    @worker.task(task_type="ProvisioningCabling_HT")
    async def provision_cabling_handler():
        print("Received a job: Provision Network Cabling For Equipment Install")
        return {"message": "Task 'Provision Network Cabling For Equipment Install' completed successfully"}


    # Start the worker
    print("Starting Network Cabler worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

