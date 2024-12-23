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
    'rename.proto',
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

class RenameServicer(rename_pb2_grpc.RenameServicer):
    def RenameResponse(self, request, context):
        id = request.id
        name = request.new_name

        try:
            conn = psycopg2.connect(*db_params)
            cursor = conn.cursor()
            
            update_query = sql.SQL("UPDATE my_table SET name = %s WHERE id = %s")
            cursor.execute(update_query, (name, id))
            conn.commit()

            if cursor.rowcount > 0:
                status = "success"
            else:
                status = "no rows updated"

            cursor.close()
            conn.close()

            response_data = {
                        "message": f"new name - {name}",
                        "status": "success",
                    }
        except Exception as e:
            response_data = {
                        "message": f"Error updating name: {e}",
                        "status": "error",
                    }

        return rename_pb2.JsonResponse(response=json.dumps(response_data))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rename_pb2_grpc.add_RenameServicer_to_server(RenameServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()