#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from dna_tools import DNATools, TEXTS

# 获取程序运行路径,兼容打包后的exe
if getattr(sys, 'frozen', False):
    # 如果是打包后的exe
    root_path = os.path.dirname(sys.executable)
else:
    # 如果是python脚本
    root_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(root_path, "..")

# 语言字典：中英双语
TEXTS = {
    'zh_CN': {
        'title': "Gibson Assembly引物设计工具",
        'input_tab': "输入",
        'result_tab': "结果",
        'about_btn': "关于",
        'language_btn': "English",
        'fragment_group': "插入片段",
        'add_fragment': "添加片段",
        'remove_fragment': "移除片段",
        'move_up': "上移",
        'move_down': "下移",
        'vector_group': "载体信息",
        'vector_select': "选择载体",
        'browse_btn': "浏览...",
        'linearization': "线性化方式",
        'restriction': "限制酶切",
        'enzyme': "限制酶",
        'pcr': "PCR扩增",
        'forward_primer': "正向引物",
        'reverse_primer': "反向引物",
        'homology_length': "同源臂长度",
        'design_btn': "设计引物",
        'export_csv': "导出为CSV",
        'export_txt': "导出为TXT",
        'export_success': "成功",
        'export_success_msg': "结果已导出到 {0}",
        'export_error': "错误",
        'export_error_msg': "导出失败: {0}",
        'save_result': "保存结果",
        'no_result': "没有可导出的结果",
        'design_progress': "设计中...",
        'design_complete': "设计完成",
        'result_title': "Gibson Assembly引物设计结果",
        'vector_info': "载体信息:",
        'name': "名称:",
        'length': "长度:",
        'file': "文件:",
        'fragments': "插入片段:",
        'primer_results': "引物设计结果:",
        'vector_primers': "载体引物:",
        'fragment_primers': "片段引物:",
        'tm': "Tm值:",
        'gc_content': "GC含量:",
        'structure_issues': "结构问题:",
        'poly_x': "连续重复碱基",
        'hairpin': "可能形成发夹结构",
        'dimer': "可能形成自二聚体",
        'primer_dimer_warning': "警告: 正向和反向引物可能形成二聚体",
        'about_title': "关于 Let's Gibson",
        'about_content': "Let's Gibson 是一个用于设计Gibson Assembly引物的工具。\n\n它可以帮助您轻松设计多片段连接的引物，\n确保引物具有良好的特性（如适当的Tm值和GC含量），\n并避免引物二聚体和发夹结构等问题。\n用户许可协议：https://creativecommons.org/licenses/by-nc/4.0/legalcode",
        'version': "版本",
        'error_header': "错误",
        'no_fragments': "未添加任何片段",
        'no_vector': "未选择载体文件",
        'select_vector': "请选择载体文件",
        'select_fragments': "选择片段文件",
        'select_enzyme': "请选择限制酶",
        'enter_primers': "请输入PCR引物",
        'incompatible_fasta': "无法读取FASTA文件，请确保文件使用UTF-8或GBK编码格式",
        'read_fasta_error': "读取FASTA文件时出错: {0}",
        'icon_error': "设置图标时出错: {0}",
        'file_filter_fasta': "FASTA文件",
        'file_filter_csv': "CSV文件",
        'file_filter_txt': "文本文件",
        'credits': "由Let's Gibson生成",
        'repo': "项目地址:",
        'disclaimer': "免责声明：引物设计仅供参考，实际使用前请进行实验验证。",
        'select_sequence_title': "选择序列",
        'select_sequence_message': "FASTA文件中包含多个序列，请选择要添加的序列:",
        'select_sequence_btn': "添加选中序列",
        'select_sequence_cancel': "取消",
        'select_sequence_none': "请至少选择一个序列"
    },
    'en_US': {
        'title': "Gibson Assembly Primer Design Tool",
        'input_tab': "Input",
        'result_tab': "Results",
        'about_btn': "About",
        'language_btn': "中文",
        'fragment_group': "Insert Fragments",
        'add_fragment': "Add Fragment",
        'remove_fragment': "Remove Fragment",
        'move_up': "Move Up",
        'move_down': "Move Down",
        'vector_group': "Vector Information",
        'vector_select': "Select Vector",
        'browse_btn': "Browse...",
        'linearization': "Linearization Method",
        'restriction': "Restriction Enzyme",
        'enzyme': "Enzyme",
        'pcr': "PCR Amplification",
        'forward_primer': "Forward Primer",
        'reverse_primer': "Reverse Primer",
        'homology_length': "Homology Arm Length",
        'design_btn': "Design Primers",
        'export_csv': "Export to CSV",
        'export_txt': "Export to TXT",
        'export_success': "Success",
        'export_success_msg': "Results exported to {0}",
        'export_error': "Error",
        'export_error_msg': "Export failed: {0}",
        'save_result': "Save Results",
        'no_result': "No results to export",
        'design_progress': "Designing...",
        'design_complete': "Design Complete",
        'result_title': "Gibson Assembly Primer Design Results",
        'vector_info': "Vector Information:",
        'name': "Name:",
        'length': "Length:",
        'file': "File:",
        'fragments': "Insert Fragments:",
        'primer_results': "Primer Design Results:",
        'vector_primers': "Vector Primers:",
        'fragment_primers': "Fragment Primers:",
        'tm': "Tm:",
        'gc_content': "GC Content:",
        'structure_issues': "Structural Issues:",
        'poly_x': "Consecutive Repeated Bases",
        'hairpin': "Possible Hairpin Structure",
        'dimer': "Possible Self-Dimer",
        'primer_dimer_warning': "Warning: Forward and reverse primers may form dimers",
        'about_title': "About Let's Gibson",
        'about_content': "Let's Gibson is a tool for designing Gibson Assembly primers.\n\nIt helps you easily design primers for multi-fragment assembly,\nensuring primers have good properties (e.g., appropriate Tm and GC content),\nand avoiding issues like primer dimers and hairpin structures.\nEnd-User License Agreement:",
        'version': "Version",
        'error_header': "Error",
        'no_fragments': "No fragments added",
        'no_vector': "No vector file selected",
        'select_vector': "Please select a vector file",
        'select_fragments': "Select Fragment File",
        'select_enzyme': "Please select an enzyme",
        'enter_primers': "Please enter PCR primers",
        'incompatible_fasta': "Cannot read FASTA file, please ensure file uses UTF-8 or GBK encoding",
        'read_fasta_error': "Error reading FASTA file: {0}",
        'icon_error': "Error setting icon: {0}",
        'file_filter_fasta': "FASTA Files",
        'file_filter_csv': "CSV Files",
        'file_filter_txt': "Text Files",
        'credits': "Generated by Let's Gibson",
        'repo': "Repository:",
        'disclaimer': "Disclaimer: Primer designs are for reference only. Please validate experimentally before actual use.",
        'select_sequence_title': "Select Sequences",
        'select_sequence_message': "The FASTA file contains multiple sequences. Please select sequences to add:",
        'select_sequence_btn': "Add Selected",
        'select_sequence_cancel': "Cancel",
        'select_sequence_none': "Please select at least one sequence"
    }
}

class GibsonPrimerDesignApp:
    """Gibson Assembly引物设计工具的图形用户界面"""
    
    def __init__(self, root):
        self.root = root
        
        # 默认语言设置
        self.current_lang = 'en_US'
        
        # 设置窗口标题
        self.update_title()
        self.root.geometry("900x700")
        
        # 设置窗口图标
        try:
            icon_path = f"{root_path}/assets/LetsGibson_subsize.ico"
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"{self.get_text('icon_error').format(str(e))}")
        
        # 创建DNA工具实例
        self.dna_tools = DNATools()
        
        # 存储插入片段和载体信息
        self.fragments = []
        self.fragment_files = []
        self.fragment_order = []
        self.vector = None
        self.vector_file = ""
        
        # 创建界面
        self.create_widgets()
    
    def get_text(self, key):
        """获取当前语言的文本"""
        return TEXTS[self.current_lang].get(key, key)
    
    def update_title(self):
        """更新窗口标题"""
        self.root.title(self.get_text('title'))
    
    def toggle_language(self):
        """切换语言"""
        if self.current_lang == 'zh_CN':
            self.current_lang = 'en_US'
        else:
            self.current_lang = 'zh_CN'
        
        # 更新按钮文本
        self.language_btn.config(text=self.get_text('language_btn'))
        
        # 更新标题
        self.update_title()
        
        # 更新标签页
        self.notebook.tab(0, text=self.get_text('input_tab'))
        self.notebook.tab(1, text=self.get_text('result_tab'))
        
        # 更新其他UI元素
        self.fragment_label_frame.config(text=self.get_text('fragment_group'))
        self.add_fragment_btn.config(text=self.get_text('add_fragment'))
        self.remove_fragment_btn.config(text=self.get_text('remove_fragment'))
        self.move_up_btn.config(text=self.get_text('move_up'))
        self.move_down_btn.config(text=self.get_text('move_down'))
        
        self.vector_label_frame.config(text=self.get_text('vector_group'))
        self.vector_file_label.config(text=self.get_text('vector_select'))
        self.browse_btn.config(text=self.get_text('browse_btn'))
        self.linearization_label.config(text=self.get_text('linearization'))
        self.restriction_radio.config(text=self.get_text('restriction'))
        self.enzyme_label.config(text=self.get_text('enzyme'))
        self.pcr_radio.config(text=self.get_text('pcr'))
        self.fw_primer_label.config(text=self.get_text('forward_primer'))
        self.rv_primer_label.config(text=self.get_text('reverse_primer'))
        self.homology_label.config(text=self.get_text('homology_length'))
        
        self.design_btn.config(text=self.get_text('design_btn'))
        self.export_csv_btn.config(text=self.get_text('export_csv'))
        self.export_txt_btn.config(text=self.get_text('export_txt'))
        self.about_btn.config(text=self.get_text('about_btn'))
    
    def create_widgets(self):
        """创建图形界面组件"""
        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建输入页面
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text=self.get_text('input_tab'))
        
        # 创建结果页面
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text=self.get_text('result_tab'))
        
        # 设置输入页面
        self.setup_input_frame()
        
        # 设置结果页面
        self.setup_result_frame()
        
        # 添加语言切换按钮（左下角）
        self.language_btn = ttk.Button(self.root, text=self.get_text('language_btn'), command=self.toggle_language)
        self.language_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 添加关于按钮（右下角）
        self.about_btn = ttk.Button(self.root, text=self.get_text('about_btn'), command=self.show_about_dialog)
        self.about_btn.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def setup_input_frame(self):
        """设置输入页面的组件"""
        # 创建左右分栏
        left_frame = ttk.Frame(self.input_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.input_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：插入片段部分
        self.fragment_label_frame = ttk.LabelFrame(left_frame, text=self.get_text('fragment_group'))
        self.fragment_label_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加片段按钮
        self.add_fragment_btn = ttk.Button(self.fragment_label_frame, text=self.get_text('add_fragment'), command=self.add_fragment)
        self.add_fragment_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # 片段列表
        self.fragment_listbox = tk.Listbox(self.fragment_label_frame, selectmode=tk.SINGLE, height=10)
        self.fragment_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 片段操作按钮
        fragment_btn_frame = ttk.Frame(self.fragment_label_frame)
        fragment_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.remove_fragment_btn = ttk.Button(fragment_btn_frame, text=self.get_text('remove_fragment'), command=self.remove_fragment)
        self.remove_fragment_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_up_btn = ttk.Button(fragment_btn_frame, text=self.get_text('move_up'), command=self.move_fragment_up)
        self.move_up_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_down_btn = ttk.Button(fragment_btn_frame, text=self.get_text('move_down'), command=self.move_fragment_down)
        self.move_down_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧：载体信息
        self.vector_label_frame = ttk.LabelFrame(right_frame, text=self.get_text('vector_group'))
        self.vector_label_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 载体文件选择
        vector_file_frame = ttk.Frame(self.vector_label_frame)
        vector_file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.vector_file_label = ttk.Label(vector_file_frame, text=self.get_text('vector_select'))
        self.vector_file_label.pack(side=tk.LEFT, padx=5)
        
        self.vector_file_entry = ttk.Entry(vector_file_frame)
        self.vector_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.browse_btn = ttk.Button(vector_file_frame, text=self.get_text('browse_btn'), command=self.select_vector_file)
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 线性化方式
        linearization_frame = ttk.Frame(self.vector_label_frame)
        linearization_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.linearization_label = ttk.Label(linearization_frame, text=self.get_text('linearization'))
        self.linearization_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # 线性化方式选择
        self.linearization_var = tk.StringVar(value="restriction")
        
        self.restriction_radio = ttk.Radiobutton(linearization_frame, text=self.get_text('restriction'), 
                                               variable=self.linearization_var, value="restriction",
                                               command=self.toggle_linearization)
        self.restriction_radio.pack(anchor=tk.W, padx=20, pady=2)
        
        # 限制酶选择
        self.enzyme_frame = ttk.Frame(linearization_frame)
        self.enzyme_frame.pack(fill=tk.X, padx=20, pady=2)
        
        self.enzyme_label = ttk.Label(self.enzyme_frame, text=self.get_text('enzyme'))
        self.enzyme_label.pack(side=tk.LEFT, padx=5)
        
        # 常用限制酶
        enzymes = ['EcoRI', 'BamHI', 'HindIII', 'XhoI', 'NdeI', 'XbaI', 
                  'PstI', 'SalI', 'SmaI', 'KpnI', 'SacI', 'SphI', 'NotI', 'BglII', 'NcoI']
        
        self.enzyme_var = tk.StringVar()
        self.enzyme_combobox = ttk.Combobox(self.enzyme_frame, textvariable=self.enzyme_var, values=enzymes)
        self.enzyme_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # PCR扩增
        self.pcr_radio = ttk.Radiobutton(linearization_frame, text=self.get_text('pcr'), 
                                        variable=self.linearization_var, value="pcr",
                                        command=self.toggle_linearization)
        self.pcr_radio.pack(anchor=tk.W, padx=20, pady=2)
        
        # 正向引物
        fw_primer_frame = ttk.Frame(linearization_frame)
        fw_primer_frame.pack(fill=tk.X, padx=20, pady=2)
        
        self.fw_primer_label = ttk.Label(fw_primer_frame, text=self.get_text('forward_primer'))
        self.fw_primer_label.pack(side=tk.LEFT, padx=5)
        
        self.fw_primer_entry = ttk.Entry(fw_primer_frame)
        self.fw_primer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 反向引物
        rv_primer_frame = ttk.Frame(linearization_frame)
        rv_primer_frame.pack(fill=tk.X, padx=20, pady=2)
        
        self.rv_primer_label = ttk.Label(rv_primer_frame, text=self.get_text('reverse_primer'))
        self.rv_primer_label.pack(side=tk.LEFT, padx=5)
        
        self.rv_primer_entry = ttk.Entry(rv_primer_frame)
        self.rv_primer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 同源臂长度
        homology_frame = ttk.Frame(self.vector_label_frame)
        homology_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.homology_label = ttk.Label(homology_frame, text=self.get_text('homology_length'))
        self.homology_label.pack(side=tk.LEFT, padx=5)
        
        self.homology_var = tk.IntVar(value=25)
        self.homology_spinbox = ttk.Spinbox(homology_frame, from_=15, to=40, textvariable=self.homology_var, width=5)
        self.homology_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 设计引物按钮
        self.design_btn = ttk.Button(self.vector_label_frame, text=self.get_text('design_btn'), command=self.design_primers)
        self.design_btn.pack(fill=tk.X, padx=5, pady=10)
        
        # 初始化线性化界面
        self.toggle_linearization()
    
    def setup_result_frame(self):
        """设置结果页面的组件"""
        # 结果显示区域
        result_text_frame = ttk.Frame(self.result_frame)
        result_text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_text_frame, wrap=tk.WORD, 
                                                   width=80, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 导出按钮
        export_frame = ttk.Frame(self.result_frame)
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.export_csv_btn = ttk.Button(export_frame, text=self.get_text('export_csv'), command=lambda: self.export_results('csv'))
        self.export_csv_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_txt_btn = ttk.Button(export_frame, text=self.get_text('export_txt'), command=lambda: self.export_results('txt'))
        self.export_txt_btn.pack(side=tk.LEFT, padx=5)
    
    def add_fragment(self):
        """添加插入片段"""
        file_path = filedialog.askopenfilename(
            title=self.get_text('select_fragments'),
            filetypes=[(self.get_text('file_filter_fasta'), "*.fasta;*.fa"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            records = self.dna_tools.read_fasta(file_path)
            
            if not records:
                messagebox.showerror(self.get_text('error_header'), self.get_text('no_fragments'))
                return
            
            # 处理多个序列的情况
            if len(records) > 1:
                # 创建选择对话框
                select_window = tk.Toplevel(self.root)
                select_window.title(self.get_text('select_sequence_title'))
                select_window.geometry("400x300")
                select_window.resizable(True, True)
                
                # 添加说明标签
                ttk.Label(select_window, text=self.get_text('select_sequence_message')).pack(pady=10)
                
                # 创建列表框
                select_listbox = tk.Listbox(select_window, selectmode=tk.EXTENDED, height=10)
                select_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # 添加序列到列表框
                for record in records:
                    select_listbox.insert(tk.END, f"{record.id} ({len(record.seq)} bp)")
                
                # 添加按钮
                btn_frame = ttk.Frame(select_window)
                btn_frame.pack(fill=tk.X, padx=10, pady=10)
                
                def add_selected():
                    selected_indices = select_listbox.curselection()
                    if not selected_indices:
                        messagebox.showinfo(self.get_text('error_header'), self.get_text('select_sequence_none'))
                        return
                    
                    for idx in selected_indices:
                        record = records[idx]
                        # 使用序列ID作为片段名称
                        fragment_name = record.id
                        if not fragment_name or fragment_name.strip() == "":
                            # 如果ID为空，则使用文件名和索引
                            fragment_name = f"{os.path.basename(file_path)}_{idx+1}"
                        
                        # 添加到片段列表
                        self.fragments.append(record)
                        self.fragment_files.append(file_path)
                        self.fragment_order.append(len(self.fragments) - 1)
                        
                        # 更新列表显示
                        self.fragment_listbox.insert(tk.END, fragment_name)
                    
                    select_window.destroy()
                
                ttk.Button(btn_frame, text=self.get_text('select_sequence_btn'), command=add_selected).pack(side=tk.LEFT, padx=5)
                ttk.Button(btn_frame, text=self.get_text('select_sequence_cancel'), command=select_window.destroy).pack(side=tk.RIGHT, padx=5)
                
                # 使对话框模态
                select_window.transient(self.root)
                select_window.grab_set()
                self.root.wait_window(select_window)
                
            else:
                # 只有一个序列的情况
                record = records[0]
                # 使用序列ID作为片段名称
                fragment_name = record.id
                if not fragment_name or fragment_name.strip() == "":
                    # 如果ID为空，则使用文件名
                    fragment_name = os.path.basename(file_path)
                
                # 添加到片段列表
                self.fragments.append(record)
                self.fragment_files.append(file_path)
                self.fragment_order.append(len(self.fragments) - 1)
                
                # 更新列表显示
                self.fragment_listbox.insert(tk.END, fragment_name)
                
        except Exception as e:
            messagebox.showerror(self.get_text('error_header'), str(e))
    
    def remove_fragment(self):
        """移除选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx:
            messagebox.showinfo(self.get_text('error_header'), self.get_text('no_fragments'))
            return
        
        idx = selected_idx[0]
        
        # 从列表中移除
        self.fragment_listbox.delete(idx)
        
        # 更新片段顺序
        removed_idx = self.fragment_order[idx]
        self.fragment_order.pop(idx)
        
        # 调整顺序索引
        for i in range(len(self.fragment_order)):
            if self.fragment_order[i] > removed_idx:
                self.fragment_order[i] -= 1
    
    def move_fragment_up(self):
        """上移选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx or selected_idx[0] == 0:
            return
        
        idx = selected_idx[0]
        
        # 交换列表项
        fragment_name = self.fragment_listbox.get(idx)
        self.fragment_listbox.delete(idx)
        self.fragment_listbox.insert(idx - 1, fragment_name)
        self.fragment_listbox.selection_set(idx - 1)
        
        # 交换顺序
        self.fragment_order[idx], self.fragment_order[idx - 1] = self.fragment_order[idx - 1], self.fragment_order[idx]
    
    def move_fragment_down(self):
        """下移选中的片段"""
        selected_idx = self.fragment_listbox.curselection()
        
        if not selected_idx or selected_idx[0] == self.fragment_listbox.size() - 1:
            return
        
        idx = selected_idx[0]
        
        # 交换列表项
        fragment_name = self.fragment_listbox.get(idx)
        self.fragment_listbox.delete(idx)
        self.fragment_listbox.insert(idx + 1, fragment_name)
        self.fragment_listbox.selection_set(idx + 1)
        
        # 交换顺序
        self.fragment_order[idx], self.fragment_order[idx + 1] = self.fragment_order[idx + 1], self.fragment_order[idx]
    
    def select_vector_file(self):
        """选择载体文件"""
        file_path = filedialog.askopenfilename(
            title=self.get_text('select_vector'),
            filetypes=[(self.get_text('file_filter_fasta'), "*.fasta;*.fa"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            records = self.dna_tools.read_fasta(file_path)
            
            if not records:
                messagebox.showerror(self.get_text('error_header'), self.get_text('no_fragments'))
                return
            
            if len(records) > 1:
                messagebox.showwarning(self.get_text('error_header'), self.get_text('incompatible_fasta'))
            
            # 设置载体信息
            self.vector = records[0]
            self.vector_file = file_path
            self.vector_file_entry.delete(0, tk.END)
            self.vector_file_entry.insert(0, file_path)
            
        except Exception as e:
            messagebox.showerror(self.get_text('error_header'), str(e))
    
    def toggle_linearization(self):
        """根据线性化方式切换选项"""
        if self.linearization_var.get() == "restriction":
            # 显示酶切选项，隐藏PCR引物选项
            self.enzyme_frame.pack(fill=tk.X, padx=20, pady=2)
            # 隐藏PCR相关的框架
            for widget in [self.fw_primer_entry, self.rv_primer_entry]:
                widget.delete(0, tk.END)  # 清空输入
            for frame in [self.fw_primer_label.master, self.rv_primer_label.master]:
                frame.pack_forget()
        else:
            # 显示PCR引物选项，隐藏酶切选项
            self.enzyme_frame.pack_forget()
            self.enzyme_var.set("")  # 清空酶选择
            # 显示PCR相关的框架
            for frame in [self.fw_primer_label.master, self.rv_primer_label.master]:
                frame.pack(fill=tk.X, padx=20, pady=2)
    
    def design_primers(self):
        """设计Gibson Assembly引物"""
        # 检查输入
        if not self.fragments:
            messagebox.showerror(self.get_text('error_header'), self.get_text('no_fragments'))
            return
        
        if not self.vector:
            messagebox.showerror(self.get_text('error_header'), self.get_text('no_vector'))
            return
        
        # 获取同源臂长度
        homology_length = self.homology_var.get()
        
        # 获取载体线性化信息
        linearization_method = self.linearization_var.get()
        linearization_info = {}
        
        if linearization_method == "restriction":
            enzyme = self.enzyme_var.get()
            if not enzyme:
                messagebox.showerror(self.get_text('error_header'), self.get_text('select_enzyme'))
                return
            linearization_info["enzyme"] = enzyme
        else:
            fw_primer = self.fw_primer_entry.get().strip()
            rv_primer = self.rv_primer_entry.get().strip()
            
            if not fw_primer or not rv_primer:
                messagebox.showerror(self.get_text('error_header'), self.get_text('enter_primers'))
                return
            
            linearization_info["fw_primer"] = fw_primer
            linearization_info["rv_primer"] = rv_primer
        
        try:
            # 按顺序获取片段
            ordered_fragments = [self.fragments[i] for i in self.fragment_order]
            
            # 设计引物
            primer_results = self.dna_tools.design_gibson_primers(
                ordered_fragments, 
                self.vector, 
                homology_length, 
                linearization_method, 
                linearization_info
            )
            
            # 显示结果
            self.display_results(primer_results)
            
            # 切换到结果页面
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror(self.get_text('error_header'), str(e))
    
    def display_results(self, primer_results):
        """显示引物设计结果"""
        self.result_text.delete(1.0, tk.END)
        
        # 存储结果用于导出
        self.primer_results = primer_results
        
        # 添加标题
        self.result_text.insert(tk.END, self.get_text('result_title') + "\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # 显示载体信息
        self.result_text.insert(tk.END, self.get_text('vector_info') + "\n")
        self.result_text.insert(tk.END, f"{self.get_text('name')}: {self.vector.id}\n")
        self.result_text.insert(tk.END, f"{self.get_text('length')}: {len(self.vector.seq)} bp\n")
        self.result_text.insert(tk.END, f"{self.get_text('file')}: {self.vector_file}\n\n")
        
        # 显示片段信息
        self.result_text.insert(tk.END, self.get_text('fragments') + "\n")
        for i, idx in enumerate(self.fragment_order):
            fragment = self.fragments[idx]
            self.result_text.insert(tk.END, f"{i+1}. {fragment.id} ({len(fragment.seq)} bp)\n")
            self.result_text.insert(tk.END, f"    {self.get_text('file')}: {self.fragment_files[idx]}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")
        
        # 显示引物信息
        self.result_text.insert(tk.END, self.get_text('primer_results') + "\n\n")
        
        # 处理同名片段，记录每个名称出现的次数
        fragment_name_counts = {}
        
        # 载体引物
        if "vector_primers" in primer_results:
            self.result_text.insert(tk.END, self.get_text('vector_primers') + "\n")
            vector_primers = primer_results["vector_primers"]
            
            # 显示正向引物名称和序列
            fw = vector_primers['fw']
            fw_name = fw.get('name', "Vector-F")
            self.result_text.insert(tk.END, f"{fw_name}: {fw['sequence']}\n")
            self.result_text.insert(tk.END, f"{self.get_text('tm')}: {fw['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"{self.get_text('gc_content')}: {fw['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"{self.get_text('length')}: {fw['length']} bp\n\n")
            
            # 显示反向引物名称和序列
            rv = vector_primers['rv']
            rv_name = rv.get('name', "Vector-R")
            self.result_text.insert(tk.END, f"{rv_name}: {rv['sequence']}\n")
            self.result_text.insert(tk.END, f"{self.get_text('tm')}: {rv['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"{self.get_text('gc_content')}: {rv['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"{self.get_text('length')}: {rv['length']} bp\n\n")
            
            # 添加分割线
            self.result_text.insert(tk.END, "-" * 80 + "\n\n")
        
        # 片段引物
        self.result_text.insert(tk.END, self.get_text('fragment_primers') + "\n")
        
        # 首先处理片段名称，为重复的名称添加编号
        for primer_info in primer_results["fragment_primers"]:
            base_name = primer_info.get("name", "Fragment")
            
            # 记录名称出现次数
            if base_name in fragment_name_counts:
                fragment_name_counts[base_name] += 1
            else:
                fragment_name_counts[base_name] = 1
            
            # 如果名称重复，添加编号后缀
            if fragment_name_counts[base_name] > 1:
                # 添加编号后缀
                fragment_name = f"{base_name}_{fragment_name_counts[base_name]}"
            else:
                # 如果只出现一次，检查是否之后会再次出现
                total_count = sum(1 for p in primer_results["fragment_primers"] if p.get("name", "Fragment") == base_name)
                if total_count > 1:
                    # 如果之后会再次出现，第一次也添加编号
                    fragment_name = f"{base_name}_1"
                else:
                    # 如果只出现一次，不添加编号
                    fragment_name = base_name
            
            # 更新primer_info中的名称，用于导出
            primer_info["display_name"] = fragment_name
        
        # 重置计数器，开始显示引物信息
        fragment_name_counts = {}
        
        for i, primer_info in enumerate(primer_results["fragment_primers"]):
            # 使用已经处理过的名称
            fragment_name = primer_info.get("display_name", f"Fragment_{i+1}")
            
            self.result_text.insert(tk.END, f"{fragment_name}:\n")
            
            # 正向引物
            fw = primer_info["fw"]
            fw_name = f"{fragment_name}-F"
            # 更新引物名称用于导出
            fw["name"] = fw_name
            
            self.result_text.insert(tk.END, f"{fw_name}: {fw['sequence']}\n")
            self.result_text.insert(tk.END, f"{self.get_text('tm')}: {fw['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"{self.get_text('gc_content')}: {fw['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"{self.get_text('length')}: {fw['length']} bp\n")
            
            # 显示结构问题
            structure_issues = []
            if fw.get('has_poly_x', False):
                structure_issues.append(self.get_text('poly_x'))
            if fw.get('has_hairpin', False):
                structure_issues.append(self.get_text('hairpin'))
            if fw.get('has_dimer', False):
                structure_issues.append(self.get_text('dimer'))
            
            if structure_issues:
                self.result_text.insert(tk.END, f"{self.get_text('structure_issues')}: {', '.join(structure_issues)}\n")
            
            self.result_text.insert(tk.END, "\n")
            
            # 反向引物
            rv = primer_info["rv"]
            rv_name = f"{fragment_name}-R"
            # 更新引物名称用于导出
            rv["name"] = rv_name
            
            self.result_text.insert(tk.END, f"{rv_name}: {rv['sequence']}\n")
            self.result_text.insert(tk.END, f"{self.get_text('tm')}: {rv['tm']:.2f}°C\n")
            self.result_text.insert(tk.END, f"{self.get_text('gc_content')}: {rv['gc_content']:.2f}%\n")
            self.result_text.insert(tk.END, f"{self.get_text('length')}: {rv['length']} bp\n")
            
            # 显示结构问题
            structure_issues = []
            if rv.get('has_poly_x', False):
                structure_issues.append(self.get_text('poly_x'))
            if rv.get('has_hairpin', False):
                structure_issues.append(self.get_text('hairpin'))
            if rv.get('has_dimer', False):
                structure_issues.append(self.get_text('dimer'))
        
            if structure_issues:
                self.result_text.insert(tk.END, f"{self.get_text('structure_issues')}: {', '.join(structure_issues)}\n")
        
            # 如果存在引物二聚体问题
            if primer_info.get('primer_dimer', False):
                self.result_text.insert(tk.END, "\n" + self.get_text('primer_dimer_warning') + "\n")
        
            self.result_text.insert(tk.END, "\n" + "-" * 40 + "\n\n")
    
    def export_results(self, format_type):
        """导出引物设计结果"""
        if not hasattr(self, 'primer_results'):
            messagebox.showerror(self.get_text('error_header'), self.get_text('no_result'))
            return
        
        # 选择保存文件
        file_types = [(self.get_text('file_filter_csv'), "*.csv")] if format_type == 'csv' else [(self.get_text('file_filter_txt'), "*.txt")]
        file_path = filedialog.asksaveasfilename(
            title=self.get_text('save_result'),
            filetypes=file_types,
            defaultextension=f".{format_type}"
        )
        
        if not file_path:
            return
        
        try:
            if format_type == 'csv':
                # 导出为CSV，传递当前语言
                self.dna_tools.export_primers_to_csv(
                    self.primer_results, 
                    file_path, 
                    language=self.current_lang
                )
            else:
                # 导出为TXT，传递当前语言
                self.dna_tools.export_primers_to_txt(
                    self.primer_results, 
                    file_path,
                    language=self.current_lang
                )
            
            messagebox.showinfo(self.get_text('export_success'), self.get_text('export_success_msg').format(file_path))
        except Exception as e:
            messagebox.showerror(self.get_text('export_error'), self.get_text('export_error_msg').format(str(e)))

    def show_about_dialog(self):
        """显示关于对话框，包含许可证信息"""
        about_window = tk.Toplevel(self.root)
        about_window.title(self.get_text('about_title'))
        about_window.geometry("600x600")
        about_window.resizable(True, True)
        
        # 设置窗口图标
        try:
            icon_path = os.path.join(root_path, "assets", "LetsGibson_subsize.ico")
            if os.path.exists(icon_path):
                about_window.iconbitmap(icon_path)
            else:
                print(f"图标文件未找到: {icon_path}")
        except Exception as e:
            print(f"设置图标时出错: {str(e)}")
        
        # 添加JPG图片
        img_frame = ttk.Frame(about_window)
        img_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 尝试加载JPG图片
        try:
            from PIL import Image, ImageTk
            img_path = os.path.join(root_path, "assets", "LetsGibson.jpg")
            
            if not os.path.exists(img_path):
                print(f"图片文件未找到: {img_path}")
                # 尝试使用相对路径
                alternate_paths = [
                    "./assets/LetsGibson.jpg",
                    "../assets/LetsGibson.jpg",
                    "../../assets/LetsGibson.jpg",
                    "repo/assets/LetsGibson.jpg"
                ]
                
                for alt_path in alternate_paths:
                    if os.path.exists(alt_path):
                        img_path = alt_path
                        print(f"使用替代图片路径: {img_path}")
                        break
            
            if os.path.exists(img_path):
                img = Image.open(img_path)
                # 调整图片大小为500x130像素，使用高质量调整
                img = img.resize((500, 130), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 创建标签并显示图片
                img_label = ttk.Label(img_frame, image=photo)
                img_label.image = photo  # 保持引用，防止被垃圾回收
                img_label.pack(pady=5)
            else:
                # 如果找不到图片，显示文本标题
                title_label = ttk.Label(img_frame, text="Let's Gibson", font=("Arial", 24, "bold"))
                title_label.pack(pady=15)
                print("无法找到图片文件，使用文本替代")
                
        except Exception as e:
            # 如果加载图片失败，显示文本标题
            title_label = ttk.Label(img_frame, text="Let's Gibson", font=("Arial", 24, "bold"))
            title_label.pack(pady=15)
            print(f"加载图片时出错: {str(e)}")
        
        # 添加版本号
        version_frame = ttk.Frame(about_window)
        version_frame.pack(fill=tk.X, padx=10, pady=5)
        
        version_label = ttk.Label(version_frame, text=f"{self.get_text('version')} Beta 0.0.2", font=("Arial", 12, "bold"))
        version_label.pack(pady=5)
        
        # 添加说明文本
        desc_frame = ttk.Frame(about_window)
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        desc_text = scrolledtext.ScrolledText(desc_frame, wrap=tk.WORD, width=60, height=15)
        desc_text.insert(tk.END, self.get_text('about_content'))
        
        # 添加许可证信息
        license_text = """

Let's Gibson - Gibson Assembly Primer Design Tool
End-User License Agreement (CC BY-NC 4.0)

Copyright (c) (c) [2025] [DINGYi,4D Genome Lab]
[francisding@qq.com, 4dgenome.net]

This work includes:

Let's Gibson source code（Files in scripts folder in github repositories.）

Let's Gibson executable (LetsGibson.exe)

GUI design

Documentation & graphical assets (Logo, etc.)

Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

You may:

Share - reproduce and distribute the material

Adapt - remix, transform, or build upon the material

Under conditions:

Attribution - Visibly credit "Let's Gibson" with Logo, link to license, indicate changes

NonCommercial - No commercial use including:
• Paid services in commercial entities
• Integration into for-profit software
• Monetization via subscriptions/ads

Special Provisions:

Trademark Protection:

No modification of Logo in derivatives

Prohibit unofficial interface cloning

Unauthorized merchandising forbidden

Technical Restrictions:

No functional clone development

Liability Exclusion:

Example files not guaranteed usable

Experimental validation required

No liability for experimental costs

Implementation:

LICENSE.txt included in installation directory

Protocol summary in "About" dialog

When using the results of the software, the user should indicate the source of the software and the address of this repositories.(https://github.com/goodenough1/LetsGibson)

Let's Gibson - Gibson Assembly 引物设计工具
最终用户许可协议（CC BY-NC 4.0）

版权所有 (c) [2025] [DINGYi,4D Genome Lab]
[francisding@qq.com, 4dgenome.net]

本作品包括：

Let's Gibson 源码（github仓库scripts中的文件）

Let's Gibson可执行程序（LetsGibson.exe）

图形用户界面设计

使用文档与图形素材（Logo等）

根据知识共享署名-非商业性使用4.0国际许可协议（CC BY-NC 4.0）授权。
完整协议内容请访问：https://creativecommons.org/licenses/by-nc/4.0/legalcode

您有权：

共享 - 通过任何媒介复制、分发本作品

演绎 - 修改、转换或基于本作品进行再创作

必须遵守以下条件：

署名 - 必须显著标注"Let's Gibson"名称及Logo，附许可协议链接，明确说明是否修改原始作品

非商业 - 禁止用于直接或间接商业用途，包括：
• 商业机构内部付费服务
• 整合至盈利性软件产品
• 通过订阅制或广告获利

特别条款：

商标保护："Let's Gibson"名称及Logo为受保护标识，禁止：

在衍生作品中修改视觉设计

用于非官方版本的程序界面

未经授权制作周边商品

技术限制：

禁止制作功能相同的衍生软件

责任免除：

示例文件不表征实际序列可用性

引物设计结果需经实验验证

因使用本工具导致的实验损耗恕不担责

协议实施：

软件安装目录包含LICENSE.txt副本

图形界面"关于"页面显示协议摘要

用户在使用本软件的结果时需注明软件出处和本仓库地址(https://github.com/goodenough1/LetsGibson)
"""
        desc_text.insert(tk.END, license_text)
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 添加链接和免责声明
        link_frame = ttk.Frame(about_window)
        link_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 打开URL的函数
        def open_url(url):
            import webbrowser
            webbrowser.open_new(url)
        
        # 创建仓库链接按钮
        repo_url = "https://github.com/goodenough1/LetsGibson"
        repo_label = ttk.Label(link_frame, text=f"{self.get_text('repo')} ", cursor="hand2")
        repo_label.pack(side=tk.LEFT, pady=5)
        
        repo_link = ttk.Label(link_frame, text=repo_url, foreground="blue", cursor="hand2")
        repo_link.pack(side=tk.LEFT, pady=5)
        repo_link.bind("<Button-1>", lambda e: open_url(repo_url))
        
        # 添加下划线
        font = ("Arial", 9, "underline")
        repo_link.configure(font=font)
        
        # 免责声明
        disclaimer_frame = ttk.Frame(about_window)
        disclaimer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        disclaimer_label = ttk.Label(disclaimer_frame, text=self.get_text('disclaimer'), wraplength=550)
        disclaimer_label.pack(pady=5)
        
        # 添加关闭按钮
        close_btn = ttk.Button(about_window, text="OK", command=about_window.destroy)
        close_btn.pack(pady=10)
        
        # 使对话框模态
        about_window.transient(self.root)
        about_window.grab_set()
        self.root.wait_window(about_window)


def main():
    root = tk.Tk()
    app = GibsonPrimerDesignApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()