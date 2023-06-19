import requests
import threading

def load_proxy_list(filename):
    with open(filename, 'r') as file:
        proxy_list = file.read().splitlines()
    return proxy_list

def make_request_with_proxy(proxy, url, headers, data, timeout):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=timeout)
        print(f"Response from {proxy}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error with {proxy}: {str(e)}")

def process_proxies(proxy_list, url, headers, data, timeout):
    for proxy in proxy_list:
        make_request_with_proxy(proxy, url, headers, data, timeout)

def main():
    url = 'https://api.urbandictionary.com/v0/vote'
    headers = {
        'Host': 'api.urbandictionary.com',
        'Connection': 'keep-alive',
        'Content-Length': '34',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-platform': '"Windows"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': '*/*',
        'Origin': 'https://www.urbandictionary.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.urbandictionary.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    data = '{"defid":5632080,"direction":"up"}'
    timeout = 10

    proxy_list = load_proxy_list('proxies.txt')

    threads = []
    num_threads = 250  # Adjust the number of threads as desired

    # Split the proxy list into equal chunks for concurrent processing
    chunk_size = len(proxy_list) // num_threads
    proxy_chunks = [proxy_list[i:i+chunk_size] for i in range(0, len(proxy_list), chunk_size)]

    # Create and start the threads
    for i in range(num_threads):
        thread = threading.Thread(target=process_proxies, args=(proxy_chunks[i], url, headers, data, timeout))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
