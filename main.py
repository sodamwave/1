from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 이미지 파일 확장자 목록
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '파일이 선택되지 않았습니다'
        
        file = request.files['file']
        if file.filename == '':
            return '파일이 선택되지 않았습니다'
            
        if file:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload_file'))
    
    files_with_time = []
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        mtime = os.path.getmtime(file_path)
        date_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        # 파일 확장자 확인
        is_image = os.path.splitext(file.lower())[1] in IMAGE_EXTENSIONS
        files_with_time.append({
            'name': file, 
            'date_time': date_time,
            'is_image': is_image
        })
    
    files_with_time.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x['name'])), reverse=True)
    return render_template('upload.html', files=files_with_time)

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('upload_file'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)