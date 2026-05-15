# Peer Review Response - Lab 6 AES-CBC Socket

## Thông tin nhóm

- **Thành viên 1**: Cao Minh Hưng - 1871020285
- **Thành viên 2**: Nguyễn Thị Tuyết - 1871020

## Phản hồi từ review

Chúng em đã nhận được review từ nhóm bạn và thực hiện các chỉnh sửa sau:

1. **UTF-8 encoding**: Đã thêm xử lý UnicodeEncodeError cho stdout trên Windows bằng cách gọi `sys.stdout.reconfigure(encoding="utf-8")` trong `receiver.py`.
2. **Hoàn thiện báo cáo**: Đã điền đầy đủ thông tin team, mục tiêu, phân công, kết quả và kết luận trong `report-1page.md` và `threat-model-1page.md`.
3. **Tạo log mẫu**: Đã chạy thử nghiệm end-to-end và tạo file log thật trong thư mục `logs/`.

## Cảm ơn

Cảm ơn nhóm đã review và góp ý để chúng em hoàn thiện bài lab tốt hơn.
