from ecdsa import SigningKey, SECP256k1, VerifyingKey
import hashlib


class Wallet:
    def __init__(self):
        # 生成私钥
        self.private_key = SigningKey.generate(curve=SECP256k1)
        # 生成公钥
        self.public_key = self.private_key.get_verifying_key()

    def sign(self, message: str) -> str:
        """用私钥对 message 签名 -> 返回 hex"""
        signature = self.private_key.sign(message.encode())
        return signature.hex()

    @staticmethod
    def from_private_key(private_key_hex):
        """根据私钥恢复钱包"""
        private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        w = Wallet()
        w.private_key = private_key
        w.public_key = private_key.get_verifying_key()
        return w

    @staticmethod
    def verify(public_key_hex: str, message: str, signature_hex: str) -> bool:
        """校验签名：pubkey 验证 message 是否由私钥签名"""
        try:
            pub_bytes = bytes.fromhex(public_key_hex)
            sig_bytes = bytes.fromhex(signature_hex)

            vk = VerifyingKey.from_string(pub_bytes, curve=SECP256k1)
            return vk.verify(sig_bytes, message.encode())
        except Exception:
            return False

    def get_address(self) -> str:
        """钱包地址 = SHA256(pubkey)[前40字节]"""
        pub_hex = self.public_key.to_string().hex()
        return hashlib.sha256(pub_hex.encode()).hexdigest()[:40]

    def export_private_key(self):
        return self.private_key.to_string().hex()

    def export_public_key(self):
        return self.public_key.to_string().hex()
