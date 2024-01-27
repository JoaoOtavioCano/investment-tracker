import subprocess

def execute_other_script():
    try:
        subprocess.run(['python', 'theServer.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing other_script.py: {e}")

if __name__ == '__main__':
    execute_other_script()