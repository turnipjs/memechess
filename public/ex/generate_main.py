with open("main.html", 'w') as fd:
	fd.write("""
<html>
<body>
<table>
""")
	for y in range(20):
		fd.write("<tr class=\"play-row\">")
		for x in range(20):
			fd.write("<td class=\"play-cell\" id=\"cell-"+str(x)+"-"+str(y)+"\">.</td>")
		fd.write("</tr>\n")
	fd.write("""
</table>
</body>
</html>
""")