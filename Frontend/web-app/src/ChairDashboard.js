import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Styles (Giữ nguyên như thiết kế của bạn)
const containerStyle = { display: 'flex', height: '100vh', backgroundColor: '#f0f2f5' };
const sidebarStyle = { width: '260px', background: '#2c3e50', color: 'white', padding: '20px' };
const mainContentStyle = { flex: 1, padding: '30px', overflowY: 'auto' };
const cardContainerStyle = { background: 'white', padding: '25px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' };
const tableStyle = { width: '100%', borderCollapse: 'collapse' };
const selectStyle = { padding: '5px', borderRadius: '4px', border: '1px solid #ddd', marginRight: '10px', minWidth: '160px' };
const btnStyle = { background: '#3498db', color: 'white', border: 'none', padding: '6px 15px', borderRadius: '4px', cursor: 'pointer' };

const ChairDashboard = ({ user }) => {
    const [allPapers, setAllPapers] = useState([]);
    const [reviewers, setReviewers] = useState([]);
    const [selectedReviewers, setSelectedReviewers] = useState({});

    const fetchData = async () => {
        try {
            const resP = await axios.get('http://127.0.0.1:5000/api/chair/papers');
            setAllPapers(resP.data);

            const resU = await axios.get('http://127.0.0.1:5000/api/admin/users');
            // Lọc cực kỳ an toàn
            const onlyReviewers = resU.data.filter(u => 
                u.role && u.role.toLowerCase().trim() === 'reviewer'
            );
            setReviewers(onlyReviewers);
        } catch (err) {
            console.error("Lỗi tải dữ liệu:", err);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleAssign = async (paperId) => {
        const rid = selectedReviewers[paperId];
        if (!rid) return alert("Vui lòng chọn Reviewer!");
        try {
            await axios.post('http://127.0.0.1:5000/api/chair/assign', {
                paper_id: paperId,
                reviewer_id: parseInt(rid)
            });
            alert("Phân công thành công!");
            fetchData();
        } catch (err) { alert("Lỗi phân công!"); }
    };

    return (
        <div style={containerStyle}>
            <div style={sidebarStyle}>
                <h2>UTH-Chair</h2>
                <div style={{marginTop: '20px', color: '#3498db'}}>⚖️ Quản lý bài báo</div>
                <div style={{marginTop: '40px', cursor: 'pointer'}} onClick={() => window.location.href='/'}>🚪 Đăng xuất</div>
            </div>
            
            <div style={mainContentStyle}>
                <h1>Bảng điều phối của Chair</h1>
                <p>Chào mừng, <strong>{user?.name || "Admin"}</strong>.</p>

                <div style={cardContainerStyle}>
                    <table style={tableStyle}>
                        <thead>
                            <tr style={{borderBottom: '2px solid #eee'}}>
                                <th style={{textAlign: 'left', padding: '12px'}}>Tác giả</th>
                                <th style={{textAlign: 'left'}}>Tiêu đề</th>
                                <th style={{textAlign: 'left'}}>Phân công Reviewer</th>
                            </tr>
                        </thead>
                        <tbody>
                            {allPapers.map(p => (
                                <tr key={p.id} style={{borderBottom: '1px solid #f9f9f9'}}>
                                    <td style={{padding: '12px'}}>{p.author}</td>
                                    <td>{p.title}</td>
                                    <td>
                                        {!p.reviewer_id ? (
                                            <div style={{display: 'flex'}}>
                                                <select 
                                                    style={selectStyle}
                                                    onChange={(e) => setSelectedReviewers({...selectedReviewers, [p.id]: e.target.value})}
                                                    value={selectedReviewers[p.id] || ""}
                                                >
                                                    <option value="">-- Chọn chuyên gia --</option>
                                                    {reviewers.map(r => (
                                                        <option key={r.id} value={r.id}>{r.full_name}</option>
                                                    ))}
                                                </select>
                                                <button style={btnStyle} onClick={() => handleAssign(p.id)}>Xác nhận</button>
                                            </div>
                                        ) : (
                                            <span style={{color: '#2ecc71', fontWeight: 'bold'}}>✅ Đã phân công</span>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ChairDashboard;