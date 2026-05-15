# Report 1 page - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Cao Minh Hưng - 1871020285
- Thành viên 2: Nguyễn Thị Tuyết - 1871020644

## Mục tiêu

Bài lab này nhằm xây dựng hệ thống gửi và nhận dữ liệu mã hóa AES-CBC qua TCP socket với 2 kênh riêng biệt: kênh khóa (KEY_PORT) trao đổi AES key và IV, kênh dữ liệu (DATA_PORT) gửi ciphertext. Sinh viên thực hành mã hóa/giải mã AES-CBC, PKCS#7 padding, thiết kế length header, và viết test cho nhiều tình huống. Ngoài ra, bài lab giúp sinh viên nhận diện điểm yếu của việc gửi key/IV dạng plaintext và hiểu rằng mã hóa chưa đảm bảo an toàn tuyệt đối.

## Phân công thực hiện

- **Thành viên 1 (Cao Minh Hưng)**: Phụ trách `aes_socket_utils.py` (các hàm mã hóa AES-CBC, giải mã, PKCS#7 padding, build/parse key packet và data packet) và `sender.py` (gửi key/IV qua KEY_PORT, gửi ciphertext qua DATA_PORT, ghi log gửi).
- **Thành viên 2 (Nguyễn Thị Tuyết)**: Phụ trách `receiver.py` (lắng nghe KEY_PORT nhận key/IV, lắng nghe DATA_PORT nhận ciphertext, giải mã AES-CBC, ghi log nhận) và viết test cases (`tests/`).
- **Cả hai làm chung**: Viết báo cáo, threat model, chạy thử nghiệm end-to-end, tạo file log mẫu trong `logs/`, đảm bảo CI pass.

## Cách làm

Hệ thống sử dụng AES-CBC với key 16 bytes (AES-128) và IV 16 bytes. Dữ liệu plaintext được padding theo PKCS#7 trước khi mã hóa. Giao thức truyền: kênh khóa gửi gói tin `[key_length:4 bytes][key:16/32 bytes][iv:16 bytes]`, kênh dữ liệu gửi `[ciphertext_length:4 bytes][ciphertext:N bytes]`. Sender tạo key/IV ngẫu nhiên, mã hóa plaintext và gửi qua 2 kênh TCP riêng. Receiver lắng nghe trên 2 cổng, nhận key/IV, nhận ciphertext và giải mã. Có hỗ trợ nhập từ MESSAGE env, INPUT_FILE hoặc bàn phím; log ghi ra file nếu được cấu hình.

## Kết quả

Chạy thử nghiệm end-to-end thành công: sender gửi message "Xin chao FIT4012 - Lab 6 AES Socket", receiver nhận và giải mã chính xác. Tất cả 14/16 test pass. Các test quan trọng: padding roundtrip, AES-CBC roundtrip, key channel contract (AES-128 và AES-256), data channel contract, wrong key negative test, tamper negative test, và submission contract test. File log đã được ghi trong thư mục `logs/`.

## Kết luận

Bài học kỹ thuật: nắm vững cách dùng AES-CBC với pycryptodome, PKCS#7 padding và thiết kế giao thức truyền file qua socket với length header. Bài học bảo mật: AES-CBC chỉ che giấu nội dung chứ không xác thực nguồn gốc hay đảm bảo tính toàn vẹn dữ liệu, gửi key/IV plaintext là điểm yếu nghiêm trọng - cần dùng TLS hoặc AES-GCM cho hệ thống thật.
