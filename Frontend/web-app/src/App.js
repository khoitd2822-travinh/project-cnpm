import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Kết nối tới Backend đang chạy ở cổng 5000
      const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
        email: email,
        password: password
      });
      alert('Đăng nhập thành công! Quyền: ' + response.data.role);
    } catch (error) {
      alert('Đăng nhập thất bại. Kiểm tra lại tài khoản hoặc kết nối Backend!');
    }
  };

  return (
    <div style={{ padding: '50px', textAlign: 'center', backgroundColor: '#f0f2f5', minHeight: '100vh' }}>
      <div style={{ display: 'inline-block', padding: '40px', backgroundColor: 'white', borderRadius: '10px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
        <h2 style={{ color: '#1877f2', marginBottom: '20px' }}>HỆ THỐNG UTH-ConfMS</h2>
        <form onSubmit={handleLogin}>
          <input type="email" placeholder="Email đăng nhập" required
            style={{ display: 'block', margin: '15px auto', padding: '12px', width: '280px', borderRadius: '5px', border: '1px solid #ddd' }}
            onChange={(e) => setEmail(e.target.value)} 
          />
          <input type="password" placeholder="Mật khẩu" required
            style={{ display: 'block', margin: '15px auto', padding: '12px', width: '280px', borderRadius: '5px', border: '1px solid #ddd' }}
            onChange={(e) => setPassword(e.target.value)} 
          />
          <button type="submit" 
            style={{ padding: '12px 40px', backgroundColor: '#1877f2', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold', width: '100%' }}>
            ĐĂNG NHẬP
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;