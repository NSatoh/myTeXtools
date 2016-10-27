# coding:utf-8

preamble = r"""%-- ↓ヤング図形関連の設定↓ -----------------------
%
\def\emp{\makebox[2.5ex]{\vrule width 0ex height 1.8ex depth 0.7ex}}
\def\hako{% 左は開いた普通の箱
\multicolumn{1}{c|}{\emp}
}
\def\hakol{% 左も閉じた普通の箱
\multicolumn{1}{|c|}{\emp}
}
\def\hakot#1{% tableau用箱
\multicolumn{1}{c|}{#1}
}
\def\hakolt#1{% tableau用左閉じ箱
\multicolumn{1}{|c|}{#1}
}
\def\ghako{% グレー
\multicolumn{1}{c|}{\cellcolor[gray]{0.8}{\emp}}%
}
\def\ghakol{% グレー 左閉じ
\multicolumn{1}{|c|}{\cellcolor[gray]{0.8}{\emp}}%
}
\newenvironment{myYoung}[1]{%
\begingroup%
\renewcommand\arraystretch{0}%
\setlength\arraycolsep{0pt}%
\begin{array}{#1}%
}{%
\end{array}%
\endgroup%
}
%
%-- ↑ヤング図形関連の設定ココマデ↑ -----------------------
%"""

def make_diagram_TeX(partition, indent_depth=2):
    indent = " " * indent_depth
    TeX = indent + r"\begin{myYoung}{"

    for i in range(partition[0]):
        TeX += "c"

    TeX += r"} % " + str(partition) + "\n"
    TeX += indent + r"\hhline{"

    for i in range(partition[0]):
        TeX += r"|-"
    TeX += r"|}"
    
    TeX += "      " * (partition[0]-1)
    TeX += "%" + "%%%%" * partition[0]

    for p in partition:
        TeX += "\n" + indent + r"\hakol"
        TeX += r" & \hako" * (p-1)
        TeX += r" & \emp " * (partition[0] - p)
        TeX += r" \\   %"
        TeX += r"   %" * p
        TeX += "\n" + indent + r"\hhline{"
        TeX += r"|-" * p
        TeX += "|"
        TeX += "~" * (partition[0]-p)
        TeX += r"}"

        TeX += "      " * (partition[0] - 1)
        TeX += " " * (partition[0] - p)
        TeX += "%" + "%%%%" * p         

    TeX += "\n" + indent + r"\end{myYoung}"
    print(TeX)
    return TeX


    
