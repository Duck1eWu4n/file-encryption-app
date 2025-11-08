// File Upload Display
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileDisplay = document.getElementById('fileDisplay');
    const fileInfo = document.getElementById('fileInfo');
    
    if (fileInput && fileDisplay) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                fileInfo.textContent = `✓ ${file.name} (${sizeMB} MB)`;
                fileDisplay.style.borderColor = '#28a745';
                fileDisplay.style.background = '#d4edda';
            }
        });
        
        // Drag and drop
        fileDisplay.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileDisplay.style.borderColor = '#667eea';
            fileDisplay.style.background = '#f0f4ff';
        });
        
        fileDisplay.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileDisplay.style.borderColor = '#dee2e6';
            fileDisplay.style.background = '#f8f9fa';
        });
        
        fileDisplay.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                const event = new Event('change');
                fileInput.dispatchEvent(event);
            }
        });
    }
    
    // Password Strength Checker
    const passwordInput = document.getElementById('password');
    const passwordStrength = document.getElementById('passwordStrength');
    
    if (passwordInput && passwordStrength) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            // Kiểm tra độ dài
            if (password.length >= 8) strength++;
            if (password.length >= 12) strength++;
            
            // Kiểm tra chữ hoa
            if (/[A-Z]/.test(password)) strength++;
            
            // Kiểm tra chữ thường
            if (/[a-z]/.test(password)) strength++;
            
            // Kiểm tra số
            if (/[0-9]/.test(password)) strength++;
            
            // Kiểm tra ký tự đặc biệt
            if (/[^A-Za-z0-9]/.test(password)) strength++;
            
            // Hiển thị độ mạnh
            passwordStrength.className = 'password-strength';
            if (strength <= 2) {
                passwordStrength.classList.add('weak');
            } else if (strength <= 4) {
                passwordStrength.classList.add('medium');
            } else {
                passwordStrength.classList.add('strong');
            }
        });
    }
    
    // Confirm Password Validation
    const encryptForm = document.getElementById('encryptForm');
    const confirmPassword = document.getElementById('confirmPassword');
    
    if (encryptForm && confirmPassword) {
        encryptForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirm = confirmPassword.value;
            
            if (password !== confirm) {
                e.preventDefault();
                alert('❌ Password không khớp! Vui lòng nhập lại.');
                confirmPassword.focus();
                confirmPassword.style.borderColor = '#dc3545';
                return false;
            }
            
            // Xác nhận trước khi submit
            if (!confirm('Bạn đã ghi nhớ password chưa? Không thể khôi phục nếu quên!')) {
                e.preventDefault();
                return false;
            }
            
            // Hiển thị loading
            const submitBtn = encryptForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Đang mã hóa...';
        });
        
        confirmPassword.addEventListener('input', function() {
            this.style.borderColor = '#dee2e6';
        });
    }
    
    // Decrypt Form Loading
    const decryptForm = document.getElementById('decryptForm');
    
    if (decryptForm) {
        decryptForm.addEventListener('submit', function(e) {
            const submitBtn = decryptForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Đang giải mã...';
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});