import spotipy
from spotipy import oauth2
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# авторизация в spotify
def autorisation():
    client_id = '52bd31fd49ac4cbbb3b7be8b0fc6c30b'
    client_secret = '1a5576844d4149dcb5d1d6f7f749f46b'
    scope = ('user-library-read, playlist-read-private, playlist-modify-private, playlist-modify-public, user-read-private, user-library-modify, user-library-read')
    redirect_uri = 'http://localhost:8888/callback/'
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    code = sp_oauth.get_auth_response(open_browser=True)
    token = sp_oauth.get_access_token(code, as_dict=False)
    sp = spotipy.Spotify(auth=token)
    time.sleep(2)
    username = sp.current_user()['id']
    time.sleep(2)
    return sp, username


sp, username = autorisation()

# поиск id трэка
def get_track_id(query, sp):
    track_id = sp.search(q=query, limit=1, type='track')
    return track_id['tracks']['items'][0]['id'].split()


number_music = int(input('Введите кол-во песен: '))
playlist_name = input('Введите название плейлиста: ')
login = input('Введите логин для вк: ')
password = input('Введите пароль для вк: ')

# открываем музыку
browser = webdriver.Chrome('./driver/chromedriver')
time.sleep(4)
browser.get('https://vk.com')
time.sleep(5)
username_input = browser.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/form/input[8]')
username_input.send_keys(login)
time.sleep(3)
password_input = browser.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[1]/form/input[9]')
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)
time.sleep(3)
browser.find_element_by_id('l_aud').click()
time.sleep(3)
browser.find_element_by_class_name('CatalogBlock__headerActions').click()
time.sleep(2)

all_music = []

# скролим страницу
number = int(number_music/100)
for i in range(1, number + 2):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
nek = browser.find_elements_by_class_name('audio_row__performer_title')
nike = 0

# получаем песни и сортируем
for i in nek:
    nike += 1
    mus = i.text
    step_1 = mus.replace('feat. ', '')
    step_2 = step_1.replace('Feat. ', '')
    step_3 = step_2.replace('ft. ', '')
    step_4 = step_3.replace('Ft. ', '')
    step_5 = step_4.replace(' [NR]', '')
    step_6 = step_5.replace(' x ', ' ')
    if 'Prod. ' in step_6:
        j, i = step_6.split('Prod. ')
        mus_list = j.split('\n')
        all_music.append(mus_list)
    elif 'prod. ' in step_6:
        j, i = step_6.split('prod. ')
        mus_list = j.split('\n')
        all_music.append(mus_list)
    else:
        mus_list = step_6.split('\n')
        all_music.append(mus_list)

browser.close()
browser.quit()

print(f'Найдено песен в вк:{nike}.(если не соотвтествует числу введёному вначале, значит песен нет в самом вк)')
time.sleep(10)

# создаём плейлист
create_spotify_playlist = sp.user_playlist_create(username, playlist_name)
new_spotify_playlist_id = create_spotify_playlist['id']
new_spotify_playlist = {}
tu = 0
ty = 0
non_music = []

# ищим id трэков
for j in all_music:
    try:
        tu += 1
        artist_name = j[0]
        track_name = j[1]
        query = ' '.join([track_name, artist_name])
        spotify_track_id = get_track_id(query, sp)
        new_spotify_playlist[spotify_track_id[0]] = new_spotify_playlist_id

    except:
        non_music.append(j)

# добавляем песни в плейлист
for new_spotify_playlist_id, track_id in new_spotify_playlist.items():
    sp.playlist_add_items(track_id, new_spotify_playlist_id.split())
    ty += 1

print('Закончили')
print(f'Песен перенесено:{ty}')
print(f'Песен не перенесено:{tu-ty}')
print('Не найденные песни: ')
for i in non_music:
    print(i)

print('Скопируйте список в файл и добавьте вручную, если хотите.')
time.sleep(1000)
