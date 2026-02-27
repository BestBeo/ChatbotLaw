Đây là nội dung file README.md, bạn có thể copy và tạo file mới:

```markdown name=README.md
# ChatbotLaw - Trợ Lý Pháp Luật Thông Minh

ChatbotLaw là một ứng dụng chatbot thông minh được xây dựng bằng Python, sử dụng công nghệ RAG (Retrieval-Augmented Generation) để cung cấp các câu trả lời chính xác về pháp luật dựa trên dữ liệu pháp lý đã được xử lý sẵn.

## 🎯 Tính Năng Chính

- **Hệ Thống RAG Tiên Tiến**: Kết hợp vector embedding và retrieval để trả lời các câu hỏi pháp lý với độ chính xác cao
- **Xử Lý Tài Liệu Tự Động**: Tự động xây dựng và cập nhật vectorstore từ tài liệu pháp luật
- **API RESTful**: Giao diện API dễ sử dụng cho các ứng dụng tích hợp
- **Cơ Sở Dữ Liệu Pháp Lý**: Hỗ trợ lưu trữ và quản lý tài liệu pháp luật
- **Prompt Template Tùy Chỉnh**: Cho phép t��y chỉnh cách trình bày kết quả

## 📋 Yêu Cầu

- Python 3.8 trở lên
- Các dependencies được liệt kê trong `requirements.txt`

## 🚀 Cài Đặt

### 1. Clone Repository
```bash
git clone https://github.com/BestBeo/ChatbotLaw.git
cd ChatbotLaw
```

### 2. Tạo Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu Hình Biến Môi Trường
```bash
cp .env.example .env
# Chỉnh sửa file .env với thông tin cấu hình của bạn
```

## 📁 Cấu Trúc Project

```
ChatbotLaw/
├── core/                          # Thành phần lõi của ứng dụng
├── services/                      # Các dịch vụ chính
├── schemas/                       # Định nghĩa schema dữ liệu
├── utils/                         # Hàm tiện ích
├── db/                           # Quản lý cơ sở dữ liệu
├── data/                         # Dữ liệu đầu vào
├── tài liệu giải nghĩa/         # Tài liệu giải thích
├── config.py                     # Tệp cấu hình chính
├── main.py                       # Điểm khởi động ứng dụng
├── build_vectorstore.py          # Script xây dựng vector store
├── rag_components.py             # Các thành phần RAG
├── prompt_templete.py            # Template cho prompt
├── demo.py                       # Demo cơ bản
├── demo2.py                      # Demo nâng cao
├── standalone_rag_demo.py        # Demo RAG độc lập
├── ragDemover2.py                # Phiên bản RAG demo 2
├── minimal-retrieval.py          # Ví dụ retrieval tối giản
├── requirements.txt              # Danh sách dependencies
└── .env.example                  # Mẫu biến môi trường
```

## 🛠️ Cách Sử Dụng

### Khởi Động Ứng Dụng Chính
```bash
python main.py
```

### Xây Dựng Vector Store
```bash
python build_vectorstore.py
```

### Chạy Demo
```bash
# Demo cơ bản
python demo.py

# Demo nâng cao
python demo2.py

# Demo RAG độc lập
python standalone_rag_demo.py

# Ví dụ retrieval tối giản
python minimal-retrieval.py
```

## 🔧 Cấu Hình

Chỉnh sửa file `config.py` để tùy chỉnh:
- Cài đặt mô hình AI
- Tham số embeddings
- Cấu hình cơ sở dữ liệu
- Các tùy chọn retrieval

## 📚 Các Thành Phần Chính

### RAG Components (`rag_components.py`)
Chứa các thành phần chính của hệ thống RAG:
- Document loading và processing
- Vector embedding
- Similarity search
- Response generation

### Dependencies (`dependencies.py`)
Quản lý các dependency injection cho toàn bộ ứng dụng

### Prompt Templates (`prompt_templete.py`)
Định nghĩa các template prompt cho các loại câu hỏi pháp lý khác nhau

## 📖 Tài Liệu Bổ Sung

Tham khảo thư mục `tài liệu giải nghĩa` để hiểu thêm về:
- Cách hoạt động của hệ thống
- Các khái niệm pháp lý
- Hướng dẫn sử dụng chi tiết

## 🤝 Góp Ý và Đóng Góp

Nếu bạn muốn đóng góp cho project, vui lòng:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Add amazing feature'`)
4. Push lên branch (`git push origin feature/amazing-feature`)
5. Mở Pull Request

## 📝 Ghi Chú

- Dự án này sử dụng công nghệ RAG để tăng độ chính xác của các câu trả lời pháp lý
- Dữ liệu được xử lý tự động và lưu trữ trong vector store
- Hệ thống được thiết kế để dễ mở rộng và tích hợp

## 📞 Liên Hệ

Nếu có câu hỏi hoặc gợi ý, vui lòng liên hệ qua:
- GitHub Issues: https://github.com/BestBeo/ChatbotLaw/issues

## 📄 Giấy Phép

Project này được cung cấp mà không có giấy phép cụ thể. Vui lòng kiểm tra với tác giả để biết thêm thông tin.

---

**Lần cập nhật cuối cùng**: 2026-02-27