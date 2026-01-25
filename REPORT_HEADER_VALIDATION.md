The serial number and part number properties in WATS allow for characters that are not recommended.
I want to implement a "soft" blocking of these characters, by raising an appropriate warning/exception when used. This should be bypassable but not "by accident".

These are the recommendations:

Allowed and Not Allowed Characters for ‘Serial Number’ in a Test Report
According to the official WATS documentation, the Serial Number field is a mandatory text field with a maximum length of 100 characters. This rule applies to all standard report formats (WATS Standard Text, WSXF XML, and WSJF JSON).
✅ Allowed Characters
Use straightforward characters that will not interfere with parsing or filters. Examples:
Alphanumeric characters: A–Z, a–z, 0–9
Safe symbols: -, _, . (hyphen, underscore, period)
These are consistently accepted for all test-report serial numbers and are recommended for best compatibility.
❌ Not Allowed or Problematic Characters
Avoid characters that have reserved meanings in searches or file/path interpretation, as they can cause issues when filtering, importing, or reporting in WATS:
Character
Issue / Reserved Function
* or %
Wildcard for any string
? or _
Wildcard for any single character
[]
Defines a range or character list
[^]
Defines negated list of characters
!
Used in exclusion filtering
/ or \
Path delimiters that interfere with parsing
Summary
Maximum length: 100 characters
Avoid using: *, %, ?, _, [], [^], !, /, \
Recommended: Stick with alphanumeric characters, hyphens (-), underscores (_), and dots (.).
