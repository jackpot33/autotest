import requests
import jsonpath


class TestApi:
    def __init__(self):
        self.token = ""

    def test_get_token(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        datas = {
            "grant_type": "client_credential",
            "appid": "wx74a8627810cfa308",
            "secret": "e40a02f9d79a8097df497e6aaf93ab80"
        }
        res = requests.get(url, params=datas)
        self.token = jsonpath.jsonpath(res.json(), "$.access_token")
        print(self.token)

    def test_select_flag(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/get"
        datas = {
            "access_token": self.token[0]
        }
        res = requests.get(url, params=datas)
        return res

    def test_create_flag(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/create?access_token=" + self.token[0]
        datas = {
            'tag': {'name': '广东'}
        }
        exist_logs = self.test_select_flag().json()
        all_log_name = [match["name"] for match in exist_logs['tags']]
        if datas["tag"]['name'] in all_log_name:
            return "创建的标签已经存在"
        else:
            res = requests.post(url, json=datas)
            print(res.json())


if __name__ == "__main__":
    app = TestApi()
    app.test_get_token()
    app.test_select_flag()
    app.test_create_flag()


def use_jsonpath():
    # 示例 JSON 数据
    data = {
        "store": {
            "book": [
                {"category": "reference", "author": "Nigel Rees", "title": "Sayings of the Century", "price": 8.95},
                {"category": "fiction", "author": "Evelyn Waugh", "title": "Sword of Honour", "price": 12.99},
                {"category": "fiction", "author": "Herman Melville", "title": "Moby Dick", "isbn": "0-553-21311-3",
                 "price": 8.99},
                {"category": "fiction", "author": "J. R. R. Tolkien", "title": "The Lord of the Rings",
                 "isbn": "0-395-19395-8", "price": 22.99}
            ],
            "bicycle": {"color": "red", "price": 19.95}
        }
    }

    # 使用 jsonpath 查询
    # json 查询方式
    #     $ 表示根节点
    #     . 表示子节点
    #     [*] 表示所有元素
    #     [] 表示第几个元素
    #     .. 递归节点
    jsonpath_expr = jsonpath.jsonpath(data, '$.store.book[*].author')
    # 列表推导式：将jsonpath_expr中的元素添加到authors中
    authors = [match for match in jsonpath_expr]

    print(jsonpath_expr)
    print(authors)

# use_jsonpath()
