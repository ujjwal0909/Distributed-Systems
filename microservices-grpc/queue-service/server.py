import grpc
from concurrent import futures
import time
import queue_pb2
import queue_pb2_grpc

class QueueServiceServicer(queue_pb2_grpc.QueueServiceServicer):
    def __init__(self):
        self.queue = []
        self.history = []

    def AddTrack(self, request, context):
        self.queue.append(request)
        return queue_pb2.QueueResponse(message="Track added", queue=self.queue)

    def RemoveTrack(self, request, context):
        self.queue = [t for t in self.queue if t.id != request.id]
        return queue_pb2.QueueResponse(message="Track removed", queue=self.queue)

    def VoteTrack(self, request, context):
        for t in self.queue:
            if t.id == request.id:
                t.votes += 1 if request.up else -1
        self.queue.sort(key=lambda x: -x.votes)
        return queue_pb2.QueueResponse(message="Vote updated", queue=self.queue)

    def GetQueue(self, request, context):
        return queue_pb2.QueueList(queue=self.queue)

    def GetMetadata(self, request, context):
        for t in self.queue:
            if t.id == request.id:
                return t
        return queue_pb2.Track()  # empty

    def PlayNext(self, request, context):
        if not self.queue:
            return queue_pb2.Track()  # empty
        track = self.queue.pop(0)
        self.history.append(track)
        return track

    def GetHistory(self, request, context):
        return queue_pb2.QueueList(queue=self.history)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    queue_pb2_grpc.add_QueueServiceServicer_to_server(QueueServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC QueueService running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
