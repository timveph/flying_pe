


def chart_speed(speed):
    chart_design = {
        "color": {

        }
        ,"gradientColor": {
            # "1": "CEEDC7"
            # ,"2": "FFF6BD"
            # ,"3": "FFD4B2"

        }
        # ,"stateAnimation": { 
        #     "animation": "auto"
        #     ,"animationDuration": 10000
        #     ,"animationDurationUpdate": 500
        #     ,"animationEasing": "cubicInOut"
        #     ,"animationEasingUpdate": "cubicInOut"
        #     ,"animationThreshold": 2000
        #     ,"progressiveThreshold": 3000
        #     ,"progressive": 400
        #     ,"hoverLayerThreshold": 3000
        #     ,"useUTC": False
        # }
        ,"series": [
            {
            "type": 'gauge',
            "progress": {
                "show": True,
                "width": 3
                ,"itemStyle": {
                    "color":"#FFF"
                    # ,"opacity": 10
                }
            },
            "pointer": {
                "itemStyle": {
                    "color": '#FFF'
                }
                ,"length": 50
                ,"width": 12
                ,"show": True
                ,"showAbove": False
                ,"icon": 'triangle' #'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'
                ,"offsetCenter": [0, '0%']
            },
            "axisTick": {
                "show": False,
                "distance": -5,
                "length": 2,
                "lineStyle": {
                    "color": '#fff',
                    "width": 2
                }
            },
            "axisLine": {
                "lineStyle": {
                    "width": 7
                    # ,"color": [
                    #     [0.3, '#367E18'],
                    #     [0.7, '#F57328'],
                    #     [1, '#CC3636']
                    #         ]
                }
            },
            "splitLine": {
                "show": True,
                "distance": 0,
                "length": 10,
                "lineStyle": {
                    "color": '#999',
                    "width": 2
                }
            },
            "axisLabel": {
                "color": '#999',
                "distance": 10,
                "fontSize": 12
            },
            "detail": {
                "valueAnimation": True
                ,"formatter": '{value} km/h'
                , "color": '#000'
                ,"fontSize": 18
                ,"backgroundColor": '#fff'
                ,"borderColor": '#000'
                ,"borderWidth": 1
                ,"borderRadius": 8
                ,"offsetCenter": [0, '90%']
                ,"lineHeight": 30
                ,"width": 80
                ,"height": 30
                # ,"valueAnimation": True
                # ,"animationDuration": 10000
                # ,"animationDurationUpdate": 500
                # ,"animationDelay": 1000
                # ,"animationEasing": "cubicInOut"
                # ,"animationEasingUpdate": "cubicInOut"
            }

            ,"anchor": {
                "show": True,
                "showAbove": True,
                "size": 10,
                'itemStyle': {
                    "borderWidth": 2
                    ,"borderColor": '#FFF'
                    ,"color": '#FFF'
                }
            },
            "title": {
                "show": False
            },
            "data": [
                {
                    "value": speed
                    # "value": 1025
                }
            ]
            , "min":0
            , "max":1050
            , "center": ['50%', '30%']
            , "radius": '50%' # size of guage chart
            , "splitNumber": 7
            }
        ]
        }
    
    return chart_design