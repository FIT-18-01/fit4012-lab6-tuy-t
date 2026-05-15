# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- **Thành viên 1**: Cao Minh Hưng - 1871020285
- **Thành viên 2**: Nguyễn Thị Tuyết - 1871020644

## Assets

- **Plaintext**: nội dung bản tin gốc cần bảo mật.
- **AES key**: khóa dùng để mã hóa/giải mã, nếu lộ thì mọi dữ liệu đều bị đọc.
- **IV**: vector khởi tạo, cần bảo vệ để tránh tấn công CBC.
- **Ciphertext**: dữ liệu đã mã hóa cần toàn vẹn.
- **File đầu vào/đầu ra**: chứa dữ liệu nhạy cảm.
- **Log files**: có thể lộ thông tin key/IV nếu không được bảo vệ.

## Attacker model

Kẻ tấn công có quyền truy cập mạng LAN (MITM), có khả năng nghe lén (sniffing), bắt và phân tích gói tin TCP trên cả KEY_PORT và DATA_PORT, sửa nội dung ciphertext (tampering), gửi lại gói tin cũ (replay attack), hoặc đọc log file nếu có quyền truy cập hệ thống.

## Threats

1. **Key disclosure**: AES key và IV được gửi plaintext qua KEY_PORT - kẻ tấn công nghe lén có thể lấy key và giải mã toàn bộ dữ liệu.
2. **Tampering**: Ciphertext bị sửa trên đường truyền - AES-CBC không có cơ chế xác thực, receiver vẫn cố giải mã và có thể nhận dữ liệu sai hoặc crash.
3. **Replay attack**: Kẻ tấn công ghi lại gói tin cũ và gửi lại - receiver không có cơ chế phát hiện packet cũ.
4. **Log leakage**: Key và IV được ghi vào log - nếu log bị rò rỉ, toàn bộ dữ liệu có thể bị giải mã.
5. **No authentication**: Receiver không xác thực được danh tính Sender - bất kỳ ai cũng có thể gửi dữ liệu giả mạo.
- Key disclosure do key/IV gửi plaintext.
- Tampering do ciphertext bị sửa.
- Replay attack do packet cũ bị gửi lại.
- Log leakage do key bị ghi vào log.
- No authentication do Receiver không xác thực Sender.

## Mitigations

1. **Không gửi key plaintext**: Trong hệ thống thật, sử dụng trao đổi khóa an toàn như Diffie-Hellman hoặc TLS.
2. **Dùng AES-GCM**: Cung cấp cả mã hóa và xác thực (AEAD), phát hiện dữ liệu bị sửa.
3. **Thêm nonce/timestamp**: Chống replay attack bằng cách kiểm tra tính mới của packet.
4. **Không ghi key vào log**: Chỉ ghi thông tin cần thiết, che giấu key/IV trong log.
5. **Xác thực Sender**: Dùng certificate hoặc pre-shared secret để xác thực nguồn gốc dữ liệu.
- Không gửi key plaintext trong hệ thống thật.
- Dùng TLS hoặc cơ chế trao đổi khóa an toàn.
- Dùng AES-GCM để có xác thực dữ liệu.
- Không ghi key thật vào log trong môi trường thật.
- Thêm nonce/timestamp để giảm replay.
- Thêm xác thực Sender.

## Residual risks

Hệ thống hiện tại chỉ là mô phỏng học tập: key channel gửi key/IV plaintext, không có TLS, không có xác thực Sender và không chống replay. Ngay cả khi thêm AES-GCM, nếu key channel vẫn là plaintext thì hệ thống vẫn không an toàn. Rủi ro còn lại: chưa có cơ chế quản lý key an toàn (key rotation, storage) và chưa có logging bảo mật (không ghi thông tin nhạy cảm).
