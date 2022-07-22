from getpass import getpass
from django.core.management.utils import get_random_secret_key
import hashlib
from Crypto.Cipher import AES
from pathlib import Path
import os


def gen_DATABASES() -> dict:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
        }
    }

    DATABASES['default']['NAME'] = input('请输入所使用的 MySQL 数据库名:')
    DATABASES['default']['USER'] = input('请输入 MySQL 数据库用户名:')
    DATABASES['default']['PASSWORD'] = getpass('请输入 MySQL 数据库用户密码(无回显):')
    DATABASES['default']['HOST'] = input('请输入 MySQL 数据库地址(本机请输入"localhost"):')
    DATABASES['default']['PORT'] = input('请输入 MySQL 数据库端口(默认为3306):')

    return DATABASES


def gen_SECRET_KEY() -> str:
    SECRET_KEY = get_random_secret_key()
    return SECRET_KEY


def read_settings(file_in) -> dict:
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    tips = '请输入加载配置文件所需的密码, 输入错误将会重新配置(无回显):'
    key = hashlib.md5(getpass(tips).encode('utf8')).hexdigest().encode('utf8')[0:16]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
    SETTINGS = eval(data)
    return SETTINGS


def gen_SETTINGS(file_out) -> dict:
    SETTINGS = {}
    SETTINGS['DATABASES'] = gen_DATABASES()
    SETTINGS['SECRET_KEY'] = gen_SECRET_KEY()
    data = str(SETTINGS)
    tips = '请输入加载配置文件所需的密码(无回显):'
    key = hashlib.md5(getpass(tips).encode('utf8')).hexdigest().encode('utf8')[0:16]
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    return SETTINGS


try:
    # 检查 __pycache__ 文件夹是否存在
    dir = Path.joinpath(Path.cwd(), '__pycache__')
    if not os.path.isdir(dir):
        os.makedirs(dir)
    with open('__pycache__/settings.aes', 'rb') as file_in:
        SETTINGS = read_settings(file_in)

except:
    with open('__pycache__/settings.aes', 'wb') as file_out:
        SETTINGS = gen_SETTINGS(file_out)
        print('已成功加密存储配置文件至 __pycache__/settings.aes')

