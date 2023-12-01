import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

date = input("Please Enter a Date in the following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")


def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []
    championships = soup.find_all("div", {"class": "matchesList"})

    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.select('.ul .item.finish.liItem')
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            team_A = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            team_B = all_matches[i].find("div", {"class": "teamB"}).text.strip()

            match_result = all_matches[i].find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{int(match_result[0].text.strip())} - {int(match_result[1].text.strip())}"

            match_time = all_matches[i].find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()

            matches_details.append({
                "نوع البطولة": championship_title,
                "الفريق الأول": team_A,
                "الفريق الثاني": team_B,
                "ميعاد المباراة": match_time,
                "النتيجة": score
            })

    for i in range(len(championships)):
        get_match_info(championships[i])

    df = pd.DataFrame(matches_details)
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "csv_dosya.csv")
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f"File created at: {file_path}")

    # Read the created CSV file
    df_read = pd.read_csv(file_path)
    print(df_read)


main(page)