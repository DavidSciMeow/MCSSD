import argparse
import json
from mcssd.mod.modutil import get_mod_details

parser = argparse.ArgumentParser(description='搜索Minecraft模组下载模式。')
parser.add_argument('-i','--id', type=str, help='modid')
args = parser.parse_args()
result = get_mod_details(args.id)

print(json.dumps(result, ensure_ascii=False, indent=4))