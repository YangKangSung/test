import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid # Content-ID 생성을 위해

# --- Gmail 계정 정보 및 수신자 설정 ---
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # SSL 사용 시
SMTP_USER = 'ksyang@gmail.com'  # 보내는 사람 Gmail 주소
SMTP_PASSWORD = 'your_app_password'  # Gmail 앱 비밀번호 (2단계 인증 사용 권장)

TO_EMAIL = 'recipient_email@example.com'  # 받는 사람 이메일 주소
SUBJECT = 'Python으로 보내는 이미지 포함 메일 (본문 상단 표시)'

# --- 이미지 파일 경로 ---
# 이 스크립트와 같은 디렉토리에 'sample_image.png' 파일이 있다고 가정합니다.
# 실제 이미지 경로로 변경해주세요.
IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'sample_image.png')
if not os.path.exists(IMAGE_PATH):
    print(f"오류: 이미지 파일을 찾을 수 없습니다 - {IMAGE_PATH}")
    print("스크립트와 같은 디렉토리에 'sample_image.png'를 준비하거나 IMAGE_PATH를 수정하세요.")
    exit()

# --- 메일 객체 생성 ---
# 전체 메일은 'related' 타입으로, HTML과 이미지가 연관됨을 나타냅니다.
msg_root = MIMEMultipart('related')
msg_root['Subject'] = SUBJECT
msg_root['From'] = SMTP_USER
msg_root['To'] = TO_EMAIL

# 'alternative' 타입으로 HTML과 일반 텍스트를 묶습니다.
msg_alternative = MIMEMultipart('alternative')
msg_root.attach(msg_alternative)

# --- 일반 텍스트 본문 (HTML 미지원 클라이언트용) ---
plain_text_body = """
안녕하세요,
이 메일은 이미지가 본문 상단에 포함된 HTML 형식입니다.
HTML을 지원하지 않는 경우 이미지가 제대로 표시되지 않을 수 있습니다.

감사합니다.
"""
msg_text = MIMEText(plain_text_body, 'plain', 'utf-8')
msg_alternative.attach(msg_text)

# --- HTML 본문 ---
# 이미지 Content-ID 생성 (꺾쇠괄호 없이)
image_cid_value = make_msgid(domain='example.com').strip('<>') # 고유 ID 생성 후 꺾쇠 제거

html_body = f"""
<html>
  <head></head>
  <body>
    <p><img src="cid:{image_cid_value}" alt="메인 이미지"></p>
    <p>안녕하세요,</p>
    <p>이것은 파이썬으로 보낸 테스트 메일입니다.</p>
    <p>이미지가 본문 상단에 잘 표시되나요?</p>
    <p>메일 내용입니다...</p>
    <p>감사합니다.</p>
  </body>
</html>
"""
msg_html = MIMEText(html_body, 'html', 'utf-8')
msg_alternative.attach(msg_html)

# --- 이미지 파일 첨부 (인라인) ---
try:
    with open(IMAGE_PATH, 'rb') as fp:
        img_data = fp.read()
    msg_image = MIMEImage(img_data)
    # Content-ID 헤더 설정 (꺾쇠괄호 포함)
    msg_image.add_header('Content-ID', f'<{image_cid_value}>')
    msg_image.add_header('Content-Disposition', 'inline', filename=os.path.basename(IMAGE_PATH))
    msg_root.attach(msg_image)
except FileNotFoundError:
    print(f"오류: 이미지 파일 '{IMAGE_PATH}'를 찾을 수 없습니다.")
    exit()
except Exception as e:
    print(f"이미지 처리 중 오류 발생: {e}")
    exit()

# --- SMTP 서버를 통해 메일 발송 ---
try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg_root)
    print("메일 전송 성공!")
except smtplib.SMTPAuthenticationError:
    print("메일 전송 실패: SMTP 인증 오류. 이메일 주소나 앱 비밀번호를 확인하세요.")
except Exception as e:
    print(f"메일 전송 중 오류 발생: {e}")

