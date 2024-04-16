import dashscope
from dashscope import TextEmbedding

from conf.env import DASHSCOPE_KEY

dashscope.api_key = DASHSCOPE_KEY


def generate_embeddings(text):
    """
    生成文本嵌入向量

    Args:
        text (str or List[str]): 待生成嵌入向量的文本或文本列表

    Returns:
        Union[List[float], float]: 生成的嵌入向量或嵌入向量列表，如果输入为文本列表，则返回嵌入向量列表，否则返回单个嵌入向量

    """
    resp = TextEmbedding.call(
        model=TextEmbedding.Models.text_embedding_v1, input=text)
    embeddings = [record["embedding"] for record in resp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]
