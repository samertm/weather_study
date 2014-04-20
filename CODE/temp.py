def main(url):
    start_time = time.time()
    forecast = make_urlrequest(url)
    print(time.time() - start_time)
    forecast = forecast.readall().decode()
    return forecast[-500:]

def make_urlrequest(url):
    """Tries to make URL request until successful."""
    content = ''
    while content == '':
        try:
            content = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            print(url, e, sep='\n', end='\n\n')
            content = ''
    return content

