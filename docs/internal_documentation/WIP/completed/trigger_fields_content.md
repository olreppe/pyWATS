[
  {
    "id": 42,
    "name": "Consecutive periods",
    "description": "Number of matching runs in row",
    "allowAnd": false,
    "allowOr": false,
    "dataType": "number",
    "identifier": "sequentialMatch",
    "inputType": "inputInt",
    "type": 2,
    "category": "a",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      }
    ],
    "sortOrder": 0
  },
  {
    "id": 82,
    "name": "Free serial numbers",
    "description": "Number of free serial numbers",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "free",
    "inputType": "inputInt",
    "type": 3,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      }
    ],
    "sortOrder": 0
  },
  {
    "id": 83,
    "name": "Reserved serial numbers",
    "description": "Number of reserved serial numbers",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "reserved",
    "inputType": "inputInt",
    "type": 3,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      }
    ],
    "sortOrder": 0
  },
  {
    "id": 84,
    "name": "Serial number type",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "string",
    "identifier": "serialNumberType",
    "inputType": "selectSnType",
    "type": 3,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      }
    ],
    "sortOrder": 0
  },
  {
    "id": 85,
    "name": "Asset name",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "assetname",
    "inputType": "input",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 0
  },
  {
    "id": 1,
    "name": "Product Group",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "group",
    "identifier": "productSelectionId",
    "inputType": "selectProductGroup",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 21,
    "name": "Product Group",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "group",
    "identifier": "productSelectionId",
    "inputType": "selectProductGroup",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 31,
    "name": "First Pass Yield",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "fpy",
    "inputType": "inputPercent",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 44,
    "name": "Product Group",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "group",
    "identifier": "productSelectionId",
    "inputType": "selectProductGroup",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 55,
    "name": "Count",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "count",
    "inputType": "inputInt",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 86,
    "name": "Level",
    "description": "The Level of the WATS Client that last used an asset",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "level",
    "identifier": "clientgroupid",
    "inputType": "selectLevel",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 1
  },
  {
    "id": 2,
    "name": "Level",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "level",
    "identifier": "clientGroupId",
    "inputType": "selectLevel",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 22,
    "name": "Level",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "level",
    "identifier": "clientGroupId",
    "inputType": "selectLevel",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 32,
    "name": "Second Pass Yield",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "spy",
    "inputType": "inputPercent",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 45,
    "name": "Level",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "level",
    "identifier": "clientGroupId",
    "inputType": "selectLevel",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 56,
    "name": "Count - Caused UUT Fail",
    "description": "Number of failures that caused UUT to fail",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "causedUutFailure",
    "inputType": "inputInt",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 87,
    "name": "Product group",
    "description": "A product group that that matches the assets partnumber and revision",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "productgroup",
    "identifier": "productgroupid",
    "inputType": "selectProductGroup",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 2
  },
  {
    "id": 3,
    "name": "Serial Number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "serialNumber",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 23,
    "name": "Part Number",
    "description": "partNumber",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "partNumber",
    "inputType": "inputPartNumber",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 33,
    "name": "Third Pass Yield",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "tpy",
    "inputType": "inputPercent",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 46,
    "name": "Part Number",
    "description": "partNumber",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "partNumber",
    "inputType": "inputPartNumber",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 57,
    "name": "Minimum time",
    "description": "Minimum time",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "minTime",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 88,
    "name": "Serial number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "serialnumber",
    "inputType": "input",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 3
  },
  {
    "id": 4,
    "name": "Part Number",
    "description": "partNumber",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "partNumber",
    "inputType": "inputPartNumber",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 24,
    "name": "Batch Number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "batchNumber",
    "inputType": "input",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 34,
    "name": "Last Pass Yield",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "lpy",
    "inputType": "inputPercent",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 47,
    "name": "Batch Number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "batchNumber",
    "inputType": "input",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 58,
    "name": "Maximum time",
    "description": "Maximum time",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "maxTime",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 89,
    "name": "Part number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "partnumber",
    "inputType": "inputPartNumber",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 4
  },
  {
    "id": 5,
    "name": "Batch Number",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "batchNumber",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 25,
    "name": "Revision",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "revision",
    "inputType": "input",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 35,
    "name": "Test Yield",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "testYield",
    "inputType": "inputPercent",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 48,
    "name": "Revision",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "revision",
    "inputType": "input",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 59,
    "name": "Average time",
    "description": "Average time",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "avgTime",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 90,
    "name": "Revision",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "revision",
    "inputType": "input",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 5
  },
  {
    "id": 6,
    "name": "Revision",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "revision",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 26,
    "name": "Station Name",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "stationName",
    "inputType": "inputStationName",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 36,
    "name": "Test Volume",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "uutCount",
    "inputType": "inputNumber",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 49,
    "name": "Station Name",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "stationName",
    "inputType": "inputStationName",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 60,
    "name": "Minimum value",
    "description": "Minimum value",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "min",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 91,
    "name": "Asset type",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "typeid",
    "inputType": "selectAssetType",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 6
  },
  {
    "id": 7,
    "name": "Station Name",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "stationName",
    "inputType": "inputStationName",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      },
      {
        "id": 13,
        "name": "In",
        "description": "in syntax",
        "identifier": "in",
        "sortOrder": 4
      },
      {
        "id": 14,
        "name": "Not in",
        "description": "not in syntax",
        "identifier": "not in",
        "sortOrder": 5
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 27,
    "name": "Process",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "processCode",
    "inputType": "selectProcess",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 37,
    "name": "Unit Volume",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "unitCount",
    "inputType": "inputNumber",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 50,
    "name": "Process",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "processCode",
    "inputType": "selectProcess",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 61,
    "name": "Maximum value",
    "description": "Maximum value",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "max",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 92,
    "name": "Status",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "bubbledstatus",
    "inputType": "selectAssetStatus",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      }
    ],
    "sortOrder": 7
  },
  {
    "id": 8,
    "name": "Process",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "processCode",
    "inputType": "selectProcess",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 29,
    "name": "SW Filename",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swFilename",
    "inputType": "input",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 38,
    "name": "First Pass Count",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "fpCount",
    "inputType": "inputNumber",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 51,
    "name": "SW Filename",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swFilename",
    "inputType": "input",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 62,
    "name": "Average value",
    "description": "Average value",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "avg",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 93,
    "name": "State",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "state",
    "inputType": "selectAssetState",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 8
  },
  {
    "id": 9,
    "name": "Status",
    "description": "status",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "result",
    "inputType": "selectStatus",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 30,
    "name": "SW Version",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swVersion",
    "inputType": "input",
    "type": 2,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 39,
    "name": "Last Pass Count",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "lpCount",
    "inputType": "inputNumber",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 52,
    "name": "SW Version",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swVersion",
    "inputType": "input",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 53,
    "name": "Measurement Path",
    "description": null,
    "allowAnd": false,
    "allowOr": true,
    "dataType": "string",
    "identifier": "measurementPath",
    "inputType": "input",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 63,
    "name": "Standard deviation",
    "description": "Standard deviation",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "stdev",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 94,
    "name": "Tag",
    "description": "A tag on an asset",
    "allowAnd": false,
    "allowOr": false,
    "dataType": "string",
    "identifier": "tags",
    "inputType": "selectTag",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 19,
        "name": "Is",
        "description": "tag is \"equal\"",
        "identifier": "like",
        "sortOrder": 0
      },
      {
        "id": 20,
        "name": "Is Not",
        "description": "tag is not \"equal\"",
        "identifier": "not like",
        "sortOrder": 1
      }
    ],
    "sortOrder": 9
  },
  {
    "id": 10,
    "name": "Run in Process",
    "description": "uuoIdx",
    "allowAnd": false,
    "allowOr": false,
    "dataType": "number",
    "identifier": "uuoIdx",
    "inputType": "inputInt",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 10
  },
  {
    "id": 40,
    "name": "Retests",
    "description": "Amount of retest due to poor FPY (uutCount - unitCount)",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "retestCount",
    "inputType": "inputInt",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 10
  },
  {
    "id": 54,
    "name": "Run",
    "description": null,
    "allowAnd": false,
    "allowOr": false,
    "dataType": "number",
    "identifier": "yieldType",
    "inputType": "selectYield",
    "type": 4,
    "category": "d",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 10
  },
  {
    "id": 64,
    "name": "Variance",
    "description": "Variance",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "var",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 10
  },
  {
    "id": 95,
    "name": "Tag value",
    "description": "A tag value on an asset",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "tags",
    "inputType": "inputTagValue",
    "type": 5,
    "category": null,
    "operators": [
      {
        "id": 19,
        "name": "Is",
        "description": "tag is \"equal\"",
        "identifier": "like",
        "sortOrder": 0
      },
      {
        "id": 20,
        "name": "Is Not",
        "description": "tag is not \"equal\"",
        "identifier": "not like",
        "sortOrder": 1
      }
    ],
    "sortOrder": 10
  },
  {
    "id": 28,
    "name": "Misc Info",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "miscInfo",
    "identifier": "reportId",
    "inputType": "inputMisc",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 17,
        "name": "Contains",
        "description": "like in syntax",
        "identifier": "in",
        "sortOrder": 2
      },
      {
        "id": 18,
        "name": "Does not contain",
        "description": "like in syntax",
        "identifier": "not in",
        "sortOrder": 3
      }
    ],
    "sortOrder": 11
  },
  {
    "id": 41,
    "name": "Sequences",
    "description": "Number of distinct sequences",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "sequenceCount",
    "inputType": "inputInt",
    "type": 2,
    "category": "c",
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 11
  },
  {
    "id": 65,
    "name": "CP",
    "description": "Process Capability",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cp",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 11
  },
  {
    "id": 11,
    "name": "Misc Info Description",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "miscInfoDescription",
    "identifier": "reportId",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 17,
        "name": "Contains",
        "description": "like in syntax",
        "identifier": "in",
        "sortOrder": 2
      },
      {
        "id": 18,
        "name": "Does not contain",
        "description": "like in syntax",
        "identifier": "not in",
        "sortOrder": 3
      }
    ],
    "sortOrder": 12
  },
  {
    "id": 66,
    "name": "CP lower",
    "description": "Process Capability Lower",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpLower",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 12
  },
  {
    "id": 12,
    "name": "Misc Info String",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "miscInfoString",
    "identifier": "reportId",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 17,
        "name": "Contains",
        "description": "like in syntax",
        "identifier": "in",
        "sortOrder": 2
      },
      {
        "id": 18,
        "name": "Does not contain",
        "description": "like in syntax",
        "identifier": "not in",
        "sortOrder": 3
      }
    ],
    "sortOrder": 13
  },
  {
    "id": 67,
    "name": "CP upper",
    "description": "Process Capability Upper",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpUpper",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 13
  },
  {
    "id": 13,
    "name": "Operator",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "operator",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 14
  },
  {
    "id": 68,
    "name": "CPK",
    "description": "Process Capability Index",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpk",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 14
  },
  {
    "id": 14,
    "name": "Execution Time",
    "description": "executionTime",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "executionTime",
    "inputType": "inputSeconds",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 15
  },
  {
    "id": 69,
    "name": "Count - without failed measurements",
    "description": "Count - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "countWof",
    "inputType": "inputInt",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 15
  },
  {
    "id": 15,
    "name": "Fixture ID",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "fixtureId",
    "inputType": "inputNumber",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 16
  },
  {
    "id": 16,
    "name": "Test Socket Index",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "testSocketIndex",
    "inputType": "inputNumber",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 17
  },
  {
    "id": 70,
    "name": "Minimum time - without failed measurements",
    "description": "Minimum time - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "minTimeWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 17
  },
  {
    "id": 17,
    "name": "Error Code",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "errorCode",
    "inputType": "inputNumber",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 18
  },
  {
    "id": 71,
    "name": "Maximum time - without failed measurements",
    "description": "Maximum time - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "maxTimeWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 18
  },
  {
    "id": 18,
    "name": "SW Filename",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swFilename",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 19
  },
  {
    "id": 72,
    "name": "Average time - without failed measurements",
    "description": "Average time - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "avgTimeWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 19
  },
  {
    "id": 19,
    "name": "SW Version",
    "description": null,
    "allowAnd": true,
    "allowOr": true,
    "dataType": "string",
    "identifier": "swVersion",
    "inputType": "input",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 3,
        "name": "Contains",
        "description": "wildcard like search",
        "identifier": "like",
        "sortOrder": 2
      },
      {
        "id": 4,
        "name": "Does not contain",
        "description": "wildcard not like search",
        "identifier": "not like",
        "sortOrder": 3
      }
    ],
    "sortOrder": 20
  },
  {
    "id": 73,
    "name": "Minimum value - without failed measurements",
    "description": "Minimum value - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "minWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 20
  },
  {
    "id": 20,
    "name": "Has Passed in Process",
    "description": "If the unit has passed in any previous run",
    "allowAnd": false,
    "allowOr": false,
    "dataType": "number",
    "identifier": "case when uuoIdx>passedInRun then 1 else 0 end",
    "inputType": "selectBoolean",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 21
  },
  {
    "id": 74,
    "name": "Maximum value - without failed measurements",
    "description": "Maximum value - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "maxWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 21
  },
  {
    "id": 96,
    "name": "Grade",
    "description": null,
    "allowAnd": false,
    "allowOr": true,
    "dataType": "string",
    "identifier": "grade",
    "inputType": "selectGrade",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      },
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      }
    ],
    "sortOrder": 21
  },
  {
    "id": 75,
    "name": "Average value - without failed measurements",
    "description": "Average value - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "avgWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 22
  },
  {
    "id": 97,
    "name": "Unit Phase",
    "description": null,
    "allowAnd": false,
    "allowOr": true,
    "dataType": "number",
    "identifier": "unitPhase",
    "inputType": "selectPhase",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 22
  },
  {
    "id": 76,
    "name": "Standard deviation - without failed measurements",
    "description": "Standard deviation - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "stdevWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 23
  },
  {
    "id": 98,
    "name": "Unit Process",
    "description": null,
    "allowAnd": false,
    "allowOr": true,
    "dataType": "number",
    "identifier": "unitProcess",
    "inputType": "selectProcess",
    "type": 1,
    "category": null,
    "operators": [
      {
        "id": 1,
        "name": "Is",
        "description": "value is equal to",
        "identifier": "=",
        "sortOrder": 0
      },
      {
        "id": 2,
        "name": "Is Not",
        "description": "value is not equal to",
        "identifier": "<>",
        "sortOrder": 1
      }
    ],
    "sortOrder": 23
  },
  {
    "id": 77,
    "name": "Variance - without failed measurements",
    "description": "Variance - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "varWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      },
      {
        "id": 11,
        "name": "Increased By (%)",
        "description": "value increased by x percent",
        "identifier": "ip",
        "sortOrder": 10
      },
      {
        "id": 12,
        "name": "Decreased By (%)",
        "description": "value decreased by x percent",
        "identifier": "dp",
        "sortOrder": 11
      }
    ],
    "sortOrder": 24
  },
  {
    "id": 78,
    "name": "CP - without failed measurements",
    "description": "Process Capability - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 25
  },
  {
    "id": 79,
    "name": "CP lower - without failed measurements",
    "description": "Process Capability Lower - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpLowerWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 26
  },
  {
    "id": 80,
    "name": "CP upper - without failed measurements",
    "description": "Process Capability Upper - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpUpperWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 27
  },
  {
    "id": 81,
    "name": "CPK - without failed measurements",
    "description": "Process Capability Index - without failed measurements",
    "allowAnd": true,
    "allowOr": true,
    "dataType": "number",
    "identifier": "cpkWof",
    "inputType": "inputNumber",
    "type": 4,
    "category": "c",
    "operators": [
      {
        "id": 5,
        "name": "Greater Than",
        "description": ">",
        "identifier": ">",
        "sortOrder": 4
      },
      {
        "id": 6,
        "name": "Lower Than",
        "description": "<",
        "identifier": "<",
        "sortOrder": 5
      },
      {
        "id": 7,
        "name": "Greater or Equal to",
        "description": ">=",
        "identifier": ">=",
        "sortOrder": 6
      },
      {
        "id": 8,
        "name": "Lower or Equal to",
        "description": "<=",
        "identifier": "<=",
        "sortOrder": 7
      },
      {
        "id": 9,
        "name": "Increased By (x)",
        "description": "value increased by x amount",
        "identifier": "ix",
        "sortOrder": 8
      },
      {
        "id": 10,
        "name": "Decreased By (x)",
        "description": "value decreased by x amount",
        "identifier": "dx",
        "sortOrder": 9
      }
    ],
    "sortOrder": 28
  }
]
Response Code
200