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
    @worker.task(task_type="send-message")
    async def send_message(job):
        try:
            # Access variables from the job
            event_type = job.variables.get("event_type")
            correlation_key = job.variables.get("correlation_key")
            event_payload = job.variables.get("event_payload", {})
            
            if not event_type or not correlation_key:
                raise ValueError("Missing 'event_type' or 'correlation_key' in job variables")
            
            # Simulate sending the event
            print(f"Sending event: {event_type} with correlation key: {correlation_key} and payload: {event_payload}")
            
            # Mark the job as successfully processed
            await job.set_success()
        except Exception as e:
            print(f"Failed to process job: {e}")
            # Mark the job as failed
            await job.set_failure(str(e), retries=0)

        # Start the worker
        print("Starting Event Caller worker...")
        await worker.work()

if __name__ == "__main__":
    # Use a safe asyncio loop policy
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    asyncio.run(main())

