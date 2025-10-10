import grpc
import queue_pb2
import queue_pb2_grpc

# Example: Add a track, get queue, play next

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = queue_pb2_grpc.QueueServiceStub(channel)

    # Add a track
    track = queue_pb2.Track(id=1, title="Song A", artist="Artist A", duration=180, votes=0)
    response = stub.AddTrack(track)
    print("AddTrack response:", response)

    # Get queue
    queue = stub.GetQueue(queue_pb2.Empty())
    print("Current queue:", queue)

    # Play next
    now_playing = stub.PlayNext(queue_pb2.Empty())
    print("Now playing:", now_playing)

    # Get history
    history = stub.GetHistory(queue_pb2.Empty())
    print("Playback history:", history)

if __name__ == '__main__':
    run()
