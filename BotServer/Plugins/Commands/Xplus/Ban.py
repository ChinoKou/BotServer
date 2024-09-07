# 导入必要的库和模块
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import CommandArg

# 导入本地模块和配置
from Scripts.Config import config
from Scripts.Managers import server_manager, data_manager
from Scripts.Utils import Rules, get_permission, get_user_name, get_args, check_player
from .Base import async_lock

# 定义一个命令匹配器，用于处理 'ban' 命令
matcher = on_command('ban', force_whitespace=True, block=True, priority=5, rule=Rules.command_rule)


# 处理群组消息事件
@matcher.handle()
async def handle_group(event: GroupMessageEvent, args: Message = CommandArg()):
    # 检查用户权限，如果没有权限则结束命令执行
    if not get_permission(event):
        await matcher.finish('你没有权限执行此命令！')
    if player := args.extract_plain_text().strip():
        message = await ban_handler(event, player)
        await matcher.finish(message, at_sender=True)
    await matcher.finish('请输入要绑定的玩家名称！')


# 处理绑定添加逻辑的异步函数
async def ban_handler(event: GroupMessageEvent, player: str):
    # 上锁以确保线程安全
    async with async_lock:
        # 参数检查：用户QQ号格式不正确则返回错误信息
        #if not user.isdigit():
        #   return '参数错误！绑定的 QQ 号格式错误。'
        # 参数检查：玩家名称不合法则返回错误信息
        if not check_player(player):
            return '玩家名称非法！玩家名称只能包含字母、数字、下划线且长度不超过 16 个字符。'
        # 参数检查：如果没有连接的服务器，则返回错误信息
        if not server_manager.check_online():
            return '当前没有已链接的服务器，绑定失败！请连接后再试。'
        # 尝试获取用户昵称，如果用户不在群聊中则返回错误信息
        #if user_name := await get_user_name(group, int(user)):
        await server_manager.execute(F'{config.ban_command} {player}')
        return F'已成功全服同步封禁玩家 {player}'
        # 用户不在群聊中，返回错误信息
        #return F'用户 {user} 不在此群聊！请检查 QQ 号是否正确。'
