from parser import Parser

parser = Parser(main_url='https://forum.criminal.ist/index.php?board=51')
main_html = parser.fetch_html()
number = parser.parse_pages_number(main_html)
parser.parse_topics(number)
