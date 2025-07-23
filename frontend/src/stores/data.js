import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// 数据表配置
const TABLE_CONFIG = {
  bilibili_video: {
    label: 'B站视频',
    icon: 'iconfont icon-bilibili',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'video_url', label: '视频链接', width: '200' },
      { prop: 'title', label: '视频标题', width: '300' },
      { prop: 'desc', label: '视频描述', width: '300' },
      { prop: 'create_time', label: '发布时间', width: '150' },
      { prop: 'video_type', label: '视频类型', width: '100' },
      { prop: 'video_play_count', label: '播放量', width: '100' },
      { prop: 'video_danmaku', label: '弹幕数', width: '100' },
      { prop: 'video_comment', label: '评论数', width: '100' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'disliked_count', label: '点踩数', width: '100' },
      { prop: 'video_favorite_count', label: '收藏数', width: '100' },
      { prop: 'video_share_count', label: '分享数', width: '100' },
      { prop: 'video_coin_count', label: '投币数', width: '100' },
      { prop: 'video_cover_url', label: '封面链接', width: '200' },
      { prop: 'user_id', label: 'UP主ID', width: '120' },
      { prop: 'nickname', label: 'UP主昵称', width: '150' },
      { prop: 'avatar', label: 'UP主头像', width: '100' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  bilibili_video_comment: {
    label: 'B站视频评论',
    icon: 'iconfont icon-bilibili',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'sex', label: '性别', width: '80' },
      { prop: 'sign', label: '签名', width: '200' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  bilibili_up_info: {
    label: 'B站UP主信息',
    icon: 'iconfont icon-bilibili',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'sex', label: '性别', width: '80' },
      { prop: 'sign', label: '签名', width: '300' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'total_fans', label: '粉丝数', width: '100' },
      { prop: 'total_liked', label: '总获赞数', width: '100' },
      { prop: 'user_rank', label: '用户等级', width: '100' },
      { prop: 'is_official', label: '是否官号', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  bilibili_contact_info: {
    label: 'B站联系人信息',
    icon: 'iconfont icon-bilibili',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'up_id', label: 'UP主ID', width: '120' },
      { prop: 'fan_id', label: '粉丝ID', width: '120' },
      { prop: 'up_name', label: 'UP主昵称', width: '150' },
      { prop: 'fan_name', label: '粉丝昵称', width: '150' },
      { prop: 'up_sign', label: 'UP主签名', width: '200' },
      { prop: 'fan_sign', label: '粉丝签名', width: '200' },
      { prop: 'up_avatar', label: 'UP主头像', width: '100' },
      { prop: 'fan_avatar', label: '粉丝头像', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  bilibili_up_dynamic: {
    label: 'B站UP主动态',
    icon: 'iconfont icon-bilibili',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'dynamic_id', label: '动态ID', width: '120' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'user_name', label: '用户昵称', width: '150' },
      { prop: 'text', label: '动态内容', width: '300' },
      { prop: 'type', label: '动态类型', width: '100' },
      { prop: 'pub_ts', label: '发布时间', width: '150' },
      { prop: 'total_comments', label: '评论数', width: '100' },
      { prop: 'total_forwards', label: '转发数', width: '100' },
      { prop: 'total_liked', label: '点赞数', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  douyin_aweme: {
    label: '抖音视频',
    icon: 'iconfont icon-douyin',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'aweme_id', label: '视频ID', width: '120' },
      { prop: 'aweme_type', label: '视频类型', width: '100' },
      { prop: 'title', label: '标题', width: '300' },
      { prop: 'desc', label: '描述', width: '300' },
      { prop: 'create_time', label: '发布时间', width: '150' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'sec_uid', label: 'SecUID', width: '150' },
      { prop: 'short_user_id', label: '短用户ID', width: '120' },
      { prop: 'user_unique_id', label: '用户唯一ID', width: '150' },
      { prop: 'user_signature', label: '用户签名', width: '200' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' },
      { prop: 'share_count', label: '分享数', width: '100' },
      { prop: 'collected_count', label: '收藏数', width: '100' },
      { prop: 'aweme_url', label: '视频链接', width: '200' },
      { prop: 'cover_url', label: '封面链接', width: '200' },
      { prop: 'video_download_url', label: '下载链接', width: '200' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  douyin_aweme_comment: {
    label: '抖音视频评论',
    icon: 'iconfont icon-douyin',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'aweme_id', label: '视频ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'sec_uid', label: '安全用户ID', width: '120' },
      { prop: 'short_user_id', label: '短用户ID', width: '120' },
      { prop: 'user_unique_id', label: '用户唯一ID', width: '120' },
      { prop: 'user_signature', label: '用户签名', width: '200' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'avatar_larger', label: '头像', width: '100' },
      { prop: 'ip_label', label: 'IP归属地', width: '120' },
      { prop: 'aweme_type', label: '视频类型', width: '100' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'pictures', label: '评论图片', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  dy_creator: {
    label: '抖音创作者',
    icon: 'iconfont icon-douyin',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'desc', label: '用户描述', width: '200' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'ip_location', label: 'IP归属地', width: '120' },
      { prop: 'follows', label: '关注数', width: '100' },
      { prop: 'fans', label: '粉丝数', width: '100' },
      { prop: 'interaction', label: '获赞数', width: '100' },
      { prop: 'videos_count', label: '作品数', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  kuaishou_video: {
    label: '快手视频',
    icon: 'iconfont icon-kuaishou',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'title', label: '视频标题', width: '300' },
      { prop: 'desc', label: '视频描述', width: '300' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'viewd_count', label: '播放数', width: '100' },
      { prop: 'video_type', label: '视频类型', width: '100' },
      { prop: 'create_time', label: '发布时间', width: '150' },
      { prop: 'video_url', label: '视频链接', width: '200' },
      { prop: 'video_cover_url', label: '封面链接', width: '200' },
      { prop: 'video_play_url', label: '播放链接', width: '200' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  kuaishou_video_comment: {
    label: '快手视频评论',
    icon: 'iconfont icon-kuaishou',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'video_id', label: '视频ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'user_eid', label: '用户EID', width: '120' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  xhs_note: {
    label: '小红书笔记',
    icon: 'iconfont icon-xiaohongshu-hui',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'note_id', label: '笔记ID', width: '120' },
      { prop: 'type', label: '笔记类型', width: '100' },
      { prop: 'title', label: '标题', width: '300' },
      { prop: 'desc', label: '描述', width: '300' },
      { prop: 'time', label: '发布时间', width: '150' },
      { prop: 'last_update_time', label: '更新时间', width: '150' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'collected_count', label: '收藏数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' },
      { prop: 'share_count', label: '分享数', width: '100' },
      { prop: 'image_list', label: '图片列表', width: '200' },
      { prop: 'tag_list', label: '标签列表', width: '200' },
      { prop: 'note_url', label: '笔记链接', width: '200' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  xhs_creator: {
    label: '小红书创作者',
    icon: 'iconfont icon-xiaohongshu-hui',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'desc', label: '简介', width: '300' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'follows', label: '关注数', width: '100' },
      { prop: 'fans', label: '粉丝数', width: '100' },
      { prop: 'interaction', label: '互动数', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  xhs_note_comment: {
    label: '小红书笔记评论',
    icon: 'iconfont icon-xiaohongshu-hui',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'note_id', label: '笔记ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'pictures', label: '评论图片', width: '150' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  weibo_note: {
    label: '微博笔记',
    icon: 'iconfont icon-weibo',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'note_id', label: '微博ID', width: '120' },
      { prop: 'note_url', label: '微博链接', width: '200' },
      { prop: 'content', label: '内容', width: '300' },
      { prop: 'create_time', label: '发布时间', width: '150' },
      { prop: 'create_date_time', label: '发布日期', width: '150' },
      { prop: 'liked_count', label: '点赞数', width: '100' },
      { prop: 'comments_count', label: '评论数', width: '100' },
      { prop: 'shared_count', label: '分享数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'profile_url', label: '个人主页', width: '200' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  weibo_note_comment: {
    label: '微博评论',
    icon: 'iconfont icon-weibo',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'note_id', label: '微博ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'create_date_time', label: '评论日期', width: '150' },
      { prop: 'comment_like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'profile_url', label: '个人主页', width: '200' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  weibo_creator: {
    label: '微博创作者',
    icon: 'iconfont icon-weibo',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '昵称', width: '150' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'profile_url', label: '个人主页', width: '200' },
      { prop: 'avatar', label: '头像', width: '100' },
      { prop: 'verified', label: '认证状态', width: '100' },
      { prop: 'verified_reason', label: '认证原因', width: '150' },
      { prop: 'desc', label: '个人描述', width: '200' },
      { prop: 'follows', label: '关注数', width: '100' },
      { prop: 'fans', label: '粉丝数', width: '100' },
      { prop: 'notes_count', label: '微博数', width: '100' },
      { prop: 'ip_location', label: 'IP归属地', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  tieba_note: {
    label: '贴吧帖子',
    icon: 'iconfont icon-social-tieba',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'note_id', label: '帖子ID', width: '120' },
      { prop: 'note_url', label: '帖子链接', width: '200' },
      { prop: 'title', label: '标题', width: '300' },
      { prop: 'content', label: '内容', width: '300' },
      { prop: 'publish_time', label: '发布时间', width: '150' },
      { prop: 'reply_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'tieba_name', label: '贴吧名称', width: '150' },
      { prop: 'tieba_link', label: '贴吧链接', width: '200' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  tieba_comment: {
    label: '贴吧评论',
    icon: 'iconfont icon-social-tieba',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'note_id', label: '帖子ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'create_time', label: '评论时间', width: '150' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'sub_comment_count', label: '回复数', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  tieba_creator: {
    label: '贴吧创作者',
    icon: 'iconfont icon-social-tieba',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'nickname', label: '用户昵称', width: '150' },
      { prop: 'avatar', label: '用户头像', width: '100' },
      { prop: 'desc', label: '用户简介', width: '200' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'ip_location', label: 'IP归属地', width: '120' },
      { prop: 'follows', label: '关注数', width: '100' },
      { prop: 'fans', label: '粉丝数', width: '100' },
      { prop: 'interaction', label: '互动数', width: '100' },
      { prop: 'task_times_id', label: '任务ID', width: '200' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' }
    ]
  },
  zhihu_content: {
    label: '知乎内容',
    icon: 'iconfont icon-zhihu',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'content_id', label: '内容ID', width: '120' },
      { prop: 'content_type', label: '内容类型', width: '100' },
      { prop: 'content_text', label: '内容文本', width: '300' },
      { prop: 'content_url', label: '内容链接', width: '200' },
      { prop: 'question_id', label: '问题ID', width: '150' },
      { prop: 'title', label: '标题', width: '300' },
      { prop: 'desc', label: '描述', width: '300' },
      { prop: 'created_time', label: '创建时间', width: '150' },
      { prop: 'updated_time', label: '更新时间', width: '150' },
      { prop: 'voteup_count', label: '点赞数', width: '100' },
      { prop: 'comment_count', label: '评论数', width: '100' },
      { prop: 'source_keyword', label: '搜索关键词', width: '150' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'user_link', label: '用户链接', width: '200' },
      { prop: 'user_nickname', label: '用户昵称', width: '150' },
      { prop: 'user_avatar', label: '用户头像', width: '100' },
      { prop: 'user_url_token', label: '用户令牌', width: '150' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' }
    ]
  },
  zhihu_comment: {
    label: '知乎评论',
    icon: 'iconfont icon-zhihu',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'comment_id', label: '评论ID', width: '120' },
      { prop: 'parent_comment_id', label: '父评论ID', width: '120' },
      { prop: 'content', label: '评论内容', width: '300' },
      { prop: 'publish_time', label: '发布时间', width: '150' },
      { prop: 'ip_location', label: 'IP位置', width: '120' },
      { prop: 'sub_comment_count', label: '子评论数', width: '100' },
      { prop: 'like_count', label: '点赞数', width: '100' },
      { prop: 'dislike_count', label: '踩数', width: '100' },
      { prop: 'content_id', label: '内容ID', width: '120' },
      { prop: 'content_type', label: '内容类型', width: '100' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'user_link', label: '用户链接', width: '200' },
      { prop: 'user_nickname', label: '用户昵称', width: '150' },
      { prop: 'user_avatar', label: '用户头像', width: '100' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' }
    ]
  },
  zhihu_creator: {
    label: '知乎创作者',
    icon: 'iconfont icon-zhihu',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'user_id', label: '用户ID', width: '120' },
      { prop: 'user_link', label: '用户链接', width: '200' },
      { prop: 'user_nickname', label: '用户昵称', width: '150' },
      { prop: 'user_avatar', label: '用户头像', width: '200' },
      { prop: 'url_token', label: 'URL Token', width: '120' },
      { prop: 'gender', label: '性别', width: '80' },
      { prop: 'ip_location', label: 'IP归属地', width: '120' },
      { prop: 'follows', label: '关注数', width: '100' },
      { prop: 'fans', label: '粉丝数', width: '100' },
      { prop: 'anwser_count', label: '回答数', width: '100' },
      { prop: 'video_count', label: '视频数', width: '100' },
      { prop: 'question_count', label: '问题数', width: '100' },
      { prop: 'article_count', label: '文章数', width: '100' },
      { prop: 'column_count', label: '专栏数', width: '100' },
      { prop: 'get_voteup_count', label: '获赞数', width: '100' },
      { prop: 'add_ts', label: '添加时间', width: '150' },
      { prop: 'last_modify_ts', label: '修改时间', width: '150' },
      { prop: 'task_times_id', label: '任务ID', width: '200' }
    ]
  },
  crawler_tasks: {
    label: '爬虫任务',
    icon: 'iconfont icon-pachong',
    columns: [
      { prop: 'id', label: 'ID', width: '80' },
      { prop: 'task_times_id', label: '任务批次ID', width: '200' },
      { prop: 'status', label: '状态', width: '100' },
      { prop: 'message', label: '消息', width: '300' },
      { prop: 'result_stdout', label: '执行输出', width: '200' },
      { prop: 'result_stderr', label: '错误输出', width: '200' },
      { prop: 'created_at', label: '创建时间', width: '150' },
      { prop: 'updated_at', label: '更新时间', width: '150' },
      { prop: 'platform', label: '平台', width: '100' },
      { prop: 'crawler_type', label: '爬虫类型', width: '120' },
      { prop: 'keywords', label: '关键词', width: '200' },
      { prop: 'login_type', label: '登录类型', width: '100' },
      { prop: 'start_page', label: '起始页', width: '100' },
      { prop: 'max_count', label: '最大数量', width: '100' },
      { prop: 'get_comment', label: '获取评论', width: '100' },
      { prop: 'get_sub_comment', label: '获取子评论', width: '120' },
      { prop: 'storage_type', label: '存储类型', width: '120' },
      { prop: 'specified_ids', label: '指定ID', width: '150' },
      { prop: 'creator_ids', label: '创作者ID', width: '150' },
      { prop: 'cookies', label: 'Cookies', width: '200' },
      { prop: 'save_format', label: '保存格式', width: '100' }
    ]
  }
 }

// 时间格式化函数
const formatDateTime = (timestamp) => {
  if (!timestamp) return '--'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN')
}

export const useDataStore = defineStore('data', () => {
  // 状态
  const loading = ref(false)
  const tableData = ref([])
  const totalCount = ref(0)
  const availableTables = ref([])
  const tableColumns = ref([])

  // 计算属性
  const hasData = computed(() => tableData.value.length > 0)

  // 方法
  const loadAvailableTables = async (dataSource = 'sqlite') => {
    try {
      const apiPath = dataSource === 'mysql' ? '/api/mysql/tables' : '/api/sqlite/tables'
      const response = await axios.get(apiPath)
      const tables = response.data.data || []
      
      // 定义表格显示顺序
      const tableOrder = [
        'bilibili_video',
        'bilibili_video_comment', 
        'bilibili_up_info',
        'bilibili_contact_info',
        'bilibili_up_dynamic',
        'douyin_aweme',
        'douyin_aweme_comment',
        'dy_creator',
        'kuaishou_video',
        'kuaishou_video_comment',
        'xhs_note',
        'xhs_note_comment',
        'xhs_creator',
        'weibo_note',
        'weibo_note_comment',
        'weibo_creator',
        'tieba_note',
        'tieba_comment',
        'tieba_creator',
        'zhihu_content',
        'zhihu_comment',
        'zhihu_creator',
        'crawler_tasks'
      ]
      
      // 按照预定义顺序排序表格
      const sortedTables = tables.sort((a, b) => {
        const indexA = tableOrder.indexOf(a)
        const indexB = tableOrder.indexOf(b)
        
        // 如果表格在预定义顺序中，按照顺序排列
        if (indexA !== -1 && indexB !== -1) {
          return indexA - indexB
        }
        // 如果只有一个在预定义顺序中，优先显示在顺序中的
        if (indexA !== -1) return -1
        if (indexB !== -1) return 1
        // 如果都不在预定义顺序中，按字母顺序排列
        return a.localeCompare(b)
      })
      
      availableTables.value = sortedTables.map(tableName => {
        const config = TABLE_CONFIG[tableName]
        return {
          value: tableName,
          label: config ? config.label : tableName,
          icon: config ? config.icon : 'fas fa-table'
        }
      })
    } catch (error) {
      console.error('加载数据表列表失败:', error)
      throw new Error('加载数据表列表失败')
    }
  }

  // 清空表格数据
  const clearTableData = () => {
    tableData.value = []
    totalCount.value = 0
    tableColumns.value = []
  }

  const loadTableData = async ({ table, page = 1, pageSize = 30, taskId = undefined, dataSource = 'sqlite' }) => {
    loading.value = true
    try {
      const params = { table, page, page_size: pageSize }
      if (taskId) {
        params.task_times_id = taskId
      }
      
      const apiPath = dataSource === 'mysql' ? '/api/mysql/data' : '/api/sqlite/data'
      const response = await axios.get(apiPath, {
        params
      })
      
      const result = response.data.data
      tableData.value = result.data || []
      totalCount.value = result.total || 0
      
      // 设置表格列配置
      const config = TABLE_CONFIG[table]
      if (config) {
        tableColumns.value = config.columns
      } else {
        // 如果没有预定义配置，动态生成列
        if (tableData.value.length > 0) {
          const firstRow = tableData.value[0]
          tableColumns.value = Object.keys(firstRow).map(key => ({
            prop: key,
            label: key,
            minWidth: '150'
          }))
        }
      }
    } catch (error) {
      console.error('加载表格数据失败:', error)
      throw new Error('加载表格数据失败')
    } finally {
      loading.value = false
    }
  }



  const exportTableData = async (tableName, taskId = null, dataSource = 'sqlite') => {
    try {
      const params = new URLSearchParams()
      params.append('table_name', tableName)
      if (taskId) {
        params.append('task_id', taskId)
      }
      
      const apiPath = dataSource === 'mysql' ? '/api/mysql/export' : '/api/sqlite/export'
      const response = await axios.get(apiPath, {
        params: Object.fromEntries(params),
        responseType: 'blob'
      })
      
      // 创建下载链接
      const blob = new Blob([response.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${tableName}_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出CSV数据失败:', error)
      throw error
    }
  }

  const exportTableDataAsJSON = async (tableName, taskId = null, dataSource = 'sqlite') => {
    try {
      const params = new URLSearchParams()
      params.append('table_name', tableName)
      if (taskId) {
        params.append('task_id', taskId)
      }
      
      const apiPath = dataSource === 'mysql' ? '/api/mysql/export-json' : '/api/sqlite/export-json'
      const response = await axios.get(apiPath, {
        params: Object.fromEntries(params)
      })
      
      // 创建JSON文件下载
      const jsonData = JSON.stringify(response.data, null, 2)
      const blob = new Blob([jsonData], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${tableName}_${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出JSON数据失败:', error)
      throw error
    }
  }

  return {
    // 状态
    loading,
    tableData,
    totalCount,
    availableTables,
    tableColumns,
    
    // 计算属性
    hasData,
    
    // 方法
    loadAvailableTables,
    loadTableData,
    clearTableData,
    exportTableData,
    exportTableDataAsJSON
  }
})