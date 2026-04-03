"""
Part 2: Restaurant Order Management System
Implements 4 tasks using Python data structures: lists, dictionaries, and nested combinations
Total Marks: 25
"""

import copy

# ============================================================================
# PROVIDED DATA - DO NOT MODIFY
# ============================================================================

menu = {
    "Paneer Tikka": {"category": "Starters", "price": 180.0, "available": True},
    "Chicken Wings": {"category": "Starters", "price": 220.0, "available": False},
    "Veg Soup": {"category": "Starters", "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains", "price": 320.0, "available": True},
    "Dal Tadka": {"category": "Mains", "price": 180.0, "available": True},
    "Veg Biryani": {"category": "Mains", "price": 250.0, "available": True},
    "Garlic Naan": {"category": "Mains", "price": 40.0, "available": True},
    "Gulab Jamun": {"category": "Desserts", "price": 90.0, "available": True},
    "Rasguilla": {"category": "Desserts", "price": 80.0, "available": True},
    "Ice Cream": {"category": "Desserts", "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka": {"stock": 10, "reorder_level": 3},
    "Chicken Wings": {"stock": 8, "reorder_level": 2},
    "Veg Soup": {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka": {"stock": 20, "reorder_level": 5},
    "Veg Biryani": {"stock": 6, "reorder_level": 3},
    "Garlic Naan": {"stock": 30, "reorder_level": 10},
    "Gulab Jamun": {"stock": 5, "reorder_level": 2},
    "Rasguilla": {"stock": 4, "reorder_level": 3},
    "Ice Cream": {"stock": 7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1, "items": ["Paneer Tikka", "Garlic Naan"], "total": 220.0},
        {"order_id": 2, "items": ["Gulab Jamun", "Veg Soup"], "total": 210.0},
        {"order_id": 3, "items": ["Butter Chicken", "Garlic Naan"], "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4, "items": ["Dal Tadka", "Garlic Naan"], "total": 220.0},
        {"order_id": 5, "items": ["Veg Biryani", "Gulab Jamun"], "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6, "items": ["Paneer Tikka", "Rasguilla"], "total": 260.0},
        {"order_id": 7, "items": ["Butter Chicken", "Veg Biryani"], "total": 570.0},
        {"order_id": 8, "items": ["Garlic Naan", "Gulab Jamun"], "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9, "items": ["Dal Tadka", "Garlic Naan", "Rasguilla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"], "total": 270.0},
    ],
}

# ============================================================================
# TASK 1: EXPLORE THE MENU (5 marks)
# ============================================================================

def task1_explore_menu():
    """
    Task 1: Print full menu grouped by category with availability status,
    then compute and display menu statistics using dictionary methods.
    """
    print("\n" + "="*70)
    print("TASK 1: EXPLORE THE MENU (5 marks)")
    print("="*70)
    
    # Step 1: Print full menu grouped by category
    print("\n1. FULL MENU GROUPED BY CATEGORY:")
    print("-" * 70)
    
    # Group items by category
    categories = {}
    for item_name, item_details in menu.items():
        category = item_details["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((item_name, item_details))
    
    # Print menu by category
    for category in sorted(categories.keys()):
        print(f"\n===== {category} =====")
        for item_name, item_details in categories[category]:
            price = item_details["price"]
            availability = "[Available]" if item_details["available"] else "[Unavailable]"
            print(f"  {item_name:<20} ₹{price:>7.2f}  {availability}")
    
    # Step 2: Compute menu statistics
    print("\n2. MENU STATISTICS:")
    print("-" * 70)
    
    # Total number of items
    total_items = len(menu)
    print(f"  Total number of items on the menu: {total_items}")
    
    # Total number of available items
    available_items = sum(1 for item in menu.values() if item["available"])
    print(f"  Total number of available items: {available_items}")
    
    # Most expensive item
    most_expensive = max(menu.items(), key=lambda x: x[1]["price"])
    print(f"  Most expensive item: {most_expensive[0]} - ₹{most_expensive[1]['price']:.2f}")
    
    # Items priced under ₹150
    items_under_150 = [(name, details["price"]) 
                       for name, details in menu.items() 
                       if details["price"] < 150.0]
    print(f"  Items priced under ₹150:")
    for item_name, price in items_under_150:
        print(f"    - {item_name} - ₹{price:.2f}")
    
    return categories


# ============================================================================
# TASK 2: CART OPERATIONS (8 marks)
# ============================================================================

def add_to_cart(cart, item_name, quantity=1):
    """
    Add an item to cart or update quantity if already present.
    Returns: True if successful, False otherwise
    """
    # Check if item exists in menu
    if item_name not in menu:
        print(f"  ERROR: '{item_name}' does not exist in menu")
        return False
    
    # Check if item is available
    if not menu[item_name]["available"]:
        print(f"  ERROR: '{item_name}' is currently unavailable")
        return False
    
    # Check if item already in cart
    for cart_item in cart:
        if cart_item["item"] == item_name:
            cart_item["quantity"] += quantity
            print(f"  ✓ Updated '{item_name}' quantity to {cart_item['quantity']}")
            return True
    
    # Add new item to cart
    cart.append({
        "item": item_name,
        "quantity": quantity,
        "price": menu[item_name]["price"]
    })
    print(f"  ✓ Added '{item_name}' x{quantity} to cart")
    return True


def remove_from_cart(cart, item_name):
    """Remove an item from cart by name. Returns True if successful."""
    for i, cart_item in enumerate(cart):
        if cart_item["item"] == item_name:
            cart.pop(i)
            print(f"  ✓ Removed '{item_name}' from cart")
            return True
    print(f"  ERROR: '{item_name}' not found in cart")
    return False


def update_cart_quantity(cart, item_name, quantity):
    """Update quantity of an item in cart. Returns True if successful."""
    for cart_item in cart:
        if cart_item["item"] == item_name:
            if quantity <= 0:
                cart.remove(cart_item)
                print(f"  ✓ Removed '{item_name}' (quantity set to {quantity})")
            else:
                cart_item["quantity"] = quantity
                print(f"  ✓ Updated '{item_name}' quantity to {quantity}")
            return True
    print(f"  ERROR: '{item_name}' not found in cart")
    return False


def print_cart(cart, title="CURRENT CART"):
    """Print the current state of the cart."""
    print(f"\n  {title}:")
    if not cart:
        print("    [Cart is empty]")
    else:
        for item in cart:
            total_price = item["quantity"] * item["price"]
            print(f"    {item['item']:<20} x{item['quantity']:>2}  ₹{total_price:>8.2f}")


def print_order_summary(cart):
    """Print final order summary with calculations."""
    print("\n  ----------- ORDER SUMMARY -----------")
    
    if not cart:
        print("    [No items in order]")
        return
    
    subtotal = 0
    for item in cart:
        item_total = item["quantity"] * item["price"]
        subtotal += item_total
        print(f"  {item['item']:<20} x{item['quantity']:>2}  ₹{item_total:>8.2f}")
    
    gst = subtotal * 0.05  # 5% GST
    total = subtotal + gst
    
    print("  " + "-" * 41)
    print(f"  {'Subtotal:':<26} ₹{subtotal:>8.2f}")
    print(f"  {'GST (5%):':<26} ₹{gst:>8.2f}")
    print(f"  {'Total Payable:':<26} ₹{total:>8.2f}")
    print("  " + "-" * 41)


def task2_cart_operations():
    """
    Task 2: Simulate cart operations - add, remove, and update items.
    Demonstrate the sequence of operations and print order summary.
    """
    print("\n" + "="*70)
    print("TASK 2: CART OPERATIONS (8 marks)")
    print("="*70)
    
    cart = []  # Start with empty cart
    
    print("\nSimulating customer order sequence:")
    print("-" * 70)
    
    # Step 1: Add Paneer Tikka x 2
    print("\nStep 1: Add 'Paneer Tikka' x 2")
    add_to_cart(cart, "Paneer Tikka", 2)
    print_cart(cart)
    
    # Step 2: Add Gulab Jamun x 1
    print("\nStep 2: Add 'Gulab Jamun' x 1")
    add_to_cart(cart, "Gulab Jamun", 1)
    print_cart(cart)
    
    # Step 3: Add Paneer Tikka x 1 (should update quantity to 3)
    print("\nStep 3: Add 'Paneer Tikka' x 1 (should update quantity to 3)")
    add_to_cart(cart, "Paneer Tikka", 1)
    print_cart(cart)
    
    # Step 4: Try to add Mystery Burger (doesn't exist)
    print("\nStep 4: Try to add 'Mystery Burger' (does not exist in menu)")
    add_to_cart(cart, "Mystery Burger", 1)
    print_cart(cart)
    
    # Step 5: Try to add Chicken Wings (unavailable)
    print("\nStep 5: Try to add 'Chicken Wings' (exists but is unavailable)")
    add_to_cart(cart, "Chicken Wings", 1)
    print_cart(cart)
    
    # Step 6: Remove Gulab Jamun
    print("\nStep 6: Remove 'Gulab Jamun'")
    remove_from_cart(cart, "Gulab Jamun")
    print_cart(cart)
    
    # Print final order summary
    print("\nStep 7: Final Order Summary")
    print_order_summary(cart)
    
    return cart


# ============================================================================
# TASK 3: INVENTORY TRACKER WITH DEEP COPY (6 marks)
# ============================================================================

def task3_inventory_deep_copy(cart):
    """
    Task 3: Demonstrate deep copy behavior and inventory deduction.
    Show that deep copy protects original data, then process order fulfillment.
    """
    print("\n" + "="*70)
    print("TASK 3: INVENTORY TRACKER WITH DEEP COPY (6 marks)")
    print("="*70)
    
    # Step 1: Create deep copy before modifications
    print("\nStep 1: Creating deep copy of inventory...")
    inventory_backup = copy.deepcopy(inventory)
    print("  ✓ Created inventory_backup using copy.deepcopy()")
    
    # Step 2: Demonstrate deep copy by modifying inventory and showing backup is unaffected
    print("\nStep 2: Demonstrating deep copy protection:")
    print("  Manually changing 'Paneer Tikka' stock from 10 to 5...")
    inventory["Paneer Tikka"]["stock"] = 5
    
    print(f"    Inventory (modified): Paneer Tikka stock = {inventory['Paneer Tikka']['stock']}")
    print(f"    Backup (protected):   Paneer Tikka stock = {inventory_backup['Paneer Tikka']['stock']}")
    print("  ✓ Deep copy protected the original data!")
    
    # Step 3: Restore inventory to original state
    print("\nStep 3: Restoring inventory to original state...")
    inventory.update(copy.deepcopy(inventory_backup))
    print(f"    Restored: Paneer Tikka stock = {inventory['Paneer Tikka']['stock']}")
    
    # Step 4: Simulate order fulfillment - deduct from inventory
    print("\nStep 4: Fulfilling order - deducting items from inventory:")
    print("-" * 70)
    
    for cart_item in cart:
        item_name = cart_item["item"]
        quantity_ordered = cart_item["quantity"]
        available_stock = inventory[item_name]["stock"]
        
        if available_stock >= quantity_ordered:
            inventory[item_name]["stock"] -= quantity_ordered
            print(f"  ✓ {item_name}: -{quantity_ordered} (available: {available_stock} → {inventory[item_name]['stock']})")
        else:
            print(f"  ⚠ WARNING: {item_name} - Only {available_stock} in stock, ordered {quantity_ordered}")
            inventory[item_name]["stock"] = max(0, available_stock - quantity_ordered)
            print(f"    Deducted {min(quantity_ordered, available_stock)}, stock now: {inventory[item_name]['stock']}")
    
    # Step 5: Print reorder alerts
    print("\nStep 5: REORDER ALERTS:")
    print("-" * 70)
    
    reorder_needed = False
    for item_name, item_data in inventory.items():
        if item_data["stock"] <= item_data["reorder_level"]:
            status = "CRITICAL" if item_data["stock"] == 0 else "LOW"
            print(f"  ⚠ {status}: {item_name} - {item_data['stock']} unit(s) left (reorder level: {item_data['reorder_level']})")
            reorder_needed = True
    
    if not reorder_needed:
        print("  ✓ No items require reordering at this time")
    
    # Step 6: Compare inventory and backup
    print("\nStep 6: Comparing Final Inventory vs Backup:")
    print("-" * 70)
    print(f"  {'Item':<20} {'Current':<10} {'Backup':<10}")
    print("  " + "-" * 40)
    
    differences = 0
    for item_name in sorted(inventory.keys()):
        current = inventory[item_name]["stock"]
        backup = inventory_backup[item_name]["stock"]
        difference = "≠" if current != backup else "="
        print(f"  {item_name:<20} {current:<10} {backup:<10} {difference}")
        if current != backup:
            differences += 1
    
    print(f"\n  ✓ Deep copy verified! {differences} item(s) differ between current and backup")


# ============================================================================
# TASK 4: DAILY SALES LOG ANALYSIS (6 marks)
# ============================================================================

def task4_sales_analysis():
    """
    Task 4: Analyze sales log - revenue per day, best-selling day,
    most ordered item, add new day, and enumerate all orders.
    """
    print("\n" + "="*70)
    print("TASK 4: DAILY SALES LOG ANALYSIS (6 marks)")
    print("="*70)
    
    # Step 1: Print revenue per day
    print("\nStep 1: REVENUE PER DAY:")
    print("-" * 70)
    
    revenue_per_day = {}
    for date, orders in sales_log.items():
        daily_revenue = sum(order["total"] for order in orders)
        revenue_per_day[date] = daily_revenue
        print(f"  {date}: ₹{daily_revenue:>8.2f}")
    
    # Step 2: Find best-selling day
    print("\nStep 2: BEST-SELLING DAY:")
    best_day = max(revenue_per_day, key=revenue_per_day.get)
    print(f"  {best_day} with ₹{revenue_per_day[best_day]:.2f} revenue")
    
    # Step 3: Find most ordered item
    print("\nStep 3: MOST ORDERED ITEM:")
    item_order_count = {}
    for date, orders in sales_log.items():
        for order in orders:
            for item in order["items"]:
                item_order_count[item] = item_order_count.get(item, 0) + 1
    
    most_ordered = max(item_order_count, key=item_order_count.get)
    count = item_order_count[most_ordered]
    print(f"  '{most_ordered}' appears in {count} individual orders")
    
    # Step 4: Add new day and show updated stats
    print("\nStep 4: ADDING NEW DAY (2025-01-05):")
    print("-" * 70)
    
    new_day_data = {
        "2025-01-05": [
            {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
            {"order_id": 12, "items": ["Paneer Tikka", "Rasguilla"], "total": 260.0},
        ]
    }
    
    sales_log.update(new_day_data)
    print("  ✓ Added new day to sales_log")
    
    # Re-calculate revenue per day
    revenue_per_day = {}
    for date, orders in sales_log.items():
        daily_revenue = sum(order["total"] for order in orders)
        revenue_per_day[date] = daily_revenue
    
    print("\n  Updated Revenue Per Day:")
    for date in sorted(revenue_per_day.keys()):
        print(f"    {date}: ₹{revenue_per_day[date]:>8.2f}")
    
    # New best-selling day
    new_best_day = max(revenue_per_day, key=revenue_per_day.get)
    print(f"\n  New Best-selling Day: {new_best_day} with ₹{revenue_per_day[new_best_day]:.2f}")
    
    # Step 5: Enumerate all orders using enumerate()
    print("\nStep 5: ALL ORDERS (NUMBERED WITH enumerate()):")
    print("-" * 70)
    
    order_count = 1
    for date in sorted(sales_log.keys()):
        print(f"\n  {date}:")
        for idx, order in enumerate(sales_log[date], start=1):
            items_str = ", ".join(order["items"])
            print(f"    {order_count}. Order #{order['order_id']} - Items: {items_str} | Total: ₹{order['total']:.2f}")
            order_count += 1


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*10 + "PART 2: RESTAURANT ORDER MANAGEMENT SYSTEM" + " "*15 + "║")
    print("║" + " "*20 + "Total Marks: 25" + " "*33 + "║")
    print("╚" + "="*68 + "╝")
    
    # Execute all tasks
    task1_explore_menu()
    cart = task2_cart_operations()
    task3_inventory_deep_copy(cart)
    task4_sales_analysis()
    
    print("\n" + "="*70)
    print("✓ ALL TASKS COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")
