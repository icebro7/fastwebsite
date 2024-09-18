from passlib import pwd
from passlib.context import CryptContext

# 创建一个密码加密上下文，使用 Argon2 算法进行加密
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# 验证明文与哈希密码是否匹配
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码的哈希值
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 生成一个随机密码
def generate_password() -> str:
    return pwd.genword()
