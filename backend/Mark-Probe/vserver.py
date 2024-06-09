from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
# from steganogan import SteganoGAN
# from steganogan.critics import BasicCritic
# from steganogan.decoders import DenseDecoder
# from steganogan.encoders import DenseEncoder
# from steganogan.loader import DataLoader
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

import argparse
import cv2
import  random
from PIL import Image

from tools.interface.utils import get_device, model_import
from tools.interface.bch import BCHHelper
from tools.interface.predict import decode
from tools.decode import getuid


app = Flask(__name__)
CORS(app)

# 修改最大上传文件大小为1GB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

@app.route('/evideo',methods=['POST'])
def handle_evideo():
    try:
        video = request.files.get('video')
        text = request.form.get('text')
        resname=''
        video.save(video.filename)
        if video.filename.split('.')[1]!='avi':
            resname=video.filename.split('.')[0]+'.avi'
            os.system('echo y | ffmpeg -i '+video.filename+' -c:v copy -c:a pcm_s16le -max_muxing_queue_size 1024 '+resname)
        print(video.filename)
        if video.filename.split('.')[1]=='avi':
            resname=video.filename
        video.save(resname)
        print('ll',resname)
        os.system('python tools/encode_video.py --video_path tools/'+resname+' --device cpu --user_id '+text)
        os.system('echo y | ffmpeg -i '+'out/encoded_video.avi'
+' -c:v libx264 -c:a aac -max_muxing_queue_size 1024 '+'encoded_video.mp4') 
        with open('encoded_video.mp4','rb') as f:
            video_msg=f.read()
        encoded_video = base64.b64encode(video_msg).decode('utf-8')
        return jsonify({'message':'success','video':encoded_video})
    except Exception as e:
        return jsonify({'message':str(e)})

@app.route('/devideo',methods=['POST'])
def handle_devideo():
    try:
        video = request.files.get('video')
        print(video)
        video.save(video.filename)
        uid=getuid(video.filename,'cpu','weight/latest-0.pth')
        return jsonify({'message':'success','text':uid})
    except Exception as e:
        return jsonify({'message':str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4001)
