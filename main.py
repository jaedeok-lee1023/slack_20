import os
import sys
import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2025-01-01",  # 신정
    "2025-10-06",  # 추석
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")


def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")


def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f":loudspeaker: *『인사총무팀 공지』*\n\n"

        # 직원식당 에티켓 안내 메시지
        notice_msg = (
            f"안녕하세요, 평택 클러스터 구성원 여러분!\n\n"
            f"쾌적하고 효율적인 직원식당 이용을 위해\n"
            f"아래와 같이 에티켓을 안내드립니다.\n"
            f"구성원 여러분의 적극적인 협조 부탁드립니다.\n\n"
            f":k체크: 직원식당 관계자에게 폭언·욕설 및 모욕적 언행을 하지 않기\n"
            f":k체크: 직원식당 집기를 외부로 반출하지 않기\n"
            f":k체크: 식사 시 타인에게 불편을 주는 행동 하지 않기\n"
            f":k체크: 적정량만 배식하여 음식물 낭비 줄이기\n"
            f":k체크: 사용한 자리는 다음 사람을 위해 깨끗하게 정리하기\n\n"
            f":point_right: (Click) - *<https://static.wixstatic.com/media/50072f_4ba099914a4b413f8bce587dec6274f0~mv2.png|직원식당 에티켓>*\n\n"
            f"*문의 : 인사총무팀 (총무/시설 담당자)*\n\n"
            f"감사합니다.\n"
        )

        # 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)


if __name__ == "__main__":
    main()
