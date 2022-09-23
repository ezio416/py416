# clear out old files from dist so we only upload the newly built version
import os

dist = f'{os.path.dirname(os.getcwd())}/dist'
for file in os.listdir(dist):
    os.remove(f'{dist}/{file}')
    print(f'deleted {file}')