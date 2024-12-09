from openai import OpenAI
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from netrequest import company_basic_post, company_basic_change_post, company_ip_copyright_software_post, \
    company_ip_patent_basic_post, company_op_bidding_baseinfo_post, company_op_finance_post
from neo4j_util import neo4j_query
import re

client = OpenAI(api_key="sk-9cb823d6cb2d48d6b7cf1783b7735749", base_url="https://api.deepseek.com")
os.environ["TAVILY_API_KEY"] = "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"
tool = TavilySearchResults(max_results=1)


def chat(user_input):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_input},
        ], stream=False
    )
    return response.choices[0].message.content


def websearch(user_input):
    result_json = tool.invoke(user_input)
    result_list = [result['content'] for result in result_json]
    return result_list


# 企业资质
def enterprise_qualification_query(enter_name):
    # print(websearch("联合汽车电子（重庆）公司获得了哪些企业资质"))
    query = enter_name + "获得了哪些企业资质"
    Enterprise_qualification_websearch_list = websearch(query)
    Enterprise_qualification_websearch_str = '\n'.join(Enterprise_qualification_websearch_list)
    Enterprise_qualification_websearch_prompt = '''
    ##功能定义##
    你是一个查询企业资质的专家，给你的信息有企业名称和检索得到的企业信息；
    你需要从检索得到的企业相关信息中找到该企业的企业资质；
    你的输出需要严格遵守检索得到的企业信息，不允许胡编乱造，也不需要输出其他分析内容，直接输出企业资质，可以是多个、一个以及没有。
    输出规则定义：多个企业资质用“、”分割，一个企业资质直接输出即可，没有查询到企业资质输出“没有查询到相关资质”，不要输出重复的资质。

    ##输入##
    企业名称：
    {enterprise_name}
    检索得到的企业信息：
    {websearch_enterpreise_info}

    ##输出##
    '''
    Enterprise_qualification_websearch_input = Enterprise_qualification_websearch_prompt.format(
        enterprise_name="联合汽车电子（重庆）公司", websearch_enterpreise_info=Enterprise_qualification_websearch_str)
    # print(chat(Enterprise_qualification_websearch_input))
    answer = chat(Enterprise_qualification_websearch_input)
    return answer


# 基本面分析
def enterprise_history_query(enter_name,
                             establishDate,
                             company_basic_change_json,
                             history_local_str):
    # print(websearch("联合汽车电子（重庆）公司获得了哪些企业资质"))
    history_change = ""
    hits = company_basic_change_json['hits']['hits']
    for i, source in enumerate(hits):
        change_date = source['_source']['change_date']
        change_item = source['_source']['change_item']
        before_content = source['_source']['before_content']
        after_content = source['_source']['after_content']
        history_item = "变更时间：" + change_date + "\n" + "变更事项：" + change_item + "\n" + "变更前内容：" + before_content + "\n" + "变更后内容：" + after_content + "\n"
        history_change += "变更记录" + str(i + 1) + "：" + "\n\n" + history_item

    query = enter_name + "的发展历程"
    Enterprise_qualification_websearch_list = websearch(query)
    # print(Enterprise_qualification_websearch_list)
    Enterprise_qualification_websearch_str = '\n'.join(Enterprise_qualification_websearch_list)
    Enterprise_qualification_websearch_prompt = '''
    ##功能定义##
    你是一个撰写企业简介的专家，给你的信息有企业名称、企业成立时间、企业工商历史变更记录和网络检索得到的企业发展历程；
    你需要从给出的所有信息写一段企业的历史发展简介信息；
    你的输出需要严格遵守给出的所有信息，不允许胡编乱造，也不需要输出其他分析内容。

    ##输入##
    企业名称：
    {enterprise_name}
    企业成立时间：
    {time}
    企业工商历史变更记录：
    {history_change}
    检索得到的企业发展历程：
    {websearch_enterpreise_info}

    ##输出##
    '''
    Enterprise_qualification_websearch_input = Enterprise_qualification_websearch_prompt.format(
        enterprise_name="联合汽车电子（重庆）公司",
        time=establishDate, history_change=history_change,
        websearch_enterpreise_info=Enterprise_qualification_websearch_str)

    history_answer = chat(Enterprise_qualification_websearch_input)

    summery_prompt = '''
    ##功能定义##
    你是一个撰写企业画像报告的专家，给你的信息有企业发展历程和企业的基本信息；
    你需要从给出的所有信息写一段企业画像的报告信息；
    你的输出需要严格遵守给出的所有信息，不允许胡编乱造，也不需要输出其他分析内容，语言表达简洁清晰。

    ##输入##
    企业发展历程：
    {history_answer}
    企业的基本信息：
    {history_local_str}
    ##输出##
    '''
    summery_prompt_input = summery_prompt.format(history_answer=history_answer, history_local_str=history_local_str)
    answer = chat(summery_prompt_input)
    return answer


# 分析所属行业、核心产品、所属战略新兴产业、所属高新技术产业、主营业务分析
def enterprise_main_business_anl(enter_name,
                                 industry,
                                 establishDate,
                                 busiScope,
                                 patent_item_list,
                                 software_item_list,
                                 project_str
                                 ):
    print("分析所属行业、核心产品、所属战略新兴产业、所属高新技术产业、主营业务分析")
    if patent_item_list != []:
        patent_str = ""
        for patent in patent_item_list:
            patent_type = patent['_source']['patent_type']
            patent_name = patent['_source']['patent_name']
            abstract = patent['_source']['abstract']
            patent_item = "专利名字：" + patent_name + "\n专利类型：" + patent_type + "\n专利介绍：" + abstract
            patent_str += patent_item + "\n\n"
        print(patent_str)

    if software_item_list != []:
        software_str_list = []
        for software in software_item_list:
            software_name = software['_source']['software_full_name']
            software_str_list.append(software_name)
        software_name_str = '、'.join(software_str_list)
        print(software_name_str)

    bidding_party_str = ""
    for i, bidding_party in enumerate(bidding_party_item_list):
        party_type = bidding_party['_source']['party_type']
        if party_type == "中标人":
            bidding_party_name = bidding_party['_source']['title']
            bidding_party_project = bidding_party['_source']['project_name']
            bidding_item = "企业中标项目合同名称：" + bidding_party_name + "\n项目名称：" + bidding_party_project
            bidding_party_str += "项目" + str(i + 1) + "：" + "\n\n" + bidding_item
    print(bidding_party_str)
    return None,None,None,None


# # 分析企业政策匹配模块
# def enterprise_policy_anl(enter_name,
#                           enter_qul,
#                           industry,
#                           establishDate,
#                           busiScope,
#                           ):

# 分析产业情况模块
def enterprise_industry_anl(enter_name, industry_list, project_list):
    print("分析产业情况模块")
    print(enter_name)
    print(industry_list)
    print(project_list)
    return None,None


# 知识产权模块
def enterprise_pantent_anl(patent_item_list, project_list):
    print("知识产权模块")
    if patent_item_list != []:
        patent_str = ""
        for patent in patent_item_list:
            patent_type = patent['_source']['patent_type']
            patent_name = patent['_source']['patent_name']
            abstract = patent['_source']['abstract']
            patent_item = "专利名字：" + patent_name + "\n专利类型：" + patent_type + "\n专利介绍：" + abstract
            patent_str += patent_item + "\n\n"
        print(patent_str)
    print(project_list)
    return None


# 融资分析
def enterprise_finance_anl(finance_company_json):
    finance_company_list = finance_company_json['hits']['hits']
    if finance_company_list == []:
        return "该企业尚未进行公开融资。"

    finance_desc_str = ""
    for item in finance_company_list:
        time = item['_source']['investing_date']
        investing_amount = item['_source']['investing_amount']
        investing_round = item['_source']['investing_round']
        invest_full_name = item['_source']['invest_full_name']
        currency = item['_source']['currency']
        finance_item_str = "时间：" + time + "\n投资公司：" + invest_full_name + "\n投资金额：" + str(investing_amount)+currency
        finance_desc_str += finance_item_str
    print(finance_desc_str)
    return None


# 招投标分析
def enterprise_bidding_anl(bidding_party_item_list):
    if bidding_party_item_list == []:
        return "该企业尚未参与公开招投标活动。"
    print("招投标分析")
    bidding_party_desc_str = ""
    nobidding_party_desc_str = ""
    for i, bidding_party in enumerate(bidding_party_item_list):
        party_type = bidding_party['_source']['party_type']
        if party_type == "中标人":
            notice_date = bidding_party['_source']['notice_date']
            winning_amount_value = bidding_party['_source']['winning_amount_value']
            currency = bidding_party['_source']['currency']
            bidding_party_name = bidding_party['_source']['title']
            bidding_party_project = bidding_party['_source']['project_name']
            bidding_item = "时间：" + notice_date + "\n中标合同名称：" + bidding_party_name + "\n项目名称：" + bidding_party_project + "\n中标金额：" + str(winning_amount_value) + currency
            bidding_party_desc_str += "项目" + str(i + 1) + "：" + "\n\n" + bidding_item
        else:
            notice_date = bidding_party['_source']['notice_date']
            winning_amount_value = bidding_party['_source']['winning_amount_value']
            currency = bidding_party['_source']['currency']
            bidding_party_name = bidding_party['_source']['title']
            bidding_party_project = bidding_party['_source']['project_name']
            bidding_item = "时间：" + notice_date + "招标合同名称：" + bidding_party_name + "\n项目名称：" + bidding_party_project + "\n招标金额：" + str(winning_amount_value) + currency
            nobidding_party_desc_str += "项目" + str(i + 1) + "：" + "\n\n" + bidding_item

    print(bidding_party_desc_str)
    print(nobidding_party_desc_str)

    return None


enter_name = "上海赛伦生物技术股份有限公司"
company_id = "CAICT_COM_100006_53C286F48D8A8A901C5C68F3B1103E62"
company_basic_json = company_basic_post(company_id)
enter_code = company_basic_json['hits']['hits'][0]['_source']['unifiedSocialCreditCode']
# 变更信息
company_basic_change_json = company_basic_change_post(company_id)
# 成立时间
establishDate = company_basic_json['hits']['hits'][0]['_source']['establishDate']
# 企业资质
enterprise_qualification = enterprise_qualification_query(enter_name)
# 国标行业
industry = company_basic_json['hits']['hits'][0]['_source']['industry']
# 注册资本
stdRegCapital = company_basic_json['hits']['hits'][0]['_source']['stdRegCapital']
# 币种
currency = company_basic_json['hits']['hits'][0]['_source']['currency']
# 实缴资本
stdRealCapital = company_basic_json['hits']['hits'][0]['_source']['stdRealCapital']
# 历年社保缴纳人数
insuredNumber = company_basic_json['hits']['hits'][0]['_source']['insuredNumber']
# 股东名称、占股比例
finance_json = neo4j_query(company_id)
print(finance_json)
finance_str = ""
for item in finance_json:
    item_json = str(item)
    pattern = r"name='([^']*)'.*?percent='([^']*)'"
    match = re.search(pattern, item_json)
    name = match.group(1)
    percent = match.group(2)
    print("Name:", name)
    print("Percent:", percent)
    finance_item = name + "占比" + percent
    finance_str += finance_item + "\n"

history_local_str = '''
企业名称：{name}
统一社会信用代码：{code}
企业资质：{qual}
国标行业：{industry}
注册资本：{stdRegCapital}
实缴资本：{stdRealCapital}
历年社保缴纳人数：{insuredNumber}
股东：{finance_str}
'''
history_local_input = history_local_str.format(name=enter_name, code=enter_code, qual=enterprise_qualification,
                                               industry=industry, stdRegCapital=stdRegCapital,
                                               stdRealCapital=stdRealCapital, insuredNumber=insuredNumber,
                                               finance_str=finance_str)
# 企业基本面模块：企业资质、基本面分析
# 企业资质
print(enterprise_qualification_query(enter_name))
# 企业历史发展
print(enterprise_history_query(enter_name, establishDate, company_basic_change_json, history_local_input))

# 企业主营业务模块： 所属产业、联网分析核心产品、战略信息产业和高新技术产业、主营业务分析
# 经营范围
busiScope = company_basic_json['hits']['hits'][0]['_source']['busiScope']
print(busiScope)

# 专利获取
patent_json = company_ip_patent_basic_post(company_id)
patent_item_list = patent_json['hits']['hits']

# 软著获取
software_json = company_ip_copyright_software_post(company_id)
software_item_list = software_json['hits']['hits']

# 中标项目
bidding_party_json = company_op_bidding_baseinfo_post(company_id)
bidding_party_item_list = bidding_party_json['hits']['hits']
industry_list, project_list, industry_children_list, enter_business__anl = enterprise_main_business_anl(enter_name,
                                                                                                        enterprise_qualification,
                                                                                                        establishDate,
                                                                                                        busiScope,
                                                                                                        patent_item_list,
                                                                                                        software_item_list,
                                                                                                        bidding_party_item_list
                                                                                                        )

# 企业政策匹配模块

# # 产业情况模块：根据主营业务分析产业情况
industry_desc_str, enter_desc_str = enterprise_industry_anl(enter_name, industry_list, project_list)

# # 知识产权模块：描述性文字、专利与核心产品相关度
project_patent_sim = enterprise_pantent_anl(patent_item_list, project_list)

# 融资：融资描述以及融资方介绍
finance_post_json = company_op_finance_post(company_id)
finance_desc_str = enterprise_finance_anl(finance_post_json)

# 招投标情况
bidding_desc_str = enterprise_bidding_anl(bidding_party_item_list)
