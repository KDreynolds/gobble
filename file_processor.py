import os
import chardet

class FileProcessor:
    def process_directory(self, dir_path, max_file_size=100000):  # 100KB limit
        files = {}
        total_size = 0
        for root, _, filenames in os.walk(dir_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if os.path.getsize(file_path) > max_file_size:
                    continue
                relative_path = os.path.relpath(file_path, dir_path)
                content = self.read_file(file_path)
                if content is not None:
                    file_size = len(content.encode('utf-8'))
                    if total_size + file_size > 1000000:  # 1MB total limit
                        break
                    files[relative_path] = content
                    total_size += file_size
        return files

    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
            
            if self.is_binary(raw_data):
                return None

            detected = chardet.detect(raw_data)
            if detected['encoding'] is None:
                return None

            return raw_data.decode(detected['encoding'], errors='ignore')
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return None

    def is_binary(self, data):
        textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
        return bool(data.translate(None, textchars))