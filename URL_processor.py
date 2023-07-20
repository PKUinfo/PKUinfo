import os
import openai
import json
from keys import openai_APIKEY, openai_BASE
openai.api_key = openai_APIKEY
openai.api_base = openai_BASE

def ask_chatgpt(my_messages):
    # print('ask ', my_messages)

    ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=my_messages,
        ).choices[0].message.content
  
    return ans

def txt2json(text):
    result = ask_chatgpt(text)
    return result



data_dir = './outcome' 
id = 0

def solve(text):
    global id
    my_messages = [
        {"role": "system", "content": "Now that you are engaged in professional text processing, please let me know if the push below is a preview of an event (such as a lecture or ticket collection) (而不是活动总结或者其它内容). If so, please use JSON format to tell me the 'event_name', 'event_time', 'location', 'organizational_unit', and 'event_summary'. 时间尽可能规范到特定的时刻，如果有多个时间请一并输出，如没有则以None存在，推送发布时间为2023年。Otherwise, tell me the activity category it belongs to."},
        {"role": "user", "content": text},
    ]
    infolist = ask_chatgpt(my_messages)
    infolist = infolist.replace('\n', ' ')
    json_list = json.loads(infolist)
    # print ('info_list = ', json_list)
    if type(json_list) != list: 
        json_list = [json_list]
    should_exist = ['event_name', 'event_time', 'location', 'organizational_unit', 'event_summary']
    for info in json_list:
        all_exist = True
        for key in should_exist:
            if key not in info:
                print('Error: ', key, ' not exist')
                all_exist = False
                break
        if not all_exist:
            continue
        ask_time_message = [
            {"role": "system", "content": "请你告诉我这个活动最早的时间，请以 XXXX-XX-XX XX:XX 的格式告诉我。请注意最早的时间只会存在一个，请直接告诉我这个格式不要回答其它多余的内容，如果没有特定的时间，截止时间请告诉我为24:00，开始时间请告诉我00:00，如果未能提供请告诉我None"},
            {"role": "user", "content": str(info)},
        ]
        start_time = ask_chatgpt(ask_time_message)
        # 如果start_time 不是 XXXX-XX-XX XX:XX 的格式，那么就是没有时间，continue
        print ('start_time = ', start_time)
        if len(start_time) != 16 or start_time[4] != '-' or start_time[7] != '-' or start_time[10] != ' ' or start_time[13] != ':' or not start_time[:4].isdigit() or not start_time[5:7].isdigit() or not start_time[8:10].isdigit() or not start_time[11:13].isdigit() or not start_time[14:16].isdigit():
            print('Error: start_time format error')
            continue
        json_data = {
            'event_name': info.get('event_name', None),
            'data': start_time[:10],
            'time': start_time[11:16],
            'event_time': str(info.get('event_time', None)),
            'location': info.get('location', None),
            'organizational_unit': info.get('organizational_unit', None),
            'event_summary': info.get('event_summary', None),
        }
        print(json_data)
        with open('./outcome.csv', 'a', encoding='utf-8') as f:
            f.write(str(id)+','+str(json_data)+'\n')
            id += 1

def process_files(current_dir):
    global id
    for filename in os.listdir(current_dir):
        try:
            file_path = os.path.join(current_dir, filename)
            
            if os.path.isdir(file_path):
                process_files(file_path)
                
            elif filename.endswith('.txt'):
                with open(file_path,encoding='utf-8') as f:
                    text = f.read()
                solve(text)

                return
        except:
            # pass
            print('Error processing file: ', filename)
            continue
# solve('''
#        微信号 yintianshenjiao 
#  功能介绍 向会员及广大天文爱好者传达活动信息、科普天文知识，与大家共赏天文之美。 
# 本文来源于「北大天文」微信公众号，欢迎大家关注。
# 恒星物理研究进展


# 内容提要

# 本报告将简要回顾恒星物理的发展历史，介绍恒星物理的主要成就，讨论恒星结构与演化、双星演化、特殊恒星的形成、星族合成、演化星族合成等，探究超新星、双致密星引力波源等的形成。报告的最后对恒星物理的发展进行展望。

# 报告人  韩占文

# 韩占文，中国科学院院士，中国科学院云南天文台研究员，主要从事恒星结构和演化研究，发展了双星星族合成，建立了热亚矮星等特殊天体的形成模型，将双星星族合成用于星系研究。曾获何梁何利基金科学与技术进步奖（天文学奖）、国家自然科学奖二等奖等。现为中国《天文天体物理研究》期刊（RAA）联合主编、欧洲《天文和天体物理》期刊（A&A）副编辑。

# 地点
# 科维理研究所报告厅
# 时间
# 2023年4月9日 15:00-16:30

# 欢迎关注北大天文！
# 图文：韩占文

# 微信扫一扫关注该公众号
# 百年风雨1北大
# 今时堆瀣I天女
# 微信公众号: ,北大天文
# '''
#       )
process_files(data_dir)
print('Done!')
