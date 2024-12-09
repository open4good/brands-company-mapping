
# brands-company-mapping
This repository hosts a JSON mapping file that maps brand names to company names 

## Purpose

The primary goa l is to allow [nudger](https://nudger.fr) to integrate external ESG ratings in it's ImpactScore. To proceed, we need to resolve companies names from brands. 

## Description
The mapping is a simple json key/value structure, where key is the brand, and value the company operating this brand. Here is a sample of the full [brands-company-mapping.json](https://github.com/open4good/brands-company-mapping/blob/main/brands-company-mapping.json) file

    {
      "SAMSUNG": "Samsung Electronics Co., Ltd.",
      "TCL": "TCL Electronics Holdings Ltd.",
      "LG": "LG Electronics, Inc.",
      "PHILIPS": "Koninklijke Philips NV"
    }

## Convention

The following convention is applied to the data : 

### brand
The brands (keys of the json structure) are sanitized. It means :
     2. upper cased
     3. trimed (removing leading end trailing whitespaces)
     4. accents stripped

Here is a sample java code implementing the sanitization :

    public String sanitizeBrand(String name) {
      if (StringUtils.isEmpty(name)) {
        return  "";
      }    
      return StringUtils.stripAccents(name.toUpperCase()).trim();
    }

### company name
The companies names (values of the json structure) are based on the one used by [Sustainalytics ESG rating platform](https://www.sustainalytics.com/).

## Wants to contribute ?
Simply fill a PR with your key / values, it will be reviewed then merged.