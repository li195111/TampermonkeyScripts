import requests

stories_url = 'https://www.instagram.com/stories/joanne_722/2998818863919030129/'

resp = requests.get(stories_url)
html_str = resp.text
reels_id_start_str = '"props":{"user":{"id":"'
reels_id_end_str = '","profile_pic_url"'
reels_id_start_idx = html_str.find(reels_id_start_str)
reels_id_end_idx = html_str.find(reels_id_end_str)
# reels_id_end_idx += len(reels_id_end_str)
reels_id_script = html_str
if reels_id_start_idx != -1 and reels_id_end_idx != -1:
  reels_id_start_idx += len(reels_id_start_str)
  reels_id_script = reels_id_script[reels_id_start_idx:reels_id_end_idx]

print(reels_id_script)

'https://instagram.ftpe3-2.fna.fbcdn.net/o1/v/t16/f1/m78/9040BA3B230D2CD9BF73A9600BD0CE88_video_dashinit.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJvaWxyMWNcIl0ifQ&_nc_ht=instagram.ftpe3-2.fna.fbcdn.net&_nc_cat=107&ccb=9-4&oh=00_AfB-MNbIVnf266CalWTTjFWMo1eT49NehP4b5SPovLSTTA&oe=63A6E0A0&_nc_sid=276363&bytestart=844&byteend=887'
ig_ftp = 'https://instagram.ftpe3-2.fna.fbcdn.net'

payload = 'https://www.instagram.com/api/v1/feed/reels_media/?media_id=2998842940641982171&reel_ids=531042427'
# payload_request_header = {
# :authority: www.instagram.com
# :method: GET
# :path: /api/v1/feed/reels_media/?media_id=2998921371509429320&reel_ids=531042427
# :scheme: https
# accept: */*
# accept-encoding: gzip, deflate, br
# accept-language: zh-TW,zh;q=0.9
# cache-control: no-cache
# cookie: csrftoken=Fkv2MlqWOTNU7QPUFvJvYcGmWOeJcnrM; ds_user_id=549894763; mid=YzqI4QALAAFiLjtBe2Aqpc08mg51; ig_did=D7FB783C-5A85-4A23-B315-E7F27A7337AF; datr=W4FoY5f6cOoxZhR0Nifv2Ytr; dpr=1.100000023841858; shbid="3317\054549894763\0541703236118:01f7bc076d705b957cb78bb660a1c8bbec640df1e17426a5119c303825b8f13be65783fb"; shbts="1671700118\054549894763\0541703236118:01f7a183d8042fd8bbc62d0506366cbc2692460ea05011f656d1701f177e292bc6fa4e05"; sessionid=549894763%3Ax16CijECLDK652%3A25%3AAYe1XD4T2xohP5x99LKX_W2rkKG8z-wL9zn4cuqx8KQ; rur="EAG\054549894763\0541703294009:01f7200f7d07060c7bc05aa8decf87e3d86000e27b88ba6da671b1942b4a6e2e38a5ee0e"
# pragma: no-cache
# referer: https://www.instagram.com/stories/freyaachuang/2998921371509429320/
# sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Brave";v="108"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"
# sec-fetch-dest: empty
# sec-fetch-mode: cors
# sec-fetch-site: same-origin
# sec-gpc: 1
# user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
# x-asbd-id: 198387
# x-csrftoken: Fkv2MlqWOTNU7QPUFvJvYcGmWOeJcnrM
# x-ig-app-id: 936619743392459
# x-ig-www-claim: hmac.AR2Hpl4p9FB99qpncSy2fUdScxJ7A8_Pv2M9MwO3TXeP_d9Z
# x-requested-with: XMLHttpRequest}

media_url = 'https://instagram.ftpe3-2.fna.fbcdn.net/o1/v/t16/f1/m78/9040BA3B230D2CD9BF73A9600BD0CE88_video_dashinit.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJvaWxyMWNcIl0ifQ&_nc_ht=instagram.ftpe3-2.fna.fbcdn.net&_nc_cat=107&ccb=9-4&oh=00_AfB-MNbIVnf266CalWTTjFWMo1eT49NehP4b5SPovLSTTA&oe=63A6E0A0&_nc_sid=276363&bytestart=0&byteend=1821659'

picture = 'https://instagram.ftpe3-1.fna.fbcdn.net/v/t51.2885-15/321377365_691313092369146_350104503102052255_n.jpg?stp=dst-jpg_e15&_nc_ht=instagram.ftpe3-1.fna.fbcdn.net&_nc_cat=106&_nc_ohc=2Bi5czdqjFwAX8XLW2P&edm=ANmP7GQBAAAA&ccb=7-5&ig_cache_key=Mjk5ODg0Mjk0MDY0MTk4MjE3MQ%3D%3D.2-ccb7-5&oh=00_AfDAHzo_L68okFz0MXVBNUtMIVI6V93KEZ70U_xcvi_J6Q&oe=63A65774&_nc_sid=276363'

