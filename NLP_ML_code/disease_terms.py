import numpy as np
import ast


def compute_freq(doc, exclude_set, label_to_find, dis_cui_map):
    """Computes frequency of entities of label 'label to find', excluding entities from exlude set and mapping entities to dis_cui_map

    Args:
        doc (Doc): nlp model applied on text
        exclude_set (set): entities in set to exclude
        label_to_find (str): "DISEASE" or "CHEMICAL"
        dis_cui_map (dict): Stores mapping of disease to CUI

    Returns:
        dict: Frequency of labels
    """
    out_dict = {}

    for ent in doc.ents:
        ent_upper = ent.text.upper()
        if ent.label_ == label_to_find and ent_upper not in exclude_set:
            out_dict[ent_upper] = out_dict.get(ent_upper, 0) + 1 # by default dict maintains the insertion order

            # dis to cui map
            if label_to_find == 'DISEASE' and ent_upper not in exclude_set and ent._.kb_ents:
                dis_cui_map[ent.text.upper()] = ent._.kb_ents[0][0]

    return out_dict

def add_missed_dis(doc, dis_dict, dis_to_add):
    """Add missed diseases through manual lookup

    Args:
        doc (Doc): nlp on text
        dis_dict (dict): Existing frequency dict of diseases
        dis_to_add (set): New diseases to add if found in doc

    Returns:
        dict: Modified dis_dict
    """
    dis_dict2 = {}
    for tok in doc:
        tok_upper = tok.text.upper()
        if tok_upper in dis_to_add:
            dis_dict2[tok_upper] = dis_dict2.get(tok_upper, 0) + 1


    for dis, freq in dis_dict2.items():
        if dis not in dis_dict:
            dis_dict[dis] = freq

    return dis_dict

def add_dis_che_from_nlp(df, dis_to_remove, dis_to_add, nlp):
    """Add disease and chemical frequency count columns to df

    Args:
        df (DataFrame): Input df
        dis_to_remove (set): Elements to remove if identified as diseases
        dis_to_add (set): New diseases to add if found in doc
        nlp (nlp): NLP model

    Returns:
        DataFrame: With 2 new Disease freq columns for title and description columns
        dict: Disease to CUI map 
    """

    title_dis_dicts = []
    title_che_dicts = []

    desc_dis_dicts = []
    desc_che_dicts = []

    dis_cui_map = {} # For diseases to CUI mapping

    for row in df.itertuples():

        # Extract entities from titile
        doc = nlp(row.PROJECTTITLE)

        dis_dict = compute_freq(doc, dis_to_remove, "DISEASE", dis_cui_map)
        che_dict = compute_freq(doc, set(), "CHEMICAL", dis_cui_map)

        dis_dict = add_missed_dis(doc, dis_dict, dis_to_add)

        title_che_dicts.append(che_dict)
        title_dis_dicts.append(dis_dict)



        # Extract entities from Description
        dis_dict = {}
        che_dict = {}
        if str(row.ABSTRACTDESCRIPTION) != "nan":

            doc = nlp(row.ABSTRACTDESCRIPTION)

            dis_dict = compute_freq(doc, dis_to_remove, "DISEASE", dis_cui_map)
            che_dict = compute_freq(doc, set(), "CHEMICAL", dis_cui_map)

            dis_dict = add_missed_dis(doc, dis_dict, dis_to_add)


        desc_che_dicts.append(che_dict)
        desc_dis_dicts.append(dis_dict)

    df['ABSTRACTDESCRIPTION_disease_freq'] = desc_dis_dicts
    df['PROJECTTITLE_disease_freq'] = title_dis_dicts

    df['ABSTRACTDESCRIPTION_disease_freq'] = df['ABSTRACTDESCRIPTION_disease_freq'].astype(str)
    df['PROJECTTITLE_disease_freq'] = df['PROJECTTITLE_disease_freq'].astype(str)

    return df, dis_cui_map


def gen_master_dis_set(df, man_add_dis):
    """Generates a master set for the list of all diseases identified by model

    Args:
        df (DataFrame): dataframe with disease freq counts of title and description
        man_add_dis (set): diseases to add manually in second iteration

    Returns:
        set: All diseases identified by model and manually added diseases
    """
    out_set = set()
    for row in df.itertuples():
        curr_abs_dict = ast.literal_eval(row.ABSTRACTDESCRIPTION_disease_freq)
        curr_tit_dict = ast.literal_eval(row.PROJECTTITLE_disease_freq)

        for dis in curr_abs_dict:
            out_set.add(dis)

        for dis in curr_tit_dict:
            out_set.add(dis)

    for dis in man_add_dis:
        out_set.add(dis)

    return out_set


def get_dis_manual_lookup(doc, text, master_dis_set):
    """Manual lookup in text/doc for diseases in master_dis_set. Used in second iteration

    Args:
        doc (Doc): nlp applied on text
        text (str): title or description
        master_dis_set (set): Set of all diseases identified by model and also manually added diseases

    Returns:
        dict: Updated disease freq dict
    """
    dis_dict = {}
    index_dis_dict = {}


    for dis in master_dis_set:
        if " " in dis:
            curr_freq = text.upper().count(dis)
            if curr_freq > 0:
                dis_dict[dis] = curr_freq
                index_dis_dict[dis] = text.upper().find(dis)
        else:
            for tok in doc:
                if not tok.is_stop and tok.text != 'mm' and tok.text.upper() == dis:
                    dis_dict[dis] = dis_dict.get(dis, 0) + 1
                    index_dis_dict[dis] = text.upper().find(dis)

    dis_dict = {k: v for k, v in sorted(dis_dict.items(), key=lambda item: index_dis_dict[item[0]])}

    # Substring diseases can get counted more than required
    # For more than 1 worded substring
    for dis1 in dis_dict:
        if " " in dis1:
            for dis2 in dis_dict:
                if " " in dis2 and dis2 != dis1 and dis2 in dis1:
                    dis_dict[dis2] -= dis_dict[dis1]

    dis_dict = {dis: freq for dis, freq in dis_dict.items() if freq > 0}

    # For 1 worded substring
    for dis1 in dis_dict:
        if " " in dis1:
            dis1_words = dis1.split(" ")
            for dis2 in dis_dict:
                if dis2 in dis1_words:
                    dis_dict[dis2] -= dis_dict[dis1]

    dis_dict = {dis: freq for dis, freq in dis_dict.items() if freq > 0}
    return dis_dict


def add_lkp_dis_to_df(df, nlp, master_dis_set):
    """Second iteration for identifying diseases in the records in which model wasn't able to identify

    Args:
        df (DataFrame): Input df
        nlp (nlp): model
        master_dis_set (set): Set of all diseases identified by model and also manually added diseases
    """

    # Add diseases from master dis set if not identified earlier

    title_dis_dicts = []
    abs_desc_dis_dicts = []


    for row in df.itertuples():
        # For PROJECTTITLE
        dis_dict = ast.literal_eval(row.PROJECTTITLE_disease_freq)
        curr_text = row.PROJECTTITLE

        if not dis_dict:
            doc = nlp(curr_text)
            dis_dict = get_dis_manual_lookup(doc, curr_text, master_dis_set)

        title_dis_dicts.append(dis_dict)

        # For ABSTRACTDESCRIPTION
        dis_dict = ast.literal_eval(row.ABSTRACTDESCRIPTION_disease_freq)
        curr_text = row.ABSTRACTDESCRIPTION

        if not dis_dict and row.ABSTRACTDESCRIPTION is not np.nan:
            doc = nlp(curr_text)
            dis_dict = get_dis_manual_lookup(doc, curr_text, master_dis_set)

        abs_desc_dis_dicts.append(dis_dict)

    df['PROJECTTITLE_disease_freq'] = title_dis_dicts
    df['PROJECTTITLE_disease_freq'] = df['PROJECTTITLE_disease_freq'].astype(str)

    df['ABSTRACTDESCRIPTION_disease_freq'] = abs_desc_dis_dicts
    df['ABSTRACTDESCRIPTION_disease_freq'] = df['ABSTRACTDESCRIPTION_disease_freq'].astype(str)

def add_more_dis_to_map(master_dis_set, dis_cui_map, dis_to_remove, nlp):
    """Forcefully map diseases to CUI that were missed in the first iteration

    Args:
        master_dis_set ([type]): Set of all diseases identified by model and also manually added diseases
        dis_cui_map (dict): Existing disease to CUI map
        dis_to_remove (set): Elements to remove if identified as diseases
        nlp (nlp): NLP model
    """
    # Mapping unmapped diseases to CUI with doc(disease only)
    for dis in master_dis_set:
        if dis not in dis_cui_map:
            doc = nlp(dis)
            for ent in doc.ents:
                if ent.label_ == 'DISEASE' and ent not in dis_to_remove and ent._.kb_ents:
                    dis_cui_map[ent.text] = ent._.kb_ents[0][0]

            doc = nlp(dis.capitalize())
            for ent in doc.ents:
                ent_upper = ent.text.upper()
                if ent.label_ == 'DISEASE' and ent_upper not in dis_to_remove and ent._.kb_ents:
                    dis_cui_map[ent_upper] = ent._.kb_ents[0][0]

def merge_freq_of_sim_dis(curr_dict, dis_cui_map):
    """Combine freq of more than one diseases mapped to same CUI

    Args:
        curr_dict (dict): disease dictionary
        dis_cui_map (dict): disease to CUI map

    Returns:
        dict: Combined freq dict
    """
    out_dict = {} # Output dict for new column
    temp_dict = {} # To store freqs with CUIs(if a diseases has a CUI) or diseases(if no CUI ) as keys
    cui_dis_map = {} # CUI to Disease (first occurence) map

    for dis, freq in curr_dict.items():
        if dis in dis_cui_map:
            if dis_cui_map[dis] not in temp_dict:
                cui_dis_map[dis_cui_map[dis]] = dis
                temp_dict[dis_cui_map[dis]] = freq
            else:
                temp_dict[dis_cui_map[dis]] += freq

        else:
            temp_dict[dis] = freq

    for cui_or_dis, freq in temp_dict.items():
        if cui_or_dis in curr_dict: # Key is a disease
            out_dict[cui_or_dis] = freq
        else: # Key is a CUI
            out_dict[cui_dis_map[cui_or_dis]] = freq # So convert it to first occurred disease in curr_dict

    return out_dict


def add_merge_freq_dis_to_df(df, dis_cui_map):
    """Add combined disease freq columns to df.

    Args:
        df (DataFrame): Input df
        dis_cui_map (dict): disease to CUI mapping
    """

    desc_merged_dis_dicts = []
    tit_merged_dis_dicts = []

    for row in df.itertuples():
        # Merge Desc diseases
        curr_dict = ast.literal_eval(row.ABSTRACTDESCRIPTION_disease_freq)
        if len(curr_dict) > 1:
            desc_merged_dis_dicts.append(merge_freq_of_sim_dis(curr_dict, dis_cui_map))
        else:
            desc_merged_dis_dicts.append(curr_dict)

        # Merge Title diseases
        curr_dict = ast.literal_eval(row.PROJECTTITLE_disease_freq)
        if len(curr_dict) > 1:
            tit_merged_dis_dicts.append(merge_freq_of_sim_dis(curr_dict, dis_cui_map))
        else:
            tit_merged_dis_dicts.append(curr_dict)

    df['ABSTRACTDESCRIPTION_disease_freq_merged'] = desc_merged_dis_dicts
    df['ABSTRACTDESCRIPTION_disease_freq_merged'] = df['ABSTRACTDESCRIPTION_disease_freq_merged'].astype(str)

    df['PROJECTTITLE_disease_freq_merged'] = tit_merged_dis_dicts
    df['PROJECTTITLE_disease_freq_merged'] = df['PROJECTTITLE_disease_freq_merged'].astype(str)


def expand_abbrvs(title, abs_desc, abs_desc_dis_dict, title_dis_dict, nlp):
    """Combine freq of abbrv and full form in title & description dis dict

    Args:
        title (str): title of a project
        abs_desc (str): description of a project
        abs_desc_dis_dict (dict): disease freq of description
        title_dis_dict (dict): disease freq of title
        nlp (nlp): NLP model

    Returns:
        dict: Modified dis dict of title
        dict: Modified dis dict of description
    """

    curr_abbrv_map = {}

    if len(abs_desc_dis_dict) > 1:
        doc = nlp(abs_desc)
        for abrv in doc._.abbreviations:
            full_form_upper = abrv._.long_form.text.upper()
            abrv_upper = abrv.text.upper()
            if abrv_upper in abs_desc_dis_dict and full_form_upper in abs_desc_dis_dict:
                #print(row.PROJECTID, ":", abrv_upper, ":", full_form_upper)
                curr_abbrv_map[abrv_upper] = full_form_upper
                abs_desc_dis_dict[full_form_upper] += abs_desc_dis_dict[abrv_upper]
                del abs_desc_dis_dict[abrv_upper]

    if len(title_dis_dict) > 1:
        doc = nlp(title)
        for abrv in doc._.abbreviations:
            full_form_upper = abrv._.long_form.text.upper()
            abrv_upper = abrv.text.upper()
            if abrv_upper in title_dis_dict and full_form_upper in title_dis_dict:
                #print(row.PROJECTID, ":", abrv_upper, ":", full_form_upper)
                title_dis_dict[full_form_upper] += title_dis_dict[abrv_upper]
                del title_dis_dict[abrv_upper]

    if curr_abbrv_map and title_dis_dict:
        title_dis_dict = {(curr_abbrv_map[key] if key in curr_abbrv_map else key): value for key, value in title_dis_dict.items()}

    return title_dis_dict, abs_desc_dis_dict

def add_combined_abrv_to_df(df, nlp):
    """Adds combined dis freq columns to the df. Uses abbrv and full form

    Args:
        df (DataFrame): Input df
        nlp (nlp ): NLP model
    """

    desc_expanded_dis_dicts = []
    tit_expanded_dis_dicts = []

    for row in df.itertuples():
        new_tit_dis_dict, new_desc_dis_dict = expand_abbrvs(row.PROJECTTITLE,
                                          row.ABSTRACTDESCRIPTION,
                                          ast.literal_eval(row.ABSTRACTDESCRIPTION_disease_freq_merged),
                                          ast.literal_eval(row.PROJECTTITLE_disease_freq_merged),
                                            nlp
                                         )

        desc_expanded_dis_dicts.append(new_desc_dis_dict)
        tit_expanded_dis_dicts.append(new_tit_dis_dict)

    df['ABSTRACTDESCRIPTION_disease_freq_merged'] = desc_expanded_dis_dicts
    df['ABSTRACTDESCRIPTION_disease_freq_merged'] = df['ABSTRACTDESCRIPTION_disease_freq_merged'].astype(str)

    df['PROJECTTITLE_disease_freq_merged'] = tit_expanded_dis_dicts
    df['PROJECTTITLE_disease_freq_merged'] = df['PROJECTTITLE_disease_freq_merged'].astype(str)


def get_max_freq_dis_from_dict(given_dict):
    """Get max occuring list of diseases from given dict(dis freq)

    Args:
        given_dict (dict): disease frequency count

    Returns:
        list: max occuring diseases
        dict: len of list to confidence mapping
    """
    dict_sorted = {k: v for k, v in sorted(given_dict.items(), key=lambda item: item[1], reverse=True)}
    dis_sorted = [d for d,f in dict_sorted.items()]

    ind = 0
    dis_pred = [dis_sorted[ind]]

    while len(dis_pred) != 3:
        ind += 1
        if ind >= len(dis_sorted):
            break

        if dict_sorted[dis_sorted[ind]] == dict_sorted[dis_pred[-1]]:
            dis_pred.append(dis_sorted[ind])
        else:
            break

    # Ensuring that order is same as present in given dict
    dis_pred = [dis for dis, freq in given_dict.items() if dis in dis_pred]

    conf_dict = {1: 100, 2: 90, 3: 80, 0: np.nan}

    return dis_pred, conf_dict[len(dis_pred)]


def pred_top3_dis(df, dis_cui_map):
    """Add top 3 predicted diseases to dataframe

    Args:
        df (DataFrame): Input df
        dis_cui_map (dict): diseases to CUI map
    """
    all_confs = []
    dis1s = []
    dis2s = []
    dis3s = []

    for row in df.itertuples():
        tit_dis_dict = ast.literal_eval(row.PROJECTTITLE_disease_freq_merged)
        desc_dis_dict = ast.literal_eval(row.ABSTRACTDESCRIPTION_disease_freq_merged)

        if not tit_dis_dict and not desc_dis_dict:
            dis_pred = []
            conf = np.nan

        elif tit_dis_dict and not desc_dis_dict:
            dis_pred, conf = get_max_freq_dis_from_dict(tit_dis_dict)

        elif not tit_dis_dict and desc_dis_dict:
            dis_pred, conf = get_max_freq_dis_from_dict(desc_dis_dict)

        elif desc_dis_dict and tit_dis_dict:
            desc_dis_pred, desc_conf = get_max_freq_dis_from_dict(desc_dis_dict)
            tit_dis_pred, tit_conf = get_max_freq_dis_from_dict(tit_dis_dict)

            dis_pred = []
            for tit_dis in tit_dis_pred:
                for desc_dis in desc_dis_pred:
                    if tit_dis == desc_dis or \
                        (tit_dis in dis_cui_map and desc_dis in dis_cui_map and dis_cui_map[tit_dis] == dis_cui_map[desc_dis]):
                        dis_pred.append(tit_dis)

            if dis_pred:
                conf = 100
            else:
                dis_pred, conf = tit_dis_pred, tit_conf

        while len(dis_pred) != 3:
            dis_pred.append(np.nan)

        dis1, dis2, dis3 = dis_pred

        dis1s.append(dis1)
        dis2s.append(dis2)
        dis3s.append(dis3)
        all_confs.append(conf)

    df['predicted_disease_1'] = dis1s
    df['predicted_disease_2'] = dis2s
    df['predicted_disease_3'] = dis3s
    df['prediction_confidence'] = all_confs
