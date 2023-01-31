import requests

url = 'https://twitter.com/Kelvin9789/status/1581630283581128712?s=20&t=4HLLahQHLgkh_236L8eNvA'
url = 'https://twitter.com/Kelvin9789/status/1581630283581128712?s=20&t=y9Muds3Ek_bzeFoR50BP-w'
url = 'https://twitter.com/Kelvin9789/status/1581630283581128712?s=20&t=gCr2AoCDoLnprqHulpcmIg'


resp = requests.get(url)

print(resp.status_code)
print(resp.text)

with open('page.html', 'w') as fp:
  fp.write(resp.text)
