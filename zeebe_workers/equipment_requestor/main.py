import asyncio
import grpc
from pyzeebe import ZeebeWorker
import time
import os

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

    @worker.task(task_type="EquipmentInstallInitiator_HT")
    async def initiate_equipment_install_handler():
        print("Received a job: Initiate Equipment Install")
        print("Task 'Initiate Equipment Install' completed successfully")
        return {"message": "Task 'Initiate Equipment Install' completed successfully"}

    @worker.task(task_type="InitiateDeviceMove_HT")
    async def initiate_equipment_install_handler():
        print("Received a job: Initiate Device Move")
        return {"message": "Task 'Initiate Device Move' completed successfully"}

    @worker.task(task_type="ServerRenameInitiator_HT")
    async def initiate_equipment_install_handler():
        print("Received a job: Server Rename Initiator")
        print("Task 'Server Rename Initiator' completed successfully")

        value = os.getenv("TEST_VAR")
        time.sleep(int(value))

        return {"message": "Task 'Server Rename Initiator' completed successfully"}

    @worker.task(task_type="ApproveEquipmentMoveRequest_HT")
    async def initiate_equipment_install_handler():
        print("Received a job: Approve Equipment Move Request")
        return {"message": "Task 'Approve Equipment Move Request' completed successfully"}

    # Start the worker
    print("Starting Equipment Requestor worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

