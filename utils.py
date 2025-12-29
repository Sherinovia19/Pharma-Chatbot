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
