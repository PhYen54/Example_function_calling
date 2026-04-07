## So sánh ReAct Agent và LLM function calling
Sự khác biệt trong cơ chế xử lý lỗi: Function Calling và ReAct Agent

Function Calling (Thực thi tuyến tính): Hoạt động theo luồng một chiều. Khi công cụ (tool) được gọi và trả về lỗi, LLM chỉ ghi nhận kết quả thất bại đó và phản hồi lại cho người dùng, kết thúc hoàn toàn chu trình xử lý.

ReAct Agent (Tự phục hồi lỗi): Hoạt động theo chu trình lặp (Loop). Khi phát hiện hàm thực thi thất bại, Agent có khả năng suy luận (Reasoning) để tìm hiểu nguyên nhân, sau đó tự động thiết lập kế hoạch mới (gọi lại hàm với tham số khác hoặc sử dụng công cụ thay thế) cho đến khi đạt được mục tiêu cuối cùng.
## Các bước thực hiện
### 1. Tạo môi trường ảo
```bash
python -m venv venv
```
### 2. Kích hoạt môi trường ảo
```bash
venv\Scripts\activate
```
### 3. Tải thư viện
```bash
pip install -r requirement.txt
```
### 4. Điền GEMINI_API_KEY (mở app.py, điền api key free)
```bash
GEMINI_API_KEY = "<YOUR KEY>"
```
### 5. Chạy code
```bash
streamlit run app.py
```
## Demo
<img width="1096" height="855" alt="image" src="https://github.com/user-attachments/assets/552b7e9f-a607-4785-918f-1c8a4355fb1d" />


