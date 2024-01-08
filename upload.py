import os
import requests


class UploadScript2DS:
    def __init__(self, local_path):
        self.headers = {
            # 自己的token
            'token': ''
        }
        # 改为自己的host
        self.host = ""
        self.local_path = local_path

    def upload_single_dir(self, current_dir, static_path, description=None):
        payload = {
            'pid': '-1',
            'type': 'FILE',
            'currentDir': f'file:{current_dir}/',
            'description': description,
            'name': static_path
        }
        response = requests.request("POST", self.host + "/dolphinscheduler/resources/directory", headers=self.headers,
                                    data=payload)
        print(f"文件夹{static_path}: {response.status_code}")

        url = self.host + "/dolphinscheduler/resources"
        current_dir = current_dir + '/' + static_path

        # Recursive function to upload files
        def upload_files(path, current_dir):
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    payload = {
                        'pid': '-1',
                        'type': 'FILE',
                        'currentDir': f'file:{current_dir}/',
                        'description': description,
                        'name': item
                    }
                    response = requests.request("POST", self.host + "/dolphinscheduler/resources/directory", headers=self.headers, data=payload)
                    print(f"文件夹{item}: {response.status_code}")
                    upload_files(full_path, current_dir + '/' + item)  # Recursive call
                else:
                    payload = {
                        'type': 'FILE',
                        'currentDir': f'file:{current_dir}/',
                        'description': description,
                        'name': item
                    }

                    files = [
                        ('file', (item, open(full_path, 'rb'), 'application/octet-stream'))
                    ]

                    response = requests.request("POST", url, headers=self.headers, data=payload, files=files)
                    print(f"{item}: {response.status_code}")

        upload_files(self.local_path, current_dir)


if __name__ == '__main__':
    # 本地文件地址
    dir_path = r"E:\LBI\项目\ask-nature"
    # 获取dir_path的最后一个文件夹名
    static_path = os.path.basename(dir_path)
    upload = UploadScript2DS(dir_path)
    upload.upload_single_dir(f'/dolphinscheduler/default/resources', static_path, '测试')
