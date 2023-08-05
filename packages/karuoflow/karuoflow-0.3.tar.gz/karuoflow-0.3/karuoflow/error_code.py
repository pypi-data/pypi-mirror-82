# -*- encoding: utf-8 -*-
'''
@文件    :erro_code.py
@说明    :
@时间    :2020/09/04 11:43:13
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

from enum import Enum

class KaruoFlowErrors(Enum):
    SUCCESS = 0
    ERR_UNKOWN = 1
    ERR_DATA_NOT_FOUND = 2                  # 数据记录没有在数据库查找到
    ERR_FLOW_STATUS_INVALID = 3             # 流程的状态被禁用
    ERR_FLOW_CLOSED = 4                     # 流程已结束
    ERR_FLOW_OWNER_INVALID = 5              # 非流程所有人
    ERR_DB_EXCEPTION = 6                    # 数据库异常


    @classmethod
    def errorMsg(cls, code):
        if code == KaruoFlowErrors.SUCCESS:
            return "success"
        elif code == KaruoFlowErrors.ERR_UNKOWN:
            return "通用错误"
        elif code == KaruoFlowErrors.ERR_DATA_NOT_FOUND:
            return "数据记录没有找到"
        elif code == KaruoFlowErrors.ERR_FLOW_STATUS_INVALID:
            return "流程阶段无效"
        elif code == KaruoFlowErrors.ERR_FLOW_CLOSED:
            return "流程状态已关闭"
        elif code == KaruoFlowErrors.ERR_FLOW_OWNER_INVALID:
            return "流程的所有者不正确，或许由权限引起"
        elif code == KaruoFlowErrors.ERR_DB_EXCEPTION:
            return "数据库异常"
        else:
            return "未捕获错误"