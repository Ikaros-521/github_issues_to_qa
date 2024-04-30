import requests
import json, traceback
from loguru import logger

# 指定用户名&仓库名
repo = 'Ikaros-521/AI-Vtuber'
# https://github.com/settings/tokens 申请token 赋予仓库issue读权限
token = ''

logger.add("日志.txt", level="INFO", rotation="1000 MB")
    
    
# 获取仓库issue列表
def get_repo_issues_list():
    try:
        ret_issues_list = []
        
        # 设置请求头
        headers = {
            'Authorization': f'Bearer {token}',
            # 'Accept': 'application/vnd.github+json'
        }

        # 获取issue的API地址
        url = f'https://api.github.com/repos/{repo}/issues'

        for page in range(1, 10000):
            data = {
                # Indicates the state of the issues to return. Can be either `open`, `closed`, or `all`.
                "state": "all",
                # One of `asc` (ascending) or `desc` (descending).
                "direction": "asc",
                # Page number of the results to fetch.
                "page": page,
                # Results per page (max 100).
                "per_page": 100,
            }

            # 发送GET请求获取issue列表
            response = requests.get(url, headers=headers, params=data)
            issues_list = response.json()
            
            if len(issues_list) == 0:
                logger.info(f"第{page}页 * 100, 获取不到更多的issue了，退出循环")
                break
            
            logger.info(f"第{page}页 * 100, 获取到 {len(issues_list)} 个issue")
            # logger.info(issues_list)
            
            tmp_json = {}
            
            for issue in issues_list:
                # 获取issue的标题和链接
                issue_title = issue['title']
                issue_number = issue['number']
                issue_body = issue['body']
                # logger.info(f'[{issue_number}] {issue_title}')
                tmp_json = {'title': issue_title, 'number': issue_number, 'body': issue_body}
                
                ret_issues_list.append(tmp_json)
                
                logger.debug(tmp_json)
            
        return ret_issues_list
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f"获取仓库issue列表失败: {e}")
        return None


# 获取issue所有评论
def get_issue_all_comments_list(issue_number):
    try:
        ret_comments_list = []
        
        # 设置请求头
        headers = {
            'Authorization': f'Bearer {token}',
            # 'Accept': 'application/vnd.github+json'
        }

        # 获取comments的API地址
        url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'

        for page in range(1, 10000):
            data = {
                # Page number of the results to fetch.
                "page": page,
                # Results per page (max 100).
                "per_page": 100,
            }

            # 发送GET请求获取issue列表
            response = requests.get(url, headers=headers, params=data)
            comments_list = response.json()
            
            if len(comments_list) == 0:
                logger.info(f"获取仓库issue#{issue_number} 第{page}页 * 100, 获取不到更多的评论了，退出循环")
                break
            
            logger.info(f"获取仓库issue#{issue_number} 第{page}页 * 100, 获取到 {len(comments_list)} 个评论")
            # logger.info(comments_list)
            
            tmp_json = {}
            
            for comment in comments_list:
                # 获取comment的标题和链接
                username = comment['user']['login']
                body = comment['body']
                # logger.info(f'[{username}] {body}')
                tmp_json = {'username': username, 'body': body}
                
                ret_comments_list.append(tmp_json)
            
        return ret_comments_list
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f"获取仓库issue列表失败: {e}")
        return None


if __name__ == '__main__':
    logger.info("开始执行...")
    logger.info("获取仓库issue列表...")
    # 获取仓库issue列表
    issues_list = get_repo_issues_list()
    
    if issues_list is None:
        logger.info("获取仓库issue列表失败")
    else:
        logger.info("获取仓库issue列表完毕")
        # 打印issue列表
        logger.info(issues_list)
        
        qa_list = []
        
        for issue in issues_list:
            logger.info(f"获取仓库issue#{issue['number']}所有评论...")
            comments_list = get_issue_all_comments_list(issue["number"])
            tmp_str = f'[issue#{issue["number"]}] {issue["title"]}。'
            
            if comments_list is None:
                continue
            
            for comment in comments_list:
                body = comment["body"]
                if body is not None:
                    body = body.replace("\r\n", "。")
                    tmp_str += f'{body}。'
                
            logger.info(f"获取仓库issue#{issue['number']}所有评论完毕，合并内容为：{tmp_str}")
            qa_list.append(tmp_str)
            
        logger.debug(qa_list)
        
        # 写入文件
        with open('qa.txt', 'w', encoding='utf-8') as f:
            for qa in qa_list:
                f.write(qa + '\n')
                
        logger.info("写入文件成功")