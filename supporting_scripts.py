import re


def extract_equation(latex_string):
    # Define the regular expression pattern to match the equation
    pattern = r'\\begin{equation}\s*(.*?)\s*\\end{equation}'

    # Use re.DOTALL to match across multiple lines
    match = re.search(pattern, latex_string, re.DOTALL)

    if match:
        # Extract the equation
        equation = match.group(1)

        # Remove curly brackets
        equation = re.sub(r'\{|\}', '', equation)
        # Replace \mhyphen with hyphen
        equation = re.sub(r'\\mhyphen ', '_', equation)
        # Replace ands, ors and negations
        equation = re.sub(r'and', '&', equation)
        equation = re.sub(r'or', '|', equation)
        equation = re.sub(r'not ', '!', equation)

        return equation
    else:
        return None


latex_string = r"""
\begin{equation}
    f_{AF4} = (X_{AF4} and not X_{s}) or (X_{AF4} and not X_{LH\mhyphen R}) or (not X_{AF4} and X_{AF3} and X_{s} and x_{LH\mhyphen R})
\end{equation}
"""

extracted_equation = extract_equation(latex_string)
print(extracted_equation)