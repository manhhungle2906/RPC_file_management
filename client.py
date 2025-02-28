import grpc
import file_sharing_pb2
import file_sharing_pb2_grpc

# Connect to Auth Service
auth_channel = grpc.insecure_channel("localhost:50051")
auth_stub = file_sharing_pb2_grpc.AuthServiceStub(auth_channel)

# Authenticate User
username = "admin"
password = "password123"
auth_response = auth_stub.Authenticate(file_sharing_pb2.UserRequest(username=username, password=password))

if auth_response.success:
    print(f"✅ {auth_response.message}")

    # Connect to File Storage Service
    file_channel = grpc.insecure_channel("localhost:50052")
    file_stub = file_sharing_pb2_grpc.FileStorageServiceStub(file_channel)

    # Read content from a real file
    filename = "test.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f" Error: {filename} not found.")
        file_content = "Sample text content for testing."

    # Upload File
    file_response = file_stub.UploadFile(
        file_sharing_pb2.FileRequest(username=username, filename=filename, content=file_content)
    )
    print(f" {file_response.message}")

    # Download File
    file_response = file_stub.DownloadFile(file_sharing_pb2.FileRequest(username=username, filename=filename))
    print(f"{file_response.message}")

else:
    print(f"Authentication Failed: {auth_response.message}")
