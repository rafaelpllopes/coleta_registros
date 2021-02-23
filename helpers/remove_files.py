from os import listdir, remove, path

class RemoveFiles:
    @staticmethod
    def remove_all():
        directory = path.abspath('downloads')
        for file in listdir(directory):
            remove(f"{directory}/{file}")
            
    @staticmethod
    def remove_one(file):
        directory = path.abspath('downloads')
        remove(f"{directory}/{file}")
        
if __name__ == '__main__':
    pass
    