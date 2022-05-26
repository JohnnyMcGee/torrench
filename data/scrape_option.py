from bs4 import ResultSet

def scrape_option(row: ResultSet) -> dict:
    option = {}
    det_link = row.find('a', class_="detLink")
    option["name"] = det_link.string if det_link else ""
    option["link"] = det_link["href"] if det_link else ""
    det_desc = row.find('font', class_="detDesc")
    if det_desc:
        option["uploader"] = det_desc.a.string if det_desc.a else det_desc.i.string
        desc_text = det_desc.get_text().replace(',', "").split(' ')
        option["date"] = desc_text[1]
        option["size"] = desc_text[3]
    else:
        option["uploader"] = option["date"] = option["size"] = ""
    
    comment: str
    comments = row.find(
        'img', {'src': '/static/img/icon_comment.gif'})
    if comments != None:
        comment = comments['alt'].split(
            " ")[-2]  # Total number of comments
    else:
        comment = "0"
    option["comment"] = comment
    option["category"] = row.find('td', class_="vertTh").find_all('a')[0].string
    option["sub_category"] = row.find('td', class_="vertTh").find_all('a')[1].string
    option["seeds"] = row.find_all('td', align="right")[0].string
    option["leeches"] = row.find_all('td', align="right")[1].string

    return option