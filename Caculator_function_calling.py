import google.generativeai as genai

# ==========================================
# BƯỚC 1: CẤU HÌNH API KEY CỦA BẠN
# ==========================================
# (Bạn có thể lấy key miễn phí tại: https://aistudio.google.com/app/apikey)
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# BƯỚC 2: ĐỊNH NGHĨA HÀM PYTHON BÌNH THƯỜNG
# ==========================================
# ĐIỂM HAY CỦA GEMINI: Nó tự đọc được kiểu dữ liệu (float, str) 
# và mô tả (docstring) dưới đây để làm Schema, bạn không cần khai báo JSON!
def calculator(a: float, b: float, operator: str) -> str:
    """Thực hiện các phép tính toán học cơ bản.
    
    Args:
        a: Số thứ nhất.
        b: Số thứ hai.
        operator: Phép toán. Chỉ chấp nhận một trong các ký tự: '+', '-', '*', '/'.
    """
    if operator == '+': return str(a + b)
    elif operator == '-': return str(a - b)
    elif operator == '*': return str(a * b)
    elif operator == '/': return str(a / b) if b != 0 else "Lỗi chia cho 0"
    return "Phép toán không hợp lệ"

# ==========================================
# BƯỚC 3: KHỞI TẠO MODEL VÀ GẮN CÔNG CỤ (TOOLS)
# ==========================================
# Dùng gemini-1.5-flash: Tốc độ cực nhanh và miễn phí
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    tools=[calculator] # Chuyền thẳng tên hàm Python vào đây!
)

# ==========================================
# BƯỚC 4: TẠO PHIÊN CHAT VÀ BẬT "TỰ ĐỘNG GỌI HÀM"
# ==========================================
# Với OpenAI, bạn phải tự lấy JSON, tự chạy code, rồi tự gửi kết quả lại cho LLM (Bước 5, 6).
# Với Gemini, khi bật tính năng này, SDK sẽ làm TẤT CẢ các bước đó thay bạn một cách tự động ngầm bên dưới!
chat = model.start_chat(enable_automatic_function_calling=True)

# ==========================================
# BƯỚC 5: NGƯỜI DÙNG HỎI & NHẬN KẾT QUẢ
# ==========================================
user_input = "tính 5 cộng 4 rồi nhân cho 2"
print(f"👤 Người dùng: {user_input}\n")

# Gửi tin nhắn. Lúc này Gemini sẽ tự phân tích -> tự gọi hàm calculator -> tự lấy kết quả -> tự soạn câu trả lời.
response = chat.send_message(user_input)

print(f"🤖 Gemini trả lời: {response.text}\n")

# ==========================================
# BƯỚC 6 (Tùy chọn): XEM LẠI NHẬT KÝ (HISTORY) ĐỂ KIỂM CHỨNG
# ==========================================
print("--- NHẬT KÝ HOẠT ĐỘNG NGẦM CỦA AI ---")
for message in chat.history:
    role = "👤 Bạn" if message.role == "user" else "🤖 AI/Hệ thống"
    
    # Kiểm tra xem message là text bình thường hay là gọi hàm
    for part in message.parts:
        if part.text:
            print(f"{role} (Nói): {part.text.strip()}")
        elif part.function_call:
            print(f"⚙️ AI (Hành động): Đã yêu cầu gọi hàm '{part.function_call.name}' với tham số {dict(part.function_call.args)}")
        elif part.function_response:
            print(f"📦 Hệ thống (Phản hồi): Trả kết quả của hàm '{part.function_response.name}' là {dict(part.function_response.response)}")