if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price: str) -> float:
    """Clean price string and convert to float"""
    # Remove dollar sign and commas, then convert to float
    cleaned = price.replace('$', '').replace(',', '').strip()
    return float(cleaned)


def clean_scraped_text(scraped_text: str) -> list[str]:
    """Clean scraped text by removing unwanted lines"""
    # Split text by newlines and strip whitespace
    lines = [line.strip() for line in scraped_text.split('\n') if line.strip()]
    
    # Filter out unwanted lines
    filtered = []
    unwanted = {'NEW!', 'NEW', 'S', 'V', 'GS', 'P'}
    
    for line in lines:
        if line not in unwanted:
            filtered.append(line)
    
    return filtered


def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    """Extract menu item details from scraped text"""
    cleaned = clean_scraped_text(scraped_text)
    
    # Get name (first item)
    name = cleaned[0] if len(cleaned) > 0 else "Unknown"
    
    # Get price (second item) and clean it
    price = clean_price(cleaned[1]) if len(cleaned) > 1 else 0.0
    
    # Get description (third item if exists)
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    
    return MenuItem(
        category=title,
        name=name,
        price=price,
        description=description
    )


if __name__ == '__main__':
    # Test cases
    price_test = "$10.99"
    print(f"Cleaned price: {clean_price(price_test)}")  # Should print 10.99
    
    scraped_text_test = """NEW!
    Tully Tots
    $11.79
    Made from scratch with shredded potatoes...
    """
    print("Cleaned text:")
    print(clean_scraped_text(scraped_text_test))  # Should print cleaned lines
    
    menu_item = extract_menu_item("Starters", scraped_text_test)
    print("\nExtracted menu item:")
    print(menu_item)