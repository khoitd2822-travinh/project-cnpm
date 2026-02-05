import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Routes, Route, useNavigate } from 'react-router-dom'; 
import './App.css';
import AdminDashboard from './AdminDashboard';

const Dashboard = () => {
  const navigate = useNavigate();
  const role = localStorage.getItem('role');
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) navigate('/');
  }, [token, navigate]);

  return (
    <div style={{ padding: '50px', textAlign: 'center' }}>
      <h1>Chào mừng {role} đã vào hệ thống!</h1>
      <button onClick={() => { localStorage.clear(); navigate('/'); }}>Đăng xuất</button>
    </div>
  );
};

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
        
        const checkRole = res.data.user.role.toLowerCase();
        if (checkRole === 'admin' || checkRole === 'chair') {
          navigate('/admin-dashboard');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (err) {
      // HIỆN LỖI THẬT TỪ BACKEND
      const errorDetail = err.response?.data?.detail || "Không thể kết nối Server";
      setMsg("Thất bại: " + errorDetail);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>{isRegister ? "Đăng ký" : "UTH-ConfMS"}</h1>
        <h3>(Hệ thống quản lý hội nghị)</h3>
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
        <p style={{cursor:'pointer', color:'blue'}} onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Đã có tài khoản? Đăng nhập" : "Chưa có tài khoản? Đăng ký"}
        </p>
        {msg && <p style={{color: msg.includes('Thất bại') ? 'red' : 'green'}}>{msg}</p>}
      </form>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<AuthForm />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/admin-dashboard" element={<AdminDashboard />} />
    </Routes>
  );
}

export default App;