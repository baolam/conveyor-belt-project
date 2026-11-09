# 🤖 Smart Conveyor Belt with Deep Learning Sorting

> **Hệ thống băng chuyền thông minh tự động phân loại vật thể (rác thải, rau củ quả, màu sắc) bằng học sâu (Deep Learning).**

## 📖 Giới thiệu
Hệ thống kết hợp mô hình thị giác máy tính và cơ cấu băng chuyền công nghiệp tự động hoá. Khi vật thể di chuyển qua camera, hệ thống chụp ảnh, dự đoán loại vật thể qua mô hình PyTorch và gửi tín hiệu kích hoạt tay gạt hoặc piston để phân loại vào đúng khay chứa.

## ✨ Tính năng chính
- **Nhận diện đa lớp mục tiêu**:
  - Phân loại màu sắc (`color.pt`, `auc_color.pt`)
  - Nhận diện & phân loại rác thải tái chế (`garbage.pt`, `auc_garbage.pt`)
  - Phân loại rau củ nông sản (`vegetable.pt`, `auc_veget.pt`)
- **Độ trễ thấp (Real-time inference)**: Tối ưu hoá luồng xử lý khung hình camera theo thời gian thực.
- **Tích hợp máy chủ điều khiển**: Kết nối logic dự đoán với bộ điều khiển vật lý qua Node.js (`server.js`).

## 🛠️ Công nghệ sử dụng
- **Deep Learning / Computer Vision**: PyTorch (`.pt`), OpenCV, NumPy
- **Server & Giao tiếp**: Node.js, Python Socket
- **Phần cứng**: Camera công nghiệp/webcam, động cơ băng chuyền, cơ cấu phân loại

## 🚀 Hướng dẫn sử dụng

```bash
# Cài đặt thư viện Node.js
npm install

# Cài đặt thư viện Python
pip install torch torchvision opencv-python

# Chạy server điều khiển
node server.js

# Khởi chạy luồng phân loại
python index.py
```

## 📄 Tác giả
Phát triển bởi [@baolam](https://github.com/baolam).
