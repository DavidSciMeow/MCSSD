import argparse
import json
from mcssd.mod.modutil import search_mods, MCVersion

def mcver_type(value):
    try:
        return MCVersion(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"错误版本号。不支持当前版本 {value}")

available_versions = ', '.join([version.value for version in MCVersion])

parser = argparse.ArgumentParser(description='搜索Minecraft模组。')
parser.add_argument('-n','--keyword', type=str, help='搜索关键词, 可空。')
parser.add_argument('-f','--fuzzy', action='store_true', help='是否进行模糊匹配。默认值为False。')
parser.add_argument('-c','--category', type=int, default=0, help='搜索类别。默认值为0, 不添加类别参数。1: 科技, 2: 魔法, 3: 冒险, 4: 农业, 5: 装饰, 6: 实用, 7: 辅助, 8: 魔改, 9: lib, 10: 资源, 11: 世界, 12: 群系, 13: 结构, 14: 生物, 15: 能源, 16: 存储, 17: 物流, 18: 道具, 19: 安全, 20: 红石, 21: 食物, 22: 模型, 23: 关卡, 24: 指南, 25: 破坏, 26: Meme, 27: 中式, 28: 日式, 29: 西式, 30: 恐怖, 31: 建材, 32: 生存, 33: 指令, 34: 优化, 35: 国创')
parser.add_argument('-m','--mode', type=int, default=0, help='搜索模式。默认值为0, 不添加模式参数。1: 仅客户端, 2: 仅服务端, 3: 主客户端, 4: 主服务端, 5: 皆需安装')
parser.add_argument('-p','--platform', type=int, default=0, help='平台。默认值为0, 不添加平台参数。1: Java版本, 2: Bedrock版本')
parser.add_argument('-v','--mcver', type=mcver_type, help=f'Minecraft版本。默认值为None, 不添加版本参数。可用版本: {available_versions}')
parser.add_argument('-i','--api', type=int, default=0, help='API类型。默认值为0, 不添加API参数。1: forge, 2: fabric, 3: quilt, 4: neoforge, 5: rift, 6: liteloader, 7: 数据包, 8: 行为包, 9: 命令方块, 10: 文件覆盖')
parser.add_argument('-t','--status', type=int, default=0, help='状态。默认值为0, 不添加状态参数。1: 活跃, 2: 半弃坑, 3: 停更')
parser.add_argument('-s','--sort', type=int, default=0, help='排序方式。默认值为0, 不添加排序参数。1: 按收录时间, 2: 按最后编辑时间')

args = parser.parse_args()
result = search_mods(args.keyword, args.fuzzy, args.category, args.mode, args.platform, args.mcver, args.api, args.status, args.sort)

print(json.dumps(result, ensure_ascii=False, indent=4))