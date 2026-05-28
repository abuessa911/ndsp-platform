def calculate_dominant_direction(timing_data: dict, tdl_data: dict):
    controller = timing_data.get('controller')
    if controller == "L&M":
        return tdl_data.get('weekly_lm_direction', 'neutral'), "Weekly_LM"
    return tdl_data.get('weekly_s_direction', 'neutral'), "Weekly_S"
