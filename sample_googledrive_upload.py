from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try :
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES) # 인증정보 파일
    creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

FILES = (
    ('방파제.jpeg'), #업로드 할 파일 이름
)

folder_id = '154vOPOdG3X2ibSmo6KlrhekP0Qe4QIz_' # 업로드 될 구글 드라이브의 위치 

for file_title in FILES :
    file_name = file_title
    metadata = {'name': '방파제.jpeg', # 업로드 될 파일 이름
                'parents' : [folder_id],
                'mimeType': None
                }

    res = DRIVE.files().create(body=metadata, media_body=file_name).execute()
    if res:
        print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))
