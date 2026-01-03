import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Routes, Route, useNavigate } from 'react-router-dom'; 
import './App.css';

// --- COMPONENT DASHBOARD ---
const Dashboard = () => {
  const navigate = useNavigate();
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      navigate('/');
    }
  }, [token, navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');        
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
        <p><strong>🔹 Trạng thái:</strong> Đăng nhập thành công ✅</p>
        <p><strong>🔹 Quyền hạn (Role):</strong> 
          <span style={{color: 'green', fontWeight: 'bold', marginLeft: '5px'}}>
            {role && role !== 'undefined' ? role.toUpperCase() : "ĐANG TẢI VAI TRÒ..."}
          </span>
        </p>
        <p><strong>🔹 Token:</strong> {token ? "Đã xác thực hệ thống ✅" : "Lỗi không tìm thấy Token ❌"}</p>
      </div>
      <br /><br />
      <button 
        onClick={handleLogout} 
        style={{ padding: '10px 25px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
      >
        Đăng xuất
      </button>
    </div>
  );
};

// --- COMPONENT FORM ĐĂNG NHẬP/ĐĂNG KÝ ---
function AuthForm() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '', role: 'author' });
  const [msg, setMsg] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const API_BASE_URL = 'http://127.0.0.1:5000/auth';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("Đang kết nối đến máy chủ...");
    
    try {
      if (isRegister) {
        await axios.post(`${API_BASE_URL}/register`, form);
        setMsg("Đăng ký thành công! Đang chuyển sang Đăng nhập...");
        setTimeout(() => {
          setIsRegister(false);
          setMsg('');
        }, 2000);
      } else {
        const res = await axios.post(`${API_BASE_URL}/login`, {
          email: form.email,
          password: form.password
        });

        if (res.status === 200) {
          localStorage.clear();
          let userRole = res.data.role || (res.data.roles && res.data.roles[0]) || "user";
          localStorage.setItem('token', res.data.token);
          localStorage.setItem('role', userRole);
          setMsg(`Đăng nhập thành công! Xin chào ${userRole}.`);
          setTimeout(() => { navigate('/dashboard'); }, 1000);
        }
      }
    } catch (err) {
      const errorDetail = err.response?.data?.error || err.response?.data?.message || "Máy chủ không phản hồi.";
      setMsg("Lỗi: " + errorDetail);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2 style={{marginBottom: '10px'}}>{isRegister ? "UTH-ConfMS Register" : "UTH-ConfMS Login"}</h2>
        
        {isRegister && (
          <>
            <input 
              type="text" 
              placeholder="Họ và tên" 
              className="input-field"
              value={form.full_name}
              onChange={e => setForm({...form, full_name: e.target.value})} 
              required 
            />
            <div style={{ textAlign: 'left', marginBottom: '15px' }}>
              <label style={{ fontSize: '13px', color: '#555', fontWeight: 'bold' }}>Vai trò:</label>
              <select 
                className="input-field" 
                style={{ marginTop: '5px' }}
                value={form.role}
                onChange={e => setForm({...form, role: e.target.value})}
              >
                <option value="author">Author (Tác giả)</option>
                <option value="reviewer">Reviewer (Người phản biện)</option>
                <option value="chair">Chair (Chủ tọa)</option>
                <option value="admin">Admin (Quản trị viên)</option>
              </select>
            </div>
          </>
        )}

        <input 
          type="email" 
          placeholder="Email" 
          className="input-field"
          value={form.email}
          onChange={e => setForm({...form, email: e.target.value})} 
          required 
        />
        
        <input 
          type="password" 
          placeholder="Mật khẩu" 
          className="input-field"
          value={form.password}
          onChange={e => setForm({...form, password: e.target.value})} 
          required 
        />

        <button type="submit" className="submit-btn">
          {isRegister ? "TẠO TÀI KHOẢN MỚI" : "ĐĂNG NHẬP HỆ THỐNG"}
        </button>

        <p style={{ cursor: 'pointer', color: '#007bff', marginTop: '20px' }} 
            onClick={() => { setIsRegister(!isRegister); setMsg(''); }}>
          {isRegister ? "Đã có tài khoản? Đăng nhập ngay" : "Chưa có tài khoản? Đăng ký ngay"}
        </p>

        {msg && <p style={{ marginTop: '15px', color: msg.includes('Lỗi') ? 'red' : 'green' }}>{msg}</p>}
      </form>
    </div>
  );
}

// --- COMPONENT CHÍNH ---
// QUAN TRỌNG: Dòng export default này phải có ở cuối file
function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthForm />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;