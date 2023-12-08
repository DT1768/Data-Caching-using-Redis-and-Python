import requests

def run_request(year_from, year_to, top_n):
    api_url = f'http://localhost:5000/topcomments?year_from={year_from}&year_to={year_to}&top_n={top_n}'
    response = requests.get(api_url)
    data = response.json()
    print(data)
    return response

if __name__ == "__main__":
    year_from = int(input("Enter the starting year: "))
    year_to = int(input("Enter the ending year: "))
    top_n = int(input("Enter the top N value: "))
    run_request(year_from,year_to,top_n)

