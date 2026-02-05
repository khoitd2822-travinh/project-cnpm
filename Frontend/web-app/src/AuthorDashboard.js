import React, { useState, useEffect } from 'react';
import axios from 'axios';

// --- STYLE (Giữ nguyên và bổ sung btnActionStyle) ---
const containerStyle = { display: 'flex', height: '100vh', backgroundColor: '#f0f2f5', fontFamily: 'Arial' };
const sidebarStyle = { width: '260px', background: '#2c3e50', color: 'white', padding: '20px' };
const mainContentStyle = { flex: 1, padding: '30px', overflowY: 'auto' };
const headerStyle = { marginBottom: '30px', borderBottom: '1px solid #ddd', paddingBottom: '10px' };
const cardStyle = { background: 'white', padding: '20px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' };
const tableStyle = { width: '100%', borderCollapse: 'collapse' };
const thStyle = { textAlign: 'left', padding: '12px', color: '#7f8c8d', borderBottom: '2px solid #eee' };
const tdStyle = { padding: '12px', borderBottom: '1px solid #f9f9f9' };
const btnActionStyle = { padding: '8px 16px', borderRadius: '6px', border: 'none', cursor: 'pointer', fontWeight: 'bold', color: 'white', background: '#3498db' };
const menuStyle = (active) => ({
    padding: '12px', borderRadius: '8px', cursor: 'pointer', marginBottom: '10px',
    background: active ? 'rgba(255,255,255,0.1)' : 'transparent',
    color: active ? '#3498db' : '#bdc3c7', fontWeight: active ? 'bold' : 'normal'
});
const logoutStyle = { marginTop: '50px', color: '#e74c3c', cursor: 'pointer', padding: '12px', fontWeight: 'bold' };
const statusBadge = (s) => ({
    padding: '4px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 'bold',
    background: s === 'pending' ? '#fef9e7' : '#eafaf1', color: s === 'pending' ? '#f1c40f' : '#2ecc71'
});

const AuthorDashboard = ({ user }) => {
    const [papers, setPapers] = useState([]);
    const [activeTab, setActiveTab] = useState('my-papers');
    const [newPaper, setNewPaper] = useState({ title: '' });

    // 1. Lấy danh sách bài báo
    const fetchPapers = async () => {
        try {
            const res = await axios.get(`http://127.0.0.1:5000/api/author/papers/${user.id}`);
            setPapers(res.data);
        } catch (err) { console.error("Lỗi lấy dữ liệu:", err); }
    };

    useEffect(() => {
        if (user?.id) fetchPapers();
    }, [user]);

    // 2. Xử lý nộp bài
    const handleSubmitPaper = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://127.0.0.1:5000/api/author/submit', {
                title: newPaper.title,
                author_id: user.id
            });
            alert("Nộp bài thành công!");
            setNewPaper({ title: '' }); // Reset form
            fetchPapers(); // Cập nhật lại danh sách ngay lập tức
            setActiveTab('my-papers'); // Quay về tab danh sách
        } catch (err) {
            alert("Lỗi khi nộp bài. Bạn đã tạo API Backend chưa?");
        }
    };

    return (
        <div style={containerStyle}>
            {/* SIDEBAR */}
<div style={sidebarStyle}>
                <h2 style={{ color: '#3498db', textAlign: 'center', marginBottom: '30px' }}>UTH-Author</h2>
                <div style={menuStyle(activeTab === 'my-papers')} onClick={() => setActiveTab('my-papers')}>📄 Bài của tôi</div>
                <div style={menuStyle(activeTab === 'submit')} onClick={() => setActiveTab('submit')}>📤 Nộp bài mới</div>
                <div style={logoutStyle} onClick={() => window.location.href='/'}>🚪 Đăng xuất</div>
            </div>

            {/* NỘI DUNG CHÍNH */}
            <div style={mainContentStyle}>
                <header style={headerStyle}>
                    <h1>Bảng điều khiển Tác giả</h1>
                    <p>Chào, <strong>{user?.name || "Người dùng"}</strong></p>
                </header>

                {activeTab === 'my-papers' ? (
                    <div style={cardStyle}>
                        <h3 style={{ marginBottom: '20px' }}>Danh sách bài báo đã nộp</h3>
                        <table style={tableStyle}>
    <thead>
        <tr>
            <th style={thStyle}>ID</th>
            <th style={thStyle}>Tiêu đề bài báo</th>
            <th style={thStyle}>Trạng thái</th>
            <th style={thStyle}>Điểm</th>      {/* CỘT MỚI */}
            <th style={thStyle}>Nhận xét</th>  {/* CỘT MỚI */}
        </tr>
    </thead>
    <tbody>
        {papers.length > 0 ? (
            papers.map((p) => (
                <tr key={p.id}>
                    <td style={tdStyle}>{p.id}</td>
                    <td style={{ ...tdStyle, fontWeight: '500' }}>{p.title}</td>
                    <td style={tdStyle}>
                        <span style={statusBadge(p.status)}>{(p.status || 'pending').toUpperCase()}</span>
                    </td>
                    {/* HIỂN THỊ ĐIỂM SỐ */}
                    <td style={{ ...tdStyle, color: '#2ecc71', fontWeight: 'bold' }}>
                        {p.score !== null ? p.score : "-"}
                    </td>
                    {/* HIỂN THỊ NHẬN XÉT */}
                    <td style={{ ...tdStyle, fontStyle: 'italic', fontSize: '13px', color: '#7f8c8d' }}>
                        {p.comments || "Đang chờ phản hồi..."}
                    </td>
                </tr>
            ))
        ) : (
            <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '30px', color: '#999' }}>
                    Bạn chưa nộp bài báo nào.
                </td>
            </tr>
        )}
    </tbody>
</table>
                    </div>
                ) : (
                    /* GIAO DIỆN NỘP BÀI */
                    <div style={cardStyle}>
                        <h3 style={{ marginBottom: '20px' }}>Nộp bài báo mới</h3>
                        <form onSubmit={handleSubmitPaper}>
                            <div style={{ marginBottom: '20px' }}>
                                <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Tiêu đề bài báo:</label>
                                <input 
type="text" 
                                    style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ddd', boxSizing: 'border-box' }}
                                    placeholder="Nhập tiêu đề nghiên cứu của bạn..."
                                    value={newPaper.title}
                                    onChange={(e) => setNewPaper({ title: e.target.value })}
                                    required 
                                />
                            </div>
                            <div style={{ marginBottom: '25px', padding: '40px', border: '2px dashed #3498db', borderRadius: '12px', textAlign: 'center', backgroundColor: '#f8fbff' }}>
                                <p style={{ color: '#3498db', marginBottom: '10px' }}>📁 Kéo thả file PDF/Docx hoặc bấm chọn file</p>
                                <input type="file" />
                            </div>
                            <button type="submit" style={{ ...btnActionStyle, width: '100%', padding: '15px', fontSize: '16px' }}>🚀 GỬI BÀI BÁO</button>
                            <button type="button" onClick={() => setActiveTab('my-papers')} style={{ width: '100%', background: 'none', border: 'none', color: '#7f8c8d', marginTop: '10px', cursor: 'pointer' }}>Hủy bỏ</button>
                        </form>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AuthorDashboard;
