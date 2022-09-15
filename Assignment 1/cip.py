from caesarcipher import CaesarCipher
def encrypt(type,filename):
    if type == "plaintext":
        return
    if type == "substitution":
        l = []
        with open(filename) as f:   
            while True:
                line = f.readline()
                if not line:
                    break
                # print(line.strip())
                cipher = CaesarCipher(line,offset=2)
                l.append(cipher.encoded)
            # print(l)
        with open(filename,'w') as f:
            f.writelines(l)
        return
    if type == "transpose":
        l = []
        with open(filename) as f:   
            while True:
                line = f.readline()
                if not line:
                    break
                # print(line.strip())
                line = line[::-1]
                l.append(line)
            # print(l)
        with open(filename,'w') as f:
            f.writelines(l)
        return

def decrypt(type,filename):
    if type == "plaintext":
        return
    if type == "substitution":
        l = []
        with open(filename) as f:   
            while True:
                line = f.readline()
                if not line:
                    break
                # print(line.strip())
                cipher = CaesarCipher(line,offset=2)
                l.append(cipher.decoded)
            # print(l)
        with open(filename,'w') as f:
            f.writelines(l)
        return
    if type == "transpose":
        l = []
        with open(filename) as f:   
            while True:
                line = f.readline()
                if not line:
                    break
                # print(line.strip())
                line = line[::-1]
                l.append(line)
            # print(l)
        with open(filename,'w') as f:
            f.writelines(l)
        return

