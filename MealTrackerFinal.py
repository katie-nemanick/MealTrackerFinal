import tkinter as tk
from tkinter import ttk, messagebox

#Meal options dictionaries with ingredients
mealOptions = {
    "breakfast": {
        "Scrambled Eggs and Bacon": {"eggs": 2, "milk": 1, "bacon": 1},
        "Pancakes": {"flour": 1, "eggs": 2, "milk": 1, "sausages": 1},
        "Egg Sandwich": {"eggs": 2, "bread": 2, "sausage": 1},
        "Oatmeal with Fruit": {"oats": 1, "milk": 1, "honey": 1, "banana": 1},
        "Smoothie Bowl": {"frozen berries": 1, "milk": 1, "yogurt": 1, "granola": 1},
    },
    "lunch": {
        "Grilled Cheese Sandwich": {"bread": 2, "cheese": 2, "butter": 1},
        "Caesar Salad": {"romaine lettuce": 1, "croutons": 1, "caesar dressing": 1, "parmesan cheese": 1},
        "Chicken Wrap": {"tortilla": 1, "cooked chicken": 1, "lettuce": 1, "cheese": 1},
        "Vegetable Soup": {"carrots": 2, "celery": 2, "onion": 1, "vegetable broth": 1},
        "Turkey and Cheese Sandwich": {"bread": 2, "turkey": 2, "cheese": 1, "lettuce": 1},
    },
    "dinner": {
        "Spaghetti with Meat Sauce": {"spaghetti": 1, "tomato sauce": 1, "ground beef": 1, "garlic": 1},
        "Chicken Stir-Fry": {"chicken breast": 1, "bell peppers": 2, "soy sauce": 1, "rice": 1},
        "Grilled Salmon with Vegetables": {"salmon": 1, "broccoli": 1, "carrots": 2, "olive oil": 1},
        "Tacos": {"tortillas": 2, "ground beef": 1, "lettuce": 1, "cheese": 1},
        "Vegetarian Chili": {"kidney beans": 1, "tomato sauce": 1, "onion": 1, "chili powder": 1},
    },
}

#Empty inventory dictionary
inventory = {}

#Meal Plan dictionary
mealPlan = {
    day: {"breakfast": None, "lunch": None, "dinner": None}
    for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
}

#Tkinter GUI Setup
root = tk.Tk()
root.title("Weekly Meal Planner")
root.geometry("800x600")

#Function to display inventory
def updateInventoryDisplay():
    inventoryText.delete("1.0", tk.END)
    for item, quantity in inventory.items():
        inventoryText.insert(tk.END, f"{item}: {quantity}\n")

#Function to add/update inventory
def manageInventory():
    item = itemEntry.get().strip().lower()
    try:
        quantity = int(quantityEntry.get().strip())
        inventory[item.lower()] = inventory.get(item, 0) + quantity
        updateInventoryDisplay()
        messagebox.showinfo("Inventory Updated", f"Added {quantity} {item}(s).")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid quantity.")

#Function to add meals to the plan
def setMealPlan():
    day = dayVar.get()
    mealType = mealTypeVar.get()
    meal = mealVar.get()
    if meal in mealOptions[mealType]:
        mealPlan[day][mealType] = meal
        messagebox.showinfo("Meal Plan Updated", f"Set {meal} for {mealType} on {day}.")
    else:
        messagebox.showerror("Invalid Meal", "Please select a valid meal.")

#Function to generate grocery list
def generateGroceryList():
    groceryList = {}
    for day, meals in mealPlan.items():
        for mealType, mealName in meals.items():
            if mealName:
                ingredients = mealOptions[mealType][mealName]
                for item, quantity in ingredients.items():
                    needed = max(0, quantity - inventory.get(item.lower(), 0))
                    if needed > 0:
                        groceryList[item] = groceryList.get(item, 0) + needed
    groceryText.delete("1.0", tk.END)
    for item, quantity in groceryList.items():
        groceryText.insert(tk.END, f"{item}: {quantity}\n")
        
def displayMealPlan():
    mealPlanWindow = tk.Toplevel(root)
    mealPlanWindow.title("Meal Plan")
    mealPlanWindow.geometry("500x400")
    #Create a grid view for the meal plan
    tree = ttk.Treeview(mealPlanWindow, columns=("Breakfast", "Lunch", "Dinner"), show="headings")
    tree.heading("Breakfast", text="Breakfast")
    tree.heading("Lunch", text="Lunch")
    tree.heading("Dinner", text="Dinner")
    tree.pack(fill="both", expand=True)
    #Insert meal plan data
    for day, meals in mealPlan.items():
        tree.insert("", "end", values=(meals["breakfast"], meals["lunch"], meals["dinner"]))

#You said that we can use Chatgpt for small things as long as we let you know, I used it to help me with the strucure of my layout I was running into too many overlaps and layout issues
#Layout
#Inventory Section
inventoryFrame = ttk.LabelFrame(root, text="Inventory Management")
inventoryFrame.pack(fill="x", padx=10, pady=10)

itemLabel = ttk.Label(inventoryFrame, text="Item:")
itemLabel.grid(row=0, column=0, padx=5, pady=5)

itemEntry = ttk.Entry(inventoryFrame)
itemEntry.grid(row=0, column=1, padx=5, pady=5)

quantityLabel = ttk.Label(inventoryFrame, text="Quantity:")
quantityLabel.grid(row=0, column=2, padx=5, pady=5)

quantityEntry = ttk.Entry(inventoryFrame)
quantityEntry.grid(row=0, column=3, padx=5, pady=5)

addButton = ttk.Button(inventoryFrame, text="Add/Update", command=manageInventory)
addButton.grid(row=0, column=4, padx=5, pady=5)

inventoryText = tk.Text(inventoryFrame, height=5, state="normal")
inventoryText.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

#Meal Planning Section
mealPlanFrame = ttk.LabelFrame(root, text="Meal Planner")
mealPlanFrame.pack(fill="x", padx=10, pady=10)

#Set valid initial empty values for dayVar and mealTypeVar
dayVar = tk.StringVar(value="")  # Initially empty
mealTypeVar = tk.StringVar(value="")  # Initially empty

#Create the dropdown for day selection with an empty initial value
dayMenu = ttk.OptionMenu(mealPlanFrame, dayVar, "empty", *mealPlan.keys())  
dayMenu.grid(row=0, column=0, padx=5, pady=5)

#Create the dropdown for meal type selection with an empty initial value
mealTypeMenu = ttk.OptionMenu(mealPlanFrame, mealTypeVar, "empty", *mealOptions.keys())
mealTypeMenu.grid(row=0, column=1, padx=5, pady=5)

#Meal options dropdown with all meals from all categories
allMeals = [meal for category in mealOptions.values() for meal in category.keys()]
mealVar = tk.StringVar(value="")
mealMenu = ttk.OptionMenu(mealPlanFrame, mealVar, *allMeals)
mealMenu.grid(row=0, column=2, padx=5, pady=5)

setMealButton = ttk.Button(mealPlanFrame, text="Set Meal", command=setMealPlan)
setMealButton.grid(row=0, column=3, padx=5, pady=5)

#Button to set the selected meal in the meal plan
setMealButton = ttk.Button(mealPlanFrame, text="Set Meal", command=setMealPlan)
setMealButton.grid(row=0, column=3, padx=5, pady=5)

viewPlanButton = ttk.Button(root, text="View Meal Plan", command=displayMealPlan)
viewPlanButton.pack(pady=10)

#Grocery List Section
groceryFrame = ttk.LabelFrame(root, text="Grocery List")
groceryFrame.pack(fill="x", padx=10, pady=10)

generateButton = ttk.Button(groceryFrame, text="Generate Grocery List", command=generateGroceryList)
generateButton.pack(pady=5)

groceryText = tk.Text(groceryFrame, height=10, state="normal")
groceryText.pack(padx=5, pady=5)

root.mainloop()
