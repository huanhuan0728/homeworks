from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# DES密钥生成函数
def generate_des_keys(key):
    print("Original Key:", key)
    subkeys = []
    pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    # 将64位密钥压缩为56位
    key = [key[i - 1] for i in pc1]
    print("Key after PC-1:", ''.join(key))

    # 生成16轮子密钥
    for round_num in range(16):
        if round_num in (0, 1, 8, 15):
            shift_amount = 1
        else:
            shift_amount = 2

        left_shifted = key[:28][shift_amount:] + key[:28][:shift_amount]
        right_shifted = key[28:][shift_amount:] + key[28:][:shift_amount]

        combined_shifted = left_shifted + right_shifted

        # 使用置换选择2生成子密钥
        subkey = [combined_shifted[i - 1] for i in pc2]
        subkeys.append(''.join(subkey))

    return subkeys

# 数据加密函数
def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
    return ciphertext

# 数据解密函数
def des_decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return plaintext

# 主程序
if __name__ == "__main__":
    key = "0001001100110100010101110111100110011011101111001101111111110001"
    key_bytes = int(key, 2).to_bytes(8, byteorder='big')

    subkeys = generate_des_keys(key)

    print("1. 密钥拓展")
    print("密钥:")
    print(key)
    print("置换选择1:")
    print("C:")
    print(key[:28])
    print("D:")
    print(key[28:])
    for i, subkey in enumerate(subkeys):
        print(f"N={i + 1}")
        print("C:")
        print(subkey[:28])
        print("D:")
        print(subkey[28:])
        print("子密钥Kn:")
        print(subkey)

    plaintext = "1101010101101100111101001010101111000010111100001010101011000110"

    ciphertext = des_encrypt(plaintext.encode(), key_bytes)

    print("\n2. 加密过程")
    print("明文:")
    print(plaintext)
    print("密文:")
    print(ciphertext.hex())

    decrypted_text = des_decrypt(ciphertext, key_bytes)

    print("\n3. 解密过程")
    print("密文:")
    print(ciphertext.hex())
    print("解密后的明文:")
    print(decrypted_text.decode())
