def get_bot_response(user_input):
    """
    Main function to generate a response for MedCheck AI.
    Handles expiry, near expiry, recalled, or general queries.
    """
    # Extract medicine name and batch
    medicine_name = normalize_medicine_name(user_input)
    batch_number = extract_batch(user_input)
    
    # Try to extract expiry date from message
    expiry_date = parse_date(user_input)

    # Check recalled batches
    recalled_info = check_recalled(medicine_name, batch_number)
    if recalled_info:
        return f"⚠️ Warning! The batch {batch_number} of {medicine_name.title()} has been recalled."

    # Check expiry
    if expiry_date:
        status = check_expiry(expiry_date)
        if status == "expired":
            return f"⚠️ This medicine expired on {expiry_date.date()}."
        elif status == "near_expiry":
            return f"⚠️ This medicine is near expiry on {expiry_date.date()}."
        else:
            return f"✅ This medicine is safe. Expiry date: {expiry_date.date()}"

    # General fallback response
    if medicine_name:
        return f"✅ {medicine_name.title()} looks fine. Provide batch number or expiry date for detailed check."
    
    return "🤖 I could not identify the medicine. Please provide name, batch, or expiry date."
def get_bot_response(user_input):
    try:
        # Example: simple handling
        name_match = re.search(r"\b[A-Za-z ]{2,}\b", user_input)
        name = name_match.group(0) if name_match else "medicine"

        batch = extract_batch(user_input)
        expiry_date = parse_date(user_input)
        expiry_status = "unknown"
        if expiry_date:
            expiry_status = check_expiry(expiry_date)

        recalled = check_recalled(name, batch)

        if recalled:
            return f"{name} batch {batch} has been recalled! ❌"
        elif expiry_status == "expired":
            return f"{name} batch {batch} is expired! ❌"
        elif expiry_status == "near_expiry":
            return f"{name} batch {batch} is near expiry ⚠️"
        else:
            return f"{name} batch {batch} is safe ✅"
    except Exception as e:
        return "⚠️ Bot encountered an error. Please try again."

