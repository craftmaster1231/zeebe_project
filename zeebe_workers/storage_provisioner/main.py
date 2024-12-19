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
    @worker.task(task_type="ProvisioningStorage_HT")
    async def provision_storage_handler():
        print("Received a job: Provision Storage For Equipment Install")
        return {"message": "Task 'Provision Storage For Equipment Install' completed successfully"}

    @worker.task(task_type="DecommissionStorage_HT")
    async def provision_storage_handler():
        print("Received a job: Decommission Storage For Equipment Move")
        return {"message": "Task 'Decommission Storage For Equipment Move' completed successfully"}

    # Start the worker
    print("Starting Storage Provisioner worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

