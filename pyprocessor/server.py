import socket
from get_content import ContentGetter
from GPT_processor import GPTProcessor

class URL2JSON:
    def __init__(self):
        self.content_getter = ContentGetter()
        self.processor = GPTProcessor() 
    
    def get_json(self, url):
        import json
        content = self.content_getter.get_fulltext(url)
        jsondata_list = self.processor.Text_to_JSON(content)
        for jsondata in jsondata_list:
            jsondata["url"] = url
        return jsondata_list

    def convert_to_ActivityInfo(self,json_data):
        import json
        import datetime
        json_data = json.loads(json_data)
        activityInfo = {}
        activityInfo["title"] = json_data["title"]
        activityInfo["address"] = json_data["location"]
        activityInfo["startDate"] = datetime.datetime.strptime(json_data["data"],"%Y-%m-%d")
        activityInfo["endDate"] = datetime.datetime.strptime(json_data["data"],"%Y-%m-%d")
        activityInfo["startTime"] = datetime.datetime.strptime(json_data["time"],"%H:%M:%S")
        activityInfo["endTime"] = datetime.datetime.strptime(json_data["time"],"%H:%M:%S")
        activityInfo["description"] = json_data["event_summary"]
        activityInfo["college"] = json_data["organizational_unit"]
        activityInfo["accountLink"] = json_data["url"]
        activityInfo["extraInfo"] = json_data["event_time"]
        return activityInfo

if __name__ == "__main__":
    url2json = URL2JSON()
    result = url2json.get_json(str('https://mp.weixin.qq.com/s/LUsA5qG5ysC77sugGcLjOA'))
    print('result = ',result)
    socket_server = socket.socket()

    socket_server.bind(("localhost", 9001))
    socket_server.listen(10)

    while True:
        result = socket_server.accept()
        conn = result[0] # 客户端连接对象
        address = result[1] # 客户端地址信息

        data = conn.recv(1024)

        result_jsonlist = url2json.get_json(str(data))
        for result in result_jsonlist:
            data = url2json.convert_to_ActivityInfo(str(result))
            import requests
            import json
            url = 'http://localhost:8080/api/admin/activity'
            headers = {'Content-Type': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers)

        info = "success"
        conn.send(info.encode())
        print("Message sent")
        conn.close()


    socket_server.close()
