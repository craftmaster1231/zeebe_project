import grpc
from gateway_pb2 import ActivateJobsRequest
from gateway_pb2_grpc import GatewayStub
from concurrent import futures

class ListJobsService:
    def __init__(self):
        # Connect to the Zeebe gateway
        self.channel = grpc.insecure_channel('localhost:26500')  # Zeebe gateway address
        self.stub = GatewayStub(self.channel)

    def getAllworkers(self):
        return {
            "worker_id": ["W_0", "W_1", "W_2", "W_3", "W_4", "W_5", "W_6", "W_7", "W_8", "W_9"],
            "worker_name": ["Equipment Requestor", "Install Approvers", "DataCenter Technician", "Power Technician", "Network Provisioner", "Storage Provisioner", "Administrator", "Decomission Requestor", "Decommission Approvers", "Move Approvers"],
            "count_tasks": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        }

    def getTasksCount(self, worker_id):
        return 4

    def list_jobs(self, job_type, worker, timeout=30000, max_jobs=10):
        request = ActivateJobsRequest(
            type=job_type,
            worker=worker,
            timeout=timeout,
            maxJobsToActivate=max_jobs
        )
        try:
            # Streaming response from Zeebe
            response_stream = self.stub.ActivateJobs(request)
            
            running_instances = []
            for response in response_stream:  # Iterate over the stream
                for job in response.jobs:  # Access jobs inside each response
                    running_instances.append({
                        "bp_id": job.processDefinitionKey,
                        "bp_name": job.bpmnProcessId,
                        "instance_id": job.processInstanceKey,
                        "start_time": "2024-12-20 14:00:00"  # Placeholder, adjust to actual job data if available
                    })
                    print(f"Job Key: {job.key}, Type: {job.type}, Worker: {job.worker}")
        
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.code()} - {e.details()}")

def serve():
    list_jobs_service = ListJobsService()

    # Example usage
    list_jobs_service.list_jobs("payment-service", "worker-1")

if __name__ == '__main__':
    serve()

