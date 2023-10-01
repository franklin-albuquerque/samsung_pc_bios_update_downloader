from os import system, name as system_name
from re import findall
from requests import get
from subprocess import run, PIPE
from time import sleep


def download_bios_update(version, platform):
    while True:
        match system_name:
            case 'nt':
                system('cls')
            case 'posix':
                system('clear')

        print(f'Current BIOS version: {version}')
        print(f'Platform ID: {platform}', end='\n\n')

        try:
            url = f"http://sbuservice.samsungmobile.com/BUWebServiceProc.asmx/GetContents?platformID={platform}&PartNumber=AAAA"
            string = get(url).text

            filepath_column = findall(r'<FilePathName>([a-zA-Z0-9_.]+)<\/FilePathName>', string)
            executable = filepath_column[0]

            version_column = findall(r'<Version>([a-zA-Z0-9]+)<\/Version>', string)
            version = version_column[0]

            file_url = f"http://sbuservice.samsungmobile.com/upload/BIOSUpdateItem/{executable}"

            if platform in file_url:
                response = get(file_url, stream=True)
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
        sleep(0.75)
    print('', end='\n')


def main():
    bios_info = run('wmic bios get smbiosbiosversion', stdout=PIPE)
    version = bios_info.stdout.decode('utf-8').split()[1]
    platform = version.split('.')[0][3:]

    download_bios_update(version, platform)


if __name__ == '__main__':
    main()
