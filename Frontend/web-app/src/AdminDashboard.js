import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
    const [activeTab, setActiveTab] = useState('stats');
    const [stats, setStats] = useState({ user_count: 0, conf_count: 0, paper_count: 0, activities: [] });
    const [users, setUsers] = useState([]);

    // 1. Lấy dữ liệu thống kê tổng quan
    const fetchStats = async () => {
        try {
            const res = await axios.get('http://127.0.0.1:5000/api/admin/stats');
            setStats(res.data);
        } catch (err) {
            console.error("Lỗi tải thống kê:", err);
        }
    };

    // 2. Lấy danh sách người dùng
    const fetchUsers = async () => {
        try {
            const res = await axios.get('http://127.0.0.1:5000/api/admin/users');
            setUsers(res.data);
            setActiveTab('users');
        } catch (err) {
            alert("Lỗi tải danh sách người dùng");
        }
    };

    // Cơ chế tự động làm mới thời gian mỗi 10 giây
    useEffect(() => {
        fetchStats(); // Chạy lần đầu khi vào trang

        const interval = setInterval(() => {
            fetchStats(); 
        }, 10000); // 10 giây cập nhật 1 lần để thời gian "X phút trước" luôn mới

        return () => clearInterval(interval); // Dọn dẹp bộ nhớ khi thoát trang
    }, []);

    return (
        <div style={{ display: 'flex', height: '100vh', fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", backgroundColor: '#f4f7f6' }}>
            {/* Sidebar */}
            <div style={{ width: '280px', background: '#2c3e50', color: 'white', padding: '30px 20px', boxShadow: '2px 0 5px rgba(0,0,0,0.1)' }}>
                <h2 style={{ textAlign: 'center', color: '#3498db', marginBottom: '30px' }}>UTH-ConfMS</h2>
                <div style={{ borderTop: '1px solid #3e4f5f', paddingTop: '20px' }}>
                    <div style={menuStyle(activeTab === 'stats')} onClick={() => { fetchStats(); setActiveTab('stats'); }}>📊 Thống kê chung</div>
                    <div style={menuStyle(activeTab === 'users')} onClick={fetchUsers}>👥 Quản lý người dùng</div>
                    <div style={menuStyle(activeTab === 'conferences')} onClick={() => setActiveTab('conferences')}>📅 Quản lý hội nghị</div>
                    <div style={{ padding: '12px 15px', cursor: 'pointer', color: '#ff7675', marginTop: '40px', fontWeight: 'bold' }} onClick={() => window.location.href='/'}>🚪 Đăng xuất</div>
                </div>
            </div>

            {/* Main Content */}
            <div style={{ flex: 1, padding: '40px', overflowY: 'auto' }}>
                {activeTab === 'stats' && (
                    <>
                        <h1 style={{ marginBottom: '30px', color: '#2c3e50' }}>Bảng điều khiển Quản trị viên</h1>
                        
                        {/* Cards Thống kê */}
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '25px' }}>
                            <div style={cardStyle}>
                                <h3 style={{ fontSize: '28px', margin: '0', color: '#2ecc71' }}>1</h3>
                                <p style={{ color: '#7f8c8d', margin: '10px 0 0' }}>Hội nghị thực tế</p>
                            </div>
                            <div style={cardStyle}>
                                <h3 style={{ fontSize: '28px', margin: '0', color: '#3498db' }}>{stats.user_count}</h3>
                                <p style={{ color: '#7f8c8d', margin: '10px 0 0' }}>Người dùng hệ thống</p>
                            </div>
                            <div style={cardStyle}>
                                <h3 style={{ fontSize: '28px', margin: '0', color: '#e74c3c' }}>{stats.paper_count}</h3>
                                <p style={{ color: '#7f8c8d', margin: '10px 0 0' }}>Bài báo chờ duyệt</p>
                            </div>
                        </div>

                        {/* Bảng hoạt động gần đây */}
                        <div style={tableContainer}>
                            <h3 style={{ marginBottom: '20px', color: '#34495e' }}>Hoạt động đăng ký mới nhất</h3>
                            <table style={tableStyle}>
                                <thead>
                                    <tr style={{ borderBottom: '2px solid #f1f1f1' }}>
                                        <th style={{ padding: '15px' }}>Người dùng</th>
                                        <th>Vai trò</th>
                                        <th>Hành động</th>
                                        <th>Thời gian</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {stats.activities.length > 0 ? (
                                        stats.activities.map((act, i) => (
                                            <tr key={i} style={{ borderBottom: '1px solid #f9f9f9' }}>
                                                <td style={{ padding: '15px', fontWeight: '500' }}>{act.name}</td>
                                                <td><span style={roleBadgeStyle}>{act.role}</span></td>
                                                <td><span style={{ color: '#27ae60', fontSize: '14px' }}>● {act.action}</span></td>
                                                <td style={{ color: '#95a5a6', fontSize: '14px' }}>{act.time}</td>
                                            </tr>
                                        ))
                                    ) : (
                                        <tr><td colSpan="4" style={{ textAlign: 'center', padding: '20px', color: '#95a5a6' }}>Chưa có hoạt động nào</td></tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </>
                )}

                {activeTab === 'users' && (
                    <div style={tableContainer}>
                        <h1 style={{ marginBottom: '25px', color: '#2c3e50' }}>Danh sách người dùng</h1>
                        <table style={tableStyle}>
                            <thead style={{ background: '#f8f9fa' }}>
                                <tr>
                                    <th style={{ padding: '15px' }}>ID</th>
                                    <th>Họ tên</th>
                                    <th>Email</th>
                                    <th>Vai trò</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map(u => (
                                    <tr key={u.id} style={{ borderBottom: '1px solid #eee' }}>
                                        <td style={{ padding: '15px', color: '#7f8c8d' }}>{u.id}</td>
                                        <td style={{ fontWeight: 'bold', color: '#2c3e50' }}>{u.name}</td>
                                        <td>{u.email}</td>
                                        <td><span style={roleBadgeStyle}>{u.role.toUpperCase()}</span></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {activeTab === 'conferences' && (
    <div style={{ ...tableContainer, textAlign: 'center', padding: '60px 40px' }}>
        {/* 1. Tiêu đề to và in đậm nằm trên cùng */}
        <h1 style={{ 
            fontSize: '36px', 
            fontWeight: 'bold', 
            color: '#2c3e50', 
            marginBottom: '10px',
            textTransform: 'uppercase',
            letterSpacing: '1px'
        }}>
            Hội nghị nghiên cứu khoa học
        </h1>

        {/* 2. Tên viết tắt hội nghị */}
        <h2 style={{ 
            fontSize: '22px', 
            color: '#3498db', 
            fontWeight: 'bold', 
            marginBottom: '40px' 
        }}>
            UTH-ConfMS
        </h2>

        {/* 3. Logo trường UTH nằm ở dưới */}
        <div style={{ display: 'flex', justifyContent: 'center' }}>
            <img 
                 
                 
                style={{ 
                    width: '550px', 
                    height: 'auto', 
                    filter: 'drop-shadow(0px 4px 8px rgba(0,0,0,0.1))' 
                }} 
            />
        </div>
    </div>
)}
            </div>
        </div>
    );
};

// --- Styles Tối ưu ---
const menuStyle = (active) => ({
    padding: '12px 15px', 
    cursor: 'pointer', 
    marginBottom: '10px', 
    borderRadius: '8px',
    background: active ? '#34495e' : 'transparent',
    color: active ? '#3498db' : '#bdc3c7',
    transition: 'all 0.3s', 
    fontWeight: active ? 'bold' : 'normal',
    display: 'flex',
    alignItems: 'center'
});

const cardStyle = { 
    background: 'white', 
    padding: '30px', 
    borderRadius: '15px', 
    textAlign: 'center', 
    boxShadow: '0 10px 20px rgba(0,0,0,0.05)',
    borderBottom: '4px solid #3498db'
};

const tableContainer = { 
    marginTop: '40px', 
    background: 'white', 
    padding: '30px', 
    borderRadius: '15px', 
    boxShadow: '0 10px 25px rgba(0,0,0,0.05)' 
};

const tableStyle = { width: '100%', borderCollapse: 'collapse', textAlign: 'left' };

const roleBadgeStyle = {
    background: '#ebf5ff',
    color: '#007bff',
    padding: '4px 10px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: 'bold',
    textTransform: 'uppercase'
};

export default AdminDashboard;