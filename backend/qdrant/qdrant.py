# Create your views here.
from qdrant_client.models import VectorParams, Distance, PointStruct

from application.settings import QDRANT


class QdrantService:
    def __init__(self):
        self._host = QDRANT.get("HOST")
        self._port = QDRANT.get("PORT")
        self.collection_name = QDRANT.get("COLLECTION_NAME")
        # self._key = QDRANT.get("KEY")
        # self._host = "192.168.3.11"
        # self._port = 6334
        # self.collection_name = "education"
        self._enable_grpc = QDRANT.get("PREFER_GRPC")
        self._client = self.__init_client()

    def __init_client(self):
        from qdrant_client import QdrantClient
        client = QdrantClient(
            host=self._host, port=self._port, prefer_grpc=self._enable_grpc)
        return client

    def create_collection(self, collection_name: str) -> bool:
        return self._client.create_collection(collection_name=collection_name,
                                              vectors_config=VectorParams(
                                                  size=1536, distance=Distance.COSINE),
                                              )

    def list_collection(self):
        return self._client.get_collections()

    def delete_collection(self, collection_name: str) -> bool:
        return self._client.delete_collection(collection_name)

    def insert_points(self, points: list, wait: bool = False):
        return self._client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=wait,
        )

    def insert_point(self, point: PointStruct, wait: bool = False):
        return self._client.upsert(
            collection_name=self.collection_name,
            points=[
                point,
            ],
            wait=wait,
        )

    def search(self, query: list, limit: int = 5, with_payload: bool = True):
        return self._client.search(collection_name=self.collection_name,
                                   query_vector=query,
                                   limit=limit,
                                   with_payload=with_payload,
                                   )
