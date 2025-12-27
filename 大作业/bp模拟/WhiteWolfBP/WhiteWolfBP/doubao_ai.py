# 文件名: doubao_ai.py
import os
from volcenginesdkarkruntime import Ark

# 使用你提供的 API Key
client = Ark(
    api_key="50fcde62-d03f-4bdb-9d02-91481829504c",
    timeout=60, # 设置60秒超时，避免网络卡顿时程序无响应
)

def get_ai_commentary(prompt_text):
    """
    接收一个提示，返回豆包AI的回答
    """
    try:
        print("正在向豆包方舟API发送请求 (模型: doubao-seed-1-6-flash)...")
        
        # 使用 client.chat.completions.create 方法
        response = client.chat.completions.create(
            model="doubao-seed-1-6-flash-250828",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位专业的KPL王者荣耀赛事解说。你的任务是根据当前的BP情况，用简洁、专业的语言进行分析和评论。不要说“你好”等多余的话，直接开始解说。"
                },
                {
                    "role": "user", 
                    "content": prompt_text
                }
            ],
        )
        
        print("成功收到AI回复。")
        # 返回AI生成的文本内容
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        print(f"调用豆包API时出错: {error_msg}")
        
        # 【新增】针对常见错误的友好中文提示
        if "429" in error_msg or "LimitExceeded" in error_msg:
            return "【AI解说暂停】: 账户免费额度已耗尽或触发限流，请前往火山引擎控制台查看“安心体验”设置。"
        elif "401" in error_msg:
            return "【AI解说暂停】: API Key 认证失败，请检查密钥是否过期。"
        elif "404" in error_msg:
            return "【AI解说暂停】: 找不到指定的模型 ID，请检查模型名称是否正确。"
            
        # 返回通用错误信息，防止程序崩溃
        return f"AI解说暂时无法连接 ({error_msg})"