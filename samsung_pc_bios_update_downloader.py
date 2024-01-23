import os
import re
import requests
import subprocess
import time


class DownloadBiosUpdate:
    def __init__(self):
        self.bios_info = subprocess.run('wmic bios get smbiosbiosversion', stdout=subprocess.PIPE)
        self.version = self.bios_info.stdout.decode('utf-8').split()[1]
        self.platform = self.version.split('.')[0][3:]


    def clear_screen(self):
        match os.name:
            case 'nt':
                os.system('cls')
            case 'posix':
                os.system('clear')


    def download_bios_update(self):
        while True:
            self.clear_screen()

            print(f'Current BIOS version: {self.version}')
            print(f'Platform ID: {self.platform}', end='\n\n')

            try:
                url = f"http://sbuservice.samsungmobile.com/BUWebServiceProc.asmx/GetContents?platformID={self.platform}&PartNumber=AAAA"
                string = requests.get(url).text

                filepath_column = re.findall(r'<FilePathName>([a-zA-Z0-9_.]+)<\/FilePathName>', string)
                executable = filepath_column[0]

                file_url = f"http://sbuservice.samsungmobile.com/upload/BIOSUpdateItem/{executable}"

                if self.platform in file_url:
                    response = requests.get(file_url, stream=True)
                    content_type = response.headers.get('content-type', '')

                    if response.status_code == 200 and not 'text' in content_type:
                        print(f'Downloading the latest bios update...')
                        with open(f'{executable}', 'wb') as bios_update:
                            for chunk in response.iter_content(chunk_size=4096):
                                bios_update.write(chunk)
                        print('Download completed successfully.')
                        break

                else:
                    print('Error! The server returned an incompatible version.')

            except KeyError:
                print('Error! The server did not return any results.')

            except:
                print('An error has occurred!')

            print('Trying again...', end='\n\n')
            time.sleep(1.15)
        print('', end='\n')


def main():
    bios_updater = DownloadBiosUpdate()
    bios_updater.download_bios_update()


if __name__ == '__main__':
    main()
