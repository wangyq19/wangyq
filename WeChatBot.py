from openai import OpenAI
from wxauto import WeChat
import time


class WeChatBot:
    def __init__(self):
        self.client = OpenAI(api_key="sk-78dc6d1cef8e4137b91f889615014fb1", base_url="https://api.deepseek.com/v1")
        self.wx = WeChat()
        self.listen_list = [
            # "haha",
            "sky"
        ]
        for whoItem in self.listen_list:
            self.wx.AddListenChat(who=whoItem)

    def __ask(self, msg):

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": """萌哥，假设你是一个高情商全能男友，性格风趣幽默，
                你的任务是对话过程中让她对你产生好感，不要让她感觉你是人机，不要过于油腻，语言要正常一些，如有表情要符合微信规范，每段对话不超过20个字"""},
                {"role": "user", "content": msg},
            ],
            stream=False
        )
        return response.choices[0].message.content

    def run(self):
        wait = 5  # 设置两秒查看一次是否有新消息
        while True:
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                msg = msgs.get(chat)
                for item in msg:
                    if item.type == "friend":
                        reply = self.__ask(item.content)
                        print(f"接受【{item.sender}】的消息：{item.content}")
                        print(f"回复【{item.sender}】的消息：{reply}")
                        chat.SendMsg(reply)
            time.sleep(wait)


if __name__ == "__main__":
    bot = WeChatBot()
    bot.run()
