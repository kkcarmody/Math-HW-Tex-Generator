# Math-HW-Tex-Generator
Simple script to generate LaTeX templates for math homework. 

Default parent directory is *C:Users/[user]/OneDrive/Coursework/*, so make sure to edit in main.py if you use a different directory to store coursework.

`main.py` creates a LaTeX project from user input on the course directory to use (e.g., 'MATH 6214 - Measure Theory'), title (e.g., 'HW 7'), and so on. Creates 3+ files:

1. **preamble.sty** copied from this repository, with standard math packages and some custom macros;
2. **main.tex** from *main_template.tex*;
3. A separate **[*prob_number*].tex** file for each problem from *problem_template.tex*;

