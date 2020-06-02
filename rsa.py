import prime_numbers

############################### PRIVATE FUNCTIONS ################################### 
def _get_e(phi_euler):
    for e in range(2, phi_euler):
        if _gcd(e, phi_euler) == 1:
            return e

def _gcd(a, b):
    r = a%b
    while r:
        a = b
        b = r
        r = a%b
    return b

def _egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = _egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def _get_d(e, phi_euler):
    g, x, y = _egcd(e, phi_euler)
    return x % phi_euler

def _fast_exponentiation(x, exp, n, r=1):
    while exp > 0:
        if exp % 2 == 0:
            x = (x ** 2) % n
            exp /= 2
        else:
            r = (x * r) % n
            exp -= 1
    return r
#####################################################################################

############################### PUBLIC FUNCTIONS #################################### 
def _encrypt_char(char, PUBLIC_KEY):
    n, e = PUBLIC_KEY   
    return _fast_exponentiation(int(char), int(e), int(n))

def _decrypt_char(y, n, PRIVATE_KEY):
    return _fast_exponentiation(int(y), PRIVATE_KEY, n)

def encrypt(message, PUBLIC_KEY):
    encrypted_msg = ""
    DELIMITER = "|"
    for c in message:
        encrypted_msg += str(_encrypt_char(ord(c), PUBLIC_KEY)) + DELIMITER
    return encrypted_msg

def decrypt(encrypted_msg, n, PRIVATE_KEY):
    decrypted_msg = ""
    DELIMITER = "|"
    print(encrypted_msg.split(DELIMITER))
    for o in encrypted_msg.split(DELIMITER):
        if o != '':
            decrypted_msg += chr(_decrypt_char(int(o), n ,PRIVATE_KEY))
    return decrypted_msg

def generate_keys():
    p = prime_numbers.get_random_prime()
    q =  prime_numbers.get_random_prime()

    n = p*q
    phi_euler = (p-1)*(q-1)

    print("n:",n, "phi euler:", phi_euler)

    e = _get_e(phi_euler)
    d = _get_d(e, phi_euler)

    PUBLIC_KEY = (n, e)
    PRIVATE_KEY = d

    print("e:",e, "d",d)

    return PUBLIC_KEY, PRIVATE_KEY

#####################################################################################