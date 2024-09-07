import asyncio

from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from Scripts.Utils import Rules, get_permission, get_user_name, turn_message

async_lock = asyncio.Lock()
matcher = on_command('xplus', force_whitespace=True, block=True, priority=5, rule=Rules.command_rule)


@matcher.handle()
async def handle_group(event: GroupMessageEvent):
    if not get_permission(event):
        await matcher.finish('你没有权限执行此命令！')
    message = turn_message(xplus_handler())
    await matcher.finish(message, at_sender=True)

def xplus_handler():
    yield ' '
    yield '====== 管理指令列表 ======'
    yield ' -------- bound --------'
    yield '  /bound remove [ID]/[QQ]'
    yield '  #解绑他人'
    yield '  /bound append [QQ] [ID]'
    yield '  #设置绑定'
    yield '  /bound query [QQ]'
    yield '  #查询某个QQ号绑定情况'
    yield '  /bound list'
    yield '  #列出绑定列表'
    yield '  ##所有QQ号均可使用@某人代替'
    yield ' '
    yield ' -------- command --------'
    yield '  /command [服务器] [指令]'
    yield '  #在某个服务器执行特定指令'
    yield '  /mcdr [服务器] [指令]'
    yield '  #在某个服务器执行MCDR指令'
    yield '  ##无返回值，请慎用！！！'
    yield ' '
    yield ' -------- ban --------'
    yield '  /ban [ID] 原因'
    yield '  #同步封禁玩家'
    yield '  /unban [ID]'
    yield '  #同步解封玩家'
    yield ' '
    yield '#没写完，别急着用'
