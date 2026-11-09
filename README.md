# Sử dụng AI trong học tập của sinh viên

Dự án khảo sát gồm 22 câu hỏi, mã phân tích và notebook. **Chưa thu thập phản hồi thật.** 120 dòng trong data/demo là mô phỏng có seed 42 để kiểm tra chương trình, không phải kết quả nghiên cứu.

- [Bảng hỏi để tạo Google Form](questionnaire.md)
- [Cấu trúc câu hỏi](data/questions.json)
- [Notebook](notebooks/01_analysis.ipynb)
- [Báo cáo chạy thử](reports/demo/findings.md)

## Chạy

Python 3.10+. Cài `python -m pip install -r requirements.txt`.
Chạy thử: `python run_all.py`.
Dữ liệu thật: `python run_all.py --input data/private/responses.csv`.

CSV cần cột Q01–Q22; ánh xạ tiêu đề Google Forms sang các mã trong data/questions.json. Câu nhiều chọn dùng dấu chấm phẩy; kiểm tra trước khi đổi dấu phân cách vì nội dung tự do có thể chứa dấu phẩy. Giữ nguyên bản xuất gốc riêng để đối chiếu. Không thêm nhãn SYNTHETIC_DEMO vào dữ liệu thật. Không áp dụng không phải điểm 0 hoặc 3.

## Thu thập và phân tích

Sao chép bảng hỏi sang Google Forms, thêm giới thiệu/đồng ý tham gia, thử với một nhóm nhỏ trước khi phát hành. Bổ sung người phụ trách và thời hạn lưu dữ liệu. Không thu email, tên hoặc mã sinh viên. Mẫu thuận tiện cần ghi rõ giới hạn; số phản hồi không tự bảo đảm tính đại diện.

Báo cáo gồm tần số từng câu, tỷ lệ theo số người trả lời, phân phối Likert, trung bình/trung vị và tỷ lệ 4–5. Không gộp các câu đo lợi ích, lo ngại và kiến thức thành một điểm chung. Xem quality.json để rà soát nhãn ngoài danh mục. Khi có dữ liệu thật cần rà soát mâu thuẫn, phản hồi thiếu và quy tắc phân nhánh trước khi viết kết luận. Không dùng dữ liệu mô phỏng làm số liệu báo cáo học thuật.
