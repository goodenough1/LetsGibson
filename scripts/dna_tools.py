#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Bio import SeqIO
from Bio.Seq import Seq
import random

class DNATools:
    """DNA序列处理和引物设计工具"""
    
    def __init__(self):
        """初始化DNA工具类"""
        # 设置引物设计参数
        self.primer_params = {
            'PRIMER_OPT_SIZE': 20,      # 最佳引物长度为20bp
            'PRIMER_MIN_SIZE': 18,      # 最小引物长度为18bp
            'PRIMER_MAX_SIZE': 30,      # 最大引物长度为30bp
            'PRIMER_OPT_TM': 60.0,      # 最佳Tm值为60°C
            'PRIMER_MIN_TM': 55.0,      # 最小Tm值为55°C
            'PRIMER_MAX_TM': 65.0,      # 最大Tm值为65°C
            'PRIMER_MIN_GC': 40.0,      # 最小GC含量为40%
            'PRIMER_MAX_GC': 60.0,      # 最大GC含量为60%
            'PRIMER_MAX_POLY_X': 4,     # 最大连续重复碱基数为4
            'PRIMER_MAX_END_STABILITY': 9.0  # 3'端稳定性
        }
    
    def read_fasta(self, file_path):
        """读取FASTA文件并返回序列记录，兼容UTF-8和GBK编码"""
        encodings = ['utf-8', 'gbk']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as handle:
                    records = list(SeqIO.parse(handle, 'fasta'))
                    if records:  # 确保成功解析了序列
                        return records
            except UnicodeDecodeError:
                continue  # 尝试下一种编码
            except Exception as e:
                raise Exception(f"读取FASTA文件时出错: {str(e)}")
        
        # 如果所有编码都失败，提示用户修改文件格式
        raise Exception("无法读取FASTA文件，请确保文件使用UTF-8或GBK编码格式")
    
    def reverse_complement(self, seq):
        """返回序列的反向互补序列"""
        return str(Seq(seq).reverse_complement())
    
    
    def calculate_tm(self, seq):
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
    
    def calculate_gc_content(self, seq):
        """计算序列的GC含量"""
        gc_count = seq.count('G') + seq.count('g') + seq.count('C') + seq.count('c')
        return (gc_count / len(seq)) * 100
    
    def check_poly_x(self, seq, max_poly=4):
        """检查序列中是否存在连续重复碱基"""
        for base in ['A', 'T', 'G', 'C']:
            if base * max_poly in seq.upper():
                return True
        return False
    
    def check_hairpin(self, seq, min_stem=3):
        """检查序列是否可能形成发夹结构"""
        seq = seq.upper()
        for i in range(len(seq) - min_stem * 2):
            stem = seq[i:i+min_stem]
            rev_comp = str(Seq(stem).reverse_complement())
            
            # 在后面的序列中查找互补序列
            if rev_comp in seq[i+min_stem:]:
                return True
        
        return False
    
    def check_self_dimer(self, seq, min_match=4):
        """检查序列是否可能形成自二聚体"""
        seq = seq.upper()
        rev_comp = str(Seq(seq).reverse_complement())
        
        for i in range(len(seq) - min_match + 1):
            for j in range(len(rev_comp) - min_match + 1):
                if seq[i:i+min_match] == rev_comp[j:j+min_match]:
                    return True
        
        return False
    
    def check_primer_dimer(self, primer1, primer2, min_match=4):
        """检查两个引物是否可能形成二聚体"""
        primer1 = primer1.upper()
        primer2 = primer2.upper()
        rev_comp2 = str(Seq(primer2).reverse_complement())
        
        for i in range(len(primer1) - min_match + 1):
            for j in range(len(rev_comp2) - min_match + 1):
                if primer1[i:i+min_match] == rev_comp2[j:j+min_match]:
                    return True
        
        return False
    
    
    def design_gibson_primers(self, fragments, vector, homology_length, linearization_method, linearization_info):
        """设计Gibson Assembly引物
        
        参数:
            fragments: 插入片段列表
            vector: 载体序列
            homology_length: 同源臂长度
            linearization_method: 线性化方式 ('restriction' 或 'pcr')
            linearization_info: 线性化相关信息
        
        返回:
            包含引物信息的字典
        """
        # 结果字典
        result = {
            "fragment_primers": []
        }
        
        # 检查输入参数
        if not fragments:
            raise ValueError("未提供插入片段")
        
        if not vector:
            raise ValueError("未提供载体序列")
        
        # 处理载体序列
        vector_seq = str(vector.seq)
        vector_name = vector.id if vector.id and vector.id.strip() != "" else "Vector"
        
        # 根据线性化方式处理载体
        if linearization_method == 'restriction':
            # 使用限制酶切
            enzyme = linearization_info.get('enzyme', '')
            
            # 酶切位点数据，格式为：'酶名': ('识别序列', 切割位置)
            # 切割位置表示在识别序列中从5'端开始计数的切割位置
            # 例如：EcoRI (G^AATTC) 在第1个位置切割，表示为1
            enzyme_sites = {
                'EcoRI': ('GAATTC', 1),     # G^AATTC
                'BamHI': ('GGATCC', 1),     # G^GATCC
                'HindIII': ('AAGCTT', 1),   # A^AGCTT
                'XhoI': ('CTCGAG', 1),      # C^TCGAG
                'NdeI': ('CATATG', 2),      # CA^TATG
                'XbaI': ('TCTAGA', 1),      # T^CTAGA
                'PstI': ('CTGCAG', 5),      # CTGCA^G
                'SalI': ('GTCGAC', 1),      # G^TCGAC
                'SmaI': ('CCCGGG', 3),      # CCC^GGG
                'KpnI': ('GGTACC', 5),      # GGTAC^C
                'SacI': ('GAGCTC', 5),      # GAGCT^C
                'SphI': ('GCATGC', 5),      # GCATG^C
                'NotI': ('GCGGCCGC', 2),    # GC^GGCCGC
                'BglII': ('AGATCT', 1),     # A^GATCT
                'NcoI': ('CCATGG', 1)       # C^CATGG
            }
            
            # 获取酶切位点信息
            enzyme_info = enzyme_sites.get(enzyme)
            if not enzyme_info:
                # 如果找不到酶切位点信息，使用随机位置
                cut_site = random.randint(0, len(vector_seq) - 1)
                linear_vector = vector_seq[cut_site:] + vector_seq[:cut_site]
                
                # 记录使用随机位置的信息
                result["linearization_info"] = {
                    "method": "restriction",
                    "enzyme": enzyme,
                    "note": "未找到酶切位点信息，使用随机位置"
                }
            else:
                # 解析酶切位点信息
                site_seq, cut_pos = enzyme_info
                
                # 查找酶切位点在载体上的位置
                site_pos = vector_seq.upper().find(site_seq.upper())
                if site_pos == -1:
                    # 如果找不到酶切位点，使用随机位置
                    cut_site = random.randint(0, len(vector_seq) - 1)
                    linear_vector = vector_seq[cut_site:] + vector_seq[:cut_site]
                    
                    # 记录使用随机位置的信息
                    result["linearization_info"] = {
                        "method": "restriction",
                        "enzyme": enzyme,
                        "note": f"载体中未找到{enzyme}酶切位点({site_seq})，使用随机位置"
                    }
                else:
                    # 根据酶切位点和切割位置切割载体
                    actual_cut_pos = site_pos + cut_pos
                    linear_vector = vector_seq[actual_cut_pos:] + vector_seq[:actual_cut_pos]
                    
                    # 记录酶切信息
                    result["linearization_info"] = {
                        "method": "restriction",
                        "enzyme": enzyme,
                        "site_sequence": site_seq,
                        "site_position": site_pos,
                        "cut_position": actual_cut_pos,
                        "note": f"{enzyme}在位置{actual_cut_pos}处切割载体"
                    }
            
            # 载体两端
            vector_start = linear_vector[:homology_length]
            vector_end = linear_vector[-homology_length:]
            
        else:
            # 使用PCR扩增
            fw_primer = linearization_info.get('fw_primer', '')
            rv_primer = linearization_info.get('rv_primer', '')
            
            # 查找引物在载体上的位置
            fw_pos = vector_seq.upper().find(fw_primer.upper())
            rv_comp = self.reverse_complement(rv_primer)
            rv_pos = vector_seq.upper().find(rv_comp.upper())
            
            if fw_pos == -1 or rv_pos == -1:
                raise Exception("无法在载体序列中找到PCR引物")
            
            # 模拟PCR扩增后的载体序列
            # PCR会从引物的3'端开始延伸，所以需要包含整个引物序列
            if fw_pos < rv_pos:
                # 正常情况：正向引物在反向引物之前
                pcr_product = fw_primer + vector_seq[fw_pos+len(fw_primer):rv_pos] + rv_comp
            else:
                # 特殊情况：正向引物在反向引物之后（跨越环状载体的起点）
                pcr_product = fw_primer + vector_seq[fw_pos+len(fw_primer):] + vector_seq[:rv_pos] + rv_comp
            
            # 线性化后的载体序列 - 将PCR产物视为线性化载体
            linear_vector = pcr_product
            
            # 载体两端 - 这里是PCR产物的两端，相当于酶切位点的两端
            # 5'端是正向引物序列，3'端是反向引物的反向互补序列
            vector_start = linear_vector[:homology_length]  # PCR产物5'端（正向引物序列）
            vector_end = linear_vector[-homology_length:]   # PCR产物3'端（反向引物的反向互补序列）
            
            # 添加载体引物信息，并命名为 Vector-F 和 Vector-R
            fw_analysis = self.analyze_primer(fw_primer)
            rv_analysis = self.analyze_primer(rv_primer)
            
            # 添加引物名称
            fw_analysis["name"] = f"{vector_name}-F"
            rv_analysis["name"] = f"{vector_name}-R"
            
            result["vector_primers"] = {
                "fw": fw_analysis,
                "rv": rv_analysis
            }
            
            # 记录PCR信息
            result["linearization_info"] = {
                "method": "pcr",
                "fw_primer": fw_primer,
                "rv_primer": rv_primer,
                "fw_position": fw_pos,
                "rv_position": rv_pos,
                "pcr_product_length": len(pcr_product),
                "pcr_product_5_end": vector_start,  # PCR产物5'端序列
                "pcr_product_3_end": vector_end,    # PCR产物3'端序列
                "note": "使用PCR引物扩增载体，PCR产物的5'端和3'端作为线性化载体的两端"
            }
        
        # 处理每个片段的引物
        for i, fragment in enumerate(fragments):
            fragment_seq = str(fragment.seq)
            
            # 获取片段名称，如果ID为空则使用索引
            fragment_name = fragment.id if fragment.id and fragment.id.strip() != "" else f"Fragment{i+1}"
            
            # 确定同源臂
            if i == 0:
                # 第一个片段：与载体末端和下一个片段起始同源
                left_homology = vector_end
                
                if len(fragments) > 1:
                    next_fragment = str(fragments[i+1].seq)
                    right_homology = next_fragment[:homology_length]
                else:
                    # 只有一个片段的情况
                    right_homology = vector_start
            
            elif i == len(fragments) - 1:
                # 最后一个片段：与前一个片段末端和载体起始同源
                prev_fragment = str(fragments[i-1].seq)
                left_homology = prev_fragment[-homology_length:]
                right_homology = vector_start
            
            else:
                # 中间片段：与前后片段同源
                prev_fragment = str(fragments[i-1].seq)
                next_fragment = str(fragments[i+1].seq)
                left_homology = prev_fragment[-homology_length:]
                right_homology = next_fragment[:homology_length]
            
            # 设计一对引物，控制退火温度差异
            best_primer_pair = self.design_balanced_primer_pair(
                fragment_seq, left_homology, right_homology
            )
            
            fw_primer = best_primer_pair["fw_primer"]
            rv_primer = best_primer_pair["rv_primer"]
            
            # 分析引物
            fw_analysis = self.analyze_primer(fw_primer)
            rv_analysis = self.analyze_primer(rv_primer)
            
            # 添加引物名称
            fw_analysis["name"] = f"{fragment_name}-F"
            rv_analysis["name"] = f"{fragment_name}-R"
            
            # 检查引物二聚体
            primer_dimer = self.check_primer_dimer(fw_primer, rv_primer)
            
            # 添加到结果，使用片段的ID作为名称
            result["fragment_primers"].append({
                "name": fragment_name,  # 直接使用FASTA中的ID作为片段名称
                "fw": fw_analysis,
                "rv": rv_analysis,
                "primer_dimer": primer_dimer,
                "tm_difference": abs(fw_analysis["tm"] - rv_analysis["tm"])
            })
        
        return result

    def design_balanced_primer_pair(self, fragment_seq, left_homology, right_homology):
        """设计一对退火温度平衡的引物
        
        参数:
            fragment_seq: 片段序列
            left_homology: 左侧同源臂
            right_homology: 右侧同源臂
            
        返回:
            包含正向和反向引物的字典
        """
        # 可能的结合位点长度范围
        binding_lengths = range(18, 25)
        
        # 生成所有可能的正向引物
        fw_candidates = []
        for length in binding_lengths:
            if length > len(fragment_seq):
                continue
            
            binding_site = fragment_seq[:length]
            primer = left_homology + binding_site
            
            # 计算结合部分的Tm值
            binding_tm = self.calculate_tm(binding_site)
            
            # 评估引物质量 
            score = self.evaluate_primer_quality(primer, binding_site)
            
            fw_candidates.append({
                "primer": primer,
                "binding_site": binding_site,
                "binding_tm": binding_tm,
                "score": score
            })
        
        # 生成所有可能的反向引物
        rv_candidates = []
        for length in binding_lengths:
            if length > len(fragment_seq):
                continue
            
            binding_site = self.reverse_complement(fragment_seq[-length:])
            primer = self.reverse_complement(right_homology) + binding_site
            
            # 计算结合部分的Tm值
            binding_tm = self.calculate_tm(binding_site)
            
            # 评估引物质量
            score = self.evaluate_primer_quality(primer, binding_site)
            
            rv_candidates.append({
                "primer": primer,
                "binding_site": binding_site,
                "binding_tm": binding_tm,
                "score": score
            })
        
        # 如果没有找到合适的候选引物，使用默认长度
        if not fw_candidates:
            binding_site = fragment_seq[:20]
            primer = left_homology + binding_site
            binding_tm = self.calculate_tm(binding_site)
            fw_candidates.append({
                "primer": primer,
                "binding_site": binding_site,
                "binding_tm": binding_tm,
                "score": 50  # 默认中等分数
            })
        
        if not rv_candidates:
            binding_site = self.reverse_complement(fragment_seq[-20:])
            primer = self.reverse_complement(right_homology) + binding_site
            binding_tm = self.calculate_tm(binding_site)
            rv_candidates.append({
                "primer": primer,
                "binding_site": binding_site,
                "binding_tm": binding_tm,
                "score": 50  # 默认中等分数
            })
        
        # 找到最佳引物对
        best_pair = None
        best_pair_score = -1
        
        for fw in fw_candidates:
            for rv in rv_candidates:
                # 计算Tm差异
                tm_diff = abs(fw["binding_tm"] - rv["binding_tm"])
                
                # 检查引物二聚体
                has_dimer = self.check_primer_dimer(fw["primer"], rv["primer"])
                
                # 计算总分数
                # 优先考虑Tm差异小的引物对，其次考虑引物质量
                pair_score = 100
                
                # Tm差异惩罚
                if tm_diff <= 2:
                    pair_score += 50  # 非常好
                elif tm_diff <= 4:
                    pair_score += 30  # 可接受
                else:
                    pair_score -= 50  # 不可接受
                
                # 引物二聚体惩罚
                if has_dimer:
                    pair_score -= 100  # 严重惩罚
                
                # 引物质量奖励
                pair_score += (fw["score"] + rv["score"]) / 2
                
                if pair_score > best_pair_score:
                    best_pair_score = pair_score
                    best_pair = {
                        "fw_primer": fw["primer"],
                        "rv_primer": rv["primer"],
                        "fw_binding_tm": fw["binding_tm"],
                        "rv_binding_tm": rv["binding_tm"],
                        "tm_difference": tm_diff,
                        "score": pair_score
                    }
        
        # 如果没有找到合适的引物对，使用分数最高的引物
        if best_pair is None:
            fw_candidates.sort(key=lambda x: x["score"], reverse=True)
            rv_candidates.sort(key=lambda x: x["score"], reverse=True)
            
            best_pair = {
                "fw_primer": fw_candidates[0]["primer"],
                "rv_primer": rv_candidates[0]["primer"],
                "fw_binding_tm": fw_candidates[0]["binding_tm"],
                "rv_binding_tm": rv_candidates[0]["binding_tm"],
                "tm_difference": abs(fw_candidates[0]["binding_tm"] - rv_candidates[0]["binding_tm"]),
                "score": (fw_candidates[0]["score"] + rv_candidates[0]["score"]) / 2
            }
        
        return best_pair

    def evaluate_primer_quality(self, primer_seq, binding_site=None):
        """评估引物质量，返回一个分数（越高越好）
        
        参数:
            primer_seq: 完整引物序列
            binding_site: 结合模板的部分，如果为None则使用整个引物
            
        返回:
            质量分数（0-100）
        """
        score = 100
        
        # 如果没有提供结合位点，使用整个引物
        if binding_site is None:
            binding_site = primer_seq
        
        # 检查引物长度
        length = len(binding_site)
        if length < 18 or length > 24:
            score -= 10
        
        # 检查3'端是否为G或C（GC夹）
        if primer_seq[-1].upper() not in ['G', 'C']:
            score -= 10
        
        # 检查3'端是否为T（不稳定）
        if primer_seq[-1].upper() == 'T':
            score -= 15
        
        # 检查3'端GC含量（最后5个碱基中不超过3个GC）
        last_5_bases = primer_seq[-5:]
        gc_count_last_5 = last_5_bases.upper().count('G') + last_5_bases.upper().count('C')
        if gc_count_last_5 > 3:
            score -= 15
        
        # 检查连续碱基
        if self.check_poly_x(primer_seq, max_poly=5):
            score -= 20
        
        # 检查发夹结构
        if self.check_hairpin(primer_seq):
            score -= 15
        
        # 检查自二聚体
        if self.check_self_dimer(primer_seq):
            score -= 15
        
        # 检查GC含量
        gc_content = self.calculate_gc_content(binding_site)
        if gc_content < 40:
            score -= 10 + (40 - gc_content) * 2  # 惩罚过低的GC含量
        elif gc_content > 60:
            score -= 10 + (gc_content - 60) * 2  # 惩罚过高的GC含量
        
        # 检查Tm值
        tm = self.calculate_tm(binding_site)
        if tm < 55:
            score -= 10 + (55 - tm) * 2  # 惩罚过低的Tm
        elif tm > 65:
            score -= 10 + (tm - 65) * 2  # 惩罚过高的Tm
        
        # 确保分数不为负
        return max(0, score)
    
    def analyze_primer(self, primer_seq):
        """分析引物的特性"""
        tm = self.calculate_tm(primer_seq)
        gc_content = self.calculate_gc_content(primer_seq)
        has_poly_x = self.check_poly_x(primer_seq)
        has_hairpin = self.check_hairpin(primer_seq)
        has_dimer = self.check_self_dimer(primer_seq)
        
        return {
            "sequence": primer_seq,
            "tm": tm,
            "gc_content": gc_content,
            "length": len(primer_seq),
            "has_poly_x": has_poly_x,
            "has_hairpin": has_hairpin,
            "has_dimer": has_dimer
        }
    
    def export_primers_to_csv(self, primers, output_file):
        """将引物导出为CSV文件"""
        with open(output_file, 'w') as f:
            f.write("Primer Name,Sequence,Tm,GC%,Length,Issues\n")
            
            # 载体引物
            if "vector_primers" in primers:
                vector_primers = primers["vector_primers"]
                
                fw = vector_primers['fw']
                fw_name = fw.get('name', "Vector-F")
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                f.write(f"{fw_name},{fw['sequence']},{fw['tm']:.2f},{fw['gc_content']:.2f},{fw['length']},{';'.join(issues_fw)}\n")
                
                rv = vector_primers['rv']
                rv_name = rv.get('name', "Vector-R")
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                f.write(f"{rv_name},{rv['sequence']},{rv['tm']:.2f},{rv['gc_content']:.2f},{rv['length']},{';'.join(issues_rv)}\n")
            
            # 片段引物
            for primer_info in primers["fragment_primers"]:
                fragment_name = primer_info.get("name", "Fragment")
                
                fw = primer_info["fw"]
                fw_name = fw.get('name', f"{fragment_name}-F")
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                f.write(f"{fw_name},{fw['sequence']},{fw['tm']:.2f},{fw['gc_content']:.2f},{fw['length']},{';'.join(issues_fw)}\n")
                
                rv = primer_info["rv"]
                rv_name = rv.get('name', f"{fragment_name}-R")
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                f.write(f"{rv_name},{rv['sequence']},{rv['tm']:.2f},{rv['gc_content']:.2f},{rv['length']},{';'.join(issues_rv)}\n")
                
                if primer_info.get('primer_dimer', False):
                    f.write(f"{fragment_name}-Warning,正向和反向引物可能形成二聚体,,,,\n")

    def export_primers_to_txt(self, primers, output_file):
        """将引物导出为TXT文件"""
        with open(output_file, 'w') as f:
            f.write("Gibson Assembly引物设计结果\n")
            f.write("=" * 80 + "\n\n")
            
            # 载体引物
            if "vector_primers" in primers:
                f.write("载体引物:\n")
                vector_primers = primers["vector_primers"]
                
                fw = vector_primers['fw']
                fw_name = fw.get('name', "Vector-F")
                f.write(f"{fw_name}: {fw['sequence']}\n")
                f.write(f"Tm值: {fw['tm']:.2f}°C\n")
                f.write(f"GC含量: {fw['gc_content']:.2f}%\n")
                f.write(f"长度: {fw['length']} bp\n")
                
                issues_fw = []
                if fw.get('has_poly_x', False):
                    issues_fw.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    issues_fw.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    issues_fw.append("可能形成自二聚体")
                
                if issues_fw:
                    f.write(f"结构问题: {', '.join(issues_fw)}\n")
                
                f.write("\n")
                
                rv = vector_primers['rv']
                rv_name = rv.get('name', "Vector-R")
                f.write(f"{rv_name}: {rv['sequence']}\n")
                f.write(f"Tm值: {rv['tm']:.2f}°C\n")
                f.write(f"GC含量: {rv['gc_content']:.2f}%\n")
                f.write(f"长度: {rv['length']} bp\n")
                
                issues_rv = []
                if rv.get('has_poly_x', False):
                    issues_rv.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    issues_rv.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    issues_rv.append("可能形成自二聚体")
                
                if issues_rv:
                    f.write(f"结构问题: {', '.join(issues_rv)}\n")
                
                f.write("\n" + "-" * 40 + "\n\n")
            
            # 片段引物
            f.write("片段引物:\n\n")
            
            for primer_info in primers["fragment_primers"]:
                fragment_name = primer_info.get("name", "Fragment")
                f.write(f"{fragment_name}:\n")
                
                # 正向引物
                fw = primer_info["fw"]
                fw_name = fw.get('name', f"{fragment_name}-F")
                f.write(f"{fw_name}: {fw['sequence']}\n")
                f.write(f"Tm值: {fw['tm']:.2f}°C\n")
                f.write(f"GC含量: {fw['gc_content']:.2f}%\n")
                f.write(f"长度: {fw['length']} bp\n")
                
                # 显示结构问题
                structure_issues = []
                if fw.get('has_poly_x', False):
                    structure_issues.append("连续重复碱基")
                if fw.get('has_hairpin', False):
                    structure_issues.append("可能形成发夹结构")
                if fw.get('has_dimer', False):
                    structure_issues.append("可能形成自二聚体")
                
                if structure_issues:
                    f.write(f"结构问题: {', '.join(structure_issues)}\n")
                
                f.write("\n")
                
                # 反向引物
                rv = primer_info["rv"]
                rv_name = rv.get('name', f"{fragment_name}-R")
                f.write(f"{rv_name}: {rv['sequence']}\n")
                f.write(f"Tm值: {rv['tm']:.2f}°C\n")
                f.write(f"GC含量: {rv['gc_content']:.2f}%\n")
                f.write(f"长度: {rv['length']} bp\n")
                
                # 显示结构问题
                structure_issues = []
                if rv.get('has_poly_x', False):
                    structure_issues.append("连续重复碱基")
                if rv.get('has_hairpin', False):
                    structure_issues.append("可能形成发夹结构")
                if rv.get('has_dimer', False):
                    structure_issues.append("可能形成自二聚体")
                
                if structure_issues:
                    f.write(f"结构问题: {', '.join(structure_issues)}\n")
                
                # 如果存在引物二聚体问题
                if primer_info.get('primer_dimer', False):
                    f.write("\n警告: 正向和反向引物可能形成二聚体\n")
                
                f.write("\n" + "-" * 40 + "\n\n")