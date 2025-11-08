from cryptography.fernet import Fernet
import base64
import hashlib
import os

def generate_key_from_password(password):
    """
    Tạo key mã hóa từ password
    """
    password_bytes = password.encode('utf-8')
    key_hash = hashlib.sha256(password_bytes).digest()
    key = base64.urlsafe_b64encode(key_hash)
    return key

def encrypt_file(input_path, output_path, password):
    """
    Mã hóa file
    Returns: (success: bool, message: str)
    """
    try:
        # Đọc file
        with open(input_path, 'rb') as f:
            file_data = f.read()
        
        # Mã hóa
        key = generate_key_from_password(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        
        # Ghi file mã hóa
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        return True, "Mã hóa thành công!"
        
    except Exception as e:
        return False, f"Lỗi mã hóa: {str(e)}"

def decrypt_file(input_path, output_path, password):
    """
    Giải mã file
    Returns: (success: bool, message: str)
    """
    try:
        # Đọc file đã mã hóa
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Giải mã
        key = generate_key_from_password(password)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Ghi file gốc
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return True, "Giải mã thành công!"
        
    except Exception as e:
        return False, f"Lỗi giải mã: Sai password hoặc file bị hỏng"

def get_file_size(filepath):
    """
    Lấy kích thước file
    """
    size = os.path.getsize(filepath)
    # Chuyển đổi sang đơn vị phù hợp
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{size/1024:.2f} KB"
    else:
        return f"{size/(1024*1024):.2f} MB"