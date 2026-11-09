import argparse,csv,json,collections,statistics,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=ROOT/'data/demo/responses.csv');a=p.parse_args()
    rows=list(csv.DictReader(a.input.open(encoding='utf-8-sig',newline='')));assert rows,'Empty CSV'
    questions=json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'));assert all(q['id'] in rows[0] for q in questions),'Missing Q01-Q22 columns'
    demo=any(r.get('data_origin')=='SYNTHETIC_DEMO' for r in rows);label='DỮ LIỆU MÔ PHỎNG — KHÔNG PHẢI KẾT QUẢ KHẢO SÁT' if demo else 'DỮ LIỆU ĐẦU VÀO DO NGƯỜI DÙNG CUNG CẤP'
    out=ROOT/'reports'/('demo' if demo else 'survey');out.mkdir(parents=True,exist_ok=True)
    records=[];lines=['# '+label,f'\nSố dòng: {len(rows)}. Không mặc định mỗi dòng là một người duy nhất.'];flags=[]
    for q in questions:
        key=q['id'];vals=[r[key].strip() for r in rows if r[key].strip()];lines+=['\n## '+key+'. '+q['question']]
        if q['type']=='text':lines+=[f'{len(vals)} phản hồi không rỗng; không xuất nguyên văn.'];continue
        tokens=[t.strip() for v in vals for t in (v.split(';') if q['type']=='multi' else [v]) if t.strip()]
        freq=collections.Counter(tokens);allowed=set(q['options'].split('|'))
        for token in freq:
            if token not in allowed:flags.append({'question':key,'issue':'Unexpected category','value':token})
        if q['type']=='likert':
            nums=[int(v) for v in vals if v in {'1','2','3','4','5'}]
            lines += [f'n hợp lệ={len(nums)}; Không áp dụng={freq["Không áp dụng"]}; trung bình={statistics.mean(nums):.2f}; trung vị={statistics.median(nums)}; mức 4–5={sum(v>=4 for v in nums)/len(nums):.1%}' if nums else 'Không có điểm hợp lệ.']
        lines+=['\n| Lựa chọn | Số lượt | % người trả lời câu |','|---|---:|---:|']
        for option,count in freq.items():
            pct=100*count/len(vals);records.append({'question':key,'option':option,'count':count,'answered':len(vals),'pct':pct});lines+=[f'| {option} | {count} | {pct:.2f}% |']
        if q['type']=='multi':lines+=['Tổng % có thể vượt 100%; mẫu số là số người trả lời câu.']
        fig,ax=plt.subplots(figsize=(10,max(3,len(freq)*.4)));ax.barh(list(freq),list(freq.values()),color='#167d9a');ax.set_title(key+(' — SYNTHETIC DEMO' if demo else ''));ax.invert_yaxis();ax.bar_label(ax.containers[0],padding=2);ax.set_xlim(0,max(freq.values())*1.15+1);fig.tight_layout();fig.savefig(out/(key+'.png'),dpi=120);plt.close(fig)
        lines+=[f'\n![{key}]({key}.png)']
    with (out/'frequencies.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    (out/'quality.json').write_text(json.dumps({'rows':len(rows),'question_columns':22,'unexpected_categories':flags,'synthetic':demo},ensure_ascii=False,indent=2),encoding='utf-8')
    lines+=['\n## Giới hạn','Dữ liệu mô phỏng chỉ kiểm tra mã, không dùng làm bằng chứng nghiên cứu. Dữ liệu thật cần thiết kế lấy mẫu và kiểm tra mâu thuẫn trước khi kết luận. Hiệu quả là tự đánh giá, không chứng minh AI làm tăng điểm. Không tự gộp các mục Likert khác nội dung thành một thang đo.']
    (out/'findings.md').write_text('\n\n'.join(lines),encoding='utf-8');print('SYNTHETIC DEMO' if demo else 'USER INPUT');print('Rows:',len(rows),'Questions:',len(questions),'Unexpected categories:',len(flags))
if __name__=='__main__':main()
