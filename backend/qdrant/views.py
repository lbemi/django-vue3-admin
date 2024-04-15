from qdrant.qdrant import QdrantService


def search_qdrant(query: list, limit: int = 5, with_payload: bool = True) -> list:
    """
    搜索qdrant
    :param query:
    :param limit:
    :param with_payload:
    :return:
    """
    qdrant = QdrantService()
    return qdrant.search(query=query, limit=limit, with_payload=with_payload)


def insert_qdrant(points: list, wait: bool = False) -> bool:
    """
    插入qdrant
    :param points:
    :param wait:
    :return:
    """
    qdrant = QdrantService()
    return qdrant.insert_points(points=points, wait=wait)
