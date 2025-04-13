# from threading import Lock, RLock, Thread
# from typing import Dict, List, Callable, Any, Optional
# import time
# import uuid
# from dataclasses import dataclass
# from collections import defaultdict

# @dataclass
# class Message:
#     """Message class representing a message in the pub-sub system."""
#     topic: str
#     data: Any
#     message_id: str = None
#     timestamp: float = None
    
#     def __post_init__(self):
#         if self.message_id is None:
#             self.message_id = str(uuid.uuid4())
#         if self.timestamp is None:
#             self.timestamp = time.time()

# class TopicManager:
#     """Thread-safe topic manager with message retention"""
#     def __init__(self, max_retention=1000):
#         self._topics: Dict[str, List[Message]] = defaultdict(list)
#         self._lock = RLock()
#         self.max_retention = max_retention

#     def add_message(self, message: Message) -> int:
#         with self._lock:
#             topic_messages = self._topics[message.topic]
#             topic_messages.append(message)
            
#             # Apply retention policy
#             if len(topic_messages) > self.max_retention:
#                 del topic_messages[0]
            
#             return len(topic_messages) - 1  # Return new offset
            
#     def get_messages(self, topic: str, offset: int) -> List[Message]:
#         with self._lock:
#             if topic not in self._topics or offset < 0:
#                 return []
#             return self._topics[topic][offset:]
            
#     def get_latest_offset(self, topic: str) -> int:
#         with self._lock:
#             return len(self._topics.get(topic, [])) - 1

# class Subscriber:
#     """Thread-safe subscriber with proper synchronization"""
#     def __init__(self, subscriber_id: str, topic_manager: TopicManager):
#         self.subscriber_id = subscriber_id
#         self.topic_manager = topic_manager
#         self._lock = RLock()
#         self._active = True
#         self._subscriptions: Dict[str, int] = {}  # topic -> offset
#         self._callbacks: Dict[str, List[Callable[[Message], None]]] = defaultdict(list)
#         self._poll_thread = Thread(target=self._poll_messages, daemon=True)
#         self._poll_thread.start()

#     def subscribe(self, topic: str, callback: Callable[[Message], None], from_beginning: bool = False) -> None:
#         with self._lock:
#             offset = 0 if from_beginning else self.topic_manager.get_latest_offset(topic) + 1
#             self._subscriptions[topic] = max(offset, 0)
#             self._callbacks[topic].append(callback)

#     def unsubscribe(self, topic: str) -> None:
#         with self._lock:
#             self._subscriptions.pop(topic, None)
#             self._callbacks.pop(topic, None)

#     def _poll_messages(self) -> None:
#         while self._active:
#             with self._lock:
#                 subscriptions = list(self._subscriptions.items())
#                 callbacks = {t: list(cb) for t, cb in self._callbacks.items()}

#             for topic, offset in subscriptions:
#                 messages = self.topic_manager.get_messages(topic, offset)
#                 if not messages:
#                     continue

#                 current_callbacks = callbacks.get(topic, [])
#                 for msg in messages:
#                     for cb in current_callbacks:
#                         try:
#                             cb(msg)
#                         except Exception as e:
#                             print(f"Callback error: {e}")

#                 with self._lock:
#                     if topic in self._subscriptions:
#                         new_offset = offset + len(messages)
#                         self._subscriptions[topic] = new_offset

#             time.sleep(0.01)  # Reduced polling interval

#     def stop(self) -> None:
#         self._active = False
#         self._poll_thread.join()

# class Publisher:
#     """Thread-safe publisher implementation"""
#     def __init__(self, publisher_id: str, topic_manager: TopicManager):
#         self.publisher_id = publisher_id
#         self.topic_manager = topic_manager

#     def publish(self, topic: str, data: Any) -> int:
#         message = Message(topic=topic, data=data)
#         return self.topic_manager.add_message(message)

# class PubSubSystem:
#     """Main system with proper resource management"""
#     def __init__(self):
#         self.topic_manager = TopicManager()
#         self._lock = RLock()
#         self._publishers: Dict[str, Publisher] = {}
#         self._subscribers: Dict[str, Subscriber] = {}

#     def create_publisher(self, publisher_id: str = None) -> Publisher:
#         with self._lock:
#             pid = publisher_id or f"pub-{uuid.uuid4()}"
#             if pid in self._publishers:
#                 raise ValueError(f"Publisher {pid} exists")
#             publisher = Publisher(pid, self.topic_manager)
#             self._publishers[pid] = publisher
#             return publisher

#     def create_subscriber(self, subscriber_id: str = None) -> Subscriber:
#         with self._lock:
#             sid = subscriber_id or f"sub-{uuid.uuid4()}"
#             if sid in self._subscribers:
#                 raise ValueError(f"Subscriber {sid} exists")
#             subscriber = Subscriber(sid, self.topic_manager)
#             self._subscribers[sid] = subscriber
#             return subscriber

#     def remove_subscriber(self, subscriber_id: str) -> None:
#         with self._lock:
#             subscriber = self._subscribers.pop(subscriber_id, None)
#             if subscriber:
#                 subscriber.stop()

#     def shutdown(self) -> None:
#         with self._lock:
#             for sub in list(self._subscribers.values()):
#                 sub.stop()
#             self._subscribers.clear()
#             self._publishers.clear()


# def test_concurrent_operations():
#     system = PubSubSystem()
#     publisher = system.create_publisher("p1")
#     subscriber = system.create_subscriber("s1")
    
#     received = []
#     def callback(msg):
#         received.append(msg.data)
    
#     # Test basic operation
#     subscriber.subscribe("test", callback)
#     publisher.publish("test", "msg1")
#     publisher.publish("test", "msg2")
#     time.sleep(0.1)
#     assert received == ["msg1", "msg2"], "Basic test failed"
    
#     # Test offset reset
#     subscriber.unsubscribe("test")
#     subscriber.subscribe("test", callback, from_beginning=True)
#     publisher.publish("test", "msg3")
#     time.sleep(0.1)
#     assert received == ["msg1", "msg2", "msg1", "msg2", "msg3"], "Offset test failed"
    
#     # Test concurrent access
#     from concurrent.futures import ThreadPoolExecutor
#     with ThreadPoolExecutor() as executor:
#         for _ in range(100):
#             executor.submit(publisher.publish, "stress", "data")
    
#     time.sleep(0.2)
#     assert system.topic_manager.get_latest_offset("stress") == 99, "Concurrency test failed"
    
#     system.shutdown()
#     print("All tests passed!")

# # Comprehensive testing with edge cases
# def comprehensive_test():
#     print("\n=== Starting comprehensive PubSub testing ===")
#     pubsub = PubSubSystem()
    
#     # Message counters
#     message_counts = defaultdict(lambda: defaultdict(int))
#     received_messages = defaultdict(lambda: defaultdict(list))
    
#     def create_callback(subscriber_id, topic):
#         def callback(message):
#             message_counts[subscriber_id][topic] += 1
#             received_messages[subscriber_id][topic].append(message.data)
#             print(f"{subscriber_id} received {topic} message: {message.data}")
#         return callback
    
#     # Create publishers and subscribers
#     publisher1 = pubsub.create_publisher("pub1")
#     publisher2 = pubsub.create_publisher("pub2")
    
#     subscriber1 = pubsub.create_subscriber("sub1")
#     subscriber2 = pubsub.create_subscriber("sub2")
    
#     # Test 1: Basic publish-subscribe
#     print("\n--- Test 1: Basic publish-subscribe ---")
#     subscriber1.subscribe("topic1", create_callback("sub1", "topic1"))
#     subscriber2.subscribe("topic1", create_callback("sub2", "topic1"))
    
#     publisher1.publish("topic1", "Message 1")
#     publisher1.publish("topic1", "Message 2")
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     assert message_counts["sub1"]["topic1"] == 2, f"Expected 2 messages, got {message_counts['sub1']['topic1']}"
#     assert message_counts["sub2"]["topic1"] == 2, f"Expected 2 messages, got {message_counts['sub2']['topic1']}"
#     print("✓ Basic publish-subscribe test passed")
    
#     # Test 2: Subscribe from beginning
#     print("\n--- Test 2: Subscribe from beginning ---")
#     subscriber3 = pubsub.create_subscriber("sub3")
#     subscriber3.subscribe("topic1", create_callback("sub3", "topic1"), from_beginning=True)
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     assert message_counts["sub3"]["topic1"] == 2, f"Expected 2 messages, got {message_counts['sub3']['topic1']}"
#     print("✓ Subscribe from beginning test passed")
    
#     # Test 3: Unsubscribe
#     print("\n--- Test 3: Unsubscribe ---")
#     subscriber1.unsubscribe("topic1")
#     publisher1.publish("topic1", "Message 3")
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     assert message_counts["sub1"]["topic1"] == 2, f"Expected 2 messages, got {message_counts['sub1']['topic1']}"
#     assert message_counts["sub2"]["topic1"] == 3, f"Expected 3 messages, got {message_counts['sub2']['topic1']}"
#     assert message_counts["sub3"]["topic1"] == 3, f"Expected 3 messages, got {message_counts['sub3']['topic1']}"
#     print("✓ Unsubscribe test passed")
    
#     # Test 4: Multiple topics
#     print("\n--- Test 4: Multiple topics ---")
#     subscriber1.subscribe("topic2", create_callback("sub1", "topic2"))
#     subscriber2.subscribe("topic2", create_callback("sub2", "topic2"))
    
#     publisher2.publish("topic2", "Topic 2 - Message 1")
#     publisher1.publish("topic1", "Message 4")
#     publisher2.publish("topic2", "Topic 2 - Message 2")
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     assert message_counts["sub1"]["topic2"] == 2, f"Expected 2 messages, got {message_counts['sub1']['topic2']}"
#     assert message_counts["sub2"]["topic1"] == 4, f"Expected 4 messages, got {message_counts['sub2']['topic1']}"
#     assert message_counts["sub2"]["topic2"] == 2, f"Expected 2 messages, got {message_counts['sub2']['topic2']}"
#     print("✓ Multiple topics test passed")
    
#     # Test 5: Rapid publishing
#     print("\n--- Test 5: Rapid publishing ---")
#     for i in range(50):
#         publisher1.publish("topic3", f"Rapid message {i}")
    
#     subscriber1.subscribe("topic3", create_callback("sub1", "topic3"))
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     # New subscriber shouldn't get old messages
#     assert message_counts["sub1"]["topic3"] == 0, f"Expected 0 messages, got {message_counts['sub1']['topic3']}"
    
#     subscriber3.subscribe("topic3", create_callback("sub3", "topic3"), from_beginning=True)
    
#     # Wait for message delivery
#     time.sleep(1)
    
#     assert message_counts["sub3"]["topic3"] == 50, f"Expected 50 messages, got {message_counts['sub3']['topic3']}"
#     print("✓ Rapid publishing test passed")
    
#     # Test 6: Concurrent subscribers and publishers
#     print("\n--- Test 6: Concurrent subscribers and publishers ---")
#     topic = "concurrent"
#     num_messages = 20
#     num_subscribers = 5
    
#     # Create subscribers
#     subscribers = []
#     for i in range(num_subscribers):
#         sub_id = f"conc_sub{i}"
#         sub = pubsub.create_subscriber(sub_id)
#         sub.subscribe(topic, create_callback(sub_id, topic))
#         subscribers.append(sub)
    
#     # Create publishers and publish concurrently
#     def publish_messages(pub_id, num):
#         pub = pubsub.create_publisher(pub_id)
#         for i in range(num):
#             pub.publish(topic, f"{pub_id}-{i}")
    
#     threads = []
#     for i in range(3):
#         pub_id = f"conc_pub{i}"
#         t = Thread(target=publish_messages, args=(pub_id, num_messages))
#         threads.append(t)
#         t.start()
    
#     # Wait for all publishing to complete
#     for t in threads:
#         t.join()
    
#     # Wait for message delivery
#     time.sleep(2)
    
#     # Verify all subscribers got all messages
#     for i in range(num_subscribers):
#         sub_id = f"conc_sub{i}"
#         expected = 3 * num_messages  # 3 publishers * 20 messages each
#         assert message_counts[sub_id][topic] == expected, f"{sub_id} expected {expected} messages, got {message_counts[sub_id][topic]}"
    
#     print("✓ Concurrent subscribers and publishers test passed")
    
#     # Cleanup
#     print("\n--- Cleaning up ---")
#     pubsub.shutdown()
#     print("✓ PubSub system shut down successfully")
#     print("\n=== All tests passed successfully ===")

# if __name__ == "__main__":
#     test_concurrent_operations()
#     comprehensive_test()


from abc import ABC, abstractmethod
from typing import Any, Callable, List
from dataclasses import dataclass
import time
import uuid

@dataclass
class Message:
    """Value object representing a message"""
    topic: str
    data: Any
    message_id: str = None
    timestamp: float = None
    
    def __post_init__(self):
        self.message_id = self.message_id or str(uuid.uuid4())
        self.timestamp = self.timestamp or time.time()

class IMessageStore(ABC):
    """Interface for message storage"""
    @abstractmethod
    def store_message(self, message: Message) -> int:
        pass
    
    @abstractmethod
    def get_messages(self, topic: str, offset: int) -> List[Message]:
        pass
    
    @abstractmethod
    def get_latest_offset(self, topic: str) -> int:
        pass

class IPublisher(ABC):
    """Interface for publisher"""
    @abstractmethod
    def publish(self, topic: str, data: Any) -> int:
        pass

class ISubscriber(ABC):
    """Interface for subscriber"""
    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[Message], None], from_beginning: bool = False) -> None:
        pass
    
    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass

class IPubSubSystem(ABC):
    """Interface for the main PubSub system"""
    @abstractmethod
    def create_publisher(self, publisher_id: str = None) -> IPublisher:
        pass
    
    @abstractmethod
    def create_subscriber(self, subscriber_id: str = None) -> ISubscriber:
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        pass

from threading import Lock, RLock, Thread
from collections import defaultdict
from typing import Dict, List, Callable, Any
import time


class InMemoryMessageStore(IMessageStore):
    """Concrete implementation of message storage using in-memory storage"""
    def __init__(self, max_retention: int = 1000):
        self._topics: Dict[str, List[Message]] = defaultdict(list)
        self._lock = RLock()
        self.max_retention = max_retention

    def store_message(self, message: Message) -> int:
        with self._lock:
            topic_messages = self._topics[message.topic]
            topic_messages.append(message)
            
            if len(topic_messages) > self.max_retention:
                del topic_messages[0]
            
            return len(topic_messages) - 1

    def get_messages(self, topic: str, offset: int) -> List[Message]:
        with self._lock:
            if topic not in self._topics or offset < 0:
                return []
            return self._topics[topic][offset:]

    def get_latest_offset(self, topic: str) -> int:
        with self._lock:
            return len(self._topics.get(topic, [])) - 1

class ConcretePublisher(IPublisher):
    """Concrete implementation of Publisher"""
    def __init__(self, publisher_id: str, message_store: IMessageStore):
        self.publisher_id = publisher_id
        self._message_store = message_store

    def publish(self, topic: str, data: Any) -> int:
        message = Message(topic=topic, data=data)
        return self._message_store.store_message(message)

class ConcreteSubscriber(ISubscriber):
    """Concrete implementation of Subscriber"""
    def __init__(self, subscriber_id: str, message_store: IMessageStore):
        self.subscriber_id = subscriber_id
        self._message_store = message_store
        self._lock = RLock()
        self._active = True
        self._subscriptions: Dict[str, int] = {}
        self._callbacks: Dict[str, List[Callable[[Message], None]]] = defaultdict(list)
        self._poll_thread = Thread(target=self._poll_messages, daemon=True)
        self._poll_thread.start()

    def subscribe(self, topic: str, callback: Callable[[Message], None], from_beginning: bool = False) -> None:
        with self._lock:
            offset = 0 if from_beginning else self._message_store.get_latest_offset(topic) + 1
            self._subscriptions[topic] = max(offset, 0)
            self._callbacks[topic].append(callback)

    def unsubscribe(self, topic: str) -> None:
        with self._lock:
            self._subscriptions.pop(topic, None)
            self._callbacks.pop(topic, None)

    def _poll_messages(self) -> None:
        while self._active:
            try:
                with self._lock:
                    subscriptions = dict(self._subscriptions)
                    callbacks = {t: list(cb) for t, cb in self._callbacks.items()}

                for topic, offset in subscriptions.items():
                    messages = self._message_store.get_messages(topic, offset)
                    if messages:
                        for msg in messages:
                            for cb in callbacks.get(topic, []):
                                try:
                                    cb(msg)
                                except Exception as e:
                                    print(f"Callback error in {self.subscriber_id}: {e}")

                        with self._lock:
                            if topic in self._subscriptions:
                                self._subscriptions[topic] = offset + len(messages)

                time.sleep(0.01)
            except Exception as e:
                print(f"Error in polling thread of {self.subscriber_id}: {e}")

    def stop(self) -> None:
        self._active = False
        if hasattr(self, '_poll_thread'):
            self._poll_thread.join(timeout=1.0)




class PubSubSystem(IPubSubSystem):
    """Main PubSub system implementation"""
    def __init__(self, message_store: IMessageStore = None):
        self._message_store = message_store or InMemoryMessageStore()
        self._lock = RLock()
        self._publishers: Dict[str, IPublisher] = {}
        self._subscribers: Dict[str, ISubscriber] = {}

    def create_publisher(self, publisher_id: str = None) -> IPublisher:
        with self._lock:
            pid = publisher_id or f"pub-{uuid.uuid4()}"
            if pid in self._publishers:
                raise ValueError(f"Publisher {pid} already exists")
            publisher = ConcretePublisher(pid, self._message_store)
            self._publishers[pid] = publisher
            return publisher

    def create_subscriber(self, subscriber_id: str = None) -> ISubscriber:
        with self._lock:
            sid = subscriber_id or f"sub-{uuid.uuid4()}"
            if sid in self._subscribers:
                raise ValueError(f"Subscriber {sid} already exists")
            subscriber = ConcreteSubscriber(sid, self._message_store)
            self._subscribers[sid] = subscriber
            return subscriber

    def shutdown(self) -> None:
        with self._lock:
            for subscriber in self._subscribers.values():
                subscriber.stop()
            self._subscribers.clear()
            self._publishers.clear()

class MessageTracker:
    def __init__(self):
        self.message_counts = defaultdict(lambda: defaultdict(int))
        self.received_messages = defaultdict(lambda: defaultdict(list))

    def create_callback(self, subscriber_id: str, topic: str):
        def callback(message: Message):
            self.message_counts[subscriber_id][topic] += 1
            self.received_messages[subscriber_id][topic].append(message.data)
            print(f"{subscriber_id} received {topic} message: {message.data}")
        return callback

def test_comprehensive(pubsub: PubSubSystem):
    """Comprehensive test covering all aspects of the PubSub system"""
    print("\n=== Starting comprehensive PubSub testing ===")
    tracker = MessageTracker()
    
    # Test 1: Basic publish-subscribe
    print("\n--- Test 1: Basic publish-subscribe ---")
    publisher1 = pubsub.create_publisher("pub1")
    publisher2 = pubsub.create_publisher("pub2")
    
    subscriber1 = pubsub.create_subscriber("sub1")
    subscriber2 = pubsub.create_subscriber("sub2")
    
    subscriber1.subscribe("topic1", tracker.create_callback("sub1", "topic1"))
    subscriber2.subscribe("topic1", tracker.create_callback("sub2", "topic1"))
    
    publisher1.publish("topic1", "Message 1")
    publisher2.publish("topic1", "Message 2")
    
    time.sleep(1)  # Wait for message delivery
    
    assert tracker.message_counts["sub1"]["topic1"] == 2
    assert tracker.message_counts["sub2"]["topic1"] == 2
    print("✓ Basic publish-subscribe test passed")
    
    # Test 2: Subscribe from beginning
    print("\n--- Test 2: Subscribe from beginning ---")
    subscriber3 = pubsub.create_subscriber("sub3")
    subscriber3.subscribe("topic1", tracker.create_callback("sub3", "topic1"), from_beginning=True)
    
    time.sleep(1)
    
    assert tracker.message_counts["sub3"]["topic1"] == 2
    print("✓ Subscribe from beginning test passed")
    
    # Test 3: Unsubscribe
    print("\n--- Test 3: Unsubscribe ---")
    subscriber1.unsubscribe("topic1")
    publisher1.publish("topic1", "Message 3")
    
    time.sleep(1)
    
    assert tracker.message_counts["sub1"]["topic1"] == 2  # Should not receive new message
    assert tracker.message_counts["sub2"]["topic1"] == 3  # Should receive new message
    assert tracker.message_counts["sub3"]["topic1"] == 3  # Should receive new message
    print("✓ Unsubscribe test passed")
    
    # Test 4: Multiple topics
    print("\n--- Test 4: Multiple topics ---")
    subscriber1.subscribe("topic2", tracker.create_callback("sub1", "topic2"))
    subscriber2.subscribe("topic2", tracker.create_callback("sub2", "topic2"))
    
    publisher2.publish("topic2", "Topic 2 - Message 1")
    publisher1.publish("topic1", "Message 4")
    publisher2.publish("topic2", "Topic 2 - Message 2")
    
    time.sleep(1)
    
    assert tracker.message_counts["sub1"]["topic2"] == 2
    assert tracker.message_counts["sub2"]["topic1"] == 4
    assert tracker.message_counts["sub2"]["topic2"] == 2
    print("✓ Multiple topics test passed")
    
    # Test 5: Concurrent operations
    print("\n--- Test 5: Concurrent operations ---")
    topic = "concurrent"
    num_messages = 20
    num_subscribers = 5
    num_publishers = 3
    
    # Create subscribers
    subscribers = []
    for i in range(num_subscribers):
        sub_id = f"conc_sub{i}"
        sub = pubsub.create_subscriber(sub_id)
        sub.subscribe(topic, tracker.create_callback(sub_id, topic))
        subscribers.append(sub)
    
    # Create publishers and publish concurrently
    def publish_messages(pub_id: str, num: int):
        pub = pubsub.create_publisher(pub_id)
        for i in range(num):
            pub.publish(topic, f"{pub_id}-{i}")
    
    threads = []
    for i in range(num_publishers):
        pub_id = f"conc_pub{i}"
        t = Thread(target=publish_messages, args=(pub_id, num_messages))
        threads.append(t)
        t.start()
    
    # Wait for publishing to complete
    for t in threads:
        t.join()
    
    # Allow time for message delivery
    time.sleep(2)
    
    # Verify all subscribers got all messages
    expected_messages = num_publishers * num_messages
    for i in range(num_subscribers):
        sub_id = f"conc_sub{i}"
        assert tracker.message_counts[sub_id][topic] == expected_messages, \
            f"{sub_id} expected {expected_messages} messages, got {tracker.message_counts[sub_id][topic]}"
    
    print("✓ Concurrent operations test passed")
    print("\n=== All tests passed successfully ===")

if __name__ == "__main__":
    pubsub = PubSubSystem()
    try:
        test_comprehensive(pubsub)
    finally:
        pubsub.shutdown()