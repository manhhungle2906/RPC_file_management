import grpc
import os
from concurrent import futures
import file_sharing_pb2
import file_sharing_pb2_grpc

# Define a directory for storing files
FILE_STORAGE_DIR = "file_storage"

# Ensure the directory exists
if not os.path.exists(FILE_STORAGE_DIR):
    os.makedirs(FILE_STORAGE_DIR)

class FileStorageService(file_sharing_pb2_grpc.FileStorageServiceServicer):
    
    def UploadFile(self, request, context):
        file_path = os.path.join(FILE_STORAGE_DIR, request.filename)
        
        # Write content to a real file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(request.content)

        return file_sharing_pb2.FileResponse(
            success=True, 
            message=f"📤 File '{request.filename}' uploaded successfully!"
        )

    def DownloadFile(self, request, context):
        file_path = os.path.join(FILE_STORAGE_DIR, request.filename)

        # Check if file exists
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            return file_sharing_pb2.FileResponse(
                success=True, 
                message=f"📥 File '{request.filename}' content: \n{content}"
            )
        
        return file_sharing_pb2.FileResponse(
            success=False, 
            message=f"❌ File '{request.filename}' not found."
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sharing_pb2_grpc.add_FileStorageServiceServicer_to_server(FileStorageService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("📁 File Storage Service is running on port 50052...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
