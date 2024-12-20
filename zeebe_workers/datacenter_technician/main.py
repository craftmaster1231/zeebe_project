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
    @worker.task(task_type="ProvisioningSpace_HT")
    async def provision_space_handler():
        print("Received a job: Provision Space For Equipment Install")
        print("Task 'Provision Space For Equipment Install' completed successfully")
        return {"message": "Task 'Provision Space For Equipment Install' completed successfully"}

    @worker.task(task_type="EquipmentInstaller_HT")
    async def install_equipment_handler():
        print("Received a job: Install Equipment")
        return {"message": "Task 'Install Equipment' completed successfully"}

    @worker.task(task_type="MoveDevicePhysically_HT")
    async def install_equipment_handler():
        print("Received a job: Move Device Physically For Move Equipment")
        return {"message": "Task 'Move Device Physically For Move Equipment' completed successfully"}

    @worker.task(task_type="ChangeServerName_HT")
    async def install_equipment_handler():
        print("Received a job: Change Server Name For Rename Equipment")
        return {"message": "Task 'Change Server Name For Rename Equipment' completed successfully"}


    # Start the worker
    print("Starting Datacenter Technician worker...")
    await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

