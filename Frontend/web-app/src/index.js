import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom' // Thêm dòng này
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter> {/* Bao bọc App lại như thế này */}
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)