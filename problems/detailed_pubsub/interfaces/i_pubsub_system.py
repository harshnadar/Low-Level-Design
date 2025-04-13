from abc import ABC, abstractmethod
from problems.detailed_pubsub.interfaces.i_publisher import IPublisher
from problems.detailed_pubsub.interfaces.i_subscriber import ISubscriber


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