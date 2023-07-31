def calculate_flakiness_index(pass_rate_percentage: float):
    """
    Calculate the Flakiness Index from the pass rate percentage.

    Parameters:
        pass_rate_percentage (float): The pass rate percentage, a value between 0 and 100.

    Returns:
        float: The Flakiness Index, a value between 0 and 100.
    """
    # Ensure the pass_rate_percentage is between 0 and 100.
    pass_rate_percentage = max(0, min(pass_rate_percentage, 100))

    # Normalize the pass rate percentage to a range between -1 and 1.
    normalized_prp = (2 * pass_rate_percentage - 100) / 100

    # Calculate the Flakiness Index.
    flakiness_index = (1 - abs(normalized_prp)) * 100

    return flakiness_index
