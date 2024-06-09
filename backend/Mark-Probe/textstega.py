import random

def encodeStr(hidden_text, to_hide_text):
    # 将隐写文本转换为二进制字符串
    binary_str = ' '.join(format(ord(char), 'b') for char in hidden_text)
    
    # 根据二进制字符串的每个字符，选择对应的零宽度字符
    encoded_str = ''.join(
        '\u200B' if bit == '1' else '\u200C' if bit == '0' else '\u200D' for bit in binary_str
    )
    
    # 将各二进制数字以零宽非连接符分隔
    encoded_str = '\u200E'.join(encoded_str)

    # 随机选择一个位置将编码后的字符串插入到载体文本中
    insert_pos = random.randint(0, len(to_hide_text))
    cipher_text = to_hide_text[:insert_pos] + encoded_str + to_hide_text[insert_pos:]
    
    return cipher_text

def decodeStr(cipher_text):
    # 将载体文本中的零宽度字符转换为二进制字符串
    binary_str = ''.join(
        '1' if char == '\u200B' else '0' if char == '\u200C' else ' ' if char == '\u200D' else '' for char in cipher_text
    )
    
    # 将二进制字符串转换回文本
    decoded_text = ''.join(
        chr(int(binary, 2)) for binary in binary_str.split()
    )
    
    return decoded_text


if __name__=='__main__':
    strss='fis1112'
    res=encodeStr('1223',strss)
    with open('tetext.txt', 'w', encoding='utf-8') as f:
        f.write(res)
    with open('tetext.txt', 'r', encoding='utf-8') as f:
        filecontent=f.read()
    print(decodeStr(filecontent))
