import React, { useState } from 'react';
import axios from 'axios';
import { Routes, Route, useNavigate } from 'react-router-dom'; 
import './App.css';

/** * TRANG DASHBOARD TẠM THỜI 
 * Đây là "điểm bàn giao": Bạn của bạn sẽ thay thế nội dung 
 * bên trong component này bằng giao diện họ làm.
 */
const Dashboard = () => {
  const navigate = useNavigate();
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.clear(); // Xóa sạch dấu vết đăng nhập
    navigate('/');        // Quay về trang login
  };

  return (
    <div style={{ padding: '50px', textAlign: 'center', fontFamily: 'Arial' }}>
      <h1 style={{ color: '#007bff' }}>Chào mừng đã vào hệ thống UTH-ConfMS!</h1>
      <div style={{ 
        background: '#ffffff', 
        padding: '30px', 
        borderRadius: '12px', 
        display: 'inline-block',
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
        textAlign: 'left'
      }}>
        <p><strong>🔹 Trạng thái:</strong> Đăng nhập thành công</p>
        <p><strong>🔹 Quyền hạn (Role):</strong> <span style={{color: 'green'}}>{role}</span></p>
        <p><strong>🔹 Token:</strong> {token ? "Đã lưu trong LocalStorage ✅" : "Lỗi không tìm thấy Token ❌"}</p>
      </div>
      <br /><br />
      <button 
        onClick={handleLogout} 
        style={{ 
          padding: '10px 25px', 
          backgroundColor: '#dc3545', 
          color: 'white', 
          border: 'none', 
          borderRadius: '5px', 
          cursor: 'pointer' 
        }}
      >
        Đăng xuất
      </button>
    </div>
  );
};

/**
 * COMPONENT XỬ LÝ ĐĂNG NHẬP & ĐĂNG KÝ
 * Đây là phần task chính của bạn.
 */
function AuthForm() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [msg, setMsg] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isRegister) {
        // LUỒNG ĐĂNG KÝ
        await axios.post('http://127.0.0.1:5000/auth/register', form);
        setMsg("Đăng ký thành công! Đang chuyển sang Đăng nhập...");
        setTimeout(() => {
          setIsRegister(false);
          setMsg('');
        }, 2000);
      } else {
        // LUỒNG ĐĂNG NHẬP
        const res = await axios.post('http://127.0.0.1:5000/auth/login', {
          email: form.email,
          password: form.password
        });

        if (res.status === 200) {
          // LƯU DỮ LIỆU ĐỂ NHÓM SỬ DỤNG CHUNG
          localStorage.setItem('token', res.data.token);
          localStorage.setItem('role', res.data.role);

          setMsg(`Đăng nhập thành công! Xin chào ${res.data.role}.`);

          // ĐIỀU HƯỚNG VÀO TRONG (Về đích task Login)
          setTimeout(() => {
            navigate('/dashboard'); 
          }, 1200);
        }
      }
    } catch (err) {
      setMsg("Lỗi: " + (err.response?.data?.message || "Không thể kết nối Server"));
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>{isRegister ? "UTH-ConfMS Register" : "UTH-ConfMS Login"}</h2>
        <p>Hệ thống quản lý giấy tờ hội nghị</p>

        {isRegister && (
          <input 
            type="text" 
            placeholder="Họ và tên" 
            value={form.full_name}
            onChange={e => setForm({...form, full_name: e.target.value})} 
            required 
          />
        )}

        <input 
          type="email" 
          placeholder="Email (Tên đăng nhập)" 
          value={form.email}
          onChange={e => setForm({...form, email: e.target.value})} 
          required 
        />
        
        <input 
          type="password" 
          placeholder="Mật khẩu" 
          value={form.password}
          onChange={e => setForm({...form, password: e.target.value})} 
          required 
        />

        <button type="submit">{isRegister ? "Đăng ký" : "Đăng nhập"}</button>

        <p style={{ cursor: 'pointer', color: '#007bff', marginTop: '15px', fontSize: '14px' }} 
            onClick={() => { setIsRegister(!isRegister); setMsg(''); }}>
          {isRegister ? "Đã có tài khoản? Đăng nhập ngay" : "Chưa có tài khoản? Đăng ký ngay"}
        </p>

        {msg && (
          <p className="message" style={{ color: msg.includes('Lỗi') ? '#dc3545' : '#28a745', fontWeight: 'bold' }}>
            {msg}
          </p>
        )}
      </form>
    </div>
  );
}

// COMPONENT CHÍNH
function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthForm />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;