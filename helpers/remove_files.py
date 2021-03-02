from os import listdir, remove, path
directory = path.abspath('downloads')

class RemoveFiles:
    @staticmethod
    def remove_all():
        for file in listdir(directory):
            remove(f"{directory}/{file}")
            
    @staticmethod
    def remove_one(file):
        remove(f"{directory}/{file}")
        
if __name__ == '__main__':
    pass
    