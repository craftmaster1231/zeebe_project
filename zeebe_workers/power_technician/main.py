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


    @worker.task(task_type="ProvisioningPower_HT")
    async def provision_power_handler():
        print("Received a job: Provision Power For Equipment Install")
        return {"message": "Task 'Provision Power For Equipment Install' completed successfully"}

    @worker.task(task_type="DecommissionPower_HT")
    async def provision_power_handler():
        print("Received a job: Decommission Power For Equipment Move")
        return {"message": "Task 'Decommission Power ' completed successfully"}


    # Start the worker
    print("Starting Power Technician worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

