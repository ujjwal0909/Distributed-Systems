import grpc
import queue_pb2
import queue_pb2_grpc
import sys

def main():
    # Test sync by adding to one node and checking another
    node1 = sys.argv[1] if len(sys.argv) > 1 else 'queue-service1:50051'
    node2 = sys.argv[2] if len(sys.argv) > 2 else 'queue-service2:50051'
    channel1 = grpc.insecure_channel(node1)
    stub1 = queue_pb2_grpc.QueueServiceStub(channel1)
    channel2 = grpc.insecure_channel(node2)
    stub2 = queue_pb2_grpc.QueueServiceStub(channel2)


    # Add a track to node1
    track = queue_pb2.Track(id="103", title="SyncSong", artist="Syncer", votes=0)
    stub1.AddTrack(track)


    # Check queue on node2
    queue = stub2.GetQueue(queue_pb2.Empty())
    assert any(t.id == "103" for t in queue.queue), "Track not synced to node2"
    print("test_sync: PASS")

if __name__ == '__main__':
    main()
