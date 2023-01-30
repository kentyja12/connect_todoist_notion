import os
import sys
from todoist_api_python .api import TodoistAPI
from notion.client import NotionClient
import time 


TODOIST_TOKEN = ' your todoist token '
NOTION_TOKEN = ' your notion token '
TODOIST_PROJECT_ID = ' your todoist project id '
NOTION_PAGE_URL = ' notion task list page URL '

# Delete a task of None.if size of task is 0.delete it.
def delete_task_of_None(tasklist_row):
    tasklist = []
    for task in tasklist_row:
        if len(task[1]) != 0:
            tasklist.append(task[1])
    return tasklist

# Get text(task) from Notion's page and put block's id and text in a list.
def get_block_info(page):
    response = page.children._get_block
    block_info = []
    for block in response.__self__:
        block_id = block.id
        block_text = response(block_id).title
        block_info.append((block_id,block_text))
    return block_info

#  Add a task list using Todoist API
def add_tasks(tasklist):
    cnt = 0
    error_tasks = []
    for task in tasklist:
        try:
            todoist_api.add_task(content=task, project_id=TODOIST_PROJECT_ID)
            cnt += 1
            print("【{}/{}】|{}を追加しました。".format(cnt,len(tasklist),task))
        except Exception as error:
            error_tasks.append(task)
            print(error)
    print("タスクの追加が終了しました。\n追加されたタスク数：{}個\n追加に失敗したタスク数：{}個".format(cnt,len(tasklist)-cnt))
    if len(error_tasks) != 0:
        print("追加に失敗したタスク一覧\n{}".format(error_tasks))
    print("この画面は5秒後に終了します。")

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2=NOTION_TOKEN)
todoist_api = TodoistAPI(token=TODOIST_TOKEN)

def main():
    # Replace this URL with the URL of the page you want to edit
    page = client.get_block(NOTION_PAGE_URL)

    block_info = get_block_info(page)
    tasklist = delete_task_of_None(block_info)
    add_tasks(tasklist)

    time.sleep(5)


if __name__ == "__main__":
    main()



