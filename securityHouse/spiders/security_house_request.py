import scrapy
import re

from securityHouse.items import SecurityhouseItem


## scrapy crawl beike -a address="普陀" -a max=20
class QuotesSpider(scrapy.Spider):
    name = "securityHouse"
    # params = {
    #     "year": "2023",  # 年份
    #     "area": "浦东新区",  # 地区
    # }
    shanghai_areas = ['黄浦', '徐汇', '长宁', '静安', '普陀', '虹口', '杨浦', '宝山', '嘉定', '浦东新区', '金山',
                      '松江', '青浦', '奉贤', '崇明', '漕河泾开发区']
    pattern_area = re.compile('|'.join(shanghai_areas))
    pattern_years = re.compile(r'\d{4}年')
    allowed_domains = ['fgj.sh.gov.cn']
    start_urls = ['https://fgj.sh.gov.cn/gycqbzfgsgg/index{}.html']

    def start_requests(self):
        for page in range(int(64)):
            suffix = '' if page == 0 else '_' + str(page)
            url = self.start_urls[0].format(suffix)
            print('start_requests-----------------------------', url)
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        lis = response.css('div.tab-content  div.tab-pane li')
        for li in lis:
            item = SecurityhouseItem()
            # 提取元素的文本内容
            text = li.css('::text').get()
            if "保障住房选房结果公告" in text:
                if "非本市户籍" in text:
                    item['local'] = '否'
                else:
                    item['local'] = '是'
                area_match = self.pattern_area.search(text)
                years_match = self.pattern_years.search(text)
                if area_match and years_match:
                    area = area_match.group()
                    years = years_match.group()
                    # print("提取到:", area, years)
                    item['area'] = area
                    item['years'] = years
                    link = 'https://fgj.sh.gov.cn' + li.css('a::attr(href)').get()
                    item['link'] = link
                    if link:
                        print('detail_url', link)
                        yield scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response, **kwargs):
        item = response.meta['item']
        content = ''.join(response.css('div#ivs_content ::text').extract())

        pattern_approved = re.compile(r'本批准予购房家庭为(\d+)户')
        pattern_participated = re.compile(r'参加选房家庭(\d+)户')
        pattern_selected = re.compile(r'选购房源家庭为(\d+)户')

        # 匹配文本
        approved_match = pattern_approved.search(content)
        participated_match = pattern_participated.search(content)
        selected_match = pattern_selected.search(content)

        # 提取匹配到的值
        approved_value = approved_match.group(1) if approved_match else 0
        participated_value = participated_match.group(1) if participated_match else 0
        selected_value = selected_match.group(1) if selected_match else 0

        # 将提取到的值存入item
        item['approved_value'] = approved_value
        item['participated_value'] = participated_value
        item['selected_value'] = selected_value

        yield item
