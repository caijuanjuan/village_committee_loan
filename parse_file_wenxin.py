import time
import pyautogui
import pyperclip

wait_short = 1
wait_mid = 5
wait_long = 10

choose_extension1 = (1044, 1318)
choose_extension2 = (965, 1076)
file_name_box = (450, 708)
ok_button = (1014, 753)
input_box = (1190, 1381)
send_button = (1957, 1442)
copy_button = (1883, 1235)
copy_button2 = (1883, 1095)
stop_gen = (989, 1234)


def parse_file_using_wenxin(file_path, question, pre_res):
    idx = question.index('1.')  # 文心的问法，要删除第一句，直接以标号问句开头
    question = question[idx:]
    
    # 览卷文档
    time.sleep(wait_short)
    pyautogui.moveTo(choose_extension1[0], choose_extension1[1])
    time.sleep(wait_short)
    pyautogui.moveTo(choose_extension2[0], choose_extension2[1])
    time.sleep(wait_short)
    pyautogui.click()

    # 上传文档
    pyperclip.copy(file_path)  # 将路径复制到剪贴板
    time.sleep(wait_short)
    pyautogui.moveTo(file_name_box[0], file_name_box[1])
    time.sleep(wait_short)
    pyautogui.click()
    time.sleep(wait_short)
    pyautogui.hotkey('ctrl', 'v')  # 将路径粘贴到输入框
    time.sleep(wait_short)
    pyautogui.moveTo(ok_button[0], ok_button[1])  # 点击打开
    time.sleep(wait_short)
    pyautogui.click()
	
    # 等待阅读摘要（阅读摘要对生成结果有帮助）
    time.sleep(wait_long)  # 等待阅读摘要
    time.sleep(wait_long)  # 等待阅读摘要
    time.sleep(wait_long)  # 等待阅读摘要
    time.sleep(wait_long)  # 等待阅读摘要

    # # 若摘要实在没有阅读完，则停止生成（停止生成和重新生成，两个按钮在一个地方，不能这样按）
    # time.sleep(wait_short)
    # pyautogui.moveTo(stop_gen[0], stop_gen[1])  # 点击打开
    # time.sleep(wait_short)
    # pyautogui.click()


    # 输入问题
    pyperclip.copy(question)  # 将文字复制到剪贴板
    time.sleep(wait_short)
    pyautogui.moveTo(input_box[0], input_box[1])  # 光标移动到输入处
    time.sleep(wait_short)
    pyautogui.click()
    time.sleep(wait_short)
    pyautogui.hotkey('ctrl', 'v')  # 将问题粘贴到输入框

    # 点击发送
    time.sleep(wait_short)
    pyautogui.moveTo(send_button[0], send_button[1])
    time.sleep(wait_short)
    pyautogui.click()

    # 等待输出结果的时间
    time.sleep(wait_long)

    text = pre_res
    pyperclip.copy(pre_res)  # 粘贴板也置为以前的答案
    wait_repeat = 1
    while text==pre_res:
        print('\n 等待第{}次'.format(wait_repeat))
        time.sleep(5)  # 若还未生成答案，则再多等5s

        # 复制输出到剪贴板
        time.sleep(wait_short)
        pyautogui.moveTo(copy_button[0], copy_button[1])
        time.sleep(wait_short)
        pyautogui.click()
        
        time.sleep(wait_short)  # 可能会出现“你可以继续问我”，则复制按钮会改变位置
        pyautogui.moveTo(copy_button2[0], copy_button2[1])
        time.sleep(wait_short)
        pyautogui.click()

        # 从剪贴板读入
        text = pyperclip.paste()
        wait_repeat += 1

    return text

