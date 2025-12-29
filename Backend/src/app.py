from flask import Flask
#from src.api.controllers.auth_controller import auth_bp
from api.controllers.auth_controller import auth_bp

app = Flask(__name__)

# Đăng ký cổng Login để Frontend có thể gọi vào
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def health_check():
    return "Hệ thống Backend UTH-ConfMS đã sẵn sàng!"

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    app.run(debug=True, port=5000)


#
from flask import Flask
from interface.controller.paper_controller import paper_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(paper_bp)
    return app
#
