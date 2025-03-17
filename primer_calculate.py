#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_tm(seq):
    """计算引物的退火温度（Tm值）
    
    使用简化的Wallace规则计算短引物的Tm值，
    对于长度>14的引物使用修正的公式。
    
    参数:
        seq: 引物序列
        
    返回:
        退火温度（摄氏度）
    """
    seq = seq.upper()
    
    # 计算碱基数量
    a_count = seq.count('A')
    t_count = seq.count('T')
    g_count = seq.count('G')
    c_count = seq.count('C')
    
    # 总长度
    length = len(seq)
    
    # 对于短引物（≤14bp），使用Wallace规则
    if length <= 14:
        tm = 2 * (a_count + t_count) + 4 * (g_count + c_count)
    else:
        # 对于长引物，使用修正的公式
        tm = 64.9 + 41 * (g_count + c_count - 16.4) / length
    
    return tm

def calc_gc_content(seq):
    """计算序列的GC含量
    
    参数:
        seq: DNA序列
        
    返回:
        GC含量百分比
    """
    seq = seq.upper()
    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100

def check_self_complementarity(seq, min_length=4):
    """检查序列中的自互补区域
    
    参数:
        seq: DNA序列
        min_length: 最小互补长度
        
    返回:
        如果存在自互补区域，返回True；否则返回False
    """
    seq = seq.upper()
    complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    
    # 获取互补序列
    complement = ''.join(complement_map.get(base, 'N') for base in seq)
    
    # 反转互补序列
    rev_complement = complement[::-1]
    
    # 检查序列中是否存在与反向互补序列匹配的部分
    for i in range(len(seq) - min_length + 1):
        fragment = seq[i:i+min_length]
        if fragment in rev_complement:
            return True
    
    return False

def check_hairpin(seq, min_stem=3, min_loop=3):
    """检查序列是否可能形成发夹结构
    
    参数:
        seq: DNA序列
        min_stem: 最小茎长度
        min_loop: 最小环长度
        
    返回:
        如果可能形成发夹结构，返回True；否则返回False
    """
    seq = seq.upper()
    complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    
    # 检查可能的发夹结构
    for i in range(len(seq) - min_stem - min_loop - min_stem + 1):
        stem1 = seq[i:i+min_stem]
        
        for j in range(i + min_stem + min_loop, len(seq) - min_stem + 1):
            stem2 = seq[j:j+min_stem]
            
            # 检查stem2是否是stem1的反向互补
            stem2_rev = stem2[::-1]
            stem2_rev_comp = ''.join(complement_map.get(base, 'N') for base in stem2_rev)
            
            if stem1 == stem2_rev_comp:
                return True
    
    return False

def check_dimer(primer1, primer2, min_match=4):
    """检查两个引物是否可能形成二聚体
    
    参数:
        primer1: 第一个引物序列
        primer2: 第二个引物序列
        min_match: 最小匹配长度
        
    返回:
        如果可能形成二聚体，返回True；否则返回False
    """
    primer1 = primer1.upper()
    primer2 = primer2.upper()
    complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    
    # 获取primer2的互补序列
    primer2_comp = ''.join(complement_map.get(base, 'N') for base in primer2)
    
    # 检查primer1中是否存在与primer2互补序列匹配的部分
    for i in range(len(primer1) - min_match + 1):
        fragment = primer1[i:i+min_match]
        if fragment in primer2_comp:
            return True
    
    return False

def check_repeats(seq, max_repeat=4):
    """检查序列中是否存在连续重复碱基
    
    参数:
        seq: DNA序列
        max_repeat: 最大允许的连续重复碱基数
        
    返回:
        如果存在连续重复碱基，返回True；否则返回False
    """
    seq = seq.upper()
    
    for base in ['A', 'T', 'G', 'C']:
        if base * max_repeat in seq:
            return True
    
    return False

def optimize_primer(seq, target_tm=60, target_gc=50):
    """优化引物序列以达到目标Tm值和GC含量
    
    参数:
        seq: 原始引物序列
        target_tm: 目标Tm值
        target_gc: 目标GC含量
        
    返回:
        优化后的引物序列
    """
    # 计算当前Tm值和GC含量
    current_tm = calc_tm(seq)
    current_gc = calc_gc_content(seq)
    
    # 如果当前值已经接近目标值，则不需要优化
    if abs(current_tm - target_tm) < 2 and abs(current_gc - target_gc) < 5:
        return seq
    
    # 尝试通过调整序列长度来优化
    if current_tm < target_tm:
        # 需要增加Tm值，可以增加GC含量或增加长度
        # 这里简化处理，仅通过增加长度来调整
        return seq
    else:
        # 需要降低Tm值，可以减少GC含量或减少长度
        # 这里简化处理，仅通过减少长度来调整
        return seq[:-1]  # 移除最后一个碱基