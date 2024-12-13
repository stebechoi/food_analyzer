import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)

# CORS 설정 변경
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, origins=["http://localhost:3000"], 
     allow_headers=["Content-Type"],
     methods=["POST", "OPTIONS"],
     supports_credentials=True)

# 또는 더 간단하게:
# CORS(app, origins=["http://localhost:3000"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/api/analyze', methods=['POST'])
def analyze_food():
    if 'foodImage' not in request.files:
        print('이미지 파일 없음')  # 디버깅 로그
        return jsonify({'error': '이미지가 제공되지 않았습니다.'}), 400

    image = request.files['foodImage']
    
    try:
        # 이미지를 base64로 인코딩
        image_base64 = base64.b64encode(image.read()).decode('utf-8')
        
        # GPT-4 Vision API를 사용하여 이미지 분석
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "이 음식 사진을 분석하여 음식의 종류와 대략적인 영양정보(칼로리, 탄수화물, 단백질, 지방)를 알려주세요."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        analysis_result = response.choices[0].message.content
        return jsonify({'nutrition': analysis_result})

    except Exception as e:
        print(f"에러 발생: {str(e)}")  # 에러 로깅
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)