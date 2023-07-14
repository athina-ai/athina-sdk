# Desc: Regex patterns for matching common data types
email = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
ssn = r"\d{3}-\d{2}-\d{4}"
domain = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"
phone_number = r"\+?[\d\s()-]*\d[\d\s()-]*"
us_phone_number = r"(\+?1\s?)?((\(\d{3}\)|\d{3}))?[\s.-]?\d{3}[\s.-]?\d{4}"
