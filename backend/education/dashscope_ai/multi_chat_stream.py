from http import HTTPStatus

import dashscope
from dashscope import Generation

from conf.env import DASHSCOPE_KEY
from education.dashscope_ai.embedding import generate_embeddings
from education.models import Question
from qdrant.qdrant import QdrantService

dashscope.api_key = DASHSCOPE_KEY


class DialogueManager:
    def __init__(self, user_id, uuid):
        self.history = []
        self.uuid = uuid
        self.user_id = user_id

    def get_history(self):
        return self.history

    def add_history(self, message: list):
        # 两个数组拼接
        self.history.extend(message)

    def set_assistant(self, message: str):
        messages = [{'role': 'system', 'content': message}]
        self.add_history(messages)

    def chat(self, message: str):
        messages = [{'role': 'user', 'content': message}]
        self.add_history(messages)
        print("开始。。。。。数据：  ", self.uuid, self.history)
        try:
            response = Generation.call("qwen-turbo",
                                       messages=self.history,
                                       result_format='message',
                                       stream=True,
                                       incremental_output=True)
            collected_content = ''
            last_role = ''
            for res in response:
                if res.status_code == HTTPStatus.OK and res.output and res.output.choices:
                    choice = res.output.choices[0]
                    if 'message' in choice and 'content' in choice['message']:
                        content = choice['message']['content']
                        role = choice['message'].get('role', '')
                        print(content, end='')
                        collected_content += content
                        last_role = role
                        yield content
                    else:
                        print("Unexpected response format.")
                else:
                    print('Request failed with id: %s, Status code: %s, error code: %s, error message: %s' % (
                        res.request_id if hasattr(res, 'request_id') else '',
                        res.status_code if hasattr(res, 'status_code') else '',
                        res.code if hasattr(res, 'code') else '',
                        res.message if hasattr(res, 'message') else ''
                    ))
            self.add_history([{'role': last_role, 'content': collected_content}])
            # 入库
            self.insert_question(message, collected_content)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def insert_question(self, question: str, answer: str):
        print("数据入库。。。。")
        Question.objects.create(question_uuid=self.uuid, question=question, creator_id=self.user_id,
                                answer=answer,
                                )


def search_similar_questions(query: str, score: float = 0.8):
    result = []
    vec = generate_embeddings(query)
    if 0 == len(vec):
        return result
    # 搜索相似问题
    points = QdrantService().search(vec, limit=5, with_payload=True)
    for point in points:
        if point.score > score:
            result.append(point)

    return result