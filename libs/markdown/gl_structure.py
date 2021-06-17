"""
This file contains data used to represent graphics in gitlab.
"""

PIEC_SCHEMA = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json", #TODO use local server/Push to github 
  "description": "All stateactors involved via ipv4.",
  "data": {
    "values": [
      
    ]
  },
  "mark": {"type": "arc", "innerRadius": 65},
  "encoding": {
    "theta": {"field": "value", "type": "quantitative"},
    "color": {"field": "State", "type": "nominal"}
  },
  "view": {"stroke": "null"}
}

BAR_WEBSITE_TYPES_SCHEMA = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "Websitetypechart",
  "data": {
    "values": [

    ]
  },
  "transform": [
    {
      "window": [{
        "op": "rank",
        "as": "rank"
      }],
      "sort": [{ "field": "Amount", "order": "descending" }]
    }, {
      "filter": "datum.rank <= 5"
    }
  ],
  "mark": "bar",
  "encoding": {
    "x": {
        "field": "Amount",
        "type": "quantitative"
    },
    "y": {
        "field": "Websitetypes",
        "type": "nominal",
        "sort": {"field": "Amount", "op": "average", "order":"descending"}
    }
  }
}

CVE_HEATMAP = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {
    "values": [

    ]
  },
  "params": [{"name": "highlight", "select": "point"}],
  "mark": {"type": "rect", "strokeWidth": 1},
  "encoding": {
    "x": {
      "field": "SCORE",
      "type": "nominal",
      "title": "CVEScore"
    },
    "y": {
      "field": "COMPLX",
      "type": "nominal",
      "title": "Complexity"
    },
    "fill": {
      "field": "APPEAR",
      "type": "quantitative",
      "title": "Occurrences"
    },
    "stroke": {
      "condition": {
        "param": "highlight",
        "empty": False,
        "value": "black"
      },
      "value": "null"
    },
    "opacity": {
      "condition": {"param": "highlight", "value": 1},
      "value": 0.5
    },
    "order": {"condition": {"param": "highlight", "value": 1}, "value": 0}
  },
  "config": {
    "scale": {
      "bandPaddingInner": 0,
      "bandPaddingOuter": 0
    },
    "view": {"step": 20},
    "range": {
      "ramp": {
        "scheme": "yellowgreenblue"
      }
    },
    "axis": {
      "domain": False
    }
  }
}