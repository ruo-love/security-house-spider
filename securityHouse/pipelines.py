# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

from openpyxl import Workbook


class SecurityhousePipeline:

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        # people
        self.ws.title = '上海保障房数据汇总'
        self.ws.append(['地区', '年份', '是否上海户籍', '本批准予（户）', '参加选房家庭（户）', '选购房源家庭（户）', '地址'])
        # house
        # self.ws.title = '上海保障房户型数据汇总'
        # self.ws.append(['地区', '年份', '一居室', '二居室', '三居室', '总户数', '地址'])

    def process_item(self, item, spider):
        try:
            # 使用字典推导式简化数据提取
            # people
            item_data = {key: item.get(key, '') for key in
                         ['area', 'years', 'local', 'approved_value', 'participated_value', 'selected_value', 'link']}

            # house
            # item_data = {key: item.get(key, '') for key in
            #              ['area', 'years', 'one', 'two', 'three', 'total', 'link']}
            # Excel 插入
            self.ws.append(list(item_data.values()))
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")

        return item

    def close_spider(self, spider):
        now = datetime.now()
        formatted_now = now.strftime("%Y年%m月%d日 %H时%M分%S秒 ")
        # Save and close the workbook
        self.wb.save(formatted_now + self.ws.title + '.xlsx')
        self.wb.close()
