import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup


username = "username"
password = "password"

login_url = "大学moodleのログインページのURL"

# usernameとpasswordを入力してログインする
def login_moodle(course_name):
    # ブラウザを開く。
    driver = webdriver.Chrome()
    
    # sessionを維持しながらログインする。
    session = requests.Session()
    session.get(login_url)
    cookies = session.cookies.get_dict()
    driver.get(login_url)
    driver.add_cookie({'name': 'MoodleSession', 'value': cookies['MoodleSession']})
    driver.refresh()
    time.sleep(1)

    
    # usernameとpasswordを入力する。
    username_elem = driver.find_element(By.ID, "username")
    username_elem.send_keys(username)
    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(password)

    # ログインボタンをクリックする。
    login_btn_elem = driver.find_element(By.ID, "loginbtn")
    login_btn_elem.click()

    # ページが開くまで待つ。
    time.sleep(2)

    # ログイン成功
    print("login success")

    # ログイン後のページのurlを取得する
    driver.get("大学moodleのログイン後のホームのURL")

    time.sleep(2)


    soup = BeautifulSoup(driver.page_source, "html.parser")

    # class="card dashboard-card" の要素をすべて取得
    course_elements = soup.find_all('div', class_='card dashboard-card')

    # 各要素をループして "multiline" の要素が "情報理論" という文字列を含むものを探す
    for course_element in course_elements:
        multiline_element = course_element.find('span', class_='multiline')
        if multiline_element:
            text = multiline_element.get_text()
            if course_name in text:
                # 見つかった場合、その要素に関連付けられたURLにアクセス
                course_link = course_element.find('a', href=True)
                if course_link:
                    course_url = course_link['href']
                    print(f"URLにアクセス: {course_url}")
                    driver.get(course_url)
                    time.sleep(2)
                    break
    
    # ブラウザを終了する。
    driver.quit()



# "木・3"のように曜日と時限を自動で生成して返す関数
def get_course_name(day, period):
    day_dict = {"Mon": "月", "Tue": "火", "Wed": "水", "Thu": "木", "Fri": "金"}

    #　大学の時間割に合わせて時限を設定する
    period_dict = {"08:40": "1", "10:30": "2", "13:00": "3", "14:50": "4", "16:40": "5"}
    print(f"****年度*学期・{day_dict[day]}{period_dict[period]}")
    return f"****年度*学期・{day_dict[day]}{period_dict[period]}"


def job():
    # 現在の曜日と時刻を取得する関数(土日は実行しない)
    day = time.strftime('%a')
    period = time.strftime('%H:%M')
    print(day, period)
    
    # periodの時刻になったら"木・3"のように曜日と時限を自動で生成して返す関数
    course_name = get_course_name(day, period)

    # moodleにログインする
    login_moodle(course_name)

    print("done")



# スケジュールを設定する
schedule.every().day.at("08:40").do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("14:50").do(job)
schedule.every().day.at("16:40").do(job)


while True:
    # 土曜日と日曜日の場合はループを抜ける
    day = time.strftime('%a')
    if day == "Sat" or day == "Sun":
        break

    schedule.run_pending()
    time.sleep(1)  # スケジュールを確認する間隔を設定


