from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import os
import psutil

def get_all_disk_partitions():
    partitions = []
    for partition in psutil.disk_partitions(all=True):
        if partition.fstype:
            partitions.append(partition.device)
    return partitions

def aes_ecb_decrypt(ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, AES.block_size)


def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    decrypted_data = aes_ecb_decrypt(ciphertext)

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
        print("[!] Decrypted file saved as " + output_file)

def read_file(file_walk):
    for root, dirs, files in os.walk(file_walk):
        for file in files:
            # Get file extension
            ext = os.path.splitext(file)[1]

            # Check if in allowed list
            if ext == ".love":
                filename=os.path.join(root, file)
                newfile = os.path.dirname(filename)+'\\'+os.path.basename(filename).replace('.love','')
                try:
                    decrypt_file(filename,newfile)
                    os.remove(filename)
                except Exception as e:
                    print("[!] Error decrypting file: " +  filename)
                    print("[!] Error:   str(e)" + str(e))
                    if "Padding is incorrect" in  str(e):
                        print("[!] 秘钥错误！")
                        sys.exit(1)







if __name__ == "__main__":
    import sys
    keys = sys.argv[1]
    key = binascii.unhexlify(keys)
    # decrypt_file(input_file, output_file)

    disk_partitions = get_all_disk_partitions()
    for partition in disk_partitions:
        read_file(partition)

    print("文件解密完成。")