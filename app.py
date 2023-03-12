import base64
import json
import os
import io
import sys
from argparse import ArgumentParser
from time import time
import hashlib
import asyncio
import logging as logger
import requests
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory, Response
from flask.logging import default_handler
from flask_cors import CORS, cross_origin


app = Flask("AiAssetServer")
app.logger.addHandler(default_handler)
CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type'

GlobalTaskQueue = []
async def RunTaskLoop():
    global GlobalTaskQueue
    while True:
        que = GlobalTaskQueue
        GlobalTaskQueue = []
        for task in que:
            try:
                await task[0](*task[1])
            except Exception as e:
                logger.error(e)
                import traceback
                logger.error(traceback.format_exc())

        await asyncio.sleep(1)

def TaskLoopAsync():
    asyncio.run(RunTaskLoop())

# ex: addTask(asyncPut, (key, newvalue))
# async def asyncPut(key, newvalue):
def addTask(fuc, d):
    GlobalTaskQueue.append((fuc, d))
    
MAX_CONCURRENCY_TASK_NUM = 1
def startTaskLoop():
    import _thread
    for _ in range(MAX_CONCURRENCY_TASK_NUM):
        _thread.start_new_thread( TaskLoopAsync, () )

startTaskLoop()



@app.route('/api/assets', methods=['GET', 'POST'])
def GetAssets():
    # ('pageNumber', '1'), ('pageSize', '20'), ('searchContent', ''), ('typeId', '1')
    logger.info(request.args)
    searchContent = request.args.get("searchContent")
    pageNumber = request.args.get("pageNumber", 0)
    typeId = int(request.args.get("typeId", 0))
    if not pageNumber:
        pageNumber = 0
    pageSize = int(request.args.get("pageSize", 0))
    pageNumber = int(pageNumber)
    skip = pageNumber * pageSize
    logger.info(pageNumber)
    logger.info(pageSize)

    logger.info(searchContent)
    result_text = []
    result_text.append({
        'id': 1,
        'name': "1.fbx",
        'fbxUrl': "",
    })
    result_text.append({
        'id': 2,
        'name': "2.fbx",
        'fbxUrl': "",
    })
    result_text.append({
        'id': 3,
        'name': "3.fbx",
        'fbxUrl': "",
    })

    return jsonify(result_text)


# 返回的内容
@app.route("/download/<fileId>", methods=['GET'])
def download_file(fileId):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    logger.info(f"in download_file fileId={fileId}")
    with open(f"./assets/fileId.fbx", 'rb') as f:
        d = io.BytesIO(f.open())

    # d = base64.b64decode(d)
    # d = d.decode(encoding='utf_8')
    response = Response(d)
    # with open("output.fbx", 'wb') as f:
    #     f.write(d)
    return response

# 浏览器打开直接下载
@app.route("/HiAsset/download_http/<fileId>", methods=['GET'])
def download_http(fileId):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    print(f"in download_http fileId={fileId}")

    project = request.args.get("project", type=str)
    # d = getData(fileId) 
    d = io.BytesIO(d)
    # name = getName(fileId)
    # print(type(name))
    # return send_file(d, download_name=name, as_attachment=True)

