import asyncio
from pathlib import Path
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Sort files into folders based on their extensions.")
parser.add_argument("-s", "--source" , type=str, help="Path to the source folder.")
parser.add_argument("-d" , "--destination", type=str, help="Path to the destination folder.")

args = parser.parse_args()
source_folder = Path(args.source)
destination_folder = Path(args.destination)

async def read_folder(source_folder):
    files = []
    for path in source_folder.rglob('*'):
        if path.is_file():
            files.append(path)
    return files


async def copy_file(file, destination_folder, index):
    
    ext = file.suffix[1:] 
    
    target_folder = destination_folder / ext
    target_folder.mkdir(parents=True, exist_ok=True)
    target_path = target_folder / file.name
    
    loop = asyncio.get_event_loop()
    try:
        print(f"[{index}] Copying {file} to {target_path}...")
        await loop.run_in_executor(None, shutil.copy, file, target_path)
        print(f"[{index}] Copied {file} to {target_path}")
    except Exception as e:
        print(f"[{index}] Error: {e}")
    


async def main(source_folder, destination_folder):
    files = await read_folder(source_folder)
    
    tasks = []
    index = 0
    for file in files:
        tasks.append(copy_file(file, destination_folder, index))
        index +=1 
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(source_folder, destination_folder))
    print("Completed.")
    input()