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
    @worker.task(task_type="DecommissionInitiator_HT")
    async def notify_administrator_handler():
        print("Received a job: Initiate Device Decommission")
        return {"message": "Task 'Initiate Device Decommission' completed successfully"}

    @worker.task(task_type="ScheduleDecommission_HT")
    async def notify_administrator_handler():
        print("Received a job: Schedule Device Decommission")
        return {"message": "Task 'Schedule Device Decommission' completed successfully"}

    @worker.task(task_type="PhysicalDecommission_HT")
    async def notify_administrator_handler():
        print("Received a job: Physical Decommission of Device")
        return {"message": "Task 'Physical Decommission of Device' completed successfully"}

    # Start the worker
    print("Starting Decommission Requestor worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

