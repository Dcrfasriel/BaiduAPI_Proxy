"""
本地服务转接程序
接收GET请求，验证key后转发搜索请求至百度服务器
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 百度API配置
BAIDU_API_URL = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"
BAIDU_API_TOKEN = "bce-v3/ALTAK-D0MCtmD3GyGImn4dwpQds/6200d9d4ded86cec825bcaeaba49b8dacb547f57"

# 读取本地key
def load_key():
    """从key.txt文件读取密钥"""
    key_file_path = os.path.join(os.path.dirname(__file__), 'key.txt')
    try:
        with open(key_file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"读取密钥文件失败: {e}")
        return None

# 验证key
def verify_key(input_key):
    """验证输入的key是否与文件中的key一致"""
    stored_key = load_key()
    if stored_key is None:
        return False
    return input_key == stored_key

# 转换百度响应为指定格式
def convert_to_qa_format(search_content, baidu_response):
    """
    将百度API响应转换为 [{q:'问题',a:'回答'}] 格式
    """
    try:
        # 提取百度返回的内容
        if isinstance(baidu_response.get('content'), dict):
            response_content = baidu_response['content']
            
            # 尝试从不同可能的字段提取回答内容
            answer = ""
            
            # 处理百度AI搜索的references格式
            if 'references' in response_content and isinstance(response_content['references'], list):
                # 提取所有引用的内容并合并
                contents = []
                for ref in response_content['references'][:3]:  # 只取前3个引用
                    if 'content' in ref:
                        # 清理内容，去除过多的Unicode转义
                        content = ref['content'].strip()
                        if content:
                            title = ref.get('title', '').strip()
                            source = ref.get('website', '').strip()
                            # 格式化单个引用
                            ref_text = f"【{title}】\n{content}"
                            if source:
                                ref_text += f"\n来源：{source}"
                            contents.append(ref_text)
                
                if contents:
                    answer = "\n\n".join(contents)
                else:
                    answer = "未找到相关内容"
            
            # 如果有result字段
            elif 'result' in response_content:
                answer = response_content['result']
            # 如果有choices字段(类似OpenAI格式)
            elif 'choices' in response_content and len(response_content['choices']) > 0:
                choice = response_content['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    answer = choice['message']['content']
                elif 'text' in choice:
                    answer = choice['text']
            # 如果直接有content字段
            elif 'content' in response_content:
                answer = response_content['content']
            # 如果有answer字段
            elif 'answer' in response_content:
                answer = response_content['answer']
            else:
                # 如果找不到标准字段,返回简化的响应信息
                answer = f"获取到响应，但格式不符合预期。request_id: {response_content.get('request_id', 'N/A')}"
            
            return [{
                "q": search_content,
                "a": answer
            }]
        else:
            return [{
                "q": search_content,
                "a": str(baidu_response.get('content', ''))
            }]
    except Exception as e:
        return [{
            "q": search_content,
            "a": f"解析响应失败: {str(e)}"
        }]

# 发送搜索请求到百度
def send_baidu_search(search_content):
    """发送POST请求到百度AI搜索服务"""
    headers = {
        "Authorization": f"Bearer {BAIDU_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {
                "content": search_content,
                "role": "user"
            }
        ],
        "search_source": "baidu_search_v2"
    }
    
    try:
        response = requests.post(BAIDU_API_URL, json=payload, headers=headers, timeout=30)
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text
        }
    except requests.exceptions.Timeout:
        return {
            "error": "请求超时",
            "status_code": 408
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"请求失败: {str(e)}",
            "status_code": 500
        }
    except Exception as e:
        return {
            "error": f"未知错误: {str(e)}",
            "status_code": 500
        }

@app.route('/search', methods=['GET'])
def search():
    """
    处理搜索请求
    参数:
        - search: 搜索内容
        - key: 验证密钥
    """
    # 获取请求参数
    search_content = request.args.get('search')
    input_key = request.args.get('key')
    
    # 参数验证
    if not search_content:
        return jsonify({
            "success": False,
            "error": "缺少search参数"
        }), 400
    
    if not input_key:
        return jsonify({
            "success": False,
            "error": "缺少key参数"
        }), 400
    
    # 验证key
    if not verify_key(input_key):
        return jsonify({
            "success": False,
            "error": "密钥验证失败"
        }), 403
    
    # 发送搜索请求
    result = send_baidu_search(search_content)
    
    # 返回结果
    if "error" in result:
        return jsonify([{
            "q": search_content,
            "a": f"错误: {result['error']}"
        }]), result.get("status_code", 500)
    else:
        # 转换为指定格式
        qa_format = convert_to_qa_format(search_content, result)
        return jsonify(qa_format), 200

@app.route('/', methods=['GET'])
def index():
    """首页信息"""
    return jsonify({
        "service": "百度搜索转接服务",
        "version": "1.0",
        "usage": "GET /search?search=<搜索内容>&key=<密钥>",
        "status": "running"
    })

@app.route('/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "key_file_exists": load_key() is not None
    })

if __name__ == '__main__':
    # 启动Flask服务
    # 支持云平台部署：从环境变量获取端口
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("百度搜索转接服务已启动")
    print(f"访问地址: http://localhost:{port}")
    print(f"使用方法: http://localhost:{port}/search?search=<搜索内容>&key=<密钥>")
    print("=" * 50)
    
    # 生产环境关闭debug模式
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
