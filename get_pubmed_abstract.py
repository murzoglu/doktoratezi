import urllib.request
import json
import urllib.parse
import xml.etree.ElementTree as ET

title = "Parenting and Psychological Health in Youth with Type 1 Diabetes: Systematic Review"
term = urllib.parse.quote(title)
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={term}&retmode=json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    id_list = data['esearchresult']['idlist']
    if id_list:
        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={id_list[0]}&retmode=xml"
        req3 = urllib.request.Request(fetch_url)
        with urllib.request.urlopen(req3) as res3:
            xml_data = res3.read().decode()
            root = ET.fromstring(xml_data)
            for abstract in root.findall('.//AbstractText'):
                print(abstract.text)
