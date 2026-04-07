import streamlit as st
import google.generativeai as genai

# ==========================================
# CẤU HÌNH GIAO DIỆN STREAMLIT
# ==========================================
st.set_page_config(page_title="AI Calculator Agent", page_icon="🧮")
st.title("🧮 AI Calculator Agent")
st.caption("Demo Function Calling sử dụng Google Gemini (Hoàn toàn miễn phí)")

# Tạo menu bên trái để nhập API Key an toàn
with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
# ==========================================
# ĐỊNH NGHĨA CÔNG CỤ (FUNCTION)
# ==========================================
def calculator(a: float, b: float, operator: str) -> str:
    """Thực hiện các phép tính toán học cơ bản.
    
    Args:
        a: Số thứ nhất.
        b: Số thứ hai.
        operator: Phép toán. Chỉ chấp nhận các ký tự: '+', '-', '*', '/'.
    """
    if operator == '+': return str(a + b)
    elif operator == '-': return str(a - b)
    elif operator == '*': return str(a * b)
    elif operator == '/': return str(a / b) if b != 0 else "Lỗi: Không thể chia cho 0"
    return "Lỗi: Phép toán không hợp lệ"

# ==========================================
# QUẢN LÝ TRẠNG THÁI (SESSION STATE)
# ==========================================
# Lưu trữ lịch sử tin nhắn để hiển thị lên UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# # Kiểm tra xem người dùng đã nhập API Key chưa
# if not api_key:
#     st.warning("👈 Vui lòng nhập API Key ở menu bên trái để bắt đầu!")
#     st.stop() # Dừng chạy code bên dưới nếu chưa có key

# Khởi tạo mô hình AI và kết nối Tool (Chỉ chạy 1 lần)
GEMINI_API_KEY = ""
if "chat_session" not in st.session_state:
    genai.configure(api_key=GEMINI_API_KEY)
    # Khai báo model gemini-1.5-flash siêu nhanh và cấp cho nó tool 'calculator'
    model = genai.GenerativeModel(
        model_name='gemini-3-flash-preview',
        tools=[calculator]
    )
    # Bật tính năng tự động lặp (ReAct) để gọi hàm
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)

# ==========================================
# GIAO DIỆN CHAT CHÍNH
# ==========================================
# 1. In lại toàn bộ lịch sử chat cũ ra màn hình
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Xử lý khi người dùng gõ tin nhắn mới
if prompt := st.chat_input("Ví dụ: Hãy tính cho tôi 125 cộng 340, sau đó nhân với 2"):
    
    # Hiển thị câu hỏi của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Hiển thị câu trả lời của AI
    with st.chat_message("assistant"):
        # Hiển thị vòng xoay đang tải trong lúc AI chạy (rất hữu ích khi nó phải gọi hàm)
        with st.spinner("AI đang phân tích và tính toán..."):
            try:
                # Gửi lên Gemini. Lúc này Gemini sẽ tự động gọi hàm calculator() chạy ngầm
                response = st.session_state.chat_session.send_message(prompt)
                
                # In kết quả cuối cùng ra màn hình
                st.markdown(response.text)
                
                # Lưu vào lịch sử giao diện
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            except Exception as e:
                st.error(f"Đã xảy ra lỗi hệ thống: {e}")