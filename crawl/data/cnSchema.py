import json
import os 
import pandas as pd 
opj = os.path.join

domain = "http://openkg.cn/dataset/genshinimpact-zju/"

data_path = 'C:\\Users\\MSI\\Desktop\\211011知识图谱课设\\genshin_impact_knowledge_graph-main\\data\\GenshinImpact\\'
properties_dir = data_path+"properties"

characters_path = opj(properties_dir, "characters.csv")
countries_path = opj(properties_dir, "countries.csv")
element_path = opj(properties_dir, "element.csv")
materials_path = opj(properties_dir, "materials.csv")
weapons_path = opj(properties_dir, "weapons.csv")
weapontypes_path = opj(properties_dir, "weapontypes.csv")

relations_dir = data_path+"relations"

character2country_path = opj(relations_dir, "character2country.csv")
character2element_path = opj(relations_dir, "character2element.csv")
character2material_path = opj(relations_dir, "character2material.csv")
character2weapontype_path = opj(relations_dir, "character2weapontype.csv")
element2element_path = opj(relations_dir, "element2element.csv")
material2material_path = opj(relations_dir, "material2material.csv")
weapon2material_path = opj(relations_dir, "weapon2material.csv")
weapon2weapontype_path = opj(relations_dir, "weapon2weapontype.csv")


all_data_jsonld = dict()
all_data_jsonld["context"] = {"@vocab": "http://cnschema.org/"}
all_data_jsonld["graph"] = []

def get_value(value):
    value = str(value).strip()
    if value == 'nan' or '无' in value or value == 'N/A':
        value = 'None'
    return value


# - 人物节点和与人物有关的关系
characters = pd.read_csv(characters_path)
character2country = pd.read_csv(character2country_path)
character2element = pd.read_csv(character2element_path)
character2material = pd.read_csv(character2material_path)
character2weapontype = pd.read_csv(character2weapontype_path)

characters.columns = [col.strip() for col in characters.columns]
for row in characters.itertuples(): 
    d = dict()
    d["@id"] = domain + get_value(row.CharacterID)
    d["@type"] = get_value(row.LABEL)
    d["id"] = get_value(row.CharacterID)
    d["name"] = get_value(row.name)
    d["title"] = get_value(row.title)   
    d["gender"] = get_value(row.gender)
    d["rarity"] = get_value(row.rarity) 
    d["pool"] = get_value(row.pool) 
    d["constellation"] = get_value(row.constellation) 
    d["specialCuisine"] = get_value(row.specialCuisine) 
    d["equipDate"] = get_value(row.equipDate)  
    d["tag"] = get_value(row.tag)
    d["intro"] = get_value(row.intro)
    d["relationships"] = {}
    affiliate_list = [
          {
              "@id": domain + cid.strip(),
              "@type": "Country"
          } for cid in character2country["END_ID"][character2country["START_ID"] == row.CharacterID.strip()]  
        ]
    if len(affiliate_list) > 0: 
        d["relationships"]["affiliate"] = affiliate_list
    
    godsEye_list = [
        {
            "@id": domain + eid.strip(),
            "@type": "Element"
        }
        for eid in character2element["END_ID"][character2element["START_ID"] == row.CharacterID.strip()]
    ]
    if len(godsEye_list)> 0: 
        d["relationships"]["godsEye"] = godsEye_list 
    
    require_list = [
        {
            "@id": domain + mid.strip(),
            "@type": "Material"
        }
        for mid in character2material["END_ID"][character2material["START_ID"] == row.CharacterID.strip()]
    ]
    if len(require_list) > 0:
        d["relationships"]["require"] = require_list

    all_data_jsonld["graph"].append(d)


# - 国家节点
countries = pd.read_csv(countries_path)
countries.columns = [col.strip() for col in countries.columns]
for row in countries.itertuples():
    d = dict()
    d["@id"] = domain + get_value(row.CountryID) 
    d["@type"] = get_value(row.LABEL)
    d["id"] = get_value(row.CountryID)
    d["name"] = get_value(row.name)
    d["eng_name"] = get_value(row.eng_name) 
    d["army"] = get_value(row.army) 
    d["desc"] = get_value(row.desc)
    d["background"] = get_value(row.background)
    
    all_data_jsonld["graph"].append(d)

# - 武器类型节点
weapontypes = pd.read_csv(weapontypes_path)
weapontypes.columns = [col.strip() for col in weapontypes.columns]
for row in weapontypes.itertuples():
    d = dict()
    d["@id"] = domain + row.WeapontypeID.strip()
    d["@type"] = row.LABEL.strip() 
    d["id"] = get_value(row.WeapontypeID)
    d["typeName"] = get_value(row.typeName)
    d["range"] = get_value(row.range) 
    d["frequency"] = get_value(row.frequency) 
    d["accumulate"] = get_value(row.accumulate)
    
    all_data_jsonld["graph"].append(d)


# - 元素节点
element = pd.read_csv(element_path)
element2element = pd.read_csv(element2element_path)

element.columns = [col.strip() for col in element.columns]
for row in element.itertuples():
    d = dict() 
    d["@id"] = domain + get_value(row.ElementID) 
    d["@type"] = get_value(row.LABEL)
    d["id"] = get_value(row.ElementID)
    d["name"] = get_value(row.name)
    d["reaction"] = get_value(row.reaction)
    d["resonance"] = get_value(row.resonance)

    d["relationships"] = {}
    react_list = [
        {
            "@id": domain + eid.strip(),
            "@type": "Element"
        }
        for eid in element2element["END_ID"][element2element["START_ID"] == row.ElementID.strip()]
    ]
    if len(react_list) > 0:
        d["relationships"]["react"] = react_list
        
    all_data_jsonld["graph"].append(d)

# - 武器节点   

weapons = pd.read_csv(weapons_path)
weapon2weapontype = pd.read_csv(weapon2weapontype_path)
weapon2material = pd.read_csv(weapon2material_path)

weapons.columns = [col.strip() for col in weapons.columns]
for row in weapons.itertuples():
    d = dict()
    d["@id"] = domain + get_value(row.WeaponID)
    d["@type"] = get_value(row.LABEL)
    d["id"] = get_value(row.WeaponID)
    d["name"] = get_value(row.name)
    d["rarity"] = get_value(row.rarity)
    d["baseProperty1"] = get_value(row.baseProperty1)
    d["baseProperty1"] = get_value(row.baseProperty2)
    d["intro"] = get_value(row.intro)
    d["skillname"] = get_value(row.skillname)
    d["skillDesc"] = get_value(row.skillDesc)
    d["obtain"] = get_value(row.obtain)
    d["tag"] = get_value(row.tag)
    
    d["relationships"] = {}
    belong_list = [
        {
            "@id": domain + wtid.strip(),
            "@type": "WeaponType"
        }
        for wtid in weapon2weapontype["END_ID"][weapon2weapontype["START_ID"] == row.WeaponID.strip()]
    ]
    if len(belong_list)> 0:
        d["relationships"]["belong"] = belong_list
    
    require_list = [
        {
            "@id": domain + mid.strip(),
            "@type": "Material"
        }
        for mid in weapon2material["END_ID"][weapon2material["START_ID"] == row.WeaponID.strip()]
    ]
    if len(require_list)> 0:
        d["relationships"]["require"] = require_list

    all_data_jsonld["graph"].append(d)

#- 材料节点
materials = pd.read_csv(materials_path)
material2material = pd.read_csv(material2material_path)
materials.columns = [col.strip() for col in materials.columns]
for row in materials.itertuples():
    d = dict()
    d["@id"] = domain + get_value(row.MaterialID)
    d["@type"] = get_value(row.LABEL)
    d["id"] = get_value(row.MaterialID)
    d["name"] = get_value(row.name)
    d["rarity"] = get_value(row.rarity)
    d["type"] = get_value(row.type)
    d["source"] = get_value(row.source)
    d["intro"] = get_value(row.intro)
    d["relatedFurnish"] = get_value(row.relatedFurnish)
    d["relatedFood"] = get_value(row.relatedFood)
    d["relationships"] = {}

    similar_list = [
        {
            "@id": domain + mid.strip(),
            "@type": "Material"
        }
        for mid in material2material["END_ID"][material2material["START_ID"] == row.MaterialID.strip()]
    ]
    if len(similar_list)> 0:
        d["relationships"]["similar"] = similar_list

    all_data_jsonld["graph"].append(d)




result_json = "genshinImpact.jsonld"
with open(result_json, "w", encoding='utf-8') as f: 
    json.dump(all_data_jsonld, f, ensure_ascii=False,indent=4)
