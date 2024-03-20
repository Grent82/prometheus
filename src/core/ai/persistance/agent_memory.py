import pymongo
from datetime import datetime

from src.core.id_types import GameId

class AgentMemory:
    def __init__(self, host='localhost', port=27027, db_name='memories'):
        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.db = self.client[db_name]
        self.conversation_collection = self.db["conversations"]
        self.memory_collection = self.db["memories"]
        self.embedding_collection = self.db["embeddings"]



    def insert(self, playerId:GameId, description:str, embeddingId:GameId, conversationId:GameId, memoryId:GameId):
        memory_document = {
            "playerId": playerId.id,
            "description": description,
            "embeddingId": embeddingId.id,
            "importance": self._calculateImportance(),
            "lastAccess": int(datetime.now().timestamp()),
            "data": {
                "relationship": {
                    "playerId": playerId.id
                },
                "conversation": {
                    "conversationId": conversationId.id,
                    "playerIds": [playerId.id]
                },
                "reflection": {
                    "relatedMemoryIds": [memoryId]
                }
            }
        }
        self.conversation_collection.insert_one(memory_document);

    def _calculateImportance(self) -> float:
        pass
