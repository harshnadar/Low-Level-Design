from typing import List, Set

class Group:
    def __init__(self, group_id: str, name: str, members: List[str]):
        self.group_id = group_id
        self.name = name
        self.members: Set[str] = set(members)
    
    def add_member(self, user_id: str):
        self.members.add(user_id)
    
    def remove_member(self, user_id: str):
        if user_id in self.members:
            self.members.remove(user_id)
    
    def is_member(self, user_id: str) -> bool:
        return user_id in self.members