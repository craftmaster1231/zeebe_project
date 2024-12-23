from concurrent import futures
import grpc
import json
from grpc_tools import protoc

# Compile the proto file at runtime
protoc.main((
    '',
    '--proto_path=.',
    '--python_out=.',
    '--grpc_python_out=.',
    'provision_space_service.proto',
))

# Import the dynamically generated modules
import rename_pb2
import rename_pb2_grpc
import psycopg2
from psycopg2 import sql
from concurrent import futures


db_params = {
        'dbname': 'mydb',
        'user': 'myuser',
        'password': 'mypassword',
        'host': 'localhost',
        'port': 5432,
    }

class ProvisionSpaceServicer(provision_space_service_pb2_grpc.ProvisionSpaceServicer):
    def ProvisionSpaceResponse(self, request, context):
        SpaceName = request.SpaceName
        ParentId = request.ParentId
        Type = request.Type
        XCoordinate = request.XCoordinate
        YCoordinate = request.YCoordinate
        ZCoordinate = request.ZCoordinate
        Rotation = request.Rotation
        RackSide = request.RackSide
        RU = request.RU
        Location = request.Location
        UHeight = request.UHeight
        XOffset = request.XOffset
        XPosition = request.XPosition

        try:
            conn = psycopg2.connect(*db_params)
            cursor = conn.cursor()
            
            update_query = sql.SQL(f"INSERT INTO Placement (SpaceName, ParentId, Type, XCoordinate, YCoordinate, ZCoordinate, Rotation, RackSide, RU, Location, UHeight, XOffset, XPosition) VALUES ({SpaceName}, {ParentId}, {Type}, {XCoordinate}, {YCoordinate}, {ZCoordinate}, {Rotation}, {RackSide}, {RU}, {Location}, {UHeight}, {XOffset}, {XPosition})")
            cursor.execute(update_query)
            conn.commit()

            if cursor.rowcount > 0:
                status = "success"
            else:
                status = "no rows updated"

            find_query = sql.SQL(f"SELECT * FROM Placement WHERE SpaceName = {SpaceName}")
            cursor.execute(update_query)
            conn.commit()

            cursor.close()
            conn.close()

            response_data = {
                        "message": f"{find_query.fetch_results}",
                        "status": "success",
                    }
        except Exception as e:
            response_data = {
                        "message": f"Error name: {e}",
                        "status": "error",
                    }

        return provision_space_service_pb2.JsonResponse(response=json.dumps(response_data))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    provision_space_service_pb2_grpc.add_ProvisionSpaceServicer_to_server(ProvisionSpace(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()