import pyautogui
import pyperclip
import time

wait_minus = 1
wait_short = 1
wait_mid = 5
wait_answer = 10


input_box = (1230, 1443)
send_button = (2008, 1440)
copy_button = (1000, 1315)  # 一次就出来的 copy button
refresh_button = (137, 96)
to_final_location = (1447, 1347)
close_helpful_button = (1701, 1314)
regenerate_button = (1488, 1430)
close_response_better_button = (1843, 1265)
copy_button2 = (1093, 1319)  # regeneate后，copy button前面会出现翻页，所以位置不一样了
copy_button3 = (1076, 1271)  # regenerate后，如果还有“询问回答是否更好”，则copy button又不一样
copy_button_reach_limit = (1096, 1276)

close_button = (2522, 20)
taskbar_google = (312, 1565)
bookmark_zhanghao = (711, 148)
bookmark_haiwai = (739, 252)
bookmark_chatgpt = (1009, 255)
new_chat = (348, 235)

# 986 1315

def parse_file_using_chatgpt(file_path, question, is_reopen_browser):
    if is_reopen_browser:  # 每隔一段时间关闭浏览器，避免长时间卡住
        # 关闭浏览器
        time.sleep(wait_minus)
        pyautogui.moveTo(close_button[0], close_button[1]) 
        time.sleep(wait_short)
        pyautogui.click()

        # 等待1分钟
        time.sleep(60)

        # 打开浏览器
        time.sleep(wait_minus)
        pyautogui.moveTo(taskbar_google[0], taskbar_google[1]) 
        time.sleep(wait_short)
        pyautogui.click()

        # 点击账号 海外 chatgpt
        time.sleep(wait_minus)
        pyautogui.moveTo(bookmark_zhanghao[0], bookmark_zhanghao[1]) 
        time.sleep(wait_short)
        pyautogui.click()
        time.sleep(wait_minus)
        pyautogui.moveTo(bookmark_haiwai[0], bookmark_haiwai[1]) 
        time.sleep(wait_short)
        pyautogui.click()
        time.sleep(wait_minus)
        pyautogui.moveTo(bookmark_chatgpt[0], bookmark_chatgpt[1]) 
        time.sleep(wait_short)
        pyautogui.click()

        # 点击 newchat
        time.sleep(wait_mid)
        pyautogui.moveTo(new_chat[0], new_chat[1]) 
        time.sleep(wait_short)
        pyautogui.click()
        time.sleep(20)  # 等待20s新对话框刷新

        
    
    # 读入文章
    file = open(file_path, "r", encoding='utf-8')
    content = file.read()
    file.close()

    # 去掉原文链接
    if '.html' in content:
        remain = content.split('.html')[1:]
        content = ''.join(remain)

    # 输入内容
    pyperclip.copy(content+'\n'+question)  # 将内容复制到剪贴板
    time.sleep(wait_minus)
    pyautogui.moveTo(input_box[0], input_box[1]) 
    time.sleep(wait_short)
    pyautogui.click()
    time.sleep(wait_short)
    pyautogui.hotkey('ctrl', 'v')  # 将路径粘贴到输入框
    
    # 点击发送
    time.sleep(wait_short)
    pyautogui.moveTo(send_button[0], send_button[1])
    time.sleep(wait_short)
    pyautogui.click()
    
    inherent_question = '根据以上信息，回答以下问题：'
    text = '根据以上信息，回答以下问题：'
    times = 1
    while inherent_question in text:  # 回答中有这一句，说明网太慢，没有加载出来。需要延长等待时间，再等一轮
        print('\n 等待第{}次'.format(times))
        
        # 若等待次数大于1，则可能出现了 regenerate
        if times >1:
            time.sleep(wait_short)
            pyautogui.moveTo(regenerate_button[0], regenerate_button[1])  # 若出现了regenerate，则重新生成
            time.sleep(wait_short)
            pyautogui.click()
        
        # 等待阅读
        time.sleep(wait_answer) 

        # 点击到本页末的箭头
        time.sleep(wait_short)
        pyautogui.moveTo(to_final_location[0], to_final_location[1])
        time.sleep(wait_short)
        pyautogui.click()

        # 如果没有那个箭头，则控制鼠标滚轮到页末
        time.sleep(wait_short)
        pyautogui.scroll(-20000)

        # 关掉 is this conversation helpful so far? 窗口
        time.sleep(wait_short)
        pyautogui.moveTo(close_helpful_button[0], close_helpful_button[1])
        time.sleep(wait_short)
        pyautogui.click()

        # 复制输出到剪贴板
        time.sleep(wait_short)
        pyautogui.moveTo(copy_button[0], copy_button[1])
        time.sleep(wait_short)
        pyautogui.click()
        time.sleep(wait_short)

        # 从剪贴板读入
        text = pyperclip.paste()
        # print('\n从剪贴板读入：\n', text)


        ################# 若答案未生成，或未复制成功
        inherent_question = '根据以上信息，回答以下问题：'
        # 若是regenerate之后的结果
        if inherent_question in text:
            # 复制输出到剪贴板
            time.sleep(wait_short)
            pyautogui.moveTo(copy_button2[0], copy_button2[1])
            time.sleep(wait_short)
            pyautogui.click()

            # 从剪贴板读入
            text = pyperclip.paste()
        
        # 若regenerate后，还出现了“询问回答是否更好”的窗口
        if inherent_question in text:
            # 复制输出到剪贴板
            time.sleep(wait_short)
            pyautogui.moveTo(copy_button3[0], copy_button3[1])
            time.sleep(wait_short)
            pyautogui.click()

            # 关闭 询问回答是否更好的窗口
            time.sleep(wait_short)
            pyautogui.moveTo(close_response_better_button[0], close_response_better_button[1])
            time.sleep(wait_short)
            pyautogui.click()

            # 从剪贴板读入
            text = pyperclip.paste()

        # 若还是没得到，则可能超出了每小时字数限制，则必须等10分钟，再进行操作
        if inherent_question in text:
            # 复制空白输出到剪贴板
            time.sleep(wait_short)
            pyautogui.moveTo(copy_button_reach_limit[0], copy_button_reach_limit[1])
            time.sleep(wait_short)
            pyautogui.click()
            tmp_text = pyperclip.paste()  # 若按到了这个copy，则为空
            if tmp_text=='':
                text = '超出1小时内字数限制，跳过本条，等10分钟继续解析下条'
                print('\n ', text)
                time.sleep(60*10)  # 等10分钟再继续
                # 刷新网页
                print('\n 刷新网页'.format(times))
                time.sleep(wait_short)
                pyautogui.moveTo(refresh_button[0], refresh_button[1])  
                time.sleep(wait_short)
                pyautogui.click()
                time.sleep(wait_mid)
                break  # 跳出本次文件解析

        if inherent_question in text and times > 5:
            text = '等待超过5次'
            # 刷新网页
            print('\n 刷新网页'.format(times))
            time.sleep(wait_short)
            pyautogui.moveTo(refresh_button[0], refresh_button[1])  
            time.sleep(wait_short)
            pyautogui.click()
            time.sleep(wait_mid)  # 等待刷新
            break  # 跳出本次文件解析

        times += 1

    return text