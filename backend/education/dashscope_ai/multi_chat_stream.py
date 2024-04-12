import uuid
from http import HTTPStatus

import dashscope
from dashscope import Generation

from conf.env import DASHSCOPE_KEY

dashscope.api_key = DASHSCOPE_KEY


class DialogueManager:
    def __init__(self, user_id):
        self.history = []
        self.uuid = uuid.uuid4()
        self.user_id = user_id

    def get_history(self):
        return self.history

    def add_history(self, message: list):
        # 两个数组拼接
        self.history.extend(message)

    def chat(self, message: str):
        messages = [{'role': 'user', 'content': message}]
        self.add_history(messages)
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
            print("结束。。。。。", self.uuid, self.history)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# if __name__ == '__main__':
#     dialogue_manager = DialogueManager(1)
#     messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
#                 {'role': 'user', 'content': '如何做西红柿炖牛腩？'}]
#     dialogue_manager.chat(messages)
#     dialogue_manager.chat([{'role': 'user', 'content': '夏天可以吃什么？'}])
