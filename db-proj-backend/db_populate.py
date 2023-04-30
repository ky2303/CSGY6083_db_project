# fills db with 'enterprise-attack.json'
# from https://github.com/mitre/cti/blob/master/enterprise-attack/enterprise-attack.json
# standards are from NIST and ISO
import json
import requests
import sqlite3
from models import INTEL_ITEMS, GROUPS, MITIGATIONS, TACTICS, TECHNIQUES, SOFTWARE, STANDARDS

sqlite_file_name = "intel_database.db"
try:
    conn = sqlite3.connect(sqlite_file_name)
except Exception as e:
    print(e)
    exit()

host = "localhost"
local = True
if not local: host = ''

with open("enterprise-attack.json") as _f:
    groups = 0
    mitigations = 0
    tactics = 0
    techniques = 0
    software = 0
    ent_attack = json.load(_f)
    for _object in ent_attack['objects']:
        # print(_object['external_references'][0])
        try:
            ext_refs = _object['external_references'][0]['url']
        except:
            ext_refs = 0

        if ext_refs:

            if "https://attack.mitre.org/groups/" in ext_refs:
                # POST to /groups/
                print(f"[+] group found: {_object['name']}")
                try:
                    description = _object['description']
                except:
                    description = ''                    
                grp = {
                    'id': groups,
                    'name': _object['name'],
                    'url': _object['external_references'][0]['url'],
                    'associated_groups': '',
                    'description': description,
                    'techniques_used_ids': '',
                    'software': '',
                }
                # # requests
                # r = requests.post(f'http://{host}:8000/groups/', json=grp)
                # print(r.json())
                # sql
                sql = ''' INSERT INTO groups(id, name, url, associated_groups, description, techniques_used_ids, software) 
                            VALUES (:id, :name, :url, :associated_groups, :description, :techniques_used_ids, :software)'''
                cur = conn.cursor()
                cur.execute(sql, grp)
                conn.commit()
                groups = groups + 1
                # print(_object['external_references'][0]['url'])
      
            if "https://attack.mitre.org/mitigations/" in ext_refs:
                # POST to /mitigations/
                print(f"[+] mitigation found: {_object['name']}")
                try:
                    description = _object['description']
                except:
                    description = ''      
                mit = {
                    'id': mitigations,
                    'name': _object['name'],
                    'description': description,
                    'url': _object['external_references'][0]['url'],
                    'policy_or_control': 0,
                    'TECHNIQUES_id': 0,
                    'STANDARDS_id': 0
                }
                # print(mit)
                # r = requests.post(f'http://{host}:8000/mitigations/', json=mit)
                # print(r.json())
                sql = ''' INSERT INTO mitigations (id, name, description, url, policy_or_control, TECHNIQUES_id, STANDARDS_id)
                            VALUES (:id, :name, :description, :url, :policy_or_control, :TECHNIQUES_id, :STANDARDS_id)'''
                cur = conn.cursor()
                cur.execute(sql, mit)
                conn.commit()
                mitigations = mitigations + 1

            if "https://attack.mitre.org/tactics/" in ext_refs:
                # POST to /tactics/
                print(f"[+] tactic found: {_object['name']}")
                try:
                    description = _object['description']
                except:
                    description = ''      
                tac = {
                    'id': tactics,
                    'name': _object['name'],
                    'description': description,
                    'url': _object['external_references'][0]['url'],
                }
                # print(tac)
                # r = requests.post(f'http://{host}:8000/tactics/', json=tac)
                # print(r.json())
                sql = ''' INSERT INTO tactics (id, name, description, url)
                            VALUES (:id, :name, :description, :url)'''
                cur = conn.cursor()
                cur.execute(sql, tac)
                conn.commit()
                tactics = tactics + 1

            if "https://attack.mitre.org/techniques/" in ext_refs:
                # POST to /techniques/
                print(f"[+] technique found: {_object['name']}")
                try:
                    description = _object['description']
                except:
                    description = ''      
                tec = {
                    'id': techniques,
                    'name': _object['name'],
                    'description': description,
                    'url': _object['external_references'][0]['url'],
                    'associated_tactic': 0,
                    'TACTICS_id': 0,
                    'is_child': 0,
                    'mitigation_control': '',
                    'mitigation_policy': '',
                }
                try:
                    # print(tec)
                    # r = requests.post(f'http://{host}:8000/techniques/', json=tec)
                    # print(r.json())
                    sql = ''' INSERT INTO techniques (id, name, description, url, associated_tactic, TACTICS_id, is_child, mitigation_control, mitigation_policy)
                            VALUES (:id, :name, :description, :url, :associated_tactic, :TACTICS_id, :is_child, :mitigation_control, :mitigation_policy)'''
                    cur = conn.cursor()
                    cur.execute(sql, tec)
                    conn.commit()
                    techniques = techniques + 1
                except:
                    print(f"\tadding technique failed: {_object['name']}")

            if "https://attack.mitre.org/software/" in ext_refs:
                # POST to /tactics/
                print(f"[+] software found: {_object['name']}")
                try:
                    description = _object['description']
                except:
                    description = ''      
                sof = {
                    'id': software,
                    'name': _object['name'],
                    'description': description,
                    'url': _object['external_references'][0]['url'],
                    'related_framework': '',
                    'TECHNIQUES_id': 0
                }
                # print(sof)
                # r = requests.post(f'http://{host}:8000/software/', json=sof)
                # print(r.json())
                sql = ''' INSERT INTO software (id, name, description, url, related_framework, TECHNIQUES_id)
                            VALUES (:id, :name, :description, :url, :related_framework, :TECHNIQUES_id)'''
                cur = conn.cursor()
                cur.execute(sql, sof)
                conn.commit()
                software = software + 1


# standards
print("Standards:")         
std = {
    'id': 0,
    'name': 'ISO/IEC 27001',
    'description': "ISO/IEC 27001 is the world's best-known standard for information security management systems (ISMS). It defines requirements an ISMS must meet. The ISO/IEC 27001 standard provides companies of any size and from all sectors of activity with guidance for establishing, implementing, maintaining and continually improving an information security management system. Conformity with ISO/IEC 27001 means that an organization or business has put in place a system to manage risks related to the security of data owned or handled by the company, and that this system respects all the best practices and principles enshrined in this International Standard.",
    'regulatory_body': 'ISO',
    'url': 'https://www.iso.org/standard/27001',
}
# print(std)
# r = requests.post(f'http://{host}:8000/standards/', json=std)
# print(r.json())
sql = ''' INSERT INTO standards (id, name, description, url, regulatory_body)
                            VALUES (:id, :name, :description, :url, :regulatory_body)'''
cur = conn.cursor()
cur.execute(sql, std)
conn.commit()

std = {
    'id': 1,
    'name': 'NIST CYBERSECURITY FRAMEWORK',
    'description': "The Framework is based on existing standards, guidelines, and practices for organizations to better manage and reduce cybersecurity risk. In addition, it was designed to foster risk and cybersecurity management communications amongst both internal and external organizational stakeholders.",
    'regulatory_body': 'NIST',
    'url': 'https://www.nist.gov/cyberframework',
}
# print(std)
# r = requests.post(f'http://{host}:8000/standards/', json=std)
# print(r.json())
sql = ''' INSERT INTO standards (id, name, description, url, regulatory_body)
                            VALUES (:id, :name, :description, :url, :regulatory_body)'''
cur = conn.cursor()
cur.execute(sql, std)
conn.commit()
