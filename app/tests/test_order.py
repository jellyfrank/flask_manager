
from flask import Flask
from app import db
from app.model.order import Order
from app.model.shop import Shop
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
import unittest
from copy import deepcopy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    "postgres", "postgres", "127.0.0.1", 5432, "unittest")
app.config['TESTING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


class TestOrder(TestCase):

    def create_app(self):
        return app

    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_shop(self):
        s = Shop(name="test",key="123",secret="123",session="atb")
        db.session.add(s)
        db.session.flush()
        return s.id

    def test_create(self):
        shop_id = self._create_shop()
        data = {
            "total_results": 1,
            "trades": {
                "trade": [
                    {
                        "buyer_nick": "本人hx",
                        "created": "2019-05-22 21:16:59",
                        "modified": "2019-05-22 21:16:59",
                        "order_tax_fee": "7.43",
                        "orders": {
                            "order": [
                                {
                                    "adjust_fee": "0.00",
                                    "buyer_rate": False,
                                    "cid": 50011980,
                                    "discount_fee": "167.43",
                                    "is_daixiao": False,
                                    "num": 1,
                                    "num_iid": 539106714422,
                                    "oid": "302605903310133611",
                                    "outer_iid": "TFZHZSC02181804",
                                    "outer_sku_id": "TFZHZSC02181804",
                                    "payment": "89.00",
                                    "pic_path": "https: //img.alicdn.com/bao/uploaded/i4/2961990038/O1CN01wBeLE61C9RZzPK40z_!!0-item_pic.jpg",
                                    "price": "249.00",
                                    "refund_status": "NO_REFUND",
                                    "seller_rate": False,
                                    "seller_type": "B",
                                    "sku_id": "3221788166629",
                                    "sku_properties_name": "化妆品净含量:250ml",
                                    "status": "WAIT_BUYER_PAY",
                                    "store_code": "STORE_8820233",
                                    "sub_order_tax_fee": "7.43",
                                    "sub_order_tax_promotion_fee": "0.00",
                                    "sub_order_tax_rate": "0",
                                    "tax_coupon_discount": "7.43",
                                    "tax_free": True,
                                    "title": "merino/美丽诺新西兰进口淡痘印控油补水保湿镇静芦荟胶250ml",
                                    "total_fee": "81.57"
                                }
                            ]
                        },
                        "payment": "89.00",
                        "post_fee": "0.00",
                        "receiver_address": "徐家营街道孙辛路278",
                        "receiver_city": "洛阳市",
                        "receiver_district": "涧西区",
                        "receiver_mobile": "18211972305",
                        "receiver_name": "孙浩鑫",
                        "receiver_state": "河南省",
                        "seller_flag": 0,
                        "status": "WAIT_BUYER_PAY",
                        "tid": "302605903310133611",
                        "total_fee": "256.43"
                    }
                ]
            },
            "request_id": "nai99t2mnrhx"
        }

        udata = deepcopy(data)

        xdata = data["trades"]["trade"][0]
        xdata["src_id"] = shop_id
        Order.create(xdata)

        udata["trades"]["trade"][0]["buyer_nick"] = "测试修改名称"

        Order.update_order(udata["trades"]["trade"][0])

        o = Order.query.filter(Order.tid==udata["trades"]["trade"][0]["tid"]).first()
        self.assertEqual(o.buyer_nick,"测试修改名称")


if __name__ == "__main__":
    unittest.main()
