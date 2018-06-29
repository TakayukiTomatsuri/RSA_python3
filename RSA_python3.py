#! -*- coding:utf-8 -*-

# 拡張ユークリッドの互除法
# 引数:ax+by = c の a,b
# 戻値:リスト(c,x,y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def gcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    #整数割り算にしないとfloatがオーバーフローするとかでてとまる
    return a * b // gcd(a, b)

#def modinv(a, m):
#    g, x, y = egcd(a, m)
#    if g != 1:
#        raise Exception('No modular inverse')
#    return x%m

#鍵生成
def generate_keys(p, q, e=65537):
    N = p * q
    L = lcm(p - 1, q - 1)
    #もしくは、
    #L = (p-1)*(q-1)//gcd(p-1, q-1)

    c, x, y = egcd(e, L)
    d = x % L
    #こちらでもよい?
    #d = inverse(e, L)
    #d = modinv(e, (p-1)*(q-1))
  
    return (e, N), (d, N)

#暗号化
def encrypt(plain_text, public_key):
    e, N = public_key
    plain_bytes = plain_text.encode("UTF-8")  
    plain_integer = int.from_bytes(plain_bytes, 'big') 
    encrypted_integer = pow(plain_integer, e, N)
    encrypted_bytes = encrypted_integer.to_bytes((encrypted_integer.bit_length() // 8) + 1, 'big')

    return encrypted_bytes


#復号
def decrypt(encrypted_bytes, private_key):
    d, N = private_key    
    encrypted_integer = int.from_bytes(encrypted_bytes, 'big')  
    plain_integer = pow(encrypted_integer, d, N)
    plain_bytes = plain_integer.to_bytes((plain_integer.bit_length() // 8) + 1, byteorder='big') 
    
    return(plain_bytes.decode(encoding='UTF-8',errors='strict'))


#--------------------------------------


p = 54311
q = 158304142767773473275973624083670689370769915077762416888835511454118432478825486829242855992134819928313346652550326171670356302948444602468194484069516892927291240140200374848857608566129161693687407393820501709299228594296583862100570595789385365606706350802643746830710894411204232176703046334374939501731

plain = "FLAG{hello}"
pub, priv = generate_keys(p, q)
encr = encrypt(plain, pub )
print(encr)
print(decrypt(encr, priv))  
