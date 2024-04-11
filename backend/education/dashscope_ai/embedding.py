import dashscope
from dashscope import TextEmbedding

from conf.env import DASHSCOPE_KEY

dashscope.api_key = DASHSCOPE_KEY


def generate_embeddings(text):
    resp = TextEmbedding.call(model=TextEmbedding.Models.text_embedding_v1, input=text)

    embeddings = [record["embedding"] for record in resp.output['embeddings']]
    return embeddings if isinstance(text, list) else embeddings[0]


print(generate_embeddings("hello"))
