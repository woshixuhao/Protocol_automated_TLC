import serial
import struct
#import numpy 
#import string
#import binascii
import time

global griper_id
gripper_id = 1

#把数据分成高字节和低字节
def data2bytes(data):
    rdata = [0xff]*2
    if data == -1:
        rdata[0] = 0xff
        rdata[1] = 0xff
    else:
        rdata[0] = data&0xff
        rdata[1] = (data>>8)&(0xff)
    return rdata

#把十六进制或十进制的数转成bytes
def num2str(num):
    str = hex(num)
    str = str[2:4]
    if(len(str) == 1):
        str = '0'+ str
    str = bytes.fromhex(str)     
    #print(str)
    return str

#求校验和
def checknum(data,leng):
    result = 0
    for i in range(2,leng):
        result += data[i]
    result = result&0xff
    #print(result)
    return result
#扫描id号
def getid(i):
    global gripper_id

    datanum = 0x05
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90

    #id号
    b[2] = i

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x12
     
    #数据
    b[5] = data2bytes(1000)[0]
    b[6] = data2bytes(1000)[1]
    
    b[7] = data2bytes(0)[0]
    b[8] = data2bytes(0)[1]
      
    #校验和
    b[9] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    getdata= ser.read(7)
    return len(getdata)

#设置开口限位（最大开口度和最小开口度）
def setopenlimit(openmax,openmin):
    global gripper_id
    if openmax <0 or openmax >1000:
        print('数据超出正确范围：0-1000')
        return
    if openmin <0 or openmin >1000:
        print('数据超出正确范围：0-1000')
        return
    if openmax < openmin:
        print('最大开口度应该大于最小开口度')
        return

    
    datanum = 0x05
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90

    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x12
     
    #数据
    b[5] = data2bytes(openmax)[0]
    b[6] = data2bytes(openmax)[1]
    
    b[7] = data2bytes(openmin)[0]
    b[8] = data2bytes(openmin)[1]
      
    #校验和
    b[9] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    print('发送的数据：')
    for i in range(1,datanum+6):
        print(hex(putdata[i-1]))
        
    getdata= ser.read(7)
    print('返回的数据：')
    for i in range(1,8):
        print(hex(getdata[i-1]))
        
#设置ID
def setid(idnew):
    global gripper_id
    if idnew <1 or idnew >254:
        print('数据超出正确范围：1-254')
        return
    
    datanum = 0x02
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x04
     
    #数据
    b[5] = idnew
    
    gripper_id = idnew
      
    #校验和
    b[6] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    # getdata= ser.read(7)
    # print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))

#运动到目标
def movetgt(tgt):
    global gripper_id
    if tgt <0 or tgt >1000:
        print('数据超出正确范围：0-1000')
        return
    
    datanum = 0x03
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x54
     
    #数据
    b[5] = data2bytes(tgt)[0]
    b[6] = data2bytes(tgt)[1]
      
    #校验和
    b[7] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    # getdata= ser.read(7)
    # print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))

#运动张开
def movemax(speed):
    global gripper_id
    if speed <1 or speed >1000:
        print('数据超出正确范围：1-1000')
        return
    
    datanum = 0x03
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x11
     
    #数据
    b[5] = data2bytes(speed)[0]
    b[6] = data2bytes(speed)[1]
      
    #校验和
    b[7] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    # getdata= ser.read(7)
    # print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))
    
#运动闭合
def movemin(speed,power):
    global gripper_id
    if speed <1 or speed >1000:
        print('数据超出正确范围：1-1000')
        return
    if power <50 or speed >1000:
        print('数据超出正确范围：50-1000')
        return
    
    datanum = 0x05
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x10
     
    #数据
    b[5] = data2bytes(speed)[0]
    b[6] = data2bytes(speed)[1]
    b[7] = data2bytes(power)[0]
    b[8] = data2bytes(power)[1]  
    #校验和
    b[9] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    print('发送的数据：')
    for i in range(1,datanum+6):
        print(hex(putdata[i-1]))
    getdata= ser.read(7)
    #print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))
    
#运动持续闭合
def moveminhold(speed,power):
    global gripper_id
    if speed <1 or speed >1000:
        print('数据超出正确范围：1-1000')
        return
    if power <50 or speed >1000:
        print('数据超出正确范围：50-1000')
        return
    
    datanum = 0x05
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x18
     
    #数据
    b[5] = data2bytes(speed)[0]
    b[6] = data2bytes(speed)[1]
    b[7] = data2bytes(power)[0]
    b[8] = data2bytes(power)[1]  
    #校验和
    b[9] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    #
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    # getdata= ser.read(7)
    # print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))


#读取开口限位
def getopenlimit():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90

    #gripper_id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x13
    
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    print('发送的数据：')
    for i in range(1,datanum+6):
        print(hex(putdata[i-1]))
    
    getdata= ser.read(10)
    print('返回的数据：')
    for i in range(1,11):
        print(hex(getdata[i-1]))
    
    openlimit = [0]*2
    for i in range(1,3):
        if getdata[i*2+3]== 0xff and getdata[i*2+4]== 0xff:
            openlimit[i-1] = -1
        else:
            openlimit[i-1] = getdata[i*2+3] + (getdata[i*2+4]<<8)
    return openlimit

#读取当前开口
def getcopen():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90

    #gripper_id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0xD9
    
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    
    getdata= ser.read(8)
    # print('返回的数据：')
    # for i in range(1,9):
    #     print(hex(getdata[i-1]))
    
    copen = [0]*1
    for i in range(1,2):
        if getdata[i*2+3]== 0xff and getdata[i*2+4]== 0xff:
            copen[i-1] = -1
        else:
            copen[i-1] = getdata[i*2+3] + (getdata[i*2+4]<<8)
    return copen

#读取当前状态
def getstate():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90

    #gripper_id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x41
    
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    
    getdata= ser.read(13)
    # print('返回的数据：')
    # for i in range(1,14):
    #     print(hex(getdata[i-1]))
    
    if getdata[5] == 1:
        print('max in place')
    elif getdata[5] == 2:
        print('min in place')
    elif getdata[5] == 3:
        print('stop in place')    
    elif getdata[5] == 4:
        print('closing')    
    elif getdata[5] == 5:
        print('openning')
    elif getdata[5] == 6:
        print('force control in place to stop')
    else:
        print('no def')

    if (getdata[6]&0x01)==1:
        print('runing stop fault')
    
    if (getdata[6]&0x02)==2:
        print('overheat fault')
  
    if (getdata[6]&0x04)==4:
        print('Over Current Fault')
        
    if (getdata[6]&0x08)==8:
        print('running fault')
    
    if (getdata[6]&0x10)==16:
        print('communication fault')
    
    print('temp:',getdata[7])
    print('curopen:',((getdata[9] << 8) & 0xff00) + getdata[8])
    print('power:',((getdata[11] << 8) & 0xff00) + getdata[10])
    
#急停
def setestop():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x16
         
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    print('发送的数据：')
    for i in range(1,datanum+6):
        print(hex(putdata[i-1]))
    getdata= ser.read(7)
    print('返回的数据：')
    for i in range(1,8):
        print(hex(getdata[i-1])) 

#参数固化
def setparam():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x01
         
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    print('发送的数据：')
    for i in range(1,datanum+6):
        print(hex(putdata[i-1]))
    getdata= ser.read(7)
    print('返回的数据：')
    for i in range(1,8):
        print(hex(getdata[i-1])) 

#清除故障
def setFrsvd():
    global gripper_id
    
    datanum = 0x01
    b = [0]*(datanum + 5)
    #包头
    b[0] = 0xEB
    b[1] = 0x90
    #id号
    b[2] = gripper_id

    #数据个数
    b[3] = datanum
    
    #操作码
    b[4] = 0x17
         
    #校验和
    b[5] = checknum(b,datanum+4)
    
    #向串口发送数据
    putdata = b''
    
    for i in range(1,datanum+6):
        putdata = putdata + num2str(b[i-1])
    ser.write(putdata)
    #print('发送的数据：',putdata)
    
    # print('发送的数据：')
    # for i in range(1,datanum+6):
    #     print(hex(putdata[i-1]))
    # getdata= ser.read(7)
    # print('返回的数据：')
    # for i in range(1,8):
    #     print(hex(getdata[i-1]))


ser=serial.Serial('COM7',115200)
ser.timeout = 0.01
ser.isOpen()
setid(7)
for i in range(1,255):
    if getid(i) == 7:
        gripper_id = i
        break
#time.sleep(10)
movetgt(0)

#moveminhold(1000,1000)
#print(getcopen())
# time.sleep(10)



