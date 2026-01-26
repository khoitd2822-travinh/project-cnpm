import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const containerStyle = { display: 'flex', height: '100vh', backgroundColor: '#f4f7f6' };
const sidebarStyle = { width: '260px', background: '#2c3e50', color: 'white', padding: '20px', display: 'flex', flexDirection: 'column' };
const mainContentStyle = { flex: 1, padding: '30px', overflowY: 'auto' };

const rowStyle = { 
    background: 'white', padding: '15px 25px', borderRadius: '8px', marginBottom: '10px', 
    display: 'flex', alignItems: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: '4px solid #2ecc71' 
};

const colStyle = (flexValue) => ({ flex: flexValue, display: 'flex', flexDirection: 'column', padding: '0 10px' });
const labelHeaderStyle = { fontSize: '0.7rem', color: '#95a5a6', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '4px' };

// Style cho Modal chấm điểm
const modalOverlayStyle = { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 };
const modalContentStyle = { background: 'white', padding: '30px', borderRadius: '12px', width: '400px', boxShadow: '0 10px 25px rgba(0,0,0,0.2)' };

const ReviewerDashboard = ({ user }) => {
    const [tasks, setTasks] = useState([]);
    const [selectedPaper, setSelectedPaper] = useState(null); // Bài báo đang được chọn để chấm hoặc xem lại
    const [reviewData, setReviewData] = useState({ score: '', comment: '' });

    const fetchTasks = useCallback(async () => {
        if (!user?.id) return;
        try {
            const res = await axios.get(`http://127.0.0.1:5000/api/reviewer/tasks/${user.id}`);
            setTasks(res.data);
        } catch (err) { console.error("Lỗi tải dữ liệu"); }
    }, [user?.id]);

    useEffect(() => { fetchTasks(); }, [fetchTasks]);

    // ...existing code...

const handleSubmitReview = async () => {
    if (!reviewData.score || !reviewData.comment) 
        return alert("Vui lòng nhập đầy đủ điểm và nhận xét!");
    try {
        await axios.post('http://127.0.0.1:5000/api/reviewer/submit-review', {
            paper_id: selectedPaper.id,
            reviewer_id: parseInt(user.id),
            score: parseFloat(reviewData.score),  // Thay đổi thành parseFloat
            comment: reviewData.comment
        });
        alert("Gửi đánh giá thành công!");
        setSelectedPaper(null);
        setReviewData({ score: '', comment: '' });
        fetchTasks();
    } catch (err) { 
        console.error(err);
        alert("Lỗi khi gửi đánh giá!"); 
    }
};

// ...existing code...

    return (
        <div style={containerStyle}>
            {/* SIDEBAR */}
            <div style={sidebarStyle}>
                <h2 style={{ color: '#2ecc71', textAlign: 'center', marginBottom: '30px' }}>UTH-Reviewer</h2>
                <div style={{ padding: '12px', background: 'rgba(255,255,255,0.1)', borderRadius: '8px', cursor: 'pointer', marginBottom: '10px', display: 'flex', alignItems: 'center' }}>
                    <span style={{ marginRight: '10px' }}>📝</span> Nhiệm vụ
                </div>
                <div 
                    style={{ padding: '12px', color: '#ff4d4d', cursor: 'pointer', fontWeight: 'bold', display: 'flex', alignItems: 'center' }}
                    onClick={() => window.location.href='/'}
                >
                    <span style={{ marginRight: '10px' }}>🚪</span> Đăng xuất
                </div>
            </div>

            {/* MAIN CONTENT */}
            <div style={mainContentStyle}>
                <header style={{ marginBottom: '30px' }}>
                    <h1>Trang chủ phản biện</h1>
                    <p>Chuyên gia: <strong>{user?.name || "Chưa xác định"}</strong></p>
                </header>

                <h3 style={{ marginBottom: '20px' }}>Bài báo được giao</h3>

                {tasks.length > 0 ? (
                    <div>
                        {tasks.map((t, index) => (
                            <div key={t.id} style={rowStyle}>
                                <div style={colStyle(0.5)}>
                                    <span style={labelHeaderStyle}>STT</span>
                                    <span style={{ fontWeight: 'bold' }}>{index + 1}</span>
                                </div>
                                <div style={colStyle(3)}>
                                    <span style={labelHeaderStyle}>Tiêu đề</span>
                                    <span style={{ fontWeight: '600' }}>{t.title}</span>
                                </div>
                                <div style={colStyle(2)}>
                                    <span style={labelHeaderStyle}>Tác giả</span>
                                    <span style={{ color: '#2c3e50', fontWeight: '500' }}>{t.author}</span>
                                </div>
                                <div style={colStyle(1.5)}>
                                    <span style={labelHeaderStyle}>Trạng thái</span>
                                    <span style={{ color: t.status === 'Đã chấm' ? '#27ae60' : '#f39c12', fontWeight: 'bold' }}>
                                        {t.status === 'Đã chấm' ? '● Đã hoàn tất' : '○ Chờ chấm'}
                                    </span>
                                </div>
                                <div style={{ flex: 1, textAlign: 'right' }}>
                                    {t.status !== 'Đã chấm' ? (
                                        <button 
                                            onClick={() => setSelectedPaper(t)}
                                            style={{ background: '#2ecc71', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
                                        >Chấm bài</button>
                                    ) : (
                                        <button 
                                            onClick={() => setSelectedPaper(t)}
                                            style={{ background: '#3498db', color: 'white', border: 'none', padding: '8px 16px', borderRadius: '4px', cursor: 'pointer' }}
                                        >Xem lại</button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : <p>Không có bài báo nào.</p>}
            </div>

            {/* MODAL CHẤM ĐIỂM / XEM LẠI */}
            {selectedPaper && (
                <div style={modalOverlayStyle}>
                    <div style={modalContentStyle}>
                        <h3>{selectedPaper.status === 'Đã chấm' ? "Kết quả phản biện" : "Đánh giá bài báo"}</h3>
                        <p style={{ fontSize: '0.9rem', color: '#666' }}>Bài báo: <strong>{selectedPaper.title}</strong></p>
                        
                        <div style={{ marginTop: '20px' }}>
                            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Điểm số (0-10):</label>
                            <input 
                                type="number" 
                                disabled={selectedPaper.status === 'Đã chấm'}
                                value={selectedPaper.status === 'Đã chấm' ? selectedPaper.score : reviewData.score}
                                onChange={(e) => setReviewData({...reviewData, score: e.target.value})}
                                style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
                            />
                        </div>

                        <div style={{ marginTop: '15px' }}>
                            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Nhận xét:</label>
                            <textarea 
                                rows="4"
                                disabled={selectedPaper.status === 'Đã chấm'}
                                value={selectedPaper.status === 'Đã chấm' ? selectedPaper.comment : reviewData.comment}
                                onChange={(e) => setReviewData({...reviewData, comment: e.target.value})}
                                style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #ddd' }}
                            ></textarea>
                        </div>

                        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                            <button onClick={() => setSelectedPaper(null)} style={{ padding: '8px 16px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Đóng</button>
                            {selectedPaper.status !== 'Đã chấm' && (
                                <button onClick={handleSubmitReview} style={{ padding: '8px 16px', border: 'none', borderRadius: '4px', background: '#2ecc71', color: 'white', cursor: 'pointer' }}>Gửi đánh giá</button>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ReviewerDashboard;