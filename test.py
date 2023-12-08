import requests
import numpy as np

api_url = 'http://localhost:5000/topcomments?year_from=2010&year_to=2015&top_n=10'
number_of_requests = 100

def run_api_requests():
    response_times = []

    for i in range(number_of_requests):
        api_url = f'http://localhost:5000/topcomments?year_from=2000&year_to=2015&top_n={i + 1}'
        start_time = time.time()
        try:
            response = requests.get(api_url)
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(duration)
            print(f"Request {i + 1}: {response.status_code} - {response.reason} - {duration:.2f} ms")
        except requests.RequestException as error:
            print(f"Request {i + 1} failed: {error}")

    # Calculate metrics
    average = np.mean(response_times)
    median = np.percentile(response_times, 50)
    ninetieth_percentile = np.percentile(response_times, 90)

    print(f"Average Response Time: {average:.2f} ms")
    print(f"50th Percentile (Median): {median:.2f} ms")
    print(f"90th Percentile: {ninetieth_percentile:.2f} ms")

if __name__ == "__main__":
    import time
    run_api_requests()
