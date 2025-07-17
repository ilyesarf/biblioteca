import grpc
import nanolock_pb2
import nanolock_pb2_grpc

class NanoLockClient:
    def __init__(self, host='nanolock', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = nanolock_pb2_grpc.NanoLockStub(self.channel)

    def verify_face(self, user_hash, b64enc_img):
        request = nanolock_pb2.FaceRequest(user_id=user_hash, image_data=b64enc_img.encode())
        response = self.stub.Verify(request)
        return response.verified, response.reason

    def add_user(self, user_hash, b64enc_img):
        # If you added AddUser to proto
        request = nanolock_pb2.AddUserRequest(user_id=user_hash, image_data=b64enc_img.encode())
        response = self.stub.AddUser(request)
        return response.success, response.reason
