from pathlib import Path
import csv,random,json
root=Path(__file__).resolve().parent
questions=[
('Q01','Bạn đang là sinh viên năm mấy?','single','Năm nhất|Năm hai|Năm ba|Năm tư trở lên'),
('Q02','Bạn đang học nhóm ngành nào?','single','Kỹ thuật - công nghệ|Kinh tế - quản trị|Xã hội - nhân văn|Sức khoẻ|Khác'),
('Q03','Bạn đã sử dụng công cụ AI cho học tập trong 30 ngày qua chưa?','single','Có|Không'),
('Q04','Bạn sử dụng AI cho học tập với tần suất nào trong 30 ngày qua?','single','Không sử dụng|Dưới 1 ngày/tuần|1–2 ngày/tuần|3–4 ngày/tuần|5–7 ngày/tuần'),
('Q05','Bạn đã dùng những công cụ AI nào cho học tập trong 30 ngày qua?','multi','ChatGPT|Gemini|Microsoft Copilot|Claude|Khác|Không sử dụng'),
('Q06','Bạn dùng AI cho những hoạt động nào trong 30 ngày qua?','multi','Giải thích kiến thức|Tóm tắt tài liệu|Luyện ngoại ngữ|Lập trình|Lên ý tưởng|Soạn nội dung|Khác|Không sử dụng'),
('Q07','Bạn thường dùng AI ở giai đoạn nào của bài tập?','single','Trước khi tự làm|Sau khi tự làm|Trong suốt quá trình|Không sử dụng'),
('Q08','Bạn có kiểm tra lại câu trả lời AI bằng tài liệu hoặc nguồn khác không?','single','Không bao giờ|Hiếm khi|Thỉnh thoảng|Thường xuyên|Luôn luôn|Không áp dụng'),
('Q09','Bạn đã gặp thông tin AI sai hoặc không có nguồn kiểm chứng chưa?','single','Có|Không|Không chắc|Không áp dụng'),
('Q10','Bạn đánh giá độ tin cậy chung của câu trả lời AI thế nào?','single','Rất thấp|Thấp|Trung bình|Cao|Rất cao|Không áp dụng'),
('Q11','AI giúp tôi hiểu rõ hơn kiến thức khó.','likert','1|2|3|4|5|Không áp dụng'),
('Q12','AI giúp tôi tiết kiệm thời gian học tập.','likert','1|2|3|4|5|Không áp dụng'),
('Q13','AI giúp tôi tìm ra nhiều cách giải quyết bài tập.','likert','1|2|3|4|5|Không áp dụng'),
('Q14','Tôi có thể tự giải thích lại nội dung sau khi dùng AI.','likert','1|2|3|4|5|Không áp dụng'),
('Q15','Tôi lo mình phụ thuộc AI khi làm bài tập.','likert','1|2|3|4|5|Không áp dụng'),
('Q16','Tôi gặp khó khăn khi đánh giá câu trả lời AI đúng hay sai.','likert','1|2|3|4|5|Không áp dụng'),
('Q17','Tôi biết khi nào cần ghi nhận việc sử dụng AI trong bài học.','likert','1|2|3|4|5|Không áp dụng'),
('Q18','Bạn gặp những khó khăn nào khi dùng AI cho học tập?','multi','Thông tin sai|Thiếu nguồn|Khó đặt câu hỏi|Chi phí|Quy định chưa rõ|Lo phụ thuộc|Không gặp khó khăn|Không áp dụng'),
('Q19','Bạn đã được hướng dẫn về sử dụng AI trong học tập chưa?','single','Có|Không|Không nhớ'),
('Q20','Bạn muốn được hướng dẫn thêm nội dung gì?','multi','Kiểm chứng thông tin|Đặt câu hỏi hiệu quả|Ghi nhận sử dụng AI|Bảo vệ dữ liệu cá nhân|Dùng AI theo môn học|Không có nhu cầu'),
('Q21','Bạn dự định sử dụng AI trong học tập trong 3 tháng tới không?','single','Có|Không|Chưa quyết định'),
('Q22','Bạn có đề xuất gì để sử dụng AI hiệu quả và có trách nhiệm?','text','')]
(root/'data/questions.json').write_text(json.dumps([dict(zip(['id','question','type','options'],q)) for q in questions],ensure_ascii=False,indent=2),encoding='utf-8')
text='''# Bảng hỏi: Sử dụng AI trong học tập của sinh viên

## Giới thiệu và đồng ý tham gia

Khảo sát phục vụ học tập, tìm hiểu hành vi sử dụng AI trong 30 ngày qua. Tham gia tự nguyện; có thể dừng hoặc bỏ qua câu hỏi. Không thu họ tên, email, mã sinh viên. Không nhập thông tin cá nhân trong câu mở. Kết quả chỉ báo cáo tổng hợp. Người tổ chức cần bổ sung tên, thông tin liên hệ và thời hạn lưu dữ liệu trước khi phát hành.

Câu sàng lọc ngoài bảng phân tích: Bạn đồng ý tham gia khảo sát không? Có → tiếp tục; Không → kết thúc. Không bật thu email hoặc bắt đăng nhập để nhận diện người tham gia.

Q11–Q17: 1 = Hoàn toàn không đồng ý; 2 = Không đồng ý; 3 = Trung lập; 4 = Đồng ý; 5 = Hoàn toàn đồng ý. Người không sử dụng chọn Không áp dụng. Không áp dụng không được mã hoá thành 0 hoặc 3. Các câu này đo những khía cạnh khác nhau, không tự gộp thành một điểm chung.

Câu nhiều lựa chọn: không chọn Không sử dụng/Không áp dụng/Không gặp khó khăn/Không có nhu cầu cùng đáp án khác. Có thể thực hiện bằng câu sàng lọc/phân nhánh trên Google Forms.

'''
for id,title,kind,options in questions:text+=f'## {id}. {title}\n\nLoại: {kind}.\n\n'+('\n'.join('- '+o for o in options.split('|')) if options else 'Trả lời tự do, không bắt buộc.')+'\n\n'
(root/'questionnaire.md').write_text(text,encoding='utf-8')
rng=random.Random(42); records=[]
for i in range(120):
    used=rng.random()<.8; row={'data_origin':'SYNTHETIC_DEMO'}
    for id,title,kind,opt in questions:
        opts=opt.split('|')
        row[id]='' if kind=='text' else '; '.join(rng.sample(opts[:-1],2)) if kind=='multi' else rng.choice(opts[:-1] if kind=='likert' else opts)
    row['Q03']='Có' if used else 'Không'
    if not used:
        for key in ['Q04','Q05','Q06','Q07']:row[key]='Không sử dụng'
        for j in range(8,19):
            if j!=10:row[f'Q{j:02}']='Không áp dụng'
        row['Q10']='Không áp dụng'
    else:row['Q04']=rng.choice(questions[3][3].split('|')[1:])
    records.append(row)
with (root/'data/demo/responses.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print('22 questions; 120 explicitly synthetic demo rows')

