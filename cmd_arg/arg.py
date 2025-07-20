# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import argparse

import config
from tools.utils import str2bool


async def parse_cmd():
    # 读取command arg
    parser = argparse.ArgumentParser(description='Media crawler program.')
    parser.add_argument('--platform', type=str, help='Media platform select (xhs | dy | ks | bili | wb | tieba | zhihu)',
                        choices=["xhs", "dy", "ks", "bili", "wb", "tieba", "zhihu"], default=config.PLATFORM)
    parser.add_argument('--lt', type=str, help='Login type (qrcode | phone | cookie)',
                        choices=["qrcode", "phone", "cookie"], default=config.LOGIN_TYPE)
    parser.add_argument('--type', type=str, help='crawler type (search | detail | creator)',
                        choices=["search", "detail", "creator"], default=config.CRAWLER_TYPE)
    parser.add_argument('--start', type=int,
                        help='number of start page', default=config.START_PAGE)
    parser.add_argument('--max_count', type=int,
                        help='max number of notes/videos to crawl', default=config.CRAWLER_MAX_NOTES_COUNT)
    parser.add_argument('--keywords', type=str,
                        help='please input keywords', default=config.KEYWORDS)
    parser.add_argument('--specified_ids', type=str,
                        help='comma-separated list of specified note/video IDs or URLs for detail crawling', default=None)
    parser.add_argument('--creator_ids', type=str,
                        help='comma-separated list of creator IDs or URLs for creator crawling', default=None)
    parser.add_argument('--get_comment', type=str2bool,
                        help='''whether to crawl level one comment, supported values case insensitive ('yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0')''', default=config.ENABLE_GET_COMMENTS)
    parser.add_argument('--get_sub_comment', type=str2bool,
                        help=''''whether to crawl level two comment, supported values case insensitive ('yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0')''', default=config.ENABLE_GET_SUB_COMMENTS)
    parser.add_argument('--sync_to_mysql', type=str2bool,
                        help='whether to sync data to MySQL database', default=False)
    parser.add_argument('--cookies', type=str,
                        help='cookies used for cookie login type', default=config.COOKIES)
    parser.add_argument('--task_id', type=str,
                        help='task ID for tracking crawled data', default=None)

    args = parser.parse_args()

    # override config
    config.PLATFORM = args.platform
    config.LOGIN_TYPE = args.lt
    config.CRAWLER_TYPE = args.type
    config.START_PAGE = args.start
    config.CRAWLER_MAX_NOTES_COUNT = args.max_count
    config.KEYWORDS = args.keywords
    config.ENABLE_GET_COMMENTS = args.get_comment
    config.ENABLE_GET_SUB_COMMENTS = args.get_sub_comment
    config.SAVE_DATA_OPTION = "db"  # 默认保存到SQLite数据库
    config.SYNC_TO_MYSQL = args.sync_to_mysql
    config.COOKIES = args.cookies
    config.TASK_ID = args.task_id  # 设置任务ID
    
    # 处理动态ID列表参数
    if args.specified_ids:
        specified_ids_list = [id.strip() for id in args.specified_ids.split(',') if id.strip()]
        # 根据平台设置对应的配置
        if config.PLATFORM == 'xhs':
            config.XHS_SPECIFIED_NOTE_URL_LIST = specified_ids_list
        elif config.PLATFORM == 'dy':
            config.DY_SPECIFIED_ID_LIST = specified_ids_list
        elif config.PLATFORM == 'ks':
            config.KS_SPECIFIED_ID_LIST = specified_ids_list
        elif config.PLATFORM == 'bili':
            config.BILI_SPECIFIED_ID_LIST = specified_ids_list
        elif config.PLATFORM == 'wb':
            config.WEIBO_SPECIFIED_ID_LIST = specified_ids_list
        elif config.PLATFORM == 'tieba':
            config.TIEBA_SPECIFIED_ID_LIST = specified_ids_list
        elif config.PLATFORM == 'zhihu':
            config.ZHIHU_SPECIFIED_ID_LIST = specified_ids_list
    
    if args.creator_ids:
        creator_ids_list = [id.strip() for id in args.creator_ids.split(',') if id.strip()]
        # 根据平台设置对应的配置
        if config.PLATFORM == 'xhs':
            config.XHS_CREATOR_ID_LIST = creator_ids_list
        elif config.PLATFORM == 'dy':
            config.DY_CREATOR_ID_LIST = creator_ids_list
        elif config.PLATFORM == 'ks':
            config.KS_CREATOR_ID_LIST = creator_ids_list
        elif config.PLATFORM == 'bili':
            config.BILI_CREATOR_ID_LIST = creator_ids_list
        elif config.PLATFORM == 'wb':
            config.WEIBO_CREATOR_ID_LIST = creator_ids_list
        elif config.PLATFORM == 'tieba':
            config.TIEBA_CREATOR_URL_LIST = creator_ids_list
        elif config.PLATFORM == 'zhihu':
            config.ZHIHU_CREATOR_URL_LIST = creator_ids_list
