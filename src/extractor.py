import re

def extract_title(lines: list):
    '''
    Extracts title from the second line of the input, the input is PDF splitted by \n.
    '''
    if len(lines) > 1:
        try:
            return lines[1]
        except ValueError:
            print("Second line is not a number.")
    return ""

def extract_rules(lines: list, rulesstart_sign: str, rulesend_sign: str):
    '''
    Extracts rules between specific markers in the input.
    '''
    start_index = next((i for i, l in enumerate(lines) if rulesstart_sign in l), -1)
    end_index = next((i for i, l in enumerate(lines) if rulesend_sign in l), -1)

    # try:
    #     start_index = lines.index(rulesstart_sign) # match with whole line, to see begining matching, check extract_codes
    #     end_index = lines.index(rulesend_sign)
    # except ValueError:
    #     return {}

    if start_index == -1 and end_index == -1:
        return {}

    section = lines[start_index + 1: end_index]
    rules = {
        "rule_id": "1", "rule_text": "Coverage Criteria", "operator": "AND", "rules": []
        }
    level_dic = {1: 0, 2: 0, 3: 0} # Use of dic to save memory
    last_matched = None

    for line in section:
        matches = re.match(r'^([IVX]+|[A-Z]+|\d+)\.\s+(.*)', line)

        if matches:
            level = matches.group(1)  # Extract level (Roman, number, or letter)
            content = matches.group(2)  # Extract content
            l_id = 0
            rule_id = ""
            operator = None
            current_level = rules["rules"]

            # IDs
            if re.match(r'^[IVX]', level):
                l_id = 1
                opeartor = "OR"
                l1_rule_id = level_dic.get(1) + 1
                rule_id = "1." + str(l1_rule_id)
                level_dic.update({1: l1_rule_id, 2: 0, 3: 0})
            elif re.match(r'^[A-Z]', level):
                l_id = 2
                operator = "OR"
                l2_rule_id = level_dic.get(2) + 1
                rule_id = "1." + str(level_dic.get(1)) + "." + str(l2_rule_id)
                level_dic.update({2: l2_rule_id,3: 0})
            elif re.match(r'^\d', level):
                l_id = 3
                l3_rule_id = level_dic.get(3) + 1
                rule_id = "1." + str(level_dic.get(1)) + "." + str(level_dic.get(2)) + "." + str(l3_rule_id)
                level_dic.update({3: l3_rule_id})
            else:
                print("Rule Extract Error: Cannot identify the sign")

            content = re.sub(r'\s+and$|\s+or$', '', content)
            obj = {"rule_id": rule_id, "rule_text": content, "operator": opeartor, "rules": None}
            last_matched = obj

            if l_id == 2:
                if rules["rules"][level_dic.get(1)-1]["rules"]:
                    current_level = rules["rules"][level_dic.get(1)-1]["rules"]
                else:
                    current_level = []
                    rules["rules"][level_dic.get(1)-1]["rules"] = [current_level]
            elif l_id == 3:
                print(rules["rules"][level_dic.get(1)-1])
                if rules["rules"][level_dic.get(1)-1]["rules"][level_dic.get(2)-1]["rules"]:
                    current_level = rules["rules"][level_dic.get(1)-1]["rules"][level_dic.get(2)-1]["rules"]
                else:
                    current_level = []
                    rules["rules"][level_dic.get(1)-1]["rules"][level_dic.get(2)-1]["rules"] = current_level
            current_level.append(obj)
        else:
            if last_matched:
                line = re.sub(r'\s+and$|\s+or$', '', line)
                last_matched["rule_text"] += " " + line

    return rules

def extract_codes(lines: list, codesstart_sign: str, codesend_sign: str):
    '''
    Extracts code from the fraction between the first existed Code Number Description and Date of Origin of input, the input is pdf tect split by [\n].
    '''
    try:
        start_index = lines.index(codesstart_sign)
        end_index = next((i for i, line in enumerate(lines) if line.startswith(codesend_sign)), None) # special case, beginning
    except ValueError:
        return {}

    if start_index == -1 and end_index == -1:
        return {}

    section = lines[start_index+1: end_index]
    codes = {
        "cpt": None, "icd10": None, "hcpcs": None
        }
    current_group = None
    current_code_number_a = None

    for line in section:
        # Match lines starting with Roman numerals or numbers (e.g., I., II., A., 1.)
        matches_1 = re.match(r'^(CPT|ICD10|HCPCS)+\s+([\dA-Z]{5})+\s+(.*)', line)

        if matches_1:
            group = matches_1.group(1)
            number = matches_1.group(2)
            des = matches_1.group(3)

            # As
            if re.match(r'^CPT', group):
                current_group = "cpt"
            elif re.match(r'^ICD10', group):
                current_group = "icd10"
            elif re.match(r'^HCPCS', group):
                current_group = "hcpcs"
            else:
                print("Rule Extract Error: Cannot identify the sign")

            codes[current_group] = number

    return codes
