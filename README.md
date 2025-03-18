# <strong>English Guide</strong>
# Let's Gibson - Gibson Assembly Primer Design Tool
<div align="center">
  <img src="https://github.com/goodenough1/LetsGibson/blob/main/assets/LetsGibson.svg?raw=true" alt="LetsGibson Logo" width="500">
</div>

## Usage Instructions

1. **Run the Program:**
   ```
   Double-click LetsGibson.exe
   ```

2. **In the Graphical Interface:**

   a. **Add Insert Fragments:**
      - Click the "Add Fragment" button
      - Select the insert fragment file in FASTA format
      - Multiple fragments can be added and reordered using the "Move Up" and "Move Down" buttons

   b. **Add Vector Information:**
      - Click the "Browse..." button to select a vector file in FASTA format
      - Choose the vector linearization method:
        * **Restriction Enzyme Digestion:** Select an enzyme from the dropdown menu
        * **PCR Amplification:** Enter forward and reverse primer sequences

   c. **Set Homology Arm Length:**
      - Default is 25 bp, adjustable between 15-40 bp as needed

   d. **Click the "Design Primers" button**

3. **View Results:**
   - The program will automatically switch to the "Results" tab
   - Displays forward and reverse primer sequences for each fragment, including sequence, Tm value, GC content, etc.
   - Results can be exported in CSV or TXT format

## Example Files

The tool includes the following example files for testing:
- `example_vector.fasta`: Example vector (pUC19)
- `example_fragment1.fasta`: Example insert fragment 1 (GFP)
- `example_fragment2.fasta`: Example insert fragment 2 (mCherry)
- `example_multiple_fragments.fasta`: Example file with multiple insert fragments (GFP, mCherry)

## Notes

1. All DNA sequence files should be in FASTA format
2. Both the vector and insert fragments should be double-stranded DNA sequences
3. If using PCR linearization, the provided primers should match the vector sequence
4. Homology arm length is typically 15-40 bp, with 25 bp being common
5. Primer design considers Tm values, GC content, and other parameters to ensure PCR specificity and efficiency

## Frequently Asked Questions (FAQ)

**Q: Why can't my vector find a restriction enzyme site?**  
A: Ensure the selected restriction enzyme has a recognition site within the vector sequence. If not, choose another enzyme or use PCR linearization.

**Q: What should I do if my primer Tm value is too low or too high?**  
A: The program attempts to optimize primer design, but you can try adjusting the homology arm length or modifying the fragment order.

**Q: Can I design primers for multiple fragments?**  
A: Yes, this tool supports any number of insert fragments. Simply add them in the desired order, but it is recommended to follow the guidelines of your Gibson Assembly kit regarding insert quantity.

# <strong>中文向导</strong>
# Let's Gibson - Gibson Assembly 引物设计工具
<div align="center">
  <img src="https://github.com/goodenough1/LetsGibson/blob/main/assets/LetsGibson.svg?raw=true" alt="LetsGibson Logo" width="500">
</div>
## 使用方法

1. 运行程序：
   ```
   双击 LetsGibson.exe
   ```

2. 在图形界面中：

   a. 添加插入片段：
      - 点击"添加片段"按钮
      - 选择FASTA格式的插入片段文件
      - 可以添加多个片段，并使用"上移"和"下移"按钮调整它们的顺序

   b. 添加载体信息：
      - 点击"浏览..."按钮选择FASTA格式的载体文件
      - 选择载体线性化方式：
        * 限制酶切：从下拉菜单中选择限制酶
        * PCR扩增：输入正向和反向引物序列

   c. 设置同源臂长度：
      - 默认为25bp，可以根据需要调整（通常在15-40bp之间）

   d. 点击"设计引物"按钮

3. 查看结果：
   - 程序会自动切换到"结果"标签页
   - 显示每个片段的正向和反向引物信息，包括序列、Tm值、GC含量等
   - 可以将结果导出为CSV或TXT格式

## 示例文件

工具包含以下示例文件，可用于测试：
- example_vector.fasta：示例载体（pUC19）
- example_fragment1.fasta：示例插入片段1（GFP）
- example_fragment2.fasta：示例插入片段2（mCherry）
- example_multiple_fragments.fasta: 示例包含多个插入片段的文件（GFP, mCherry）

## 注意事项

1. 所有DNA序列文件应为FASTA格式
2. 载体和插入片段都应为双链DNA序列
3. 如果使用PCR线性化载体，提供的引物应能在载体上找到匹配位置
4. 同源臂长度通常为15-40bp，25bp是常用的长度
5. 引物设计会考虑Tm值、GC含量等参数，以确保PCR反应的特异性和效率

## 常见问题

**Q: 为什么我的载体找不到限制酶切位点？**  
A: 确保载体序列中包含所选限制酶的识别位点。如果没有，可以选择其他限制酶或使用PCR线性化方法。

**Q: 引物Tm值过低或过高怎么办？**  
A: 程序会尝试优化引物设计，但如果仍有问题，可以尝试调整同源臂长度或选择不同的片段连接顺序。

**Q: 我可以设计多个片段的连接吗？**  
A: 是的，本工具支持任意数量的插入片段，只需按所需顺序添加它们即可，但是建议根据所使用的Gibson Assembly试剂盒的说明来选择插入数量。
