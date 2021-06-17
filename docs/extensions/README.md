# YAFRA-Extensions

## What is YAFRA-Extensions

With YAFRA-Extensions we wanna provide an easy to use and fast way to add new IoC-Patterns.

## How does it work

1. Create a new file with extentionname like: ` md5.yafex, monero.yafex ` in the extensions folder.

2. Fill in all information as in the `Empty extension` section shown.

## Empty extension


```yaml
Name: name_of_the_pattern
Field: fieldname_must_by_unique
Pattern: \b(...)\b"
PatternArgs: 24
Group: 0
Hidden: False
Summary: Description of this pattern
Status: enabled/disabled
MISPType: misp_type
Reportclass: [Network, ...] (Only in beta)
Reportfield: Name of the section on the report
```

` Notice: If the field value is not unique the allready existing field will be extended with the values found be the extension. In order to hide the extension values in a seperate field in the report in gitlab just set the value of hidden to true. `

## RE flags for the PatternArgs

The pattern args follow the ` re `-PACKAGE from python. So in order to set multiple values like SRE_FLAG_MULTILINE and SRE_FLAG_VERBOSE you have to do an OR-Operation on the values.

- SRE_FLAG_TEMPLATE = 1 # template mode (disable backtracking)
- SRE_FLAG_IGNORECASE = 2 # case insensitive
- SRE_FLAG_LOCALE = 4 # honour system locale
- SRE_FLAG_MULTILINE = 8 # treat target as multiline string
- SRE_FLAG_DOTALL = 16 # treat target as a single string
- SRE_FLAG_UNICODE = 32 # use unicode "locale"
- SRE_FLAG_VERBOSE = 64 # ignore whitespace and comments
- SRE_FLAG_DEBUG = 128 # debugging
- SRE_FLAG_ASCII = 256 # use ascii "locale"
