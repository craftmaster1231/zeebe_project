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
    'my_service.proto',
))

# Import the dynamically generated modules
import my_service_pb2
import my_service_pb2_grpc
import psycopg2
from psycopg2 import sql


class MyServiceServicer(my_service_pb2_grpc.MyServiceServicer):
    def GetJsonResponse(self, request, context):
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
            conn = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="postgres",
                                    host="localhost",
                                    port=5432)
            cursor = conn.cursor()
            
            
            update_query = sql.SQL(f"INSERT INTO Placement (SpaceName, ParentId, Type, XCoordinate, YCoordinate, ZCoordinate, Rotation, RackSide, RU, Location, UHeight, XOffset, XPosition) VALUES ('{SpaceName}', '{ParentId}', '{Type}', {XCoordinate}, {YCoordinate}, {ZCoordinate}, {Rotation}, '{RackSide}', {RU}, {Location}, {UHeight}, {XOffset}, {XPosition})")
            cursor.execute(update_query)
            conn.commit()

            if cursor.rowcount > 0:
                status = "success"
            else:
                status = "no rows updated"

            cursor.close()
            conn.close()

            response_data = {
                        "message": f"",
                        "status": "success",
                    }
        except Exception as e:
            response_data = {
                        "message": f"Error updating name: {e}",
                        "status": "error",
                    }

        return my_service_pb2.JsonResponse(response=json.dumps(response_data))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:30001')
    server.start()
    print("Server is running on port 30001...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()