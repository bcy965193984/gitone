#-*-coding:utf-8-*-
import urllib.request
import urllib
import requests
import websocket
import struct
import sys
sys.path.append('F:/Project/project 1219/modules/robot/')
import UsrDomain_pb2 as ControlCommand
import threading
import signal
import time
import tarfile
import os
import json
from google.protobuf import json_format
import pandas as pd
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PIL import Image

ROBOT_CONTROL_URL = "http://192.168.18.236:8000/pb?cmd=Cmd"
global_tourstate = 0
global_tourstate_lock = threading.Lock()


class System(object):
    #查询设备类型配置
    def GetDvsTypeConfig(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetDvsTypeConfig"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand()
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class robot(object):
    #查询机器人信息
    def GetRobotInfo(queryType, queryPos, queryNum, queryTotal):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetRobotInfo"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        #command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal)
        #print(command_message)

        reqMsg = ControlCommand.CommonMsg()
        queryCondition = ControlCommand.QueryCondition()
        queryCondition.queryType = 1
        queryCondition.queryPos = 0
        queryCondition.queryNum = 100
        queryCondition.queryTotal = True
        reqMsg.data.Pack(queryCondition)
        print(reqMsg)
        print(queryCondition)

        reqData = reqMsg.SerializeToString()

        # #发送POST请求
        response = requests.post(url, headers=headers, data=reqData)

        if response.status_code == 200:
            respData = response.content
            print(respData)
            respMsg = ControlCommand.CommonMsg()
            respMsg.ParseFromString(respData)
            print('respMsg.ret:', respMsg.ret)
            print(respMsg)
            if(0 == respMsg.ret):
                queryResult = ControlCommand.QueryResult()
                respMsg.data.Unpack(queryResult)
                print('totalNum:', queryResult.totalNum)
                print('queryResult.results.size:', len(queryResult.results))
                for result in queryResult.results:
                    robotInfo = ControlCommand.RobotInfo()
                    result.Unpack(robotInfo)
                    print(robotInfo)
        else:
            print('Error:', response.status_code)

    #查询机器人流媒体信息
    def GetRobotMediaUrl(sld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetRobotMediaUrl"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #机器人能力
    def RobotAbility(sld, sParam):
        url = ROBOT_CONTROL_URL + "RobotAbility"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld, sParam=sParam)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #位置校正
    def RobotReviseLocation(sld, uld, sParam, iParam):
        url = ROBOT_CONTROL_URL + "RobotReviseLocation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld, uld=uld, sParam=sParam, iParam=iParam)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #一键定位
    def RobotGotoLocation(sld, sParam, uld, iParam):
        url = ROBOT_CONTROL_URL + "RobotGotoLocation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld, sParam=sParam, uld=uld, iParam=iParam)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #机器人运动控制
    def RobotMotionCtrl(sld, iParam):
        url = ROBOT_CONTROL_URL + "RobotMotionCtrl"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld, iParam=iParam)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #获取机器人实时巡检状态
    def GetRobotTourStatus(sld):
        url = ROBOT_CONTROL_URL + "GetRobotTourStatus"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #获取机器人部件状态
    def GetRobotUnits(sld):
        url = ROBOT_CONTROL_URL + "GetRobotUnits"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #机器人救援脱钩
    def RobotUnhook(sld, bParam):
        url = ROBOT_CONTROL_URL + "RobotUnhook"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(sld=sld, bParam=bParam)
        data_in = command_message.SerializeToString()

        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class Roadbase(object):
    #新增路基网关
    def AddRoadbaseS2E(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddRoadbaseS2E"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(0)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询路基网关
    def GetRoadbaseS2E(queryType, queryPos, queryNum, queryTotal, intId, strID):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetRoadbaseS2E"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId, strID=strID)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置路基网关
    def SetRoadbaseS2E(queryType, queryPos, queryNum, queryTotal, intId, strID):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "SetRoadbaseS2E"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId, strID=strID)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除路基网关
    def DelRoadbaseS2E(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelRoadbaseS2E"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #启动代理路基网关
    def ActivateS2E(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "ActivateS2E"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #新增路基设备
    def AddRoadbase(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddRoadbase"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(0)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询路基设备
    def GetRoadbase(queryType, queryPos, queryNum, queryTotal, intId):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetRoadbase"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置路基设备
    def setRoadbase(queryType, queryPos, queryNum, queryTotal, intId):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "setRoadbase"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除路基设备
    def DelRoadbase(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelRoadbase"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #路基控制
    def RoadbaseCtr(data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "RoadbaseCtr"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class Tour(object):
    #添加巡检站点
    def AddTourStation(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddTourStation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(0)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检站点
    def GetTourStation(queryType, queryPos, queryNum, queryTotal, intId, intparams):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourStation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId, intparams=intparams)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置巡检站点
    def SetTourStation(data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "SetTourStation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除巡检站点
    def DelTourStation(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelTourStation"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #添加巡检线路
    def AddTourLine(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddTourLine"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(0)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检线路
    def GetTourLine(queryType, queryPos, queryNum, queryTotal, intId):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourLine"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置巡检线路
    def SetTourLine(data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "SetTourLine"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除巡检线路
    def DelTourLine(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelTourLine"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #添加巡检任务
    def AddTourTask(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddTourTask"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(0)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检任务
    def GetTourTask(queryType, queryPos, queryNum, queryTotal, intId):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourTask"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intId=intId)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置巡检任务
    def SetTourTask(data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "SetTourTask"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除巡检任务
    def DelTourTask(uld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelTourTask"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #巡检控制
    def TourCtrl(ctrlType, tour, beginTime, tourType, gallery, robot):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "TourCtrl"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(ctrlType=ctrlType, tour=tour, beginTime=beginTime, tourType=tourType, gallery=gallery, robot=robot)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检状态
    def GetTourStatus(queryType, queryPos, queryNum, queryTotal, uintId, beginTime, endTime, strID, intParams):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourStatus"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, uintId=uintId, beginTime=beginTime, endTime=endTime, strID=strID, intParams=intParams)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检详情
    def GetTourDetails(queryPos, queryNum, queryTotal, strID, beginTime, endTime, strParams, uintId):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourDetails"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, strID=strID, beginTime=beginTime, endTime=endTime, uintId=uintId, strParams=strParams[0])
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询巡检统计
    def GetTourSummary(uId, uParam):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetTourSummary"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uId=uId, uParam=uParam)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class Alarm(object):
    #添加对象分析
    def AddObjectAnalysis(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "AddObjectAnalysis"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand()
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询对象分析
    def GetObjectAnalysis(queryType, intId, strID):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "GetObjectAnalysis"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, intId=intId, strID=strID)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #设置对象分析
    def SetObjectAnalysis(uId, data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "SetObjectAnalysis"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uId=uId, data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #删除对象分析
    def DelObjectAnalysis(uld, sld):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "DelObjectAnalysis"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(uld=uld, sld=sld)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class Log(object):
    #查询机器人位置或传感器信息
    def QueryRobotSensor(queryType, intParams, beginTime, endTime, strID):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "QueryRobotSensor"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, intParams=intParams, beginTime=beginTime, endTime=endTime, strID=strID)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询机器人部件信息
    def QueryRobotUnitsStatus(beginTime, endTime, strID):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "QueryRobotUnitsStatus"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(beginTime=beginTime, endTime=endTime, strID=strID)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #查询报警信息
    def QueryAlarmInfo(queryType, queryPos, queryNum, queryTotal, intParams, beginTime, endTime, strID, strParams):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "QueryAlarmInfo"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(queryType=queryType, queryPos=queryPos, queryNum=queryNum, queryTotal=queryTotal, intParams=intParams, beginTime=beginTime, endTime=endTime, strID=strID, strParams=strParams)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #处理报警
    def HandleAlarm(iParam, id, desc, handler):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "HandleAlarm"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(iParam=iParam, id=id, desc=desc, handler=handler)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #文件传输
    def FileTransfer(bParam, sParam, sId, uParam, TourStatus):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "FileTransfer"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(bParam=bParam, sParam=sParam, sId=sId, uParam=uParam, TourStatus=TourStatus)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class SmartAnalysis(object):
    #添加分析样本
    def IvasAddSample(data):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "IvasAddSample"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand(data=data)
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #清空分析样本
    def IvasClearSample(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "IvasClearSample"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand()
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

    #重新训练模型
    def IvasRelearn(self):
        # 定义服务器地址和端口
        url = ROBOT_CONTROL_URL + "IvasRelearn"
        # 定义请求头
        headers = {
            "Content-Type":"application/octet-stream",
        }

        # 构造 Protocol Buffers 对象并序列化
        command_message = ControlCommand()
        data_in = command_message.SerializeToString()

        #发送POST请求
        response = requests.post(url, headers=headers, data=data_in)

        if response.status_code == 200:
            print('Success:', response.json())
            result_data = response.content
        else:
            print('Error:', response.status_code)

class Unfilepack(object):
    def __init__(self):
        file_path = 'F:/站点0_20230830_181418/站点0_20230830_181418.json'
        self.load_json(file_path)   
        # pd.read_json(file_path)   

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # data = json.load(file)
                data = file.read()
                # print(data)
                tourreport = json_format.Parse(data, ControlCommand.TourReport())
                print(tourreport)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    

class MyWebSocket:
    def __init__(self, ws_address):
        self.ws = websocket.WebSocketApp(ws_address,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.on_open = self.on_open

    def download_tar(url, filename):    
        try:
            # 检查文件是否已存在
            if os.path.exists(filename):
                print(f"File {filename} already exists. Skipping download.")
                return
            
            response = requests.get(url, stream=True)
            response.raise_for_status()  # 检查是否发生了下载错误

            # 确保文件不为空
            if len(response.content) == 0:
                raise ValueError("Downloaded file is empty.")
            
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            # 解压文件
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall(path='F:/Project/project 1219/cameras/')  # 将文件解压到指定目录

            # 删除下载的 tar.gz 文件
            os.remove(filename)

            print(f"File {filename} has been downloaded and extracted to 'extracted_folder'.")
        except Exception as e:
            print(f"Error: {e}")

    def on_message(self, ws, message):
        global global_tourstate
        # 处理接收到的消息
        # print(f"Received: {message}")
        content = struct.unpack("<HIII", message[0:14])
        magic = content[0]
        hex_magic="%x" % magic
        cmd = content[1]
        hex_cmd="%x" % cmd
        seq = content[2]
        hex_seq="%x" % seq
        len = content[3]
        hex_len="%x" % len

        if(0x8608 == cmd):
            tourStatus = ControlCommand.TourStatus()
            # tourStatus.ParseFromString(message[14:14+len])

            if tourStatus.len > 0:
                with global_tourstate_lock:
                    global_tourstate = tourStatus.task
                    getph=signal.Getphoto_signal()
                    getph.getphoto_signal.emit()
                # 创建线程对象
                # tar.gz 文件的下载链接和本地保存路径
                file_url = 'http://192.168.18.236:8000/TourReport/' + tourStatus.file
                local_filename = 'F:/Project/project 1219/cameras/' + tourStatus.file
                # print(file_url)
                download_thread = threading.Thread(target=MyWebSocket.download_tar, args=(file_url, local_filename))

                # 启动线程
                download_thread.start()

                # 主线程等待所有线程完成
                download_thread.join()

            else:
                with global_tourstate_lock:
                    global_tourstate = 0
    
        
    def on_error(self, ws, error):
        # 处理错误
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        # 处理连接关闭
        print("Connection closed")

    def on_open(self, ws):
        # 连接建立后发送数据
        # message = "Hello, WebSocket Server!"
        # ws.send(message)
        print("Connection opened")

    def connect_to_websocket(self, event):
        self.ws.run_forever()


# if __name__ == '__main__':

#     # 定义 WebSocket 地址
#     ws_address = "ws://192.168.18.236:8000/subscribe"
#     client = MyWebSocket(ws_address)
#     client.connect_to_websocket(ws_address)
        
#     # robot.GetRobotInfo(1, 0, 100, True)
#     # obj = Unfilepack()
