# ★このサービスの独自コンテキスト（品質向上のため必ず参照）:
# 解決する問題: 収縮期・拡張期血圧を入力して正常・高血圧の判定と生活改善アドバイスを提供
# 対象ユーザー: 健康管理に取り組むアクティブな方
# キーワード: 血圧
TITLE = '血圧チェック・生活改善アドバイス【無料】無料診断・アドバイス'
DESCRIPTION = '収縮期・拡張期血圧を入力して正常・高血圧の判定と生活改善アドバイスを提供。登録不要・完全無料でご利用いただけます。'
DESCRIPTION_SHORT = '収縮期・拡張期血圧を入力して正常・高血圧の判定と生活改善アドバイスを提供。'
COLOR1 = '#FFEDD5'
COLOR2 = '#FFF7ED'
COLOR_BTN = '#EA580C'
FOOTER_LINKS = [('https://appadaycreator.com/mental-health-checker/', 'メンタルヘルス・ストレスチェック'), ('https://appadaycreator.com/sleep-quality-checker/', 'Sleep Quality Checker'), ('https://appadaycreator.com/health-check-explainer/', '健康診断数値解説ツール')]

CUSTOM_CSS = """"""

# MAIN_HTML≤100行 / 色=#EA580C / class="card"でUI / id="result"で結果隠し
MAIN_HTML = """<div class="card">
  <h2 style="font-size:18px;font-weight:700;margin-bottom:16px;">🩺 血圧判定・アドバイザー</h2>
  <label>収縮期血圧（上の血圧）mmHg</label>
  <input type="number" id="systolic" placeholder="例: 120" min="60" max="250">
  <label>拡張期血圧（下の血圧）mmHg</label>
  <input type="number" id="diastolic" placeholder="例: 80" min="40" max="150">
  <label>年齢</label>
  <select id="age">
    <option value="young">〜39歳</option>
    <option value="middle" selected>40〜64歳</option>
    <option value="senior">65歳以上</option>
  </select>
  <label>測定タイミング</label>
  <select id="timing">
    <option value="morning">朝（起床後1時間以内・服薬前）</option>
    <option value="evening" selected>夜（就寝前）</option>
    <option value="clinic">病院・医院での測定</option>
  </select>
  <button class="btn" style="margin-top:20px;" onclick="generate()">血圧を判定する</button>
</div>
<div class="result" id="result" style="margin-top:16px;">
  <div class="card">
    <h3 style="font-size:15px;font-weight:700;margin-bottom:12px;color:#6366F1;">📋 血圧判定結果</h3>
    <div id="output"></div>
  </div>
</div>"""

# JS: スタブの TODO コメント箇所を実装してください（骨格は変えないこと）
JS_CODE = """const STANDARDS = [
  { label:'低血圧', sMax:89, dMax:59, color:'#3b82f6', advice:'低血圧は急な立ち上がり時のめまい・立ちくらみに注意。水分をしっかり摂り、急に動かないよう気をつけてください。貧血の可能性もあるため、症状が続く場合は内科を受診しましょう。' },
  { label:'正常血圧', sMax:119, dMax:79, color:'#10b981', advice:'理想的な血圧です。この状態を維持するために、適度な運動（週150分の有酸素運動）、減塩（1日6g未満）、禁煙、節酒を継続しましょう。定期的な測定を習慣化することが大切です。' },
  { label:'正常高値血圧', sMax:129, dMax:84, color:'#f59e0b', advice:'正常範囲ですが、将来的に高血圧になるリスクが高い状態です。減塩（1日6g未満）・体重管理（BMI25未満）・禁煙・節酒（男性21単位/週以下）を実践。3〜6ヶ月で改善しない場合は内科を受診してください。' },
  { label:'高値血圧', sMax:139, dMax:89, color:'#f97316', advice:'高血圧の一歩手前です。生活習慣の改善が強く推奨されます。①食塩を減らす（外食・加工食品に注意） ②毎日30分以上のウォーキング ③ストレス管理（深呼吸・瞑想） ④体重を標準体重に近づける。内科で定期チェックを始めましょう。' },
  { label:'Ⅰ度高血圧', sMax:159, dMax:99, color:'#ef4444', advice:'高血圧です。かかりつけ医への受診をお勧めします。生活習慣改善（減塩・運動・節酒）と並行して、必要に応じて降圧薬の服用を医師と相談してください。朝晩の定期測定（家庭血圧測定）で変化を記録することが重要です。' },
  { label:'Ⅱ〜Ⅲ度高血圧（重症）', sMax:999, dMax:999, color:'#dc2626', advice:'重症の高血圧です。早急に内科・循環器科を受診してください。脳卒中・心筋梗塞・腎臓病のリスクが高い状態です。降圧薬による治療が必要な可能性が高く、自己判断での治療中断は危険です。ただちに医療機関を受診してください。' },
];
function getInputs() {
  const sys = parseInt(document.getElementById('systolic').value);
  const dia = parseInt(document.getElementById('diastolic').value);
  if(!sys || !dia || sys < 60 || sys > 250 || dia < 40 || dia > 150) {
    alert('正しい血圧値を入力してください（収縮期60-250、拡張期40-150）'); return null;
  }
  return { sys, dia, age: document.getElementById('age').value, timing: document.getElementById('timing').value };
}
function buildOutput(inputs) {
  const { sys, dia, timing } = inputs;
  let std = STANDARDS[STANDARDS.length-1];
  for(const s of STANDARDS) {
    if(sys <= s.sMax && dia <= s.dMax) { std = s; break; }
  }
  const timingNote = timing === 'morning' ? '（朝測定値）' : timing === 'evening' ? '（夜測定値）' : '（診察室測定値）';
  const clinicNote = timing === 'clinic' ? '<p style="font-size:12px;color:#6b7280;margin-top:8px;">※診察室血圧は家庭血圧より5〜10mmHg高く出る傾向があります</p>' : '';
  return `<div style="background:${std.color}15;border-left:4px solid ${std.color};border-radius:8px;padding:16px;margin-bottom:12px;">
    <div style="font-size:12px;color:#6b7280;margin-bottom:4px;">あなたの血圧 ${sys}/${dia} mmHg ${timingNote}</div>
    <div style="font-size:24px;font-weight:700;color:${std.color};">${std.label}</div>
    ${clinicNote}
  </div>
  <div style="font-size:13px;color:#374151;line-height:1.8;padding:12px;background:#f8fafc;border-radius:8px;">
    <strong>💡 アドバイス</strong><br>${std.advice}
  </div>`;
}
document.addEventListener('DOMContentLoaded',()=>{});
function generate() {
  const inputs = getInputs(); if(!inputs) return;
  document.getElementById('output').innerHTML = buildOutput(inputs);
  document.getElementById('result').classList.add('show');
  document.getElementById('result').scrollIntoView({behavior:'smooth',block:'start'});
}"""

FAQ = [
    ("血圧チェック・生活改善アドバイスは無料で使えますか？", "はい、完全無料・登録不要でご利用いただけます。"),
    ("何回でも使えますか？", "はい、回数制限なく何度でもご利用いただけます。"),
    ("入力したデータはサーバーに送信されますか？", "いいえ。すべての処理はブラウザ内で完結し、入力内容はサーバーへ送信されません。"),
    ("スマートフォンでも使えますか？", "はい、スマートフォン・タブレット・PCすべてに最適化されています。"),
    ("結果を保存・共有できますか？", "スクリーンショットでの保存またはSNSシェアボタンからご共有いただけます。"),
]

HOW_TO = [
    "ページを開き、入力フォームの項目を確認する",
    "必要な情報を入力または選択する",
    "実行ボタンをクリックして結果を取得する",
    "表示された結果・アドバイスを確認する",
    "必要に応じてコピー・SNSシェアで活用する",
]

