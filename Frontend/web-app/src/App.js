import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Routes, Route, useNavigate } from 'react-router-dom'; 
import './App.css';

// IMPORT TẤT CẢ CÁC DASHBOARD
import AdminDashboard from './AdminDashboard';
import AuthorDashboard from './AuthorDashboard';
import ChairDashboard from './ChairDashboard';
import ReviewerDashboard from './ReviewerDashboard';

function AuthForm() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '', role: 'author' });
  const [msg, setMsg] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const navigate = useNavigate();

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:5000/api'; 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("Đang xử lý...");
    try {
      if (isRegister) {
        await axios.post(`${API_BASE_URL}/register`, {
          full_name: form.full_name,
          email: form.email,
          password: form.password,
          role: form.role
        });
        setMsg("Đăng ký thành công! Hãy đăng nhập.");
        setIsRegister(false);
      } else {
        const res = await axios.post(`${API_BASE_URL}/login`, {
          username: form.email, 
          password: form.password
        });

        localStorage.setItem('token', res.data.token);
        localStorage.setItem('role', res.data.user.role);
        localStorage.setItem('userId', res.data.user.id);
        localStorage.setItem('userName', res.data.user.name);
        
        const checkRole = res.data.user.role.toLowerCase();
        
        if (checkRole === 'admin') navigate('/admin-dashboard');
        else if (checkRole === 'author') navigate('/author-dashboard');
        else if (checkRole === 'chair') navigate('/chair-dashboard');
        else if (checkRole === 'reviewer') navigate('/reviewer-dashboard');
        else navigate('/');
      }
    } catch (err) {
      const errorDetail = err.response?.data?.detail || "Không thể kết nối Server";
      setMsg("Thất bại: " + errorDetail);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        {/* GIỮ NGUYÊN TIÊU ĐỀ VÀ THÊM DÒNG CHỮ DƯỚI */}
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
            <h1 style={{ margin: 0 }}>UTH-ConfMS</h1>
            <p style={{ 
                fontSize: '18px', 
                color: '#444', 
                marginTop: '5px',
                fontWeight: 'bold',    /* In đậm */
                fontStyle: 'italic'    /* In nghiêng */
            }}>
                (Hệ thống quản lý hội nghị)
            </p>
        </div>

        {isRegister && (
          <>
            <input type="text" placeholder="Họ tên" className="input-field" onChange={e => setForm({...form, full_name: e.target.value})} required />
            <select className="input-field" value={form.role} onChange={e => setForm({...form, role: e.target.value})}>
              <option value="author">Author</option>
              <option value="reviewer">Reviewer</option>
              <option value="chair">Chair</option>
              <option value="admin">Admin</option>
            </select>
          </>
        )}
        <input type="email" placeholder="Email" className="input-field" onChange={e => setForm({...form, email: e.target.value})} required />
        <input type="password" placeholder="Mật khẩu" className="input-field" onChange={e => setForm({...form, password: e.target.value})} required />
        <button type="submit" className="submit-btn">{isRegister ? "TẠO TÀI KHOẢN" : "ĐĂNG NHẬP"}</button>
        <p style={{cursor:'pointer', color:'blue', textAlign: 'center'}} onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Đã có tài khoản? Đăng nhập" : "Chưa có tài khoản? Đăng ký"}
        </p>
        {msg && <p style={{textAlign: 'center', color: msg.includes('Thất bại') ? 'red' : 'green'}}>{msg}</p>}
      </form>
    </div>
  );
}

const UserProvider = ({ Component }) => {
    const user = {
        id: localStorage.getItem('userId'),
        name: localStorage.getItem('userName'),
        role: localStorage.getItem('role')
    };
    return <Component user={user} />;
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthForm />} />
      <Route path="/admin-dashboard" element={<AdminDashboard />} />
      <Route path="/author-dashboard" element={<UserProvider Component={AuthorDashboard} />} />
      <Route path="/chair-dashboard" element={<UserProvider Component={ChairDashboard} />} />
      <Route path="/reviewer-dashboard" element={<UserProvider Component={ReviewerDashboard} />} />
    </Routes>
  );
}

export default App;