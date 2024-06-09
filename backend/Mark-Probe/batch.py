import shutil
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import wave
import os
from tools.encode import encoderapi
from tools.decode import decoderapi
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dateutil.relativedelta import relativedelta 
import secrets
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.utils import secure_filename
from textstega import encodeStr,decodeStr
import zipfile
import tempfile
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/batch/text/steg', methods=['POST'])
def handle_batch_text_steg():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        secret_message = request.form.get('content')  # 获取表单中的文本内容
        
        if not files or not secret_message:
            return jsonify({'error': 'Invalid request, files or content missing'}),200

        with tempfile.TemporaryDirectory() as temp_dir:
            encoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)
                    
                    # 读取文件内容和执行隐写编码
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    encoded_content = encodeStr(file_content, secret_message)
                    
                    encoded_file_path = os.path.join(temp_dir, filename)
                    with open(encoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(encoded_content)
                    
                    encoded_file_paths.append(encoded_file_path)
                    
                    # 清理临时文件
                    os.remove(file_path)
            
            # 将所有编码后的文件打包成一个压缩文件
            zip_filename = "encoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in encoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200



@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['TEMP_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
