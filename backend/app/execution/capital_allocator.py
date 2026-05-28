def get_position_size(urgency):
    if urgency == "aggressive":
        return 0.01
    elif urgency == "moderate":
        return 0.005
    else:
        return 0.002
