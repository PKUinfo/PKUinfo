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

        print("Address: ", address)

        data = conn.recv(1024)
        # print("Accepted Information: ", str(data).split("'")[1])
        print("Accepted Information: ", str(data))
        print('json_info = ', url2json.get_json(str(data)))

        info = "success"
        conn.send(info.encode())
        print("Message sent")
        conn.close()

    socket_server.close()
