import os
import numpy as  np
import createBayes
import sys
import main
import jointfunc
from flask import  Flask ,render_template,request, Response
import subprocess

app=Flask(__name__)


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/function',methods=['POST','GET']) #页面链接该路由名称
def function():

    img_path = 'static/bayes.png'
    response={
        'image1':img_path,
        'image2':'static/causal_pic.jpg'
    }
    return render_template('function.html',response=response)

@app.route('/run_main')
def run_create_bayes():
    subprocess.run(['python', 'main.py'])
    subprocess.run(['python', 'createBayes.py'])
    subprocess.run(['python', 'jointfunc.py'])
    return '数据标注程序 main.py has been run in the background'


if __name__=='__main__':
    # os.system('python main.py')
    os.system('python createBayes.py')
    os.system('python jointfunc.py')
    app.run(debug=True)
