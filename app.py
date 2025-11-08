from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import encryption_utils

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Đổi key này trong production

# Cấu hình
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Tạo thư mục uploads nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Kiểm tra file có được phép upload không
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Trang chủ
    """
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    """
    Trang mã hóa file
    """
    if request.method == 'POST':
        # Kiểm tra file có được upload không
        if 'file' not in request.files:
            flash('Chưa chọn file!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        password = request.form.get('password')
        
        # Kiểm tra file và password
        if file.filename == '':
            flash('Chưa chọn file!', 'error')
            return redirect(request.url)
        
        if not password:
            flash('Chưa nhập password!', 'error')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash(f'File không được hỗ trợ! Chỉ chấp nhận: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(request.url)
        
        # Lưu file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Mã hóa file
        output_filename = filename + '.encrypted'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        success, message = encryption_utils.encrypt_file(input_path, output_path, password)
        
        if success:
            # Xóa file gốc
            os.remove(input_path)
            
            flash(f'✅ {message}', 'success')
            flash(f'📦 File đã mã hóa: {output_filename}', 'info')
            
            # Gửi file về cho user
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename
            )
        else:
            flash(f'❌ {message}', 'error')
            # Xóa file nếu có lỗi
            if os.path.exists(input_path):
                os.remove(input_path)
            return redirect(request.url)
    
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    """
    Trang giải mã file
    """
    if request.method == 'POST':
        # Kiểm tra file có được upload không
        if 'file' not in request.files:
            flash('Chưa chọn file!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        password = request.form.get('password')
        
        # Kiểm tra file và password
        if file.filename == '':
            flash('Chưa chọn file!', 'error')
            return redirect(request.url)
        
        if not password:
            flash('Chưa nhập password!', 'error')
            return redirect(request.url)
        
        # Lưu file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Giải mã file
        # Bỏ .encrypted khỏi tên file
        if filename.endswith('.encrypted'):
            output_filename = filename[:-10]
        else:
            output_filename = filename + '.decrypted'
        
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        success, message = encryption_utils.decrypt_file(input_path, output_path, password)
        
        if success:
            # Xóa file đã mã hóa
            os.remove(input_path)
            
            flash(f'✅ {message}', 'success')
            flash(f'📦 File gốc: {output_filename}', 'info')
            
            # Gửi file về cho user
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename
            )
        else:
            flash(f'❌ {message}', 'error')
            # Xóa file nếu có lỗi
            if os.path.exists(input_path):
                os.remove(input_path)
            return redirect(request.url)
    
    return render_template('decrypt.html')

@app.route('/about')
def about():
    """
    Trang giới thiệu
    """
    return render_template('about.html')

# Xóa file tạm sau khi gửi
@app.after_request
def cleanup(response):
    """
    Dọn dẹp file tạm sau mỗi request
    """
    try:
        # Xóa các file cũ hơn 1 giờ
        import time
        current_time = time.time()
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                # Xóa file cũ hơn 3600 giây (1 giờ)
                if file_age > 3600:
                    os.remove(filepath)
    except:
        pass
    
    return response

if __name__ == '__main__':
    # Chạy app ở chế độ debug
    app.run(debug=True, host='0.0.0.0', port=5000)