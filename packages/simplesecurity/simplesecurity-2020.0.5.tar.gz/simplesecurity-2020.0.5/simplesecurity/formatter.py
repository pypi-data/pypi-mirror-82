"""
Take our findings dictionary and give things a pretty format

finding dictionary

```json
{
	title: str
	description: str
	file: str
	evidence: str
	severity: Level
	confidence: Level
	line: str
	_other: {}
}
```

Formats

- markdown
- json
- csv
- ansi
"""
from __future__ import annotations

from io import StringIO
from json import dumps
from csv import writer
import typing
from simplesecurity.findings import Finding


def markdown(findings: list[Finding],
heading: typing.Optional[str] = None) -> str:
	"""Format to Markdown

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	if len(findings) == 0:
		return "No findings"

	heading = heading if heading is not None else \
	"# Findings\nFind a list of findings below ordered by severity"
	strBuf = [heading]
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)

	# Summary Table
	strBuf.append("")
	strBuf.append("|Severity|Finding|\n|:--|:--|")
	for finding in findings:
		strBuf.append(f"|{finding['severity']}|{finding['title']}|")
	strBuf.append("")

	# Details
	for finding in findings:
		strBuf.extend([
		f"## {finding['title']}", f"{finding['description']}",
		f"\n\nFile: {finding['file']}",
		f"### Severity\n\n{finding['severity']} (confidence: {finding['confidence']})",
		f"### Evidence\n\nLine: {finding['line']}\n\n```python\n{finding['evidence']}\n```",
		])
	return "\n".join(strBuf) + "\n"


def json(findings: list[Finding],
heading: typing.Optional[str] = None) -> str:
	"""Format to Json

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)
	out = {"heading": heading if heading is not None else \
	"Findings - Findings below are ordered by severity",
	"findings": findings}
	return dumps(out, indent="\t")


def csv(findings: list[Finding],
heading: typing.Optional[str] = None) -> str:
	"""Format to CSV

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)
	output = StringIO()
	csvString = writer(output)
	csvString.writerow([heading if heading is not None else \
	"Findings - Findings below are ordered by severity (you may want to delete this line)"])
	csvString.writerow([
	"title", "description", "file", "evidence", "severity", "confidence", "line"])
	for finding in findings:
		csvString.writerow([
		finding["title"], finding["description"], finding["file"],
		finding["evidence"], finding["severity"], finding["confidence"],
		finding["line"]])
	return output.getvalue()


def ansi(findings: list[Finding],
heading: typing.Optional[str] = None) -> str:
	"""Format to ansi

	Args:
		findings (list[Finding]): Findings to format
		heading (str, optional): Optional heading to include. Defaults to None.

	Returns:
		str: String to write to a file of stdout
	"""
	# pylint: disable=invalid-name
	BLD = "\033[01m"
	CLS = "\033[00m"
	UL = "\033[04m"
	CB = "\033[36m"
	CG = "\033[32m"
	CY = "\033[33m"
	CODE = "\033[100m\033[93m"

	if len(findings) == 0:
		return f"{BLD}{UL}{CB}No findings{CLS}"

	# pylint: enable=invalid-name
	heading = heading if heading is not None else \
	f"{BLD}{UL}{CB}Findings{CLS}\n\nFind a list of findings below ordered by severity\n"
	strBuf = [heading]
	findings = sorted(findings, key=lambda i: i["severity"], reverse=True)

	# Summary Table
	strBuf.append(
	"|Severity  |Finding                                           |")
	strBuf.append(
	"|----------|--------------------------------------------------|")
	for finding in findings:
		strBuf.append(f"|{finding['severity']: <10}|{finding['title'][:50]: <50}|")
	strBuf.append("")

	# Details
	for finding in findings:
		strBuf.extend([
		f"{BLD}{UL}{CG}{finding['title']}{CLS}", f"\n{finding['description']}",
		f"File: {finding['file']}\n",
		f">{UL}{CY}Severity: {finding['severity']} (confidence: {finding['confidence']}){CLS}\n",
		f">{UL}{CY}Evidence{CLS}\n\nLine: {finding['line']}\n{CODE}{finding['evidence']}{CLS}\n",
		])
	return "\n".join(strBuf)
