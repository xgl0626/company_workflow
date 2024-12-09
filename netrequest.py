import requests


# 企业基本数据
def company_basic_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_basic_change_info/_search'
    company_basic_url = 'http://47.109.144.203:9200/company_basic_info/_search'
    get_json_data = {
        "query": {
            "match": {
                "cid": company_id
            }
        }
    }
    response = requests.get(url=company_basic_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_basic请求成功')
        company_basic_json = response.json()
        return company_basic_json
    else:
        print('company_basic请求失败，状态码：', response.status_code)
        return response.status_code


# 企业变更情况
def company_basic_change_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_basic_change_info/_search'
    get_json_data = {
        "query": {
            "match": {
                "company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_basic_change请求成功')
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_basic_change请求失败，状态码：', response.status_code)
        return response.status_code


# 股权信息
def company_op_stockholder_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_op_stockholder/_search'
    get_json_data = {
        "query": {
            "match": {
                "company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_op_stockholder请求成功')
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_op_stockholder请求失败，状态码：', response.status_code)
        return response.status_code


# 软著
def company_ip_copyright_software_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_ip_copyright_software/_search'
    get_json_data = {
        "query": {
            "match": {
                "company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_ip_copyright_software请求成功')
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_ip_copyright_software请求失败，状态码：', response.status_code)
        return response.status_code


# 专利
def company_ip_patent_basic_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_ip_patent_basic/_search'
    get_json_data = {
        "query": {
            "match": {
                "company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_ip_patent_basic请求成功')
        # print(response.json())
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_ip_patent_basic请求失败，状态码：', response.status_code)
        return response.status_code


# 中标项目
def company_op_bidding_baseinfo_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_op_bidding_party/_search'
    get_json_data = {
        "query": {
            "match": {
                "company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_op_bidding_baseinfo请求成功')
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_op_bidding_baseinfo请求失败，状态码：', response.status_code)
        return response.status_code


# 企业融资信息
def company_op_finance_post(company_id):
    company_basic_change_url = 'http://47.109.144.203:9200/company_op_finance/_search'
    get_json_data = {
        "query": {
            "match": {
                "financing_company_id": company_id
            }
        }
    }
    response = requests.get(url=company_basic_change_url, json=get_json_data, timeout=10)
    if response.status_code == 200:
        print('company_op_finance请求成功')
        company_basic_change_json = response.json()
        return company_basic_change_json
    else:
        print('company_op_finance请求失败，状态码：', response.status_code)
        return response.status_code
