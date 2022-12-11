from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't get the website!")
    else:
        results = []
        soup = BeautifulSoup(response.text, 'html.parser')
        job_section = soup.find_all('section', class_="jobs")
        for section in job_section:
            job_list = section.find_all('li')
            job_list.pop(-1)
            for list in job_list:
                anchors = list.find_all('a')
                anchor = anchors[1]
                title = anchor.find('span', class_='title')
                company, kind, location = anchor.find_all('span',
                                                          class_="company")
                result = {
                    'company': company.string,
                    'position': title.string,
                    'location': location.string
                }

                for each in result:
                    if result[each] != None:
                        result[each] = result[each].replace(",", "  ")
                results.append(result)
            return results
