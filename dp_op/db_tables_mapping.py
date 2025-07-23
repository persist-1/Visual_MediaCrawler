# -*- coding: utf-8 -*-
"""
存储表配置模块

该模块定义了所有数据表的配置信息，包括表名、显示名称、主键、时间字段、显示字段等。
用于SQLite和MySQL数据库API的统一配置管理。

作者: 项目增强师
创建时间: 2024
"""

from typing import Dict, List, Any


# 基础表配置 - 用于SQLite API的简化配置
BASE_TABLE_CONFIGS = {
    'bilibili_video': {
        'name': 'B站视频',
        'primary_key': 'video_id',
        'time_field': 'create_time',
        'display_fields': ['video_id', 'title', 'desc', 'nickname', 'view_count', 'like_count', 'create_time']
    },
    'bilibili_video_comment': {
        'name': 'B站视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'video_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'bilibili_up_info': {
        'name': 'B站UP主信息',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['user_id', 'nickname', 'avatar', 'desc', 'fans', 'follows', 'add_ts']
    },
    'bilibili_contact_info': {
        'name': 'B站联系信息',
        'primary_key': 'id',
        'time_field': 'add_ts',
        'display_fields': ['id', 'user_id', 'contact_type', 'contact_value', 'add_ts']
    },
    'bilibili_up_dynamic': {
        'name': 'B站UP主动态',
        'primary_key': 'dynamic_id',
        'time_field': 'create_time',
        'display_fields': ['dynamic_id', 'user_id', 'content', 'create_time']
    },
    'douyin_aweme': {
        'name': '抖音视频',
        'primary_key': 'aweme_id',
        'time_field': 'create_time',
        'display_fields': ['aweme_id', 'desc', 'nickname', 'digg_count', 'comment_count', 'create_time']
    },
    'douyin_aweme_comment': {
        'name': '抖音视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'aweme_id', 'content', 'nickname', 'digg_count', 'create_time']
    },
    'dy_creator': {
        'name': '抖音创作者',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['user_id', 'sec_uid', 'nickname', 'avatar', 'follower_count', 'following_count', 'add_ts']
    },
    'kuaishou_video': {
        'name': '快手视频',
        'primary_key': 'video_id',
        'time_field': 'create_time',
        'display_fields': ['video_id', 'title', 'desc', 'nickname', 'view_count', 'like_count', 'create_time']
    },
    'kuaishou_video_comment': {
        'name': '快手视频评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'video_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'xhs_note': {
        'name': '小红书笔记',
        'primary_key': 'note_id',
        'time_field': 'time',
        'display_fields': ['note_id', 'title', 'desc', 'nickname', 'liked_count', 'collected_count', 'time']
    },
    'xhs_note_comment': {
        'name': '小红书笔记评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'xhs_creator': {
        'name': '小红书创作者',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['user_id', 'nickname', 'avatar', 'desc', 'fans', 'follows', 'add_ts']
    },
    'weibo_note': {
        'name': '微博内容',
        'primary_key': 'note_id',
        'time_field': 'create_time',
        'display_fields': ['note_id', 'title', 'desc', 'nickname', 'attitudes_count', 'comments_count', 'create_time']
    },
    'weibo_note_comment': {
        'name': '微博评论',
        'primary_key': 'comment_id',
        'time_field': 'create_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'nickname', 'like_count', 'create_time']
    },
    'weibo_creator': {
        'name': '微博创作者',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['user_id', 'nickname', 'desc', 'fans_count', 'follows_count', 'add_ts']
    },
    'tieba_note': {
        'name': '贴吧帖子',
        'primary_key': 'note_id',
        'time_field': 'publish_time',
        'display_fields': ['note_id', 'title', 'desc', 'user_nickname', 'tieba_name', 'total_replay_num', 'publish_time']
    },
    'tieba_comment': {
        'name': '贴吧评论',
        'primary_key': 'comment_id',
        'time_field': 'publish_time',
        'display_fields': ['comment_id', 'note_id', 'content', 'user_nickname', 'publish_time']
    },
    'tieba_creator': {
        'name': '贴吧创作者',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['user_id', 'nickname', 'desc', 'fans_count', 'follows_count', 'add_ts']
    },
    'zhihu_content': {
        'name': '知乎内容',
        'primary_key': 'content_id',
        'time_field': 'created_time',
        'display_fields': ['content_id', 'title', 'desc', 'user_nickname', 'voteup_count', 'comment_count', 'created_time']
    },
    'zhihu_comment': {
        'name': '知乎评论',
        'primary_key': 'comment_id',
        'time_field': 'publish_time',
        'display_fields': ['comment_id', 'content_id', 'content', 'user_nickname', 'like_count', 'publish_time']
    },
    'zhihu_creator': {
        'name': '知乎创作者',
        'primary_key': 'user_id',
        'time_field': 'add_ts',
        'display_fields': ['id', 'user_id', 'user_link', 'user_nickname', 'user_avatar', 'url_token', 'gender', 'ip_location', 'follows', 'fans', 'anwser_count', 'video_count', 'question_count', 'article_count', 'column_count', 'get_voteup_count', 'add_ts', 'last_modify_ts', 'task_times_id']
    },
    'crawler_tasks': {
        'name': '爬虫任务',
        'primary_key': 'id',
        'time_field': 'created_at',
        'display_fields': ['id', 'task_times_id', 'keywords', 'platform', 'crawler_type', 'status', 'created_at']
    }
}


# 详细表配置 - 用于MySQL API的详细列配置
DETAILED_TABLE_CONFIGS = {
    "bilibili_video": {
        "name": "B站视频",
        "description": "B站视频数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "sec_uid", "title": "安全用户ID", "width": 150},
            {"key": "short_user_id", "title": "短用户ID", "width": 120},
            {"key": "user_unique_id", "title": "用户唯一ID", "width": 150},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "user_signature", "title": "用户签名", "width": 200},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "aweme_id", "title": "视频ID", "width": 150},
            {"key": "video_id", "title": "视频编号", "width": 150},
            {"key": "video_type", "title": "视频类型", "width": 100},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "liked_count", "title": "点赞数", "width": 100},
            {"key": "comment_count", "title": "评论数", "width": 100},
            {"key": "share_count", "title": "分享数", "width": 100},
            {"key": "collected_count", "title": "收藏数", "width": 100},
            {"key": "tag_list", "title": "标签列表", "width": 200},
            {"key": "aweme_url", "title": "视频链接", "width": 200},
            {"key": "video_url_list", "title": "视频地址列表", "width": 300},
            {"key": "video_cover_url_list", "title": "视频封面列表", "width": 300},
            {"key": "note_url", "title": "笔记链接", "width": 200},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "bilibili_video_comment": {
        "name": "B站视频评论",
        "description": "B站视频评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "aweme_id", "title": "视频ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "comment_like_count", "title": "点赞数", "width": 100},
            {"key": "sub_comment_count", "title": "子评论数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "bilibili_up_info": {
        "name": "B站UP主信息",
        "description": "B站UP主信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "archiveCount", "title": "投稿数", "width": 100},
            {"key": "articlesCount", "title": "文章数", "width": 100},
            {"key": "follower", "title": "粉丝数", "width": 100},
            {"key": "following", "title": "关注数", "width": 100},
            {"key": "user_desc", "title": "用户描述", "width": 200},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "bilibili_contact_info": {
        "name": "B站联系信息",
        "description": "B站联系信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "contact_type", "title": "联系方式类型", "width": 120},
            {"key": "contact_value", "title": "联系方式值", "width": 200},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "bilibili_up_dynamic": {
        "name": "B站UP主动态",
        "description": "B站UP主动态表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "dynamic_id", "title": "动态ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "content", "title": "动态内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "douyin_aweme": {
        "name": "抖音视频",
        "description": "抖音视频数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "sec_uid", "title": "安全用户ID", "width": 150},
            {"key": "short_user_id", "title": "短用户ID", "width": 120},
            {"key": "user_unique_id", "title": "用户唯一ID", "width": 150},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "user_signature", "title": "用户签名", "width": 200},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "aweme_id", "title": "视频ID", "width": 150},
            {"key": "video_id", "title": "视频编号", "width": 150},
            {"key": "video_type", "title": "视频类型", "width": 100},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "liked_count", "title": "点赞数", "width": 100},
            {"key": "comment_count", "title": "评论数", "width": 100},
            {"key": "share_count", "title": "分享数", "width": 100},
            {"key": "collected_count", "title": "收藏数", "width": 100},
            {"key": "tag_list", "title": "标签列表", "width": 200},
            {"key": "aweme_url", "title": "视频链接", "width": 200},
            {"key": "video_url_list", "title": "视频地址列表", "width": 300},
            {"key": "video_cover_url_list", "title": "视频封面列表", "width": 300},
            {"key": "note_url", "title": "笔记链接", "width": 200},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "douyin_aweme_comment": {
        "name": "抖音视频评论",
        "description": "抖音视频评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "aweme_id", "title": "视频ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "digg_count", "title": "点赞数", "width": 100},
            {"key": "reply_comment_total", "title": "回复数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "dy_creator": {
        "name": "抖音创作者",
        "description": "抖音创作者信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "sec_uid", "title": "安全用户ID", "width": 150},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "user_signature", "title": "用户签名", "width": 200},
            {"key": "follower_count", "title": "粉丝数", "width": 100},
            {"key": "total_favorited", "title": "获赞数", "width": 100},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "kuaishou_video": {
        "name": "快手视频",
        "description": "快手视频数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "user_signature", "title": "用户签名", "width": 200},
            {"key": "video_id", "title": "视频ID", "width": 150},
            {"key": "video_type", "title": "视频类型", "width": 100},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "liked_count", "title": "点赞数", "width": 100},
            {"key": "viewd_count", "title": "观看数", "width": 100},
            {"key": "video_url", "title": "视频链接", "width": 200},
            {"key": "video_cover_url", "title": "视频封面", "width": 200},
            {"key": "video_play_url", "title": "播放地址", "width": 300},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "kuaishou_video_comment": {
        "name": "快手视频评论",
        "description": "快手视频评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "aweme_id", "title": "视频ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "like_count", "title": "点赞数", "width": 100},
            {"key": "sub_comment_count", "title": "子评论数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "xhs_note": {
        "name": "小红书笔记",
        "description": "小红书笔记数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "note_id", "title": "笔记ID", "width": 150},
            {"key": "type", "title": "类型", "width": 100},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "video_url", "title": "视频链接", "width": 200},
            {"key": "time", "title": "时间", "width": 150},
            {"key": "last_update_time", "title": "最后更新时间", "width": 150},
            {"key": "liked_count", "title": "点赞数", "width": 100},
            {"key": "collected_count", "title": "收藏数", "width": 100},
            {"key": "comment_count", "title": "评论数", "width": 100},
            {"key": "share_count", "title": "分享数", "width": 100},
            {"key": "image_list", "title": "图片列表", "width": 300},
            {"key": "tag_list", "title": "标签列表", "width": 200},
            {"key": "note_url", "title": "笔记链接", "width": 200},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "xhs_note_comment": {
        "name": "小红书笔记评论",
        "description": "小红书笔记评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "note_id", "title": "笔记ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "like_count", "title": "点赞数", "width": 100},
            {"key": "sub_comment_count", "title": "子评论数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "xhs_creator": {
        "name": "小红书创作者",
        "description": "小红书创作者信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "desc", "title": "描述", "width": 200},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "follows", "title": "关注数", "width": 100},
            {"key": "fans", "title": "粉丝数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "weibo_note": {
        "name": "微博笔记",
        "description": "微博笔记数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "profile_url", "title": "个人主页", "width": 200},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "note_id", "title": "笔记ID", "width": 150},
            {"key": "content", "title": "内容", "width": 400},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "create_date_time", "title": "创建日期时间", "width": 150},
            {"key": "liked_count", "title": "点赞数", "width": 100},
            {"key": "comments_count", "title": "评论数", "width": 100},
            {"key": "shared_count", "title": "分享数", "width": 100},
            {"key": "note_url", "title": "笔记链接", "width": 200},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "weibo_note_comment": {
        "name": "微博笔记评论",
        "description": "微博笔记评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "note_id", "title": "笔记ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "avatar", "title": "头像", "width": 100},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "comment_like_count", "title": "点赞数", "width": 100},
            {"key": "sub_comment_count", "title": "子评论数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "weibo_creator": {
        "name": "微博创作者",
        "description": "微博创作者信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "profile_url", "title": "个人主页", "width": 200},
            {"key": "profile_image_url", "title": "头像", "width": 100},
            {"key": "desc", "title": "描述", "width": 200},
            {"key": "follows_count", "title": "关注数", "width": 100},
            {"key": "fans_count", "title": "粉丝数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "tieba_note": {
        "name": "贴吧帖子",
        "description": "贴吧帖子数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "user_link", "title": "用户链接", "width": 200},
            {"key": "tieba_name", "title": "贴吧名称", "width": 120},
            {"key": "tieba_link", "title": "贴吧链接", "width": 200},
            {"key": "note_id", "title": "帖子ID", "width": 150},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "note_url", "title": "帖子链接", "width": 200},
            {"key": "publish_time", "title": "发布时间", "width": 150},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "tieba_comment": {
        "name": "贴吧评论",
        "description": "贴吧评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "note_id", "title": "帖子ID", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "create_time", "title": "创建时间", "width": 150},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "tieba_creator": {
        "name": "贴吧创作者",
        "description": "贴吧创作者信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "nickname", "title": "昵称", "width": 120},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "desc", "title": "描述", "width": 200},
            {"key": "fans_count", "title": "粉丝数", "width": 100},
            {"key": "follows_count", "title": "关注数", "width": 100},
            {"key": "post_count", "title": "发帖数", "width": 100},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "task_times_id", "title": "任务ID", "width": 200},
            {"key": "add_ts", "title": "添加时间戳", "width": 150}
        ]
    },
    "zhihu_content": {
        "name": "知乎内容",
        "description": "知乎内容数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "content_id", "title": "内容ID", "width": 150},
            {"key": "content_type", "title": "内容类型", "width": 100},
            {"key": "content_text", "title": "内容文本", "width": 300},
            {"key": "content_url", "title": "内容链接", "width": 200},
            {"key": "question_id", "title": "问题ID", "width": 150},
            {"key": "title", "title": "标题", "width": 300},
            {"key": "desc", "title": "描述", "width": 300},
            {"key": "created_time", "title": "创建时间", "width": 150},
            {"key": "updated_time", "title": "更新时间", "width": 150},
            {"key": "voteup_count", "title": "点赞数", "width": 100},
            {"key": "comment_count", "title": "评论数", "width": 100},
            {"key": "source_keyword", "title": "搜索关键词", "width": 150},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "user_link", "title": "用户链接", "width": 200},
            {"key": "user_nickname", "title": "用户昵称", "width": 120},
            {"key": "user_avatar", "title": "用户头像", "width": 100},
            {"key": "user_url_token", "title": "用户令牌", "width": 150},
            {"key": "add_ts", "title": "添加时间戳", "width": 150},
            {"key": "last_modify_ts", "title": "修改时间戳", "width": 150},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "zhihu_comment": {
        "name": "知乎评论",
        "description": "知乎评论数据表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "comment_id", "title": "评论ID", "width": 150},
            {"key": "parent_comment_id", "title": "父评论ID", "width": 150},
            {"key": "content", "title": "评论内容", "width": 300},
            {"key": "publish_time", "title": "发布时间", "width": 150},
            {"key": "ip_location", "title": "IP位置", "width": 100},
            {"key": "sub_comment_count", "title": "子评论数", "width": 100},
            {"key": "like_count", "title": "点赞数", "width": 100},
            {"key": "dislike_count", "title": "踩数", "width": 100},
            {"key": "content_id", "title": "内容ID", "width": 150},
            {"key": "content_type", "title": "内容类型", "width": 100},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "user_link", "title": "用户链接", "width": 200},
            {"key": "user_nickname", "title": "用户昵称", "width": 120},
            {"key": "user_avatar", "title": "用户头像", "width": 100},
            {"key": "add_ts", "title": "添加时间戳", "width": 150},
            {"key": "last_modify_ts", "title": "修改时间戳", "width": 150},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "zhihu_creator": {
        "name": "知乎创作者",
        "description": "知乎创作者信息表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "user_id", "title": "用户ID", "width": 120},
            {"key": "user_link", "title": "用户链接", "width": 200},
            {"key": "user_nickname", "title": "用户昵称", "width": 120},
            {"key": "user_avatar", "title": "用户头像", "width": 200},
            {"key": "url_token", "title": "URL Token", "width": 120},
            {"key": "gender", "title": "性别", "width": 80},
            {"key": "ip_location", "title": "IP位置", "width": 120},
            {"key": "follows", "title": "关注数", "width": 100},
            {"key": "fans", "title": "粉丝数", "width": 100},
            {"key": "anwser_count", "title": "回答数", "width": 100},
            {"key": "video_count", "title": "视频数", "width": 100},
            {"key": "question_count", "title": "问题数", "width": 100},
            {"key": "article_count", "title": "文章数", "width": 100},
            {"key": "column_count", "title": "专栏数", "width": 100},
            {"key": "get_voteup_count", "title": "获赞数", "width": 100},
            {"key": "add_ts", "title": "添加时间戳", "width": 150},
            {"key": "last_modify_ts", "title": "修改时间戳", "width": 150},
            {"key": "task_times_id", "title": "任务ID", "width": 200}
        ]
    },
    "crawler_tasks": {
        "name": "爬虫任务",
        "description": "爬虫任务记录表",
        "columns": [
            {"key": "id", "title": "ID", "width": 80},
            {"key": "task_times_id", "title": "任务批次ID", "width": 200},
            {"key": "status", "title": "状态", "width": 100},
            {"key": "message", "title": "消息", "width": 300},
            {"key": "result_stdout", "title": "执行输出", "width": 200},
            {"key": "result_stderr", "title": "错误输出", "width": 200},
            {"key": "created_at", "title": "创建时间", "width": 150},
            {"key": "updated_at", "title": "更新时间", "width": 150},
            {"key": "platform", "title": "平台", "width": 100},
            {"key": "crawler_type", "title": "爬虫类型", "width": 120},
            {"key": "keywords", "title": "关键词", "width": 200},
            {"key": "login_type", "title": "登录类型", "width": 100},
            {"key": "start_page", "title": "起始页", "width": 100},
            {"key": "max_count", "title": "最大数量", "width": 100},
            {"key": "get_comment", "title": "获取评论", "width": 100},
            {"key": "get_sub_comment", "title": "获取子评论", "width": 120},
            {"key": "storage_type", "title": "存储类型", "width": 120},
            {"key": "specified_ids", "title": "指定ID", "width": 150},
            {"key": "creator_ids", "title": "创作者ID", "width": 150},
            {"key": "cookies", "title": "Cookies", "width": 200},
            {"key": "save_format", "title": "保存格式", "width": 100}
        ]
    }
}


def get_base_table_config(table_name: str) -> Dict[str, Any]:
    """
    获取基础表配置（用于SQLite API）
    
    Args:
        table_name: 表名
        
    Returns:
        表配置字典，如果表不存在则返回None
    """
    return BASE_TABLE_CONFIGS.get(table_name)


def get_detailed_table_config(table_name: str) -> Dict[str, Any]:
    """
    获取详细表配置（用于MySQL API）
    
    Args:
        table_name: 表名
        
    Returns:
        表配置字典，如果表不存在则返回None
    """
    return DETAILED_TABLE_CONFIGS.get(table_name)


def get_all_base_table_configs() -> Dict[str, Dict[str, Any]]:
    """
    获取所有基础表配置
    
    Returns:
        所有基础表配置的字典
    """
    return BASE_TABLE_CONFIGS.copy()


def get_all_detailed_table_configs() -> Dict[str, Dict[str, Any]]:
    """
    获取所有详细表配置
    
    Returns:
        所有详细表配置的字典
    """
    return DETAILED_TABLE_CONFIGS.copy()


def get_table_names() -> List[str]:
    """
    获取所有表名列表
    
    Returns:
        表名列表
    """
    return list(BASE_TABLE_CONFIGS.keys())


def is_valid_table(table_name: str) -> bool:
    """
    检查表名是否有效
    
    Args:
        table_name: 表名
        
    Returns:
        如果表名有效返回True，否则返回False
    """
    return table_name in BASE_TABLE_CONFIGS


def get_table_display_name(table_name: str) -> str:
    """
    获取表的显示名称
    
    Args:
        table_name: 表名
        
    Returns:
        表的显示名称，如果表不存在则返回表名本身
    """
    config = BASE_TABLE_CONFIGS.get(table_name)
    return config['name'] if config else table_name


def get_table_primary_key(table_name: str) -> str:
    """
    获取表的主键字段名
    
    Args:
        table_name: 表名
        
    Returns:
        主键字段名，如果表不存在则返回'id'
    """
    config = BASE_TABLE_CONFIGS.get(table_name)
    return config['primary_key'] if config else 'id'


def get_table_time_field(table_name: str) -> str:
    """
    获取表的时间字段名
    
    Args:
        table_name: 表名
        
    Returns:
        时间字段名，如果表不存在则返回'create_time'
    """
    config = BASE_TABLE_CONFIGS.get(table_name)
    return config['time_field'] if config else 'create_time'


def get_table_display_fields(table_name: str) -> List[str]:
    """
    获取表的显示字段列表
    
    Args:
        table_name: 表名
        
    Returns:
        显示字段列表，如果表不存在则返回空列表
    """
    config = BASE_TABLE_CONFIGS.get(table_name)
    return config['display_fields'].copy() if config else []