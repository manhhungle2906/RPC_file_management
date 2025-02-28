import grpc
from concurrent import futures
import file_sharing_pb2
import file_sharing_pb2_grpc

# Mock user database
users = {"admin": "password123", "user1": "securepass"}

class AuthService(file_sharing_pb2_grpc.AuthServiceServicer):
    def Authenticate(self, request, context):
        if request.username in users and users[request.username] == request.password:
            return file_sharing_pb2.AuthResponse(success=True, message="Authentication Successful")
        return file_sharing_pb2.AuthResponse(success=False, message="Invalid Credentials")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sharing_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Auth Service is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
