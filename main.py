import logging
# Cấu hình logging hệ thống
logging.basicConfig(
    level=logging.INFO, # CHÚ Ý: Mức độ log hiện tại của hệ thống - Đã sửa từ WARNING thành INFO
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

def get_shipping_rate(method: str, distance: int) -> float:
    """Trả về chi phí vận chuyển cơ sở dựa trên phương thức và khoảng cách"""
    logger.info(f"Đang tính phí giao hàng cho phương thức {method} với khoảng cách {distance} km")
    
    if distance <= 0:
        # FIXED: Nâng cấp exception handling theo Clean Code principle
        logger.error("Khoảng cách vận chuyển không được nhỏ hơn hoặc bằng 0")
        raise ValueError("Khoảng cách vận chuyển phải lớn hơn 0")

    # Xác định phí cơ sở theo phương thức vận chuyển
    if method == "standard":
        base_rate = 15000
    elif method == "express":
        base_rate = 30000
    elif method == "next_day":
        base_rate = 50000
    else:
        base_rate = 20000
        
    # Phụ thu đường xa nếu khoảng cách từ 20km trở lên
    # FIXED: Đổi từ base_rate = 10000 thành base_rate += 10000
    if distance >= 20:
        base_rate += 10000 # Cộng thêm 10,000 VND cho đường xa (>= 20km)
        
    return base_rate

def calculate_final_shipping(weight: float, distance: int, method: str) -> float:
    """Tính tổng chi phí vận chuyển cuối cùng dựa trên trọng lượng hàng hóa"""
    # Validate dữ liệu đầu vào theo Clean Code principles
    if weight < 0:
        raise ValueError("Trọng lượng hàng hóa không được âm")
    
    if distance <= 0:
        raise ValueError("Khoảng cách vận chuyển phải lớn hơn 0")
    
    if method not in ["standard", "express", "next_day"]:
        raise ValueError(f"Phương thức vận chuyển '{method}' không hợp lệ")
        
    base_rate = get_shipping_rate(method, distance)
    
    # Giả sử phí tăng thêm 2,000đ cho mỗi kg hàng hóa
    total_cost = base_rate + (weight * 2000)
    
    logger.info(f"Kết quả: Tổng phí vận chuyển = {total_cost} VND (Phương thức: {method}, Khoảng cách: {distance}km, Trọng lượng: {weight}kg)")
    return total_cost

# Khúc code chạy thử của Intern (Sinh viên dùng IDE Debugger để quét qua các dòng này)
if __name__ == "__main__":
    logger.info("=== Bắt đầu kiểm tra hệ thống tính phí vận chuyển ===")
    
    # Case 1: Kiểm tra lỗi logic biên (đường xa)
    try:
        result1 = calculate_final_shipping(3.5, 25, "express")
        logger.info(f"Case 1 thành công: {result1} VND")
    except ValueError as e:
        logger.error(f"Case 1 thất bại: {e}")
    
    # Case 2: Kiểm tra lỗi dữ liệu đầu vào (distance âm)
    try:
        result2 = calculate_final_shipping(2.0, -5, "standard")
        logger.info(f"Case 2 thành công: {result2} VND")
    except ValueError as e:
        logger.error(f"Case 2 thất bại (Expected): {e}")
    
    logger.info("=== Kết thúc kiểm tra hệ thống ===")
