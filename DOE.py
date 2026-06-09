# -*- coding: utf-8 -*-

"""
林大神的實驗設計, DOE 的基本物件
Version 0.1 2026/05/09 我一定是瘋了…哈哈哈…
"""

import streamlit as st
import numpy as np
import pandas as pd
import string, itertools, random

valid_vars = string.ascii_uppercase.replace("I", "")
FAC_EXP_NUM_DIC={2:4, 3:8, 4:8, 5:16, 6:16, 7:16, 8:16, 9:32, 10:32, 11:32, 12:32, 13:32, 14:32, 15:32}
FAC_BASE_NUM_DIC = {2:2, 3:3, 4:3, 5:4, 6:4, 7:4, 8:4, 9:5, 10:5, 11:5, 12:5, 13:5, 14:5, 15:5}

def get_var_name(var_id):
    """把 1,2,3 變成 ABC
    args:
        var_id: integer 如 2,3,4
    returns:
        out: 會回覆 B, C, D
    on error returns:
        None
    """
    out = valid_vars[var_id % len(valid_vars)]
    if var_id >= len(valid_vars) * 2:
        out += '"'
    elif var_id >= len(valid_vars):
        out += "'"
    return out

def get_var_id(var_name):
    """把 ABC 變成 123
    args:
        var_name: strng 如 A,B,C
    returns:
        out: 會回覆 1,2,3
    on error returns:
        None
    """
    return valid_vars.index(var_name)

def get_factor_names(n_factors):
    """產生系統 factor names 用小寫的 x1,x2,x3,x4,...
    args:
        n_factors: integer 實驗的因子數
    returns:
        factors_list: a list of variables, ["x1", "x2", "x3"]
    on error returns:
        None, if n_factors <2
    """
    if n_factors >= 2:
        return ["x" + str(i+1) for i in range(n_factors)]
    else:
        return None

def get_response_names(n_responses):
    """產生系統 response names 用小寫的 y1,y2,y3,y4,...
    args:
        n_responses: integer 實驗的 y 數
    returns:
        response_list: a list of response, ["y1", "y2", "y3"]
    on error returns:
        response 可以為 1
    """
    return ['y' + str(i+1) for i in range(n_responses)]

def build_exp_orders(n_experiments):
    """產生系統 standard order and shuffled order
    args:
        n_experiments: integer 實驗的實驗數 (有加過中值的)
    returns: std_order, run_order
        std_order: a list of numbers, [1,2,3,4,5,6,7,8,9,...]
        run_order: a list of numbers, being shuffled [4,2,3,1,6,5,7,8,9,...]
    on error returns:
        None, if n_factors <2
    """
    std_order = []
    run_order = []
    for i in range(n_experiments):
        std_order.append(i+1)
        run_order.append(i+1)
    random.shuffle(run_order)
    return std_order, run_order

def build_full_factorial(n_factors):
    """建構全因子實驗
    args:
        n_factors: integer 實驗的因子數
    returns:
        e_design: pandas.DataFrame object
    on error returns:
        None
    """
    factor_data = []
    for run in itertools.product([-1, 1], repeat=n_factors):
        factor_data.append(list(run))
    return factor_data

def build_mid_factorial(n_factors):
    return [0 for n in range(n_factors)]

def build_factorial(n_factors):
    """建構一個基於多個因子和最小運行次數的兩水平設計+中值
    最多可運行 15 個因子的全兩水平析因設計。本設計允許估計所有主效應和雙因子交互效應。
    args:
        n_factors: integer 實驗的因子數
    returns:
        e_design: pandas.DataFrame object
    on error returns:
        None
    """
    
    EXP_GEN_DIC = {
        3: {4: ["C=AB"]},
        4: {8: ["D=ABC"]},
        5: {8: ["D=AB", "E=AC"], 16: ["E=ABCD"]},
        6: {8: ["D=AB", "E=AC", "F=BC"], 16: ["E=ABC", "F=BCD"], 32: ["F=ABCDE"]},
        7: {8: ["D=AB", "E=AC", "F=BC", "G=ABC"], 16: ["E=ABC", "F=BCD", "G=ACD"], 32: ["F=ABCD", "G=ABCE"],64: ["G=ABCDEF"]},
        8: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD"], 32: ["F=ABC", "G=ABD", "H=BCDE"], 64: ["G=ABCD", "H=ABEF"], 128: ["H=ABCDEFG"]},
        9: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD"], 32: ["F=ABCD", "G=ABCE", "H=ABDE", "J=ACDE"], 64: ["G=ABCD", "H=ACEF", "J=CDEF"], 128: ["H=ABCDE", "J=ABCFG"], 256: ["J=ABCDEFGH"]}, # noqa
        10: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD", "K=AB"], 32: ["F=ABCD", "G=ABCE", "H=ABDE", "J=ACDE", "K=BCDE"], 64: ["G=ABCD", "H=ABCE", "J=ADEF", "K=BDEF"], 128: ["H=ABCG", "J=BCDE", "K=ACDF"], 256: ["J=ABCDEF", "K=ABCDGH"], 512: ["K=ABCDEFGHJ"]}, # noqa
        11: {16: ["E=ABC", "F=BCD", "G=ACD", "H=ABD", "J=ABCD", "K=AB", "L=AC"], 32: ["F=ABC", "G=BCD", "H=CDE", "J=ACD", "K=ADE", "L=BDE"], 64: ["G=ABCD", "H=ABCE", "J=ABDE", "K=ACDEF", "L=BCDEF"], 128: ["H=ABCG", "J=BCDE", "K=ACDF", "L=ABCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH"], 512: ["K=ABCDEF", "L=ABCGHJ"]}, # noqa
        12: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE"], 64: ["G=ABC", "H=ABD", "J=ACDE", "K=ACDF", "L=ABEF", "M=BCDEF"], 128: ["H=ABC", "J=ADEF", "K=BDEG", "L=CDFG", "M=ABCEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH", "M=ACEGH"], 512: ["K=ABCDEF", "L=ABCDGH", "M=ABEFGJ"]}, # noqa
        13: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ACF", "M=ADEF", "N=ABCDEF"], 128: ["H=ABC", "J=ABDE", "K=ABDF", "L=ACDG", "M=AEFG", "N=ABCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDFH", "M=ACEGH", "N=ADEFGH"], 512: ["K=ABCDEF", "L=ABCDGH", "M=ABEFGJ", "N=ACEGHJ"]}, # noqa
        14: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC", "O=BD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE", "O=BDE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ABF", "M=ACDF", "N=ACEF", "O=ADEF"], 128: ["H=ABC", "J=ABDE", "K=ABDF", "L=ACEF", "M=ACDG", "N=ABEFG", "O=BCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDEFG", "M=ABDFH", "N=ADEGH", "O=ACEFGH"], 512: ["K=ABCDE", "L=ABFGH", "M=CDFGJ", "N=ACEFHJ", "O=BDEGHJ"]}, # noqa
        15: {16: ["E=ABC", "F=ABD", "G=ACD", "H=BCD", "J=ABCD", "K=AB", "L=AC", "M=AD", "N=BC", "O=BD", "P=CD"], 32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=ADE", "N=BCE", "O=BDE", "P=CDE"], 64: ["G=ABC", "H=ABD", "J=ABE", "K=ACDE", "L=ABF", "M=ACDF", "N=ACEF", "O=ADEF", "P=ABCDEF"], 128: ["H=ABC", "J=ADE", "K=BDF", "L=ACEF", "M=CDG", "N=BCEG", "O=EFG", "P=ABCDEFG"], 256: ["J=ABCD", "K=ABEF", "L=ACEG", "M=BDFG", "N=ABDEH", "O=ACDFH", "P=BEGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACDFJ", "O=AEGHJ", "P=ABCDEFGHJ"]}, # noqa
        16: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABE", "L=ACE", "M=BCE", "N=ADE", "O=BDE", "P=CDE", "Q=ABCDE"], 64: ["G=ABCD", "H=ABCE", "J=ABDE", "K=ACDE", "L=BCDE", "M=ABCF", "N=ABDF", "O=ACDF", "P=BCDF", "Q=ABCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ACDG", "N=BCEG", "O=ABCFG", "P=ABDEFG", "Q=BCDEFG"], 256: ["J=ABCDE", "K=ABCFG", "L=ABDEFG", "M=ABCDFH", "N=CDEFH", "O=ACDEGH", "P=AEFGH", "Q=BCEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ"]}, # noqa
        17: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ADE", "P=BDE", "Q=CDE", "R=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=ABF", "O=ACF", "P=ADEF", "Q=BDEF", "R=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ADEF", "N=ACDG", "O=ABEG", "P=ADEG", "Q=ABFG", "R=BCDEFG"], 256: ["J=ABCD", "K=ABEF", "L=ACEG", "M=BDFG", "N=BCEH", "O=ABDFH", "P=ABDEGH", "Q=ACDFGH", "R=ABCEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ", "R=ABDEGHJ"]}, # noqa
        18: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=CDE", "S=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=ADEF", "R=BDEF", "S=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDF", "L=ACEF", "M=ADEF", "N=ACDG", "O=ABEG", "P=ADEG", "Q=ABFG", "R=ACFG", "S=BCDEFG"], 256: ["J=ABCD", "K=ABCE", "L=ADEF", "M=ADEG", "N=ABFG", "O=ACFG", "P=BCDEH", "Q=BDFH", "R=CEGH", "S=BCFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ACDFJ", "P=BCEGJ", "Q=ABCEFHJ", "R=ABDEGHJ", "S=BCDFGHJ"]}, # noqa
        19: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=BCF", "R=ADEF", "S=BDEF", "T=CDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ABCF", "M=ADEF", "N=BDEF", "O=ACDG", "P=ACEG", "Q=CDEG", "R=ABFG", "S=ADFG", "T=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEG", "M=ABDEFG", "N=ACDEFG", "O=BCEFH", "P=ADEGH", "Q=BCDEGH", "R=ABCFGH", "S=BDFGH", "T=CDFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ"]}, # noqa
        20: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ACDE", "U=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ABF", "P=ACF", "Q=BCF", "R=ADEF", "S=BDEF", "T=CDEF", "U=ABCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ABCF", "M=ADEF", "N=BDEF", "O=ACDG", "P=ACEG", "Q=CDEG", "R=ABFG", "S=ADFG", "T=AEFG", "U=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEF", "M=ABCDG", "N=ABEFG", "O=ACDEFG", "P=ABDEH", "Q=ACDEFH", "R=ABCEGH", "S=BDEGH", "T=ABDFGH", "U=BCDEFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ", "U=CDFGHJ"]}, # noqa
        21: {32: ["F=ABC", "G=ABD", "H=ACD", "J=BCD", "K=ABCD", "L=ABE", "M=ACE", "N=BCE", "O=ABCE", "P=ADE", "Q=BDE", "R=ABDE", "S=CDE", "T=ACDE", "U=BCDE", "V=ABCDE"], 64: ["G=ABC", "H=ABD", "J=ACD", "K=BCD", "L=ABE", "M=ACE", "N=BCE", "O=ADE", "P=ABF", "Q=ADF", "R=BDF", "S=AEF", "T=CEF", "U=DEF", "V=BCDEF"], 128: ["H=ABCD", "J=ABCE", "K=ABDE", "L=ACDE", "M=ABCF", "N=ABDF", "O=ACEF", "P=ADEF", "Q=ACDG", "R=ABEG", "S=BCDEG", "T=CDFG", "U=BEFG", "V=ABCDEFG"], 256: ["J=ABCDE", "K=ABCDF", "L=ABCEF", "M=ABDEF", "N=ABCDG", "O=ABEFG", "P=ACDEFG", "Q=ACDEFH", "R=BCDEFH", "S=BCEGH", "T=ABDEGH", "U=ABCFGH", "V=BDFGH"], 512: ["K=ABCDE", "L=ABCFG", "M=ABDFH", "N=ACEGH", "O=ADEFGH", "P=BCEFJ", "Q=ABDEGJ", "R=BDFGJ", "S=ACFHJ", "T=BCEGHJ", "U=CDFGHJ", "V=DEHJ"]} # noqa
    }
    
    # 計算「基礎因子數」, 查表 
    base_factor = FAC_BASE_NUM_DIC[n_factors]
    
    # 產生基礎實驗設計
    factor_df = pd.DataFrame(build_full_factorial(base_factor), columns=get_factor_names(base_factor))
    
    if n_factors == base_factor:
        # 加中值
        factor_df.loc[len(factor_df)] = build_mid_factorial(n_factors)
        return factor_df
    
    for gen in EXP_GEN_DIC[n_factors][FAC_EXP_NUM_DIC[n_factors]]:
        lhs, rhs = gen.split('=')
        lhs = 'x' + str(get_var_id(lhs) + 1)  #把 ABCDE 變成 x1,2,3,4,5
        cols = []
        for var in rhs:
            cols.append(get_var_id(var))
            
        generator_column = factor_df.iloc[:, cols].product(axis=1).rename(lhs)
        factor_df = factor_df.join(generator_column)

    # 加中值
    factor_df.loc[len(factor_df)] = build_mid_factorial(n_factors)

    return factor_df

def check_factor(n_factors, factor_configs):
    """寫一個 check factor 和 設定的函數，確認因子重覆名稱、大小設置錯誤
    args:
        n_factors: integer 實驗的因子數
        factor_configs: list of dictionary 儲存每個因子的 "Name", "Max", "Min", 像這樣：
        [{'Name': '因子_1', 'Min': -1.0, 'Max': 1.0},
        {'Name': '因子_2', 'Min': -1.0, 'Max': 1.0},
    returns:
        error_messages, f_names, f_mins, f_maxs
        error_messages: str 問題的說明
        f_names: list of str, 每個因子的名字
        f_mins: list of num, 每個因子的小值
        f_maxs: list of num, 每個因子的大值
    on error returns:
        error_messages, None, None, None
    """
    f_names = []
    f_mins = []
    f_maxs = []
    n_error = 0
    error_messages = ''
    if len(factor_configs) != n_factors:
        error_messages += '因子數目與 factor_configs 數目不一致, 無法繼續查核'
        return error_messages, None, None, None
        
    for factor in factor_configs:
        if factor['Name'] in f_names:
            new_name = factor['Name'] + '_' + str(n_error)
            error_messages += '因子名稱 ' + factor['Name'] + ' 有重覆到了哦! 我改成： ' + new_name + '\n\n'
            f_names.append(new_name)
            n_error += 1
        else:
            f_names.append(factor['Name'])
    
        if factor['Min'] > factor['Max']:
            # 大小值設定反了，自動對調
            error_messages += '因子名稱 ' + factor['Name'] + '的大小值設定反了哦!, 我幫你改回來\n\n'
            f_mins.append(factor['Max'])
            f_maxs.append(factor['Min'])
            n_error += 1
        elif factor['Min'] == factor['Max']:
            # 大小值相同，自動在大值加 1（原本獨立的 if 改成 elif，避免重複 append）
            error_messages += '因子名稱 ' + factor['Name'] + '的大小值設定一樣也是不行的哦!, 我幫你在大值加 1 \n\n'
            f_mins.append(factor['Min'])
            f_maxs.append(factor['Max'] + 1)
            n_error += 1
        else:
            # 正常情況
            f_mins.append(factor['Min'])
            f_maxs.append(factor['Max'])
            
    if n_error != 0:
        error_messages += '總共有 '+ str(n_error) + ' 個錯誤，建議重新設定看看\n\n'
    return error_messages, f_names, f_mins, f_maxs

def assign_values(factor_df, f_names, f_mins, f_maxs):
    """寫一個 assign value 到 pandas dataframe 的程序
    args:
        factor_df: pandas dataframe, 正常是一開始開出來的 +1, -1, 0 的 df
        f_names: list of str, 每個因子的名字
        f_mins: list of num, 每個因子的小值
        f_maxs: list of num, 每個因子的大值

    returns:
        factor_df: pandas dataframe, 改好的 dataframe
    on error returns:
        N/A
    """    
    factor_df.columns = f_names
    
    for i in range(len(f_names)):
        items = factor_df[f_names[i]].tolist()
        value_min = f_mins[i]
        value_max = f_maxs[i]
        value_mean = ( value_min + value_max ) * 0.5
        new_list = []
        for item in items:
            if item == -1:
                new_list.append(value_min)
            elif item == 1:
                new_list.append(value_max)
            else:
                new_list.append(value_mean)
                
        factor_df[f_names[i]] = pd.Series(new_list)
        
    return factor_df

def build_final_sheet(factor_df, n_factors, n_responses):
    """寫一個 最後 finalize 實驗設計書的程序, 把 std_order, run_order, responses 排列整齊
    args:
        factor_df: pandas dataframe, 正常是一開始開出來的 +1, -1, 0 的 df
        n_responses: integer 實驗的 y 數
    returns:
        df: pandas dataframe, 改好的 dataframe
    on error returns:
        N/A
    """   
    df = pd.DataFrame()
    n_experiments = FAC_EXP_NUM_DIC[n_factors]+1
    std_order, run_order = build_exp_orders(n_experiments)
    df['std_order'] = pd.Series(std_order)
    df['run_order'] = pd.Series(run_order)
    df = df.join(factor_df)
    r_names = get_response_names(n_responses)
    for name in r_names:
        df[name] = 0.0
    return df

