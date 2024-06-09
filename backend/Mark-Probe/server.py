import io
import random
import shutil
import string
import time
from flask import Flask, request, jsonify, send_file, send_from_directory, session
from flask_cors import CORS
import base64
import wave
import os
from tools.encode import encoderapi
from tools.decode import decoderapi, getuid
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
from captcha.image import ImageCaptcha
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/nossdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)


scapt = {} # 用于验证码验证
UPLOAD_FOLDER = 'weight'
ALLOWED_EXTENSIONS = {'pth', 'pt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_FOLDER'] = 'temp'

db = SQLAlchemy(app)

class NossUser(db.Model):
    __tablename__ = 'nossuser'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    noss_points = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='user')
    membership_expiration = db.Column(db.DateTime)

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Model {self.name}>"


with app.app_context():
    db.create_all()

@app.route('/eaudio',methods=['POST'])
def handle_audio():
    try:
        audio = request.files.get('audio')
        text = request.form.get('text')
        audio.save(audio.filename)
        res=''
        if audio.filename.split('.')[1] != "wav":
            res=audio.filename.split('.')[0]+'.wav'
            cmdls="echo y | ffmpeg -i "+audio.filename+" -acodec pcm_s16le -ac 2 -ar 44100 "+res
            os.system(cmdls)
        print(audio.filename)
        if res=='':
            res=audio.filename
        song = wave.open(res, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        string=text
        string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)
        with wave.open("embed_"+audio.filename, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()
        with open("embed_"+audio.filename, 'rb') as f:
            audio_bytes = f.read()
        encoded_string = base64.b64encode(audio_bytes)
        return jsonify({'message':'success','audio':str(encoded_string)})
    except Exception as e:
        return jsonify({'message':str(e)})

@app.route('/deaudio',methods=['POST'])
def handle_deaudio():
    try:
        audio = request.files.get('audio')
        audio.save(audio.filename)
        song = wave.open(audio.filename, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        decoded = string.split("###")[0]
        print("Sucessfully decoded: "+decoded)
        song.close()
        return jsonify({'message':'success','text':decoded})
    except Exception as e:
        return jsonify({'message':str(e)})

@app.route('/evideo',methods=['POST'])
def handle_evideo():
    try:
        video = request.files.get('video')
        print(video)
        video.save(video.filename)
        return jsonify({'message':'success'})
    except Exception as e:
        return jsonify({'message':str(e)})



@app.route('/encrypt', methods=['POST'])
def handle_excrpt():
    try:
        img = request.files.get('image')
        print(img)
        text = request.form.get('text')
        print(text)
        suffix=img.filename.split('.')[1]
        imgname='input.'+suffix
        img.save(imgname)
        encoderapi(imgname,'weight/latest-0.pth','outimg',text,'encoded.jpg')
        with open('outimg/encoded.jpg', 'rb') as f:
            outimg = f.read()
        encoded_string = base64.b64encode(outimg)
        return jsonify({'result': 'success', 'img': str(encoded_string)})
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)})


@app.route('/decoimg',methods=['POST'])
def handle_decoimg():
    try:
        img = request.files.get('image')
        suffix=img.filename.split('.')[1]
        imgname='input.'+suffix
        img.save(imgname)
        restext=decoderapi(imgname,'weight/latest-0.pth','cpu')
        return jsonify({'result':'success','text':restext})
    except Exception as e:
        return jsonify({'result':'error','message':str(e)})
    

@app.route('/register', methods=['POST'])
def register():
    try:
        hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        new_user = NossUser(username=request.form.get('username'), password=hashed_password, email=request.form.get('email'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message':'Fail to register!'}),200

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = NossUser.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Fail to login!'}), 200
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)

        # 创建Token
        token = jwt.encode({
            'user_id': user.user_id, 
            'exp': exp_time
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Login successful!', 'token': token}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Fail to login!'}), 200
    

@app.route('/validate', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 200

    try:
        # 从 Authorization 头中提取 token，前缀是 'Bearer'
        if token.startswith('Bearer '):
            token = token[7:] 
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Token is valid!', 'user_id': data['user_id']}), 200
    except ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 200
    except InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Something went wrong!'}), 200
    
@app.route('/getuinfo', methods=['POST'])
def get_user_info():
    try:
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({'message': 'User ID is required'}), 200

        user = NossUser.query.filter_by(user_id=user_id).first()
        memExp = ''
        if user.membership_expiration==None or user.membership_expiration=='':
            memExp= ''
        else:
            memExp=user.membership_expiration.strftime('%Y/%m/%d')
        if user:
            user_info = {
                'username': user.username,
                'noss_points': user.noss_points,
                'role': user.role,
                'membership_expiration': memExp
            }
            return jsonify({'message': 'User found', 'user_info': user_info}), 200
        else:
            return jsonify({'message': 'User not found'}), 200
    except Exception as e:

        return jsonify({'message': str(e)}), 200

@app.route('/topup', methods=['POST'])
def topup():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        points = data.get('points')

        if not user_id or points is None:
            return jsonify({'success': False, 'message': 'User ID and points are required'}), 200

        user = NossUser.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 200

        user.noss_points = points
        db.session.commit()

        return jsonify({'success': True, 'message': 'Points successfully topped up!', 'new_points': user.noss_points}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 200
    
@app.route('/topup/vip', methods=['POST'])
def handleTopupVip():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        points = data.get('points')
        months = data.get('expiration')

        if not user_id or points is None or months is None:
            return jsonify({'success': False, 'message': 'User ID and points and months are required'}), 200

        user = NossUser.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 200

        user.noss_points = points  
        user.role = 'vip' 
        new_expiration_date = datetime.datetime.utcnow() + relativedelta(months=+int(months))
        user.membership_expiration = new_expiration_date
        db.session.commit()

        formatted_expiration_date = new_expiration_date.strftime('%Y/%m/%d')
        return jsonify({
            'success': True,
            'message': 'VIP membership successfully renewed!',
            'new_points': user.noss_points,
            'new_role': user.role,
            'membership_expiration': formatted_expiration_date,
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 200
    
@app.route('/setuser', methods=['POST'])
def set_user():
    data = request.get_json()  

    ex_date = '1970/01/01'
    if data['membershipExpiration']:
       ex_date = data['membershipExpiration']
  
    if not all(key in data for key in ['username', 'password', 'email', 'nossPoints', 'role']):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 200


    if NossUser.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'User already exists'}), 200

    try:
        
        new_user = NossUser(
            username=data['username'],
            password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
            email=data['email'],
            noss_points=data['nossPoints'],
            role=data['role'],
            membership_expiration=datetime.datetime.strptime(ex_date, '%Y/%m/%d')
        )


        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User added successfully', 'user_id': new_user.user_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error adding user', 'error': str(e)}), 200


@app.route('/getuser', methods=['GET'])
def get_user():
    try:
        users = NossUser.query.all()
        user_list = [{
            'id': user.user_id,
            'username': user.username,
            'email': user.email,
            'nossPoints': user.noss_points,
            'role': user.role,
            'membershipExpiration': user.membership_expiration.strftime('%Y/%m/%d') if user.membership_expiration else None
        } for user in users]

        return jsonify({'success': True, 'users': user_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error fetching users', 'error': str(e)}), 500

@app.route('/updateuser', methods=['POST'])
def update_user():
    data = request.get_json()
    user_id = data.get('id')

    if not user_id:
        return jsonify({'success': False, 'message': 'User ID is required'}), 200

    user = NossUser.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 200

    try:
        # 更新用户信息，仅更新提供了新值的字段
        username = data.get('username')
        if username:
            user.username = username

        email = data.get('email')
        if email:
            user.email = email

        password = data.get('password')
        if password:
            user.password = generate_password_hash(password, method='pbkdf2:sha256')

        noss_points = data.get('nossPoints')
        if noss_points is not None:
            user.noss_points = noss_points

        role = data.get('role')
        if role:
            user.role = role

        membership_expiration = data.get('membershipExpiration')
        if membership_expiration:
            user.membership_expiration = datetime.datetime.strptime(membership_expiration, '%Y/%m/%d')

        db.session.commit()
        return jsonify({'success': True, 'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update user', 'error': str(e)}), 200


@app.route('/deleteuser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = NossUser.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 200

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to delete user', 'error': str(e)}), 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upmodel', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 200
    file = request.files['file']
    category = request.form.get('type', 'iorv')
    model_name = request.form.get('name', 'default')
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 200
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    
        new_model = Model(name=model_name, category=category, path=file_path)
        db.session.add(new_model)
        db.session.commit()
        
        return jsonify({'message': 'File uploaded successfully', 'id': new_model.id}), 200
    else:
        return jsonify({'message': 'Invalid file type'}), 200


@app.route('/deletemodel/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    model = Model.query.get(model_id)
    if model is None:
        return jsonify({'message': 'Model not found'}), 200
    
    try:
        os.remove(model.path)
        db.session.delete(model)
        db.session.commit()
        return jsonify({'message': 'Model deleted successfully'}), 200
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 200
    except Exception as e:
        return jsonify({'message': 'Error deleting model', 'error': str(e)}), 200


@app.route('/listmodels', methods=['GET'])
def list_models():
    models = Model.query.all()
    models_info = [{'id': model.id, 'name': model.name, 'type': model.category, 'path': model.path} for model in models]
    return jsonify(models_info), 200

@app.route('/gettypemodel', methods=['POST'])
def get_type_model():
    try:
        data = request.get_json() 
        model_type = data.get('type') 
        
        if not model_type:
            return jsonify({'message': 'Type is required'}), 200

        models = Model.query.filter_by(category=model_type).all()
        
        if models:
            model_names = [model.name for model in models]
            return jsonify({'message': 'Available models received!', 'models': model_names}), 200
        else:
            return jsonify({'message': 'No models found for the given type'}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching models', 'error': str(e)}), 200


@app.route('/batch/text/steg', methods=['POST'])
def handle_batch_text_steg():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        secret_message = request.form.get('content')  # 获取表单中的文本内容
        user_id = request.form.get('userid') 
        
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
                    
                    encoded_content = encodeStr(secret_message,file_content)
                    
                    encoded_file_path = os.path.join(temp_dir, filename)
                    with open(encoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(encoded_content)
                    
                    encoded_file_paths.append(encoded_file_path)
                    
                    # 清理临时文件
                    os.remove(file_path)
            
            # 将所有编码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]
            zip_filename =str(user_id)+"_"+timestampstr+"_encoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in encoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!','download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200
    

@app.route('/batch/text/decode', methods=['POST'])
def handle_batch_text_decode():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        user_id = request.form.get('userid')
        
        if not files:
            return jsonify({'error': 'Invalid request, files missing'}), 200

        with tempfile.TemporaryDirectory() as temp_dir:
            decoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)
                    
                    # 读取文件内容和执行隐写解码
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    decoded_content = decodeStr(file_content)
                    
                    decoded_file_path = os.path.join(temp_dir, filename)
                    with open(decoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(decoded_content)
                    
                    decoded_file_paths.append(decoded_file_path)
                    
                    # 清理临时文件
                    os.remove(file_path)
            
            # 将所有解码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).split('.')[0] + str(time.time()).split('.')[1]
            zip_filename = str(user_id) + "_" + timestampstr + "_decoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in decoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!', 'download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200
 
@app.route('/batch/img/steg', methods=['POST'])
def handle_batch_image_steg():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        secret_message = request.form.get('content')  
        user_id = request.form.get('userid') 
        model_name = request.form.get('model')

        models = Model.query.filter_by(name=model_name).all()

        model_path = models[0].path
        
        if not files or not secret_message:
            return jsonify({'error': 'Invalid request, files or content missing'}),200

        with tempfile.TemporaryDirectory() as temp_dir:
            encoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)
                    
                    encoderapi(file_path,model_path,temp_dir,secret_message,filename)

                    encoded_file_path = os.path.join(temp_dir, filename)

                    encoded_file_paths.append(encoded_file_path)
                
                    os.remove(file_path)
            
            # 将所有编码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]
            zip_filename =str(user_id)+"_"+timestampstr+"_encoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in encoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!','download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200

@app.route('/batch/img/decode', methods=['POST'])
def handle_batch_image_decode():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        user_id = request.form.get('userid') 
        model_name = request.form.get('model')

        models = Model.query.filter_by(name=model_name).all()

        model_path = models[0].path
        
        if not files:
            return jsonify({'error': 'Invalid request, files missing'}),200

        with tempfile.TemporaryDirectory() as temp_dir:
            decoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)

                    restext=decoderapi(file_path,model_path,'cpu')
                    decoded_text_path=filename.split('.')[0]+'.txt'
                    decoded_file_path = os.path.join(temp_dir, decoded_text_path)
                    with open(decoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(str(restext))

                    decoded_file_paths.append(decoded_file_path)
                
                    os.remove(file_path)
            
            # 将所有编码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]
            zip_filename =str(user_id)+"_"+timestampstr+"_decoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in decoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!','download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200
    

@app.route('/batch/audio/steg', methods=['POST'])
def handle_batch_audio_steg():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        secret_message = request.form.get('content')  
        user_id = request.form.get('userid') 
        
        if not files or not secret_message:
            return jsonify({'error': 'Invalid request, files or content missing'}),200

        with tempfile.TemporaryDirectory() as temp_dir:
            encoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)
                    res=''
                    if filename.split('.')[1] != "wav":
                        res=os.path.join(app.config['TEMP_FOLDER'], filename.split('.')[0]+'.wav')
                        cmdls="echo y | ffmpeg -i "+file_path+" -acodec pcm_s16le -ac 2 -ar 44100 "+res
                        os.system(cmdls)
                    if res=='':
                        res=file_path
                    song = wave.open(res, mode='rb')
                    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
                    string=secret_message
                    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
                    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
                    for i, bit in enumerate(bits):
                        frame_bytes[i] = (frame_bytes[i] & 254) | bit
                    frame_modified = bytes(frame_bytes)

                    encoded_file_path = os.path.join(temp_dir, filename)
                    with wave.open(encoded_file_path, 'wb') as fd:
                        fd.setparams(song.getparams())
                        fd.writeframes(frame_modified)
                    song.close()

                    encoded_file_paths.append(encoded_file_path)
                
                    os.remove(file_path)
                    os.remove(res)
            
            # 将所有编码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).split('.')[0]+str(time.time()).split('.')[1]
            zip_filename =str(user_id)+"_"+timestampstr+"_encoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in encoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])
        
        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!','download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200

@app.route('/batch/audio/decode', methods=['POST'])
def handle_batch_audio_decode():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        user_id = request.form.get('userid') 

        if not files:
            return jsonify({'error': 'Invalid request, files missing'}), 200

        with tempfile.TemporaryDirectory() as temp_dir:
            decoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)

                    # 读取并解码文件内容
                    with wave.open(file_path, mode='rb') as song:
                        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
                        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
                        string = "".join(chr(int("".join(map(str, extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))
                        decoded = string.split("###")[0]

                    decoded_text_path = filename.split('.')[0] + '.txt'
                    decoded_file_path = os.path.join(temp_dir, decoded_text_path)
                    with open(decoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(str(decoded))

                    decoded_file_paths.append(decoded_file_path)

                    # 确保文件句柄已关闭后再删除文件
                    os.remove(file_path)

            # 将所有解码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).replace('.', '')
            zip_filename = f"{user_id}_{timestampstr}_decoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in decoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))

            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])

        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!', 'download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200
    
@app.route('/batch/video/steg', methods=['POST'])
def handle_batch_video_steg():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        secret_message = request.form.get('content')
        user_id = request.form.get('userid')
        model_name = request.form.get('model')

        models = Model.query.filter_by(name=model_name).all()

        model_path = models[0].path

        if not files or not secret_message:
            return jsonify({'error': 'Invalid request, files or content missing'}), 200

        with tempfile.TemporaryDirectory() as temp_dir:
            encoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)
                    
                    # 将文件转为avi格式
                    resname = ''
                    if filename.split('.')[1] != 'avi':
                        resname = filename.split('.')[0] + '.avi'
                        os.system(f'echo y | ffmpeg -i {file_path} -c:v copy -c:a pcm_s16le -max_muxing_queue_size 1024 {resname}')
                    else:
                        resname = file_path

                    # 执行视频隐写编码
                    os.system(f'python tools/encode_video.py --video_path {resname} --device cpu --user_id {secret_message} --decoder_model_path {model_path}')
                    os.system(f'echo y | ffmpeg -i out/encoded_video.avi -c:v libx264 -c:a aac -max_muxing_queue_size 1024 encoded_video.mp4')

                    encoded_file_path = os.path.join(temp_dir,filename)
                    shutil.move('encoded_video.mp4', encoded_file_path)
                    
                    encoded_file_paths.append(encoded_file_path)
                    
                    os.remove(file_path)
                    if resname != file_path:
                        os.remove(resname)

            # 将所有编码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).replace('.', '')
            zip_filename = f"{user_id}_{timestampstr}_encoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in encoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))

            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])

        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!', 'download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200


@app.route('/batch/video/decode', methods=['POST'])
def handle_batch_video_decode():
    try:
        files = request.files.getlist('files')  # 获取上传的文件列表
        user_id = request.form.get('userid')
        model_name = request.form.get('model')

        models = Model.query.filter_by(name=model_name).all()

        model_path = models[0].path

        if not files:
            return jsonify({'error': 'Invalid request, files missing'}), 200

        with tempfile.TemporaryDirectory() as temp_dir:
            decoded_file_paths = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['TEMP_FOLDER'], filename)
                    file.save(file_path)

                    # 执行视频隐写解码
                    uid = getuid(file_path, 'cpu', model_path)

                    decoded_text_path = filename.split('.')[0] + '.txt'
                    decoded_file_path = os.path.join(temp_dir, decoded_text_path)
                    with open(decoded_file_path, 'w', encoding='utf-8') as f:
                        f.write(str(uid))

                    decoded_file_paths.append(decoded_file_path)
                    
                    os.remove(file_path)

            # 将所有解码后的文件打包成一个压缩文件
            timestampstr = str(time.time()).replace('.', '')
            zip_filename = f"{user_id}_{timestampstr}_decoded_files.zip"
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in decoded_file_paths:
                    zipf.write(file_path, os.path.basename(file_path))

            # 移动压缩文件到可访问的文件夹
            shutil.move(zip_path, app.config['TEMP_FOLDER'])

        # 返回下载链接
        return jsonify({'message': 'Task Finished Success!', 'download_url': '/download/' + zip_filename}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing files', 'error': str(e)}), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['TEMP_FOLDER'], filename, as_attachment=True)
    
@app.route('/generate-captcha', methods=['GET'])
def generate_captcha():
    image = ImageCaptcha(width=280, height=90)
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Save the captcha text in the session
    scapt['captcha_text'] = captcha_text
    
    data = image.generate(captcha_text)
    return send_file(io.BytesIO(data.read()), mimetype='image/png')

@app.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    user_input = request.form.get('captcha')
    if 'captcha_text' in scapt and scapt['captcha_text'].lower() == user_input.lower():
        return jsonify({"message": "Captcha verified successfully"}), 200
    else:
        return jsonify({"message": "Invalid captcha"}), 200
    
@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        newPassword = request.form.get('newPassword')

        user = NossUser.query.filter_by(username=username, email=email).first()
        if user:
            hashed_password = generate_password_hash(newPassword, method='pbkdf2:sha256')
            user.password = hashed_password
            db.session.commit()
            return jsonify({'message': 'Password reset successfully'}), 200
        else:
            return jsonify({"message": "User not found"}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
