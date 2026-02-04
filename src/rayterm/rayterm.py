import os

def apps():
    prompt = input('{rayterm}\n')
    if prompt == 'all':
        apps = [f for f in sorted(os.listdir('/Applications')) if f.endswith('.app')]
        print('\n'.join(apps))
    else:
        os.system(f'open -a {prompt}') 



if __name__ == "__main__":
    apps()

